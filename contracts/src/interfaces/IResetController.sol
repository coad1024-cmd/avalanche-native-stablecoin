// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IResetController {
    enum ResetType { NONE, UPWARD, DOWNWARD }

    event ResetExecuted(ResetType indexed resetType, uint256 triggerPrice, uint256 timestamp, uint256 newBeta);

    function checkReset() external view returns (ResetType, uint256 currentNAV_B);
    function executeReset() external returns (ResetType);
}
