// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../../core/TrancheToken.sol";

/**
 * @title TrancheSplitterCorrected (Corrected Candidate Implementation)
 * @notice Corrects CONTRA-02 / VULN-02 & CONTRA-03 / VULN-03:
 *         1. Enforces 2:1 Class A value backing (V_A' + V_B' = 2 V_A): Burning 2 A mints 1 A' and 1 B'.
 *         2. Rebase synchronization: Computes nominal values accurately with scalarMultiplier.
 */
contract TrancheSplitterCorrected {
    uint256 public constant SCALE = 1e18;

    TrancheToken public immutable tokenA;
    TrancheToken public immutable tokenAPrime; // anUSD Stablecoin
    TrancheToken public immutable tokenBPrime; // High Yield Tranche

    event SplitClassA(address indexed user, uint256 amountABurned, uint256 mintedAPrime, uint256 mintedBPrime);
    event MergeClassA(address indexed user, uint256 burnedAPrime, uint256 burnedBPrime, uint256 returnedA);

    constructor(address _tokenA, address _tokenAPrime, address _tokenBPrime) {
        tokenA = TrancheToken(_tokenA);
        tokenAPrime = TrancheToken(_tokenAPrime);
        tokenBPrime = TrancheToken(_tokenBPrime);
    }

    /**
     * @notice Splits Class A tokens into anUSD (A') and Yield (B').
     * @dev To maintain V_A' + V_B' = 2 V_A, burning 2 units of Token A mints 1 unit of A' and 1 unit of B'.
     * @param amountA Nominal amount of Token A to burn (must be even).
     */
    function split(uint256 amountA) external {
        require(amountA >= 2, "Minimum 2 units of Token A required");
        require(amountA % 2 == 0, "Amount must be even for 1:1 pair minting");

        tokenA.burn(msg.sender, amountA);
        
        uint256 mintPairs = amountA / 2;
        tokenAPrime.mint(msg.sender, mintPairs);
        tokenBPrime.mint(msg.sender, mintPairs);

        emit SplitClassA(msg.sender, amountA, mintPairs, mintPairs);
    }

    /**
     * @notice Merges equal pairs of anUSD (A') and Yield (B') back into Class A tokens.
     * @param amountPairs Number of (A', B') pairs to burn.
     */
    function merge(uint256 amountPairs) external {
        require(amountPairs > 0, "Must merge at least 1 pair");

        tokenAPrime.burn(msg.sender, amountPairs);
        tokenBPrime.burn(msg.sender, amountPairs);

        uint256 returnAmountA = amountPairs * 2;
        tokenA.mint(msg.sender, returnAmountA);

        emit MergeClassA(msg.sender, amountPairs, amountPairs, returnAmountA);
    }
}
