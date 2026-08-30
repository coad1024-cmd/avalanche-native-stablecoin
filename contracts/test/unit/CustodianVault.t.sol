// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../../src/core/CustodianVault.sol";
import "../../src/core/TrancheToken.sol";
import "../../src/core/TrancheSplitter.sol";
import "../../src/controller/ResetController.sol";

contract CustodianVaultUnitTest {
    CustodianVault vault;
    TrancheToken tokenA;
    TrancheToken tokenB;
    TrancheToken tokenAPrime;
    TrancheToken tokenBPrime;
    TrancheSplitter splitter;
    ResetController controller;

    function setUp() public {
        // Reference price = $25.00 (25e18)
        vault = new CustodianVault(25e18);

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
            0.25e18   // Hd = 0.25
        );

        tokenA.setResetController(address(controller));
        tokenB.setResetController(address(controller));

        vault.initializeTranches(address(tokenA), address(tokenB), address(controller));
        splitter = new TrancheSplitter(address(tokenA), address(tokenAPrime), address(tokenBPrime));

        tokenA.setSplitter(address(splitter));
        tokenAPrime.setSplitter(address(splitter));
        tokenBPrime.setSplitter(address(splitter));
    }

    function testDepositAndMint() public {
        setUp();
        
        // Deposit 1 AVAX (1e18) -> generates 25 pairs ($25 USD reference)
        (uint256 mintedA, uint256 mintedB) = vault.depositAndMint(1e18);
        
        require(mintedA == 25e18, "Class A mint mismatch");
        require(mintedB == 25e18, "Class B mint mismatch");
        require(tokenA.balanceOf(address(this)) == 25e18, "Token A balance incorrect");
        require(tokenB.balanceOf(address(this)) == 25e18, "Token B balance incorrect");
        require(vault.totalCollateral() == 1e18, "Vault collateral mismatch");
    }

    function testSecondaryTrancheSplit() public {
        setUp();
        vault.depositAndMint(1e18);

        // Split 10 Class A tokens into 10 anUSD (Class A') and 10 Class B' tokens
        tokenA.approve(address(splitter), 10e18);
        splitter.split(10e18);

        require(tokenAPrime.balanceOf(address(this)) == 10e18, "anUSD balance mismatch");
        require(tokenBPrime.balanceOf(address(this)) == 10e18, "Class B' balance mismatch");
        require(tokenA.balanceOf(address(this)) == 15e18, "Remaining Class A mismatch");
    }

    function testSolvencyInvariant() public {
        setUp();
        vault.depositAndMint(4e18); // 4 AVAX = $100 collateral

        uint256 balA = tokenA.balanceOf(address(this));
        uint256 balB = tokenB.balanceOf(address(this));

        require(balA == 100e18, "Bal A mismatch");
        require(balB == 100e18, "Bal B mismatch");

        // Total pool value equals 2 * P_t * collateral
        uint256 poolValue = (balA + balB);
        require(poolValue == 200e18, "Solvency parity violated");
    }
}
