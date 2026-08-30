// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../interfaces/ITrancheToken.sol";

/**
 * @title TrancheToken
 * @notice Implements an O(1) constant-time rebasing ERC-20 token for dual-class tranches.
 * Upward/Downward resets update the global scalar multiplier in O(1) gas without iterating balances.
 */
contract TrancheToken is ITrancheToken {
    string public name;
    string public symbol;
    uint8 public constant decimals = 18;
    uint256 public constant SCALE = 1e18;

    TrancheType public immutable override trancheType;
    address public immutable vault;
    address public resetController;
    address public splitter;

    uint256 public override scalarMultiplier; // Base 1e18
    uint256 private _totalRawSupply;
    mapping(address => uint256) private _rawBalances;
    mapping(address => mapping(address => uint256)) private _allowances;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event ScalarUpdated(uint256 previousMultiplier, uint256 newMultiplier);

    modifier onlyAuthorized() {
        require(msg.sender == vault || msg.sender == resetController || msg.sender == splitter, "Unauthorized");
        _;
    }

    constructor(string memory _name, string memory _symbol, TrancheType _type, address _vault) {
        name = _name;
        symbol = _symbol;
        trancheType = _type;
        vault = _vault;
        scalarMultiplier = SCALE;
    }

    function setResetController(address _controller) external {
        require(resetController == address(0), "Already set");
        resetController = _controller;
    }

    function setSplitter(address _splitter) external {
        require(splitter == address(0), "Already set");
        splitter = _splitter;
    }

    function totalSupply() public view returns (uint256) {
        return (_totalRawSupply * scalarMultiplier) / SCALE;
    }

    function balanceOf(address account) public view override returns (uint256) {
        return (_rawBalances[account] * scalarMultiplier) / SCALE;
    }

    function rawBalanceOf(address account) external view override returns (uint256) {
        return _rawBalances[account];
    }

    function mint(address to, uint256 rawAmount) external override onlyAuthorized {
        _totalRawSupply += rawAmount;
        _rawBalances[to] += rawAmount;
        emit Transfer(address(0), to, (rawAmount * scalarMultiplier) / SCALE);
    }

    function burn(address from, uint256 rawAmount) external override onlyAuthorized {
        require(_rawBalances[from] >= rawAmount, "Burn amount exceeds raw balance");
        _rawBalances[from] -= rawAmount;
        _totalRawSupply -= rawAmount;
        emit Transfer(from, address(0), (rawAmount * scalarMultiplier) / SCALE);
    }

    function applyScalarSplit(uint256 newMultiplier) external override onlyAuthorized {
        require(newMultiplier > 0, "Invalid multiplier");
        emit ScalarUpdated(scalarMultiplier, newMultiplier);
        scalarMultiplier = newMultiplier;
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        _transfer(msg.sender, to, amount);
        return true;
    }

    function allowance(address owner, address spender) external view returns (uint256) {
        return _allowances[owner][spender];
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        _allowances[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) external returns (bool) {
        uint256 currentAllowance = _allowances[from][msg.sender];
        if (currentAllowance != type(uint256).max) {
            require(currentAllowance >= amount, "Allowance exceeded");
            _allowances[from][msg.sender] = currentAllowance - amount;
        }
        _transfer(from, to, amount);
        return true;
    }

    function _transfer(address from, address to, uint256 amount) internal {
        require(from != address(0) && to != address(0), "Zero address");
        uint256 rawAmount = (amount * SCALE) / scalarMultiplier;
        require(_rawBalances[from] >= rawAmount, "Insufficient balance");
        _rawBalances[from] -= rawAmount;
        _rawBalances[to] += rawAmount;
        emit Transfer(from, to, amount);
    }
}
