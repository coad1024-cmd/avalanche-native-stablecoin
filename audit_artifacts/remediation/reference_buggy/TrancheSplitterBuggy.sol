// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../../core/TrancheToken.sol";

/**
 * @title TrancheSplitterBuggy (Reference Bug-Preserving Implementation)
 * @notice Preserves CONTRA-02 / VULN-02 and CONTRA-03 / VULN-03.
 */
contract TrancheSplitterBuggy {
    TrancheToken public immutable tokenA;
    TrancheToken public immutable tokenAPrime; // anUSD Stablecoin
    TrancheToken public immutable tokenBPrime; // High Yield Tranche

    event SplitClassA(address indexed user, uint256 amountA, uint256 mintedAPrime, uint256 mintedBPrime);
    event MergeClassA(address indexed user, uint256 burnedAPrime, uint256 burnedBPrime, uint256 returnedA);

    constructor(address _tokenA, address _tokenAPrime, address _tokenBPrime) {
        tokenA = TrancheToken(_tokenA);
        tokenAPrime = TrancheToken(_tokenAPrime);
        tokenBPrime = TrancheToken(_tokenBPrime);
    }

    function split(uint256 amountA) external {
        require(amountA > 0, "Zero amount");
        tokenA.burn(msg.sender, amountA);
        
        tokenAPrime.mint(msg.sender, amountA);
        tokenBPrime.mint(msg.sender, amountA);

        emit SplitClassA(msg.sender, amountA, amountA, amountA);
    }

    function merge(uint256 amountAPrime, uint256 amountBPrime) external {
        require(amountAPrime == amountBPrime && amountAPrime > 0, "Must merge equal pairs");
        
        tokenAPrime.burn(msg.sender, amountAPrime);
        tokenBPrime.burn(msg.sender, amountBPrime);

        tokenA.mint(msg.sender, amountAPrime);

        emit MergeClassA(msg.sender, amountAPrime, amountBPrime, amountAPrime);
    }
}
