// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../../src/core/CustodianVault.sol";
import "../../src/core/TrancheToken.sol";
import "../../src/core/TrancheSplitter.sol";
import "../../src/controller/ResetController.sol";

/**
 * @title ResetAndSplitterVulnerabilitiesTest
 * @notice Empirical verification and adversarial proof of vulnerabilities in ResetController.sol,
 * TrancheSplitter.sol, and TrancheToken.sol as documented in SOURCE_AND_DERIVATION_AUDIT.md.
 */
contract ResetAndSplitterVulnerabilitiesTest {
    CustodianVault vault;
    TrancheToken tokenA;
    TrancheToken tokenB;
    TrancheToken tokenAPrime;
    TrancheToken tokenBPrime;
    TrancheSplitter splitter;
    ResetController controller;

    function setUp() public {
        // P_0 = $25.00
        vault = new CustodianVault(address(0), 25e18, address(0));

        tokenA = new TrancheToken("Class A Senior Bond", "clA", ITrancheToken.TrancheType.CLASS_A, address(vault));
        tokenB = new TrancheToken("Class B Leveraged Equity", "clB", ITrancheToken.TrancheType.CLASS_B, address(vault));
        tokenAPrime = new TrancheToken("Avalanche Native USD", "anUSD", ITrancheToken.TrancheType.CLASS_A_PRIME, address(vault));
        tokenBPrime = new TrancheToken("Class B Prime Yield", "clBPrime", ITrancheToken.TrancheType.CLASS_B_PRIME, address(vault));

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
        splitter = new TrancheSplitter(address(tokenA), address(tokenAPrime), address(tokenBPrime));

        tokenA.setSplitter(address(splitter));
        tokenAPrime.setSplitter(address(splitter));
        tokenBPrime.setSplitter(address(splitter));
    }

    /**
     * @notice Proof 1: Verify the Reset Flapping Defect in ResetController.sol.
     * When spot price increases to $40, an upward reset triggers and executes.
     * Due to beta * P_0 double-counting, in the very next check at the SAME price $40,
     * NAV_B evaluates to 0.25 <= H_d ($0.25), immediately triggering a spurious DOWNWARD reset.
     */
    function testEmpiricalProof_ResetFlappingDefect() public {
        setUp();
        vault.depositAndMint(10e18); // 10 AVAX = 250 pairs

        // 1. Initial State Check at P_0 = $25, beta = 1.0
        require(vault.referencePrice() == 25e18, "Initial reference price must be $25");
        require(vault.beta() == 1e18, "Initial beta must be 1.0");

        // 2. Price rises to $40 -> poolValue = 2 * 40 / 25 = 3.20 -> NAV_B = 2.20 >= H_u (2.00)
        controller.setMarketPrice(40e18);
        (IResetController.ResetType rType1, uint256 navB1) = controller.checkReset();
        require(rType1 == IResetController.ResetType.UPWARD, "Step 1: Should detect UPWARD reset");
        require(navB1 == 2.2e18, "Step 1: NAV_B should be 2.20");

        // 3. Execute Upward Reset
        controller.executeReset();

        // Check state immediately post-reset
        require(vault.referencePrice() == 40e18, "Post-reset referencePrice should be $40");
        require(vault.beta() == 1.6e18, "Post-reset beta should be 1.6");
        require(tokenA.scalarMultiplier() == 1.5e18, "Token A scalar should be 1.5");
        require(tokenB.scalarMultiplier() == 1.5e18, "Token B scalar should be 1.5");

        // 4. In the VERY NEXT CHECK at the EXACT SAME market price of $40:
        // Denominator evaluates to beta * P_0 = 1.6 * 40 = $64
        // poolValue = 2 * 40 / 64 = 1.25
        // NAV_B = 1.25 - 1.00 = 0.25 <= H_d (0.25)
        (IResetController.ResetType rType2, uint256 navB2) = controller.checkReset();
        
        // EMPIRICAL VERIFICATION: Spurious DOWNWARD reset is triggered immediately at $40!
        require(rType2 == IResetController.ResetType.DOWNWARD, "FLAPPING PROVED: Spurious DOWNWARD reset triggered at $40!");
        require(navB2 == 0.25e18, "FLAPPING PROVED: NAV_B collapsed to 0.25 at constant $40 price!");

        // 5. Executing the spurious downward reset
        controller.executeReset();

        // Post downward reset: Token A and Token B are both scaled down by 75/100 (25% haircut!)
        // scalar = 1.5 * 0.75 = 1.125
        require(tokenA.scalarMultiplier() == 1.125e18, "Token A improperly haircutted to 1.125x");
        require(tokenB.scalarMultiplier() == 1.125e18, "Token B improperly haircutted to 1.125x");
        require(vault.referencePrice() == 40e18, "Reference price remains $40");
        require(vault.beta() == 1.0e18, "Beta resets to 1.0");

        // Now NAV_B = 2 * 40 / 40 - 1.0 = 1.0 -> NONE
        (IResetController.ResetType rType3, uint256 navB3) = controller.checkReset();
        require(rType3 == IResetController.ResetType.NONE, "Post-haircut state evaluates to NONE");
        require(navB3 == 1.0e18, "NAV_B restored to 1.0 after spurious downward haircut");
    }

    /**
     * @notice Proof 2: Verify Secondary Tranche Rebase Disconnect & Unbacked Wealth Extraction.
     * Splitting 100 Class A into 100 A' and 100 B', experiencing an upward reset,
     * and merging back mints 100 raw Class A which is now worth 150 nominal Class A (+50% free tokens).
     */
    function testEmpiricalProof_SecondaryTrancheRebaseDisconnect() public {
        setUp();
        // Deposit 4 AVAX at $25 -> 100 Class A and 100 Class B pairs
        vault.depositAndMint(4e18);

        uint256 initialBalA = tokenA.balanceOf(address(this));
        require(initialBalA == 100e18, "Initial Class A balance must be 100");

        // 1. Split 100 Class A into 100 A' (anUSD) and 100 B' (Yield)
        splitter.split(100e18);
        require(tokenA.balanceOf(address(this)) == 0, "Class A burned to 0");
        require(tokenAPrime.balanceOf(address(this)) == 100e18, "Holding 100 anUSD");
        require(tokenBPrime.balanceOf(address(this)) == 100e18, "Holding 100 Yield");

        // 2. Upward Reset occurs (simulated market price rises to $40)
        controller.setMarketPrice(40e18);
        controller.executeReset();

        // Token A scalar multiplier is now 1.5x, but A' and B' multipliers remain 1.0x!
        require(tokenA.scalarMultiplier() == 1.5e18, "Token A scalar scaled to 1.5x");
        require(tokenAPrime.scalarMultiplier() == 1e18, "anUSD scalar remained 1.0x (DISCONNECTED)");
        require(tokenBPrime.scalarMultiplier() == 1e18, "Yield scalar remained 1.0x (DISCONNECTED)");

        // 3. User merges 100 A' and 100 B' back through TrancheSplitter
        splitter.merge(100e18, 100e18);

        // 4. Verification of unbacked token creation:
        // User burned 100 A' (worth 100 nominal) and 100 B' (worth 100 nominal)
        // Splitter minted 100 RAW Token A.
        // With scalarMultiplier = 1.5x, balanceOf(user) = 100 * 1.5 = 150 nominal Token A!
        uint256 finalBalA = tokenA.balanceOf(address(this));
        require(finalBalA == 150e18, "DISCONNECT PROVED: User extracted 150 nominal Token A from 100 initial!");

        // 50 Token A minted out of thin air (+50% free extraction)
        uint256 freeNominalProfit = finalBalA - initialBalA;
        require(freeNominalProfit == 50e18, "FREE ARBITRAGE PROVED: Exactly 50.0 Token A extracted for free");
    }

    /**
     * @notice Proof 3: Verify 2:1 Accounting Discrepancy in TrancheSplitter.sol.
     * Burning 1 unit of Class A ($1.00) mints 1 unit of A' ($1.00) AND 1 unit of B' ($1.00),
     * creating $2.00 in nominal claims from $1.00 in collateral.
     */
    function testEmpiricalProof_TrancheSplitterTwoToOneAccounting() public {
        setUp();
        vault.depositAndMint(1e18); // 25 Class A tokens

        // User splits 10 Class A tokens (nominal value = $10.00 at par)
        splitter.split(10e18);

        uint256 mintedAPrime = tokenAPrime.balanceOf(address(this));
        uint256 mintedBPrime = tokenBPrime.balanceOf(address(this));

        // 10 Class A burned -> 10 A' + 10 B' minted = 20 total secondary tokens
        require(mintedAPrime == 10e18, "Minted 10 anUSD");
        require(mintedBPrime == 10e18, "Minted 10 Yield");
        require(mintedAPrime + mintedBPrime == 20e18, "ACCOUNTING BUG PROVED: 20 tokens created from 10 Class A");
    }
}
