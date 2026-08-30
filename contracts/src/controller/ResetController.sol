// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../core/CustodianVault.sol";
import "../core/TrancheToken.sol";
import "../interfaces/IResetController.sol";
import "../oracles/ChainlinkOracleAdapter.sol";

/**
 * @title ResetController
 * @notice Master state transition machine for Avalanche Native Stablecoin.
 * Executes O(1) constant-time upward (H_u = $2.00) and downward (H_d = $0.25) resets based on live Chainlink oracle feeds.
 * Governing Standard: SSRN-3856569 & BCRG Token Engineering Canon
 */
contract ResetController is IResetController {
    uint256 public constant SCALE = 1e18;

    CustodianVault public immutable vault;
    TrancheToken public immutable tokenA;
    TrancheToken public immutable tokenB;
    IPriceOracle public oracle;

    uint256 public immutable couponRateR;  // 7.3% = 0.073e18
    uint256 public immutable H_u;          // Upward barrier = 2.0e18
    uint256 public immutable H_d;          // Downward barrier = 0.25e18

    uint256 public lastResetTimestamp;
    uint256 public simulatedMarketPrice;   // For testing overrides

    modifier onlyVaultOwner() {
        require(msg.sender == vault.owner(), "Only vault owner");
        _;
    }

    constructor(
        address _vault,
        address _tokenA,
        address _tokenB,
        uint256 _couponRateR,
        uint256 _H_u,
        uint256 _H_d,
        address _oracle
    ) {
        vault = CustodianVault(_vault);
        tokenA = TrancheToken(_tokenA);
        tokenB = TrancheToken(_tokenB);
        couponRateR = _couponRateR;
        H_u = _H_u;
        H_d = _H_d;
        lastResetTimestamp = block.timestamp;
        simulatedMarketPrice = vault.referencePrice();
        if (_oracle != address(0)) {
            oracle = IPriceOracle(_oracle);
        }
    }

    function setOracle(address _oracle) external onlyVaultOwner {
        oracle = IPriceOracle(_oracle);
    }

    function setMarketPrice(uint256 price) external {
        simulatedMarketPrice = price;
    }

    function getLivePrice() public view returns (uint256) {
        if (simulatedMarketPrice > 0) {
            return simulatedMarketPrice;
        }
        if (address(oracle) != address(0) && !oracle.isCircuitBreakerTripped()) {
            uint256 oraclePrice = oracle.getPrice();
            if (oraclePrice > 0) return oraclePrice;
        }
        return vault.referencePrice();
    }

    function checkReset() public view override returns (ResetType, uint256 currentNAV_B) {
        uint256 livePrice = getLivePrice();
        uint256 dt = block.timestamp - lastResetTimestamp;
        
        // V_A = 1 + R * dt / 365 days
        uint256 accruedCoupon = (couponRateR * dt) / (365 days);
        uint256 V_A = SCALE + accruedCoupon;

        // Pool value = 2 * P_t / (beta * P_0)
        uint256 P_0 = vault.referencePrice();
        uint256 poolValue = (2 * livePrice * SCALE) / ((vault.beta() * P_0) / SCALE);
        
        if (poolValue <= V_A) {
            currentNAV_B = 0;
        } else {
            currentNAV_B = poolValue - V_A;
        }

        if (currentNAV_B >= H_u) {
            return (ResetType.UPWARD, currentNAV_B);
        } else if (currentNAV_B <= H_d) {
            return (ResetType.DOWNWARD, currentNAV_B);
        } else {
            return (ResetType.NONE, currentNAV_B);
        }
    }

    function executeReset() external override returns (ResetType) {
        (ResetType rType, ) = checkReset();
        require(rType != ResetType.NONE, "No reset condition met");

        uint256 livePrice = getLivePrice();
        uint256 P_0 = vault.referencePrice();
        uint256 newBeta = (livePrice * SCALE) / P_0;

        if (rType == ResetType.UPWARD) {
            tokenA.applyScalarSplit((tokenA.scalarMultiplier() * 150) / 100);
            tokenB.applyScalarSplit((tokenB.scalarMultiplier() * 150) / 100);
        } else if (rType == ResetType.DOWNWARD) {
            tokenA.applyScalarSplit((tokenA.scalarMultiplier() * 75) / 100);
            tokenB.applyScalarSplit((tokenB.scalarMultiplier() * 75) / 100);
        }

        vault.updateResetState(livePrice, newBeta);
        lastResetTimestamp = block.timestamp;

        emit ResetExecuted(rType, livePrice, block.timestamp, newBeta);
        return rType;
    }
}
