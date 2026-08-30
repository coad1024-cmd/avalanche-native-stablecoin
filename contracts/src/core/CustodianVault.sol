// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "./TrancheToken.sol";
import "./MocksAVAX.sol";
import "../interfaces/ICustodianVault.sol";
import "../oracles/ChainlinkOracleAdapter.sol";

interface IERC20Minimal {
    function transfer(address to, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

/**
 * @title CustodianVault
 * @notice Master collateral custody and primary tranche issuance vault for Avalanche Native Stablecoin.
 * Holds liquid-staked sAVAX collateral and mints/burns matching Class A (Senior) and Class B (Leveraged) pairs.
 * Governing Standard: SSRN-3856569 & BCRG Token Engineering Canon
 */
contract CustodianVault is ICustodianVault {
    uint256 public constant SCALE = 1e18;

    address public immutable owner;
    IERC20Minimal public immutable collateralToken; // sAVAX
    IPriceOracle public oracle;

    TrancheToken public tokenA;
    TrancheToken public tokenB;
    address public resetController;

    uint256 public override totalCollateral;
    uint256 public override referencePrice; // USD with 18 decimals
    uint256 public beta;                    // Cumulative conversion scaling factor (Base 1e18)

    event DepositAndMint(address indexed user, uint256 collateralIn, uint256 mintedA, uint256 mintedB);
    event RedeemAndBurn(address indexed user, uint256 burnedA, uint256 burnedB, uint256 collateralOut);
    event StateReset(uint256 newReferencePrice, uint256 newBeta);
    event PriceUpdated(uint256 newPrice);
    event OracleUpdated(address newOracle);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    modifier onlyControllerOrOwner() {
        require(msg.sender == resetController || msg.sender == owner, "Unauthorized");
        _;
    }

    constructor(address _collateralToken, uint256 _initialPrice, address _oracle) payable {
        require(_initialPrice > 0, "Price must be positive");
        owner = msg.sender;
        collateralToken = IERC20Minimal(_collateralToken);
        referencePrice = _initialPrice;
        beta = SCALE;
        if (_oracle != address(0)) {
            oracle = IPriceOracle(_oracle);
        }
    }

    function initializeTranches(address _tokenA, address _tokenB, address _controller) external onlyOwner {
        require(address(tokenA) == address(0), "Already initialized");
        require(_tokenA != address(0) && _tokenB != address(0) && _controller != address(0), "Invalid address");
        tokenA = TrancheToken(_tokenA);
        tokenB = TrancheToken(_tokenB);
        resetController = _controller;
    }

    function setOracle(address _oracle) external onlyOwner {
        oracle = IPriceOracle(_oracle);
        emit OracleUpdated(_oracle);
    }

    function syncPriceWithOracle() public returns (uint256) {
        if (address(oracle) != address(0) && !oracle.isCircuitBreakerTripped()) {
            uint256 livePrice = oracle.getPrice();
            if (livePrice > 0) {
                referencePrice = livePrice;
                emit PriceUpdated(livePrice);
                return livePrice;
            }
        }
        return referencePrice;
    }

    function setReferencePrice(uint256 newPrice) external onlyOwner {
        require(newPrice > 0, "Price must be positive");
        referencePrice = newPrice;
        emit PriceUpdated(newPrice);
    }

    /**
     * @notice Deposits sAVAX ERC-20 collateral and mints matching Class A and Class B pairs
     * @param collateralAmount Amount of sAVAX deposited (18 decimals)
     */
    function depositAndMint(uint256 collateralAmount) external override returns (uint256 mintedA, uint256 mintedB) {
        require(collateralAmount > 0, "Zero deposit");
        require(address(tokenA) != address(0), "Tranches not initialized");

        // Transfer sAVAX from caller to vault if collateralToken is configured
        if (address(collateralToken) != address(0)) {
            bool success = collateralToken.transferFrom(msg.sender, address(this), collateralAmount);
            require(success, "Collateral transfer failed");
        }

        totalCollateral += collateralAmount;

        // 1 unit collateral generates pairs according to reference conversion
        uint256 pairAmount = (collateralAmount * referencePrice) / SCALE;
        
        tokenA.mint(msg.sender, pairAmount);
        tokenB.mint(msg.sender, pairAmount);

        emit DepositAndMint(msg.sender, collateralAmount, pairAmount, pairAmount);
        return (pairAmount, pairAmount);
    }

    /**
     * @notice Redeems matching Class A and Class B pairs to retrieve sAVAX collateral
     */
    function redeemAndBurn(uint256 rawAmountA, uint256 rawAmountB) external override returns (uint256 collateralReturned) {
        require(rawAmountA == rawAmountB && rawAmountA > 0, "Must redeem matching pairs");
        require(address(tokenA) != address(0), "Tranches not initialized");
        
        tokenA.burn(msg.sender, rawAmountA);
        tokenB.burn(msg.sender, rawAmountB);

        collateralReturned = (rawAmountA * SCALE) / referencePrice;
        require(totalCollateral >= collateralReturned, "Insufficient pool reserves");
        totalCollateral -= collateralReturned;

        // Return sAVAX collateral to caller
        if (address(collateralToken) != address(0)) {
            bool success = collateralToken.transfer(msg.sender, collateralReturned);
            require(success, "Collateral return failed");
        }

        emit RedeemAndBurn(msg.sender, rawAmountA, rawAmountB, collateralReturned);
        return collateralReturned;
    }

    function updateResetState(uint256 newPrice, uint256 newBeta) external onlyControllerOrOwner {
        require(newPrice > 0 && newBeta > 0, "Invalid reset parameters");
        referencePrice = newPrice;
        beta = newBeta;
        emit StateReset(newPrice, newBeta);
    }
}
