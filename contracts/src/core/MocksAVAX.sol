// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title MocksAVAX
 * @notice Mock Liquid Staked AVAX (sAVAX) token for Avalanche Fuji Testnet and local fuzzing.
 * Allows users to deposit native testnet AVAX or call faucet() to receive sAVAX.
 */
contract MocksAVAX {
    string public constant name = "Mock Staked AVAX";
    string public constant symbol = "sAVAX";
    uint8 public constant decimals = 18;

    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Deposited(address indexed user, uint256 avaxAmount, uint256 savaxMinted);

    receive() external payable {
        deposit();
    }

    function deposit() public payable {
        require(msg.value > 0, "Zero deposit");
        _mint(msg.sender, msg.value);
        emit Deposited(msg.sender, msg.value, msg.value);
    }

    function faucet(uint256 amount) external {
        require(amount <= 1000 ether, "Faucet limit exceeded");
        _mint(msg.sender, amount);
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        _transfer(msg.sender, to, amount);
        return true;
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) external returns (bool) {
        uint256 currentAllowance = allowance[from][msg.sender];
        if (currentAllowance != type(uint256).max) {
            require(currentAllowance >= amount, "Insufficient allowance");
            allowance[from][msg.sender] = currentAllowance - amount;
        }
        _transfer(from, to, amount);
        return true;
    }

    function _transfer(address from, address to, uint256 amount) internal {
        require(balanceOf[from] >= amount, "Insufficient balance");
        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        emit Transfer(from, to, amount);
    }

    function _mint(address to, uint256 amount) internal {
        totalSupply += amount;
        balanceOf[to] += amount;
        emit Transfer(address(0), to, amount);
    }
}
