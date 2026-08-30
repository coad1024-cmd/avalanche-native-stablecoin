// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title DynamicValidatorSubsidy
 * @notice Computes countercyclical validator income subsidy shares based on AVAX price drawdowns and staking yield compression.
 * Governing Standard: BCRG Avalanche Validator Economic Decision Architecture (G.VALIDATOR_MARKET)
 */
contract DynamicValidatorSubsidy {
    address public immutable owner;

    // Basis points denominator (100.00% = 10000)
    uint256 public constant TOTAL_BPS = 10000;

    // Boundary parameters
    uint256 public constant BASE_VALIDATOR_BPS = 2000; // 20.00%
    uint256 public constant MAX_VALIDATOR_BPS = 4500;  // 45.00%
    uint256 public constant ECOSYSTEM_BPS = 1500;      // 15.00%
    uint256 public constant MIN_BURN_BPS = 4000;       // 40.00%

    // Responsiveness parameters (scaled by 1e18)
    uint256 public constant KAPPA_DRAWDOWN = 3500;     // 0.35 in BPS scale

    // Exponential Moving Average tracking
    uint256 public emaPrice;
    uint256 public lastEmaTimestamp;
    uint256 public constant EMA_ALPHA_BPS = 500;       // Weight for new price (5.00%)

    event EmaPriceUpdated(uint256 oldEma, uint256 newEma, uint256 spotPrice, uint256 timestamp);
    event DynamicAllocationCalculated(uint256 valBps, uint256 burnBps, uint256 ecoBps, uint256 drawdownBps);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    constructor(uint256 _initialPrice) {
        require(_initialPrice > 0, "Price must be positive");
        owner = msg.sender;
        emaPrice = _initialPrice;
        lastEmaTimestamp = block.timestamp;
    }

    /**
     * @notice Updates the 90-day EMA reference price with a new spot observation
     * @param spotPrice Current spot oracle price (18 decimals)
     */
    function updateEmaPrice(uint256 spotPrice) public {
        require(spotPrice > 0, "Invalid spot price");
        
        uint256 oldEma = emaPrice;
        // EMA = (alpha * spot) + ((1 - alpha) * oldEma)
        uint256 newEma = (EMA_ALPHA_BPS * spotPrice + (TOTAL_BPS - EMA_ALPHA_BPS) * oldEma) / TOTAL_BPS;
        
        emaPrice = newEma;
        lastEmaTimestamp = block.timestamp;
        
        emit EmaPriceUpdated(oldEma, newEma, spotPrice, block.timestamp);
    }

    /**
     * @notice Computes dynamic allocation shares based on current spot price vs EMA
     * @param spotPrice Current spot price (18 decimals)
     * @return valBps Basis points allocated to active validator boost (e.g. 2000 - 4500)
     * @return burnBps Basis points allocated to open-market AVAX buyback & burn (e.g. 4000 - 6500)
     * @return ecoBps Basis points allocated to sovereign L1 & ecosystem grants (1500)
     */
    function computeDynamicShares(uint256 spotPrice) public view returns (
        uint256 valBps,
        uint256 burnBps,
        uint256 ecoBps
    ) {
        ecoBps = ECOSYSTEM_BPS;
        
        if (spotPrice >= emaPrice || emaPrice == 0) {
            // Normal / Bull market: baseline 20% validator, 65% burn
            valBps = BASE_VALIDATOR_BPS;
            burnBps = TOTAL_BPS - valBps - ecoBps;
            return (valBps, burnBps, ecoBps);
        }

        // Drawdown = (emaPrice - spotPrice) / emaPrice (in BPS)
        uint256 drawdownBps = ((emaPrice - spotPrice) * TOTAL_BPS) / emaPrice;
        
        // Subsidy boost = kappa * drawdown
        uint256 subsidyBoostBps = (drawdownBps * KAPPA_DRAWDOWN) / TOTAL_BPS;
        
        valBps = BASE_VALIDATOR_BPS + subsidyBoostBps;
        if (valBps > MAX_VALIDATOR_BPS) {
            valBps = MAX_VALIDATOR_BPS;
        }

        burnBps = TOTAL_BPS - valBps - ecoBps;
        require(burnBps >= MIN_BURN_BPS, "Burn share below floor");
    }
}
