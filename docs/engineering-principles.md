# Engineering Principles — Avalanche Native Stablecoin (`anUSD`)

**Governing Standard:** BCRG Senior Engineering Standard  
**Owner:** Bonding Curve Research Group (BCRG)  
**Status:** Canonical Standard · August 2026  

---

## 0. The Prime Directive

**Every number, unit, and modeling choice must be traceable to a primary source, an official ACP, or an explicit parameter sweep.**  
A reviewer reading any rendered report or simulation must be able to trace any parameter (e.g. $0.0730$, $0.25$, $0.65$) directly to:
1. The foundational paper (**SSRN-3856569**),
2. The filed proposal (**ACP-67**),
3. On-chain empirical Avalanche calibration data, or
4. An entry in `params.PSUU_SWEEPS`.

No silent constants, no orphan assumptions.

---

## 1. Magic Numbers & Constants

1. **No Bare Numeric Literals in Code:** Every governance lever, physical constant, or behavioral elasticity is a named entry in `params.py` with an explicit docstring and citation.
2. **Physical Constants Named at Module Level:**
   ```python
   DAYS_PER_YEAR = 365.0
   SECONDS_PER_YEAR = 31536000
   MACHINE_EPSILON = 1e-12
   ```
3. **Fixed Deterministic Seeds:** All simulation experiments fix random seeds (e.g. `seed = 20260521`) for 100% bitwise reproducibility.

---

## 2. Units & Conventions

1. **Yields & Rates:** Always **annualized fractions** (`0.0730` for 7.30%), never percentages as raw integers. Daily conversion is explicit:
   $$\Delta t = \frac{1.0}{365.0}$$
2. **Tokens & Amounts:** Denominated in standard token units ($AVAX$, $sAVAX$, $\text{anUSD}$), normalized in decimal adapters.
3. **Time Fractions:** $v(t)$ is in continuous years; daily increments are explicitly $\Delta t = \frac{1}{365}$.

---

## 3. Pure Mechanism Logic & Pluggability

1. **Pure Mechanism Functions:** Functions in `simulations/cadcad_core/mechanisms/` must be pure: output depends strictly on inputs, with zero hidden global state or side effects.
2. **Pluggable Curves:** Where design alternatives exist (e.g., linear vs PI-controlled benchmark rate $R'$, Kou double-exponential vs Merton log-normal jumps), the mechanism accepts a selector parameter.
3. **Validate Inputs & Fail Loud:** If state variables violate invariant bounds (e.g. $V_B < -0.01$ or $\text{gap} > 10^{-6}$), the simulation must fail immediately with an explicit diagnostic error.

---

## 4. Invariant Assertion Gates

Every state transition must assert:
1. **Solvency Conservation:**
   $$\left| V_A(t) + V_B(t) - 2 \cdot S(t) \right| \le 10^{-12}$$
2. **Sub-Tranche Value Parity:**
   $$\left| V_{A'}(t) + V_{B'}(t) - 2 \cdot V_A(t) \right| \le 10^{-12}$$
3. **Principal Preservation:**
   $$V_{A'}(t) \ge 1.00 \quad \forall \Delta P \ge -60.00\%$$

---

## 5. Result Provenance & Lineage Tracking

Every simulation run must record:
1. Git Commit SHA of the simulation codebase.
2. Parameter dictionary and random seed.
3. Output dataset SHA-256 hash.
4. Timestamp appended to `data/_lineage.jsonl`.
