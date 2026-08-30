// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../core/TrancheToken.sol";

/**
 * @title TeleporterUSDAdapter
 * @notice Adapter for Avalanche Inter-Chain Messaging (ICM / Teleporter) cross-L1 dispatching.
 * Burns anUSD on the origin L1 and emits cross-chain payload for native minting on target L1.
 */
contract TeleporterUSDAdapter {
    TrancheToken public immutable anUSD;
    address public immutable owner;

    event TeleportDispatched(
        bytes32 indexed destinationBlockchainID,
        address indexed destinationAddress,
        address indexed sender,
        uint256 amount
    );

    event TeleportReceived(
        bytes32 indexed originBlockchainID,
        address indexed recipient,
        uint256 amount
    );

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    constructor(address _anUSD) {
        anUSD = TrancheToken(_anUSD);
        owner = msg.sender;
    }

    function sendCrossChain(bytes32 destinationBlockchainID, address destinationAddress, uint256 amount) external {
        require(amount > 0, "Zero amount");
        
        // Burn anUSD on local chain
        anUSD.burn(msg.sender, amount);

        emit TeleportDispatched(destinationBlockchainID, destinationAddress, msg.sender, amount);
    }

    function receiveCrossChain(bytes32 originBlockchainID, address recipient, uint256 amount) external onlyOwner {
        require(amount > 0, "Zero amount");

        // Mint native anUSD on destination chain
        anUSD.mint(recipient, amount);

        emit TeleportReceived(originBlockchainID, recipient, amount);
    }
}
