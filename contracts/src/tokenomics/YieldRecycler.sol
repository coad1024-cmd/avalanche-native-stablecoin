// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "./DynamicValidatorSubsidy.sol";

/**
 * @title YieldRecycler
 * @notice Programmatically executes the ACP-67 Yield Recycling Waterfall for Avalanche Native Stablecoin.
 * Supports both static baseline allocation and dynamic countercyclical validator income subsidy.
 * Governing Standard: BCRG Token Engineering Canon & ACP-67
 */
contract YieldRecycler {
    address public immutable owner;
    address public validatorTreasury;
    address public ecosystemTreasury;
    address public constant BURN_ADDRESS = 0x000000000000000000000000000000000000dEaD;

    DynamicValidatorSubsidy public subsidyController;
    bool public dynamicSubsidyEnabled;

    uint256 public constant STATIC_BUYBACK_BPS = 6500;   // 65.0%
    uint256 public constant STATIC_VALIDATOR_BPS = 2000; // 20.0%
    uint256 public constant STATIC_ECOSYSTEM_BPS = 1500; // 15.0%
    uint256 public constant TOTAL_BPS = 10000;

    uint256 public totalYieldRecycled;
    uint256 public totalAvaxBurned;
    uint256 public totalValidatorSubsidies;
    uint256 public totalEcosystemGrants;

    event YieldDistributed(
        uint256 totalAmount,
        uint256 buybackAmount,
        uint256 validatorAmount,
        uint256 ecosystemAmount,
        bool isDynamic
    );
    event AvaxBurned(uint256 amount);
    event DynamicSubsidyToggled(bool enabled);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    constructor(
        address _validatorTreasury,
        address _ecosystemTreasury,
        address _subsidyController
    ) {
        require(_validatorTreasury != address(0), "Invalid validator treasury");
        require(_ecosystemTreasury != address(0), "Invalid ecosystem treasury");
        
        owner = msg.sender;
        validatorTreasury = _validatorTreasury;
        ecosystemTreasury = _ecosystemTreasury;
        
        if (_subsidyController != address(0)) {
            subsidyController = DynamicValidatorSubsidy(_subsidyController);
            dynamicSubsidyEnabled = true;
        }
    }

    function setDynamicSubsidyController(address _subsidyController, bool _enabled) external onlyOwner {
        subsidyController = DynamicValidatorSubsidy(_subsidyController);
        dynamicSubsidyEnabled = _enabled;
        emit DynamicSubsidyToggled(_enabled);
    }

    receive() external payable {
        distributeNativeSurplus(0);
    }

    /**
     * @notice Distributes incoming liquid staking surplus across the 3 ACP-67 sinks
     * @param spotPrice Optional spot price for dynamic subsidy calculations (18 decimals, 0 for static)
     */
    function distributeNativeSurplus(uint256 spotPrice) public payable {
        uint256 amount = msg.value;
        require(amount > 0, "Zero amount");

        uint256 buybackBps = STATIC_BUYBACK_BPS;
        uint256 validatorBps = STATIC_VALIDATOR_BPS;
        uint256 ecosystemBps = STATIC_ECOSYSTEM_BPS;
        bool isDynamic = false;

        if (dynamicSubsidyEnabled && address(subsidyController) != address(0) && spotPrice > 0) {
            (validatorBps, buybackBps, ecosystemBps) = subsidyController.computeDynamicShares(spotPrice);
            isDynamic = true;
        }

        uint256 buybackAmount = (amount * buybackBps) / TOTAL_BPS;
        uint256 validatorAmount = (amount * validatorBps) / TOTAL_BPS;
        uint256 ecosystemAmount = (amount * ecosystemBps) / TOTAL_BPS;

        // Ensure rounding dust is allocated to burn
        uint256 allocated = buybackAmount + validatorAmount + ecosystemAmount;
        if (allocated < amount) {
            buybackAmount += (amount - allocated);
        }

        totalYieldRecycled += amount;
        totalAvaxBurned += buybackAmount;
        totalValidatorSubsidies += validatorAmount;
        totalEcosystemGrants += ecosystemAmount;

        // 1. Burn AVAX
        (bool burnSuccess, ) = payable(BURN_ADDRESS).call{value: buybackAmount}("");
        require(burnSuccess, "Burn transfer failed");
        emit AvaxBurned(buybackAmount);

        // 2. Transfer to Validator Treasury
        (bool valSuccess, ) = payable(validatorTreasury).call{value: validatorAmount}("");
        require(valSuccess, "Validator transfer failed");

        // 3. Transfer to Ecosystem Fund
        (bool ecoSuccess, ) = payable(ecosystemTreasury).call{value: ecosystemAmount}("");
        require(ecoSuccess, "Ecosystem transfer failed");

        emit YieldDistributed(amount, buybackAmount, validatorAmount, ecosystemAmount, isDynamic);
    }
}
