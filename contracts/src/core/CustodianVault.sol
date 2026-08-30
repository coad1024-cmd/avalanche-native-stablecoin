// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "./TrancheToken.sol";
import "../interfaces/ICustodianVault.sol";

contract CustodianVault is ICustodianVault {
    uint256 public constant SCALE = 1e18;

    address public immutable owner;
    TrancheToken public tokenA;
    TrancheToken public tokenB;
    address public resetController;

    uint256 public override totalCollateral;
    uint256 public override referencePrice; // USD with 18 decimals
    uint256 public beta;                    // Cumulative conversion scaling factor (Base 1e18)

    event DepositAndMint(address indexed user, uint256 collateralIn, uint256 mintedA, uint256 mintedB);
    event RedeemAndBurn(address indexed user, uint256 burnedA, uint256 burnedB, uint256 collateralOut);
    event StateReset(uint256 newReferencePrice, uint256 newBeta);
    event PriceUpdated(uint256 newPrice);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    modifier onlyControllerOrOwner() {
        require(msg.sender == resetController || msg.sender == owner, "Unauthorized");
        _;
    }

    constructor(uint256 _initialPrice) payable {
        owner = msg.sender;
        referencePrice = _initialPrice;
        beta = SCALE;
    }

    function initializeTranches(address _tokenA, address _tokenB, address _controller) external onlyOwner {
        require(address(tokenA) == address(0), "Already initialized");
        tokenA = TrancheToken(_tokenA);
        tokenB = TrancheToken(_tokenB);
        resetController = _controller;
    }

    function setReferencePrice(uint256 newPrice) external onlyOwner {
        referencePrice = newPrice;
        emit PriceUpdated(newPrice);
    }

    function depositAndMint(uint256 collateralAmount) external override returns (uint256 mintedA, uint256 mintedB) {
        require(collateralAmount > 0, "Zero deposit");
        totalCollateral += collateralAmount;

        // 1 unit collateral generates pairs according to reference conversion
        uint256 pairAmount = (collateralAmount * referencePrice) / SCALE;
        
        tokenA.mint(msg.sender, pairAmount);
        tokenB.mint(msg.sender, pairAmount);

        emit DepositAndMint(msg.sender, collateralAmount, pairAmount, pairAmount);
        return (pairAmount, pairAmount);
    }

    function redeemAndBurn(uint256 rawAmountA, uint256 rawAmountB) external override returns (uint256 collateralReturned) {
        require(rawAmountA == rawAmountB && rawAmountA > 0, "Must redeem matching pairs");
        
        tokenA.burn(msg.sender, rawAmountA);
        tokenB.burn(msg.sender, rawAmountB);

        collateralReturned = (rawAmountA * SCALE) / referencePrice;
        require(totalCollateral >= collateralReturned, "Insufficient pool reserves");
        totalCollateral -= collateralReturned;

        emit RedeemAndBurn(msg.sender, rawAmountA, rawAmountB, collateralReturned);
        return collateralReturned;
    }

    function updateResetState(uint256 newPrice, uint256 newBeta) external onlyControllerOrOwner {
        referencePrice = newPrice;
        beta = newBeta;
        emit StateReset(newPrice, newBeta);
    }
}
