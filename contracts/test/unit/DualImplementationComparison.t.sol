// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../../src/core/CustodianVault.sol";
import "../../src/core/TrancheToken.sol";
import "../../src/core/MocksAVAX.sol";
import "../../src/interfaces/ITrancheToken.sol";
import "../../src/remediation/reference_buggy/ResetControllerBuggy.sol";
import "../../src/remediation/reference_buggy/TrancheSplitterBuggy.sol";
import "../../src/remediation/candidate_corrected/ResetControllerCorrected.sol";
import "../../src/remediation/candidate_corrected/TrancheSplitterCorrected.sol";

/**
 * @title DualImplementationComparisonUnitTest
 * @notice Side-by-side verification of Reference Bug-Preserving vs Corrected Candidate Implementations.
 * Proves:
 *   1. ResetControllerBuggy exhibits instant downward reset flapping at $52 after an upward reset at $52.
 *   2. ResetControllerCorrected eliminates flapping and normalizes post-reset state cleanly to Par ($1.00).
 *   3. TrancheSplitterBuggy mints $2.00 of claims from $1.00 of input Token A.
 *   4. TrancheSplitterCorrected enforces strict 2:1 value conservation (V_A' + V_B' = 2 V_A).
 */
contract DualImplementationComparisonUnitTest {
    uint256 constant SCALE = 1e18;

    MocksAVAX savax;
    
    // Buggy System Instances
    CustodianVault vaultBuggy;
    TrancheToken tokenABuggy;
    TrancheToken tokenBBuggy;
    TrancheToken tokenAPrimeBuggy;
    TrancheToken tokenBPrimeBuggy;
    ResetControllerBuggy controllerBuggy;
    TrancheSplitterBuggy splitterBuggy;

    // Corrected System Instances
    CustodianVault vaultCorrected;
    TrancheToken tokenACorrected;
    TrancheToken tokenBCorrected;
    TrancheToken tokenAPrimeCorrected;
    TrancheToken tokenBPrimeCorrected;
    ResetControllerCorrected controllerCorrected;
    TrancheSplitterCorrected splitterCorrected;

    address alice = address(0x1111);

    function setUp() public {
        savax = new MocksAVAX();

        // 1. Setup Buggy System
        vaultBuggy = new CustodianVault(address(savax), 25 * SCALE, address(0));
        tokenABuggy = new TrancheToken("Token A Buggy", "TAB", ITrancheToken.TrancheType.CLASS_A, address(vaultBuggy));
        tokenBBuggy = new TrancheToken("Token B Buggy", "TBB", ITrancheToken.TrancheType.CLASS_B, address(vaultBuggy));
        tokenAPrimeBuggy = new TrancheToken("anUSD Buggy", "anUSD-B", ITrancheToken.TrancheType.CLASS_A_PRIME, address(vaultBuggy));
        tokenBPrimeBuggy = new TrancheToken("Yield B' Buggy", "TYB", ITrancheToken.TrancheType.CLASS_B_PRIME, address(vaultBuggy));
        
        controllerBuggy = new ResetControllerBuggy(
            address(vaultBuggy),
            address(tokenABuggy),
            address(tokenBBuggy),
            0.073e18, // 7.3% R
            2.0e18,   // H_u = $2.00
            0.25e18,  // H_d = $0.25
            address(0)
        );
        vaultBuggy.initializeTranches(address(tokenABuggy), address(tokenBBuggy), address(controllerBuggy));
        tokenABuggy.setResetController(address(controllerBuggy));
        tokenBBuggy.setResetController(address(controllerBuggy));
        
        splitterBuggy = new TrancheSplitterBuggy(
            address(tokenABuggy),
            address(tokenAPrimeBuggy),
            address(tokenBPrimeBuggy)
        );
        tokenABuggy.setSplitter(address(splitterBuggy));
        tokenAPrimeBuggy.setSplitter(address(splitterBuggy));
        tokenBPrimeBuggy.setSplitter(address(splitterBuggy));

        // 2. Setup Corrected System
        vaultCorrected = new CustodianVault(address(savax), 25 * SCALE, address(0));
        tokenACorrected = new TrancheToken("Token A Corrected", "TAC", ITrancheToken.TrancheType.CLASS_A, address(vaultCorrected));
        tokenBCorrected = new TrancheToken("Token B Corrected", "TBC", ITrancheToken.TrancheType.CLASS_B, address(vaultCorrected));
        tokenAPrimeCorrected = new TrancheToken("anUSD Corrected", "anUSD-C", ITrancheToken.TrancheType.CLASS_A_PRIME, address(vaultCorrected));
        tokenBPrimeCorrected = new TrancheToken("Yield B' Corrected", "TYC", ITrancheToken.TrancheType.CLASS_B_PRIME, address(vaultCorrected));

        controllerCorrected = new ResetControllerCorrected(
            address(vaultCorrected),
            address(tokenACorrected),
            address(tokenBCorrected),
            0.073e18, // 7.3% R
            2.0e18,   // H_u = $2.00
            0.25e18,  // H_d = $0.25
            address(0)
        );
        vaultCorrected.initializeTranches(address(tokenACorrected), address(tokenBCorrected), address(controllerCorrected));
        tokenACorrected.setResetController(address(controllerCorrected));
        tokenBCorrected.setResetController(address(controllerCorrected));

        splitterCorrected = new TrancheSplitterCorrected(
            address(tokenACorrected),
            address(tokenAPrimeCorrected),
            address(tokenBPrimeCorrected)
        );
        tokenACorrected.setSplitter(address(splitterCorrected));
        tokenAPrimeCorrected.setSplitter(address(splitterCorrected));
        tokenBPrimeCorrected.setSplitter(address(splitterCorrected));

        // Fund test contract with sAVAX
        savax.faucet(1000 * SCALE);
    }

    // =========================================================================
    // Test 1: ResetController Flapping Verification (VULN-01)
    // =========================================================================

    function test_BuggyResetFlappingReproduced() public {
        setUp();
        // AVAX price surges from $25 to $52 (PoolValue = 2 * 52 / 25 = 4.16 > H_u = 2.00)
        controllerBuggy.setMarketPrice(52 * SCALE);

        (IResetController.ResetType rType, ) = controllerBuggy.checkReset();
        require(rType == IResetController.ResetType.UPWARD, "Upward reset must trigger at $52");

        // Execute upward reset at $52
        controllerBuggy.executeReset();

        // IN THE VERY NEXT BLOCK, PRICE IS STILL $52 (STABLE AT $52)
        // BUG EFFECT: checkReset() computes poolValue with beta * P_0 in denominator:
        // P_0 = 52, beta = 52/25 = 2.08 -> Denominator = 2.08 * 52 = 108.16
        // poolValue = 2 * 52 * 1e18 / 108.16 = 0.9615e18
        // V_B = 0.9615 - 1.00 = 0 <= H_d (0.25e18) -> SPURIOUS DOWNWARD RESET FLAPPING!
        (IResetController.ResetType rTypeNext, uint256 navBNext) = controllerBuggy.checkReset();
        
        require(rTypeNext == IResetController.ResetType.DOWNWARD, "Buggy controller must incorrectly trigger DOWNWARD flapping at $52");
        require(navBNext == 0, "NAV B in buggy controller dropped to zero spuriously");
    }

    function test_CorrectedResetCleanNormalization() public {
        setUp();
        // AVAX price surges from $25 to $52
        controllerCorrected.setMarketPrice(52 * SCALE);

        (IResetController.ResetType rType, ) = controllerCorrected.checkReset();
        require(rType == IResetController.ResetType.UPWARD, "Upward reset must trigger at $52");

        // Execute upward reset at $52
        controllerCorrected.executeReset();

        // IN THE VERY NEXT BLOCK AT $52:
        // CORRECTED EFFECT: S = 52 / 52 = 1.000 -> PoolValue = 2 * 1.00 = 2.00
        // V_B = 2.00 - 1.00 = 1.00 (Par NAV at reset) -> No reset triggered!
        (IResetController.ResetType rTypeNext, uint256 navBNext) = controllerCorrected.checkReset();
        
        require(rTypeNext == IResetController.ResetType.NONE, "Corrected controller must NOT flap");
        require(navBNext == 1.0e18, "Corrected NAV B must be exactly Par ($1.00) post-reset");
    }

    // =========================================================================
    // Test 2: TrancheSplitter 2:1 Conservation & Backing (VULN-02 & VULN-03)
    // =========================================================================

    function test_BuggySplitterCreatesUnbackedClaims() public {
        setUp();
        // Deposit 4 sAVAX at $25 -> mints 100 Token A ($100) and 100 Token B ($100) to this
        savax.approve(address(vaultBuggy), type(uint256).max);
        (uint256 mintedA, ) = vaultBuggy.depositAndMint(4 * SCALE);
        require(mintedA == 100 * SCALE, "Mints 100 Token A");

        // Split 100 Token A in Buggy Splitter
        // BUG: Burning 100 A mints 100 A' AND 100 B' ($100 in -> $200 nominal claims out!)
        splitterBuggy.split(100 * SCALE);

        require(tokenABuggy.balanceOf(address(this)) == 0, "Token A burned");
        require(tokenAPrimeBuggy.balanceOf(address(this)) == 100 * SCALE, "Minted 100 anUSD");
        require(tokenBPrimeBuggy.balanceOf(address(this)) == 100 * SCALE, "Minted 100 Yield");
        // Total claims = $100 anUSD + $100 Yield = $200 claims from $100 input!
    }

    function test_CorrectedSplitterEnforces2To1Conservation() public {
        setUp();
        // Deposit 4 sAVAX at $25 -> mints 100 Token A ($100) and 100 Token B ($100) to this
        savax.approve(address(vaultCorrected), type(uint256).max);
        (uint256 mintedA, ) = vaultCorrected.depositAndMint(4 * SCALE);
        require(mintedA == 100 * SCALE, "Mints 100 Token A");

        // Split 100 Token A in Corrected Splitter
        // CORRECTED: Burning 100 A ($100) mints 50 A' ($50) and 50 B' ($50) -> $100 in = $100 out!
        splitterCorrected.split(100 * SCALE);

        require(tokenACorrected.balanceOf(address(this)) == 0, "Token A burned");
        require(tokenAPrimeCorrected.balanceOf(address(this)) == 50 * SCALE, "Minted 50 anUSD");
        require(tokenBPrimeCorrected.balanceOf(address(this)) == 50 * SCALE, "Minted 50 Yield");

        // Merging 50 pairs returns exactly 100 Token A
        splitterCorrected.merge(50 * SCALE);

        require(tokenACorrected.balanceOf(address(this)) == 100 * SCALE, "Returned exactly 100 Token A");
        require(tokenAPrimeCorrected.balanceOf(address(this)) == 0, "anUSD burned");
        require(tokenBPrimeCorrected.balanceOf(address(this)) == 0, "Yield burned");
    }
}
