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
        // Reference price = $25.00 (25e18), zero address for mock collateral/oracle
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

        // Split 25 Class A tokens into 25 anUSD and 25 Class B'
        splitter.split(25e18);

        require(tokenA.balanceOf(address(this)) == 0, "Class A should be burned");
        require(tokenAPrime.balanceOf(address(this)) == 25e18, "anUSD minted mismatch");
        require(tokenBPrime.balanceOf(address(this)) == 25e18, "Class B' minted mismatch");

        // Merge back
        splitter.merge(25e18, 25e18);
        require(tokenA.balanceOf(address(this)) == 25e18, "Class A should be restored");
        require(tokenAPrime.balanceOf(address(this)) == 0, "anUSD burned mismatch");
        require(tokenBPrime.balanceOf(address(this)) == 0, "Class B' burned mismatch");
    }

    function testSolvencyInvariant() public {
        setUp();
        vault.depositAndMint(10e18);

        // Total pool value = 10 AVAX * $25 = $250
        // Class A raw = 250, Class B raw = 250
        uint256 poolAssets = (vault.totalCollateral() * vault.referencePrice()) / 1e18;
        uint256 trancheSum = (tokenA.totalSupply() + tokenB.totalSupply()) / 2;

        require(poolAssets == 250e18, "Asset pool mismatch");
        require(trancheSum == 250e18, "Tranche liability mismatch");
    }
}
