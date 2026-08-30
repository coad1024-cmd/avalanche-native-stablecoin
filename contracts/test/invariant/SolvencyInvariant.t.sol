// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../../src/core/CustodianVault.sol";
import "../../src/core/TrancheToken.sol";
import "../../src/controller/ResetController.sol";

contract SolvencyInvariantTest {
    CustodianVault vault;
    TrancheToken tokenA;
    TrancheToken tokenB;
    ResetController controller;

    function setUp() public {
        vault = new CustodianVault(address(0), 25e18, address(0)); // P_0 = $25.00

        tokenA = new TrancheToken("Class A Senior Bond", "clA", ITrancheToken.TrancheType.CLASS_A, address(vault));
        tokenB = new TrancheToken("Class B Leveraged Equity", "clB", ITrancheToken.TrancheType.CLASS_B, address(vault));

        controller = new ResetController(
            address(vault),
            address(tokenA),
            address(tokenB),
            0.073e18, // 7.3% coupon
            2.0e18,   // Hu = 2.0
            0.25e18,  // Hd = 0.25
            address(0)
        );

        tokenA.setResetController(address(controller));
        tokenB.setResetController(address(controller));

        vault.initializeTranches(address(tokenA), address(tokenB), address(controller));
    }

    function testUpwardResetExecution() public {
        setUp();
        vault.depositAndMint(10e18); // 10 AVAX = 250 pairs

        // Market price rises from $25 to $40 -> Pool value = 2 * 40 / 25 = 3.2 -> NAV_B = 3.2 - 1.0 = 2.2 >= 2.0
        controller.setMarketPrice(40e18);

        (IResetController.ResetType rType, ) = controller.checkReset();
        require(rType == IResetController.ResetType.UPWARD, "Upward reset should be detected");

        controller.executeReset();

        // Multiplier should have scaled up
        require(tokenA.scalarMultiplier() > 1e18, "Scalar A should increase post upward reset");
        require(tokenB.scalarMultiplier() > 1e18, "Scalar B should increase post upward reset");
    }

    function testDownwardResetExecution() public {
        setUp();
        vault.depositAndMint(10e18);

        // Market price drops from $25 to $15 -> Pool value = 2 * 15 / 25 = 1.2 -> NAV_B = 1.2 - 1.0 = 0.20 <= 0.25
        controller.setMarketPrice(15e18);

        (IResetController.ResetType rType, ) = controller.checkReset();
        require(rType == IResetController.ResetType.DOWNWARD, "Downward reset should be detected");

        controller.executeReset();

        // Multiplier should have scaled down
        require(tokenA.scalarMultiplier() < 1e18, "Scalar A should decrease post downward reset");
        require(tokenB.scalarMultiplier() < 1e18, "Scalar B should decrease post downward reset");
    }
}
