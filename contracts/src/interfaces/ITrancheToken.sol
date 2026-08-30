// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface ITrancheToken {
    enum TrancheType { CLASS_A, CLASS_B, CLASS_A_PRIME, CLASS_B_PRIME }

    function trancheType() external view returns (TrancheType);
    function scalarMultiplier() external view returns (uint256);
    function mint(address to, uint256 rawAmount) external;
    function burn(address from, uint256 rawAmount) external;
    function applyScalarSplit(uint256 newMultiplier) external;
    function balanceOf(address account) external view returns (uint256);
    function rawBalanceOf(address account) external view returns (uint256);
}
