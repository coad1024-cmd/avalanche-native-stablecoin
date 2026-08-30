// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../../src/tokenomics/YieldRecycler.sol";
import "../../src/tokenomics/DynamicValidatorSubsidy.sol";

contract YieldRecyclerUnitTest {
    YieldRecycler public recycler;
    DynamicValidatorSubsidy public subsidy;

    address public validatorTreasury = address(0x1111111111111111111111111111111111111111);
    address public ecosystemTreasury = address(0x2222222222222222222222222222222222222222);

    uint256 public initialPrice = 40 * 1e18; // $40 AVAX

    function setUp() public {
        subsidy = new DynamicValidatorSubsidy(initialPrice);
        recycler = new YieldRecycler(validatorTreasury, ecosystemTreasury, address(subsidy));
    }

    function test_InitialStaticDistribution() public {
        setUp();
        uint256 yieldAmount = 100 ether;

        // Distribute with spotPrice = 0 (Static mode: 65% burn, 20% val, 15% eco)
        recycler.distributeNativeSurplus{value: yieldAmount}(0);

        require(validatorTreasury.balance == 20 ether, "Static validator share must be 20%");
        require(ecosystemTreasury.balance == 15 ether, "Static ecosystem share must be 15%");
        require(recycler.totalAvaxBurned() == 65 ether, "Static burn share must be 65%");
    }

    function test_DynamicDrawdownSubsidyBoost() public {
        setUp();
        // Severe market drawdown: spot price drops from $40 to $20 (50% drawdown)
        uint256 crashedSpotPrice = 20 * 1e18;
        
        (uint256 valBps, uint256 burnBps, uint256 ecoBps) = subsidy.computeDynamicShares(crashedSpotPrice);
        
        // Drawdown = 5000 bps (50%), Kappa = 0.35 -> Subsidy boost = 1750 bps -> Val = 2000 + 1750 = 3750 bps (37.5%)
        require(valBps == 3750, "Dynamic validator share must increase to 37.50% during 50% crash");
        require(ecoBps == 1500, "Ecosystem share must remain 15.00%");
        require(burnBps == 4750, "Residual burn share must be 47.50%");
        require(valBps + burnBps + ecoBps == 10000, "Total basis points must strictly equal 10000");

        // Execute yield distribution with dynamic price
        uint256 yieldAmount = 100 ether;
        recycler.distributeNativeSurplus{value: yieldAmount}(crashedSpotPrice);

        require(validatorTreasury.balance == 37.5 ether, "Validator received dynamic 37.5% subsidy");
        require(ecosystemTreasury.balance == 15 ether, "Ecosystem received 15%");
        require(recycler.totalAvaxBurned() == 47.5 ether, "Burn received 47.5%");
    }

    function test_MaxDynamicValidatorCeiling() public {
        setUp();
        // Extreme crash: spot price drops from $40 to $5 (87.5% crash)
        uint256 extremeCrashPrice = 5 * 1e18;
        
        (uint256 valBps, uint256 burnBps, uint256 ecoBps) = subsidy.computeDynamicShares(extremeCrashPrice);
        
        // Capped at MAX_VALIDATOR_BPS = 4500 (45.0%)
        require(valBps == 4500, "Validator share must be capped at 45.00%");
        require(burnBps == 4000, "Burn share must not drop below 40.00% floor");
        require(ecoBps == 1500, "Ecosystem share is 15.00%");
        require(valBps + burnBps + ecoBps == 10000, "Total sum invariant conserved");
    }
}
