// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title YieldRecycler
 * @notice Programmatically executes the ACP-67 Yield Recycling Waterfall for Avalanche Native Stablecoin.
 * 65% to AVAX Buyback & Burn, 20% to Validator Staking Boost, 15% to Ecosystem Growth Fund.
 */
contract YieldRecycler {
    address public immutable owner;
    address public validatorTreasury;
    address public ecosystemTreasury;
    address public constant BURN_ADDRESS = 0x000000000000000000000000000000000000dEaD;

    uint256 public constant BUYBACK_BPS = 6500;  // 65.0%
    uint256 public constant VALIDATOR_BPS = 2000;// 20.0%
    uint256 public constant ECOSYSTEM_BPS = 1500;// 15.0%
    uint256 public constant TOTAL_BPS = 10000;

    uint256 public totalYieldRecycled;
    uint256 public totalAvaxBurned;

    event YieldDistributed(uint256 totalAmount, uint256 buybackAmount, uint256 validatorAmount, uint256 ecosystemAmount);
    event AvaxBurned(uint256 amount);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    constructor(address _validatorTreasury, address _ecosystemTreasury) {
        owner = msg.sender;
        validatorTreasury = _validatorTreasury;
        ecosystemTreasury = _ecosystemTreasury;
    }

    receive() external payable {
        distributeNativeSurplus();
    }

    function distributeNativeSurplus() public payable {
        uint256 amount = msg.value;
        require(amount > 0, "Zero amount");

        uint256 buybackAmount = (amount * BUYBACK_BPS) / TOTAL_BPS;
        uint256 validatorAmount = (amount * VALIDATOR_BPS) / TOTAL_BPS;
        uint256 ecosystemAmount = (amount * ECOSYSTEM_BPS) / TOTAL_BPS;

        totalYieldRecycled += amount;
        totalAvaxBurned += buybackAmount;

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

        emit YieldDistributed(amount, buybackAmount, validatorAmount, ecosystemAmount);
    }
}
