// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IPriceOracle {
    function getPrice() external view returns (uint256 priceUsd18);
    function isCircuitBreakerTripped() external view returns (bool);
}

interface AggregatorV3Interface {
    function decimals() external view returns (uint8);
    function latestRoundData() external view returns (
        uint80 roundId,
        int256 answer,
        uint256 startedAt,
        uint256 updatedAt,
        uint80 answeredInRound
    );
}

/**
 * @title ChainlinkOracleAdapter
 * @notice Consumes Chainlink AVAX/USD feeds on Avalanche (C-Chain / Fuji) and normalizes to 18 decimals with staleness checks.
 * Avalanche Fuji AVAX/USD Feed: 0x5498BB86e9D018D222BF7B8971c67420515605E8
 */
contract ChainlinkOracleAdapter is IPriceOracle {
    address public immutable owner;
    AggregatorV3Interface public immutable priceFeed;
    uint8 public immutable feedDecimals;

    uint256 public maxStalenessSeconds = 3600; // 1 hour for testnet, 300s for mainnet
    uint256 public manualOverridePrice;        // Fallback / simulated testing price (18 decimals)
    bool public useManualOverride;

    event PriceUpdated(uint256 priceUsd18, uint256 timestamp);
    event OverrideToggled(bool active, uint256 overridePrice);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    constructor(address _chainlinkFeed) {
        owner = msg.sender;
        if (_chainlinkFeed != address(0)) {
            priceFeed = AggregatorV3Interface(_chainlinkFeed);
            feedDecimals = AggregatorV3Interface(_chainlinkFeed).decimals();
        } else {
            feedDecimals = 8;
        }
    }

    function setManualOverride(bool _useOverride, uint256 _price18) external onlyOwner {
        useManualOverride = _useOverride;
        manualOverridePrice = _price18;
        emit OverrideToggled(_useOverride, _price18);
    }

    function setMaxStaleness(uint256 _seconds) external onlyOwner {
        require(_seconds >= 60, "Staleness too low");
        maxStalenessSeconds = _seconds;
    }

    function getPrice() external view override returns (uint256) {
        if (useManualOverride && manualOverridePrice > 0) {
            return manualOverridePrice;
        }

        require(address(priceFeed) != address(0), "No price feed configured");

        (
            ,
            int256 answer,
            ,
            uint256 updatedAt,
            
        ) = priceFeed.latestRoundData();

        require(answer > 0, "Negative or zero price");
        require(block.timestamp - updatedAt <= maxStalenessSeconds, "Oracle price stale");

        // Normalize feed decimals (typically 8) to 18 decimals
        if (feedDecimals < 18) {
            return uint256(answer) * (10 ** (18 - feedDecimals));
        } else if (feedDecimals > 18) {
            return uint256(answer) / (10 ** (feedDecimals - 18));
        } else {
            return uint256(answer);
        }
    }

    function isCircuitBreakerTripped() external view override returns (bool) {
        if (address(priceFeed) == address(0)) return false;
        try priceFeed.latestRoundData() returns (
            uint80,
            int256 answer,
            uint256,
            uint256 updatedAt,
            uint80
        ) {
            if (answer <= 0) return true;
            if (block.timestamp - updatedAt > maxStalenessSeconds) return true;
            return false;
        } catch {
            return true;
        }
    }
}
