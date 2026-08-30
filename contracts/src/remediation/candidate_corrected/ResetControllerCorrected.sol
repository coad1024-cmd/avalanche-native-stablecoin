// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../../core/CustodianVault.sol";
import "../../core/TrancheToken.sol";
import "../../interfaces/IResetController.sol";
import "../../oracles/ChainlinkOracleAdapter.sol";

/**
 * @title ResetControllerCorrected (Corrected Candidate Implementation)
 * @notice Corrects CONTRA-01 / VULN-01 by normalizing pool value cleanly as 2 * (P_t / P_0)
 *         and preventing denominator price ratio squaring.
 */
contract ResetControllerCorrected is IResetController {
    uint256 public constant SCALE = 1e18;

    CustodianVault public immutable vault;
    TrancheToken public immutable tokenA;
    TrancheToken public immutable tokenB;
    IPriceOracle public oracle;

    uint256 public immutable couponRateR;
    uint256 public immutable H_u;
    uint256 public immutable H_d;

    uint256 public lastResetTimestamp;
    uint256 public simulatedMarketPrice;

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
        
        uint256 accruedCoupon = (couponRateR * dt) / (365 days);
        uint256 V_A = SCALE + accruedCoupon;

        // CORRECTED: Normalized collateral index S = livePrice / P_0
        uint256 P_0 = vault.referencePrice();
        require(P_0 > 0, "Invalid reference price");
        uint256 poolValue = (2 * livePrice * SCALE) / P_0;
        
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
        
        // Cumulative beta update: beta_new = beta_old * (livePrice / P_0)
        uint256 currentBeta = vault.beta();
        if (currentBeta == 0) currentBeta = SCALE;
        uint256 newBeta = (currentBeta * livePrice) / P_0;

        if (rType == ResetType.UPWARD) {
            uint256 splitRatio = (livePrice * SCALE) / P_0;
            tokenA.applyScalarSplit((tokenA.scalarMultiplier() * splitRatio) / SCALE);
            tokenB.applyScalarSplit((tokenB.scalarMultiplier() * splitRatio) / SCALE);
        } else if (rType == ResetType.DOWNWARD) {
            uint256 mergeRatio = (livePrice * SCALE) / P_0;
            tokenA.applyScalarSplit((tokenA.scalarMultiplier() * mergeRatio) / SCALE);
            tokenB.applyScalarSplit((tokenB.scalarMultiplier() * mergeRatio) / SCALE);
        }

        vault.updateResetState(livePrice, newBeta);
        lastResetTimestamp = block.timestamp;

        emit ResetExecuted(rType, livePrice, block.timestamp, newBeta);
        return rType;
    }
}
