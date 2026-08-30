// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface ICustodianVault {
    function depositAndMint(uint256 collateralAmount) external returns (uint256 mintedA, uint256 mintedB);
    function redeemAndBurn(uint256 rawAmountA, uint256 rawAmountB) external returns (uint256 collateralReturned);
    function totalCollateral() external view returns (uint256);
    function referencePrice() external view returns (uint256);
}
