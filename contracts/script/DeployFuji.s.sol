// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../src/core/MocksAVAX.sol";
import "../src/core/CustodianVault.sol";
import "../src/core/TrancheToken.sol";
import "../src/core/TrancheSplitter.sol";
import "../src/controller/ResetController.sol";
import "../src/oracles/ChainlinkOracleAdapter.sol";
import "../src/tokenomics/DynamicValidatorSubsidy.sol";
import "../src/tokenomics/YieldRecycler.sol";
import "../src/icm/TeleporterUSDAdapter.sol";

/**
 * @title DeployFuji
 * @notice Master deployment and initialization script for Avalanche Fuji Testnet (Chain ID: 43113).
 * Deploys the complete anUSD Dual-Class Securitization Suite, links all smart contracts, and exports addresses.
 */
contract DeployFuji {
    // Avalanche Fuji Testnet Addresses
    address public constant FUJI_CHAINLINK_AVAX_USD = 0x5498BB86e9D018D222BF7B8971c67420515605E8;
    address public constant FUJI_TELEPORTER_MESSENGER = 0x253b2784c75e510dD0fF1da844684a1aC0aa5fcf;

    // Configurable Initial Parameters
    uint256 public constant INITIAL_AVAX_PRICE = 25 * 1e18; // $25.00 USD
    uint256 public constant SENIOR_COUPON_R = 0.073 * 1e18; // 7.30% APR
    uint256 public constant BARRIER_H_U = 2.00 * 1e18;      // $2.00 Upper Barrier
    uint256 public constant BARRIER_H_D = 0.25 * 1e18;      // $0.25 Lower Barrier

    struct DeployedContracts {
        address savaxCollateral;
        address oracleAdapter;
        address custodianVault;
        address tokenA;
        address tokenB;
        address tokenAPrime_anUSD;
        address tokenBPrime_Yield;
        address trancheSplitter;
        address resetController;
        address dynamicSubsidy;
        address yieldRecycler;
        address teleporterAdapter;
    }

    event DeploymentComplete(
        address vault,
        address anUSD,
        address splitter,
        address controller,
        address yieldRecycler
    );

    function run(
        address validatorTreasury,
        address ecosystemTreasury
    ) external returns (DeployedContracts memory contracts) {
        address deployer = msg.sender;
        if (validatorTreasury == address(0)) validatorTreasury = deployer;
        if (ecosystemTreasury == address(0)) ecosystemTreasury = deployer;

        // 1. Deploy Mock Liquid Staking Collateral (sAVAX)
        MocksAVAX savax = new MocksAVAX();
        contracts.savaxCollateral = address(savax);

        // 2. Deploy Chainlink Oracle Adapter
        ChainlinkOracleAdapter oracle = new ChainlinkOracleAdapter(FUJI_CHAINLINK_AVAX_USD);
        contracts.oracleAdapter = address(oracle);

        // 3. Deploy Custodian Vault
        CustodianVault vault = new CustodianVault(
            address(savax),
            INITIAL_AVAX_PRICE,
            address(oracle)
        );
        contracts.custodianVault = address(vault);

        // 4. Deploy Tranche Tokens
        TrancheToken tokenA = new TrancheToken(
            "Class A Senior Bond",
            "clA",
            ITrancheToken.TrancheType.CLASS_A,
            address(vault)
        );
        contracts.tokenA = address(tokenA);

        TrancheToken tokenB = new TrancheToken(
            "Class B Leveraged Equity",
            "clB",
            ITrancheToken.TrancheType.CLASS_B,
            address(vault)
        );
        contracts.tokenB = address(tokenB);

        TrancheToken tokenAPrime = new TrancheToken(
            "Avalanche Native USD",
            "anUSD",
            ITrancheToken.TrancheType.CLASS_A_PRIME,
            address(vault)
        );
        contracts.tokenAPrime_anUSD = address(tokenAPrime);

        TrancheToken tokenBPrime = new TrancheToken(
            "Class B Prime Leveraged Yield",
            "clBPrime",
            ITrancheToken.TrancheType.CLASS_B_PRIME,
            address(vault)
        );
        contracts.tokenBPrime_Yield = address(tokenBPrime);

        // 5. Deploy Tranche Splitter
        TrancheSplitter splitter = new TrancheSplitter(
            address(tokenA),
            address(tokenAPrime),
            address(tokenBPrime)
        );
        contracts.trancheSplitter = address(splitter);

        // 6. Deploy Reset Controller
        ResetController controller = new ResetController(
            address(vault),
            address(tokenA),
            address(tokenB),
            SENIOR_COUPON_R,
            BARRIER_H_U,
            BARRIER_H_D,
            address(oracle)
        );
        contracts.resetController = address(controller);

        // 7. Authorize and Link Smart Contracts
        tokenA.setResetController(address(controller));
        tokenB.setResetController(address(controller));
        
        tokenA.setSplitter(address(splitter));
        tokenAPrime.setSplitter(address(splitter));
        tokenBPrime.setSplitter(address(splitter));

        vault.initializeTranches(
            address(tokenA),
            address(tokenB),
            address(controller)
        );

        // 8. Deploy Dynamic Validator Subsidy Controller
        DynamicValidatorSubsidy subsidy = new DynamicValidatorSubsidy(INITIAL_AVAX_PRICE);
        contracts.dynamicSubsidy = address(subsidy);

        // 9. Deploy ACP-67 Yield Recycler
        YieldRecycler recycler = new YieldRecycler(
            validatorTreasury,
            ecosystemTreasury,
            address(subsidy)
        );
        contracts.yieldRecycler = address(recycler);

        // 10. Deploy Teleporter Cross-L1 Adapter
        TeleporterUSDAdapter teleporter = new TeleporterUSDAdapter(
            address(tokenAPrime),
            FUJI_TELEPORTER_MESSENGER
        );
        contracts.teleporterAdapter = address(teleporter);

        emit DeploymentComplete(
            address(vault),
            address(tokenAPrime),
            address(splitter),
            address(controller),
            address(recycler)
        );
    }
}
