## 2026-08-30T11:25:00Z

<USER_REQUEST>
You are worker_2.
Your working directory is: /home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/worker_2

MANDATORY FIRST STEP:
Read `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/ORIGINAL_REQUEST.md` and `/home/hash/Hub/Projects/avalanche-native-stablecoin/PROJECT.md`.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

WRITE OWNERSHIP:
You have exclusive write ownership of:
- `simulations/cadcad_core/mechanisms/pide_solver.py`
- `simulations/cadcad_core/params.py`
- `simulations/cadcad_core/mechanisms/tranche_math.py`
- `docs/reports/OPEN_SOURCE_TOOLING_AUDIT.md`
- `data/_lineage.jsonl`
- Your own working directory `.agents/worker_2/`

INPUTS TO READ:
1. `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/explorer_remediation_1/handoff.md` (Full, verified remediation diffs and specification)
2. `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/challenger_1/handoff.md`
3. `/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/challenger_2/handoff.md`
4. `/home/hash/Hub/Projects/avalanche-native-stablecoin/docs/reports/OPEN_SOURCE_TOOLING_AUDIT.md`

YOUR TASKS:
Execute the complete remediation plan detailed in `explorer_remediation_1/handoff.md`:
1. **Fix PIDE Solver (`simulations/cadcad_core/mechanisms/pide_solver.py`)**:
   Implement the unconditionally stable IMEX Crank-Nicolson finite-difference solver with Thomas algorithm ($O(N_S)$ tridiagonal matrix solver) for the Merton-Kou jump-diffusion pricing surface.
2. **Fix Module Imports (`simulations/cadcad_core/params.py` and `tranche_math.py`)**:
   - Add `DEFAULT_PARAMS = {**DEFAULT_GOVERNANCE_LEVERS, **DEFAULT_ENV_PARAMS}` to `params.py`.
   - Add `verify_solvency_invariant` function to `mechanisms/tranche_math.py`.
3. **Upgrade Audit Deliverable (`docs/reports/OPEN_SOURCE_TOOLING_AUDIT.md`)**:
   - Section 3.1: Add `SimulationTelemetry` dataclass; update `SystemState` to include all 28 canonical fields; expand `GovernanceLevers` and `EnvironmentParams` validators.
   - Section 3.3: Upgrade `CanonicalInvariantValidator` to enforce admissible domain ($V_B \ge 0$), physical vault conservation ($|C_{\text{pool}} P_{\text{spot}} - \text{Liabilities}| \le \text{tol}$), and check historical rebase scalars.
   - Section 3.4: Update Float64 precision table to real IEEE 754 limits (ULP $\approx \text{TVL} \times 2^{-52} \approx 1.49 \times 10^{-8}$ at $\$100\text{M}$ TVL, $\approx 14.90\text{ Gwei}$) and document Solidity fixed-point truncation dust tolerances.
   - Section 6.2: Synchronize JSON Schema with Merkle hash chaining (`prev_record_hash`), `sequence_id`, and specify Canonical JSON serialization.
4. **Update Lineage Ledger (`data/_lineage.jsonl`)**:
   Rewrite `data/_lineage.jsonl` with Canonical JSON records matching 100% of the Section 6.2 schema with valid Merkle hash chaining.
5. **Run Verification & Test Suites**:
   - Run `python3 workflows/validation/adversarial_challenge_harness.py` (ensure 4/4 challenge tests pass).
   - Run `python3 simulations/cadcad_core/experiments/run_pide_surface.py` (ensure PIDE solver executes cleanly with bounded outputs).
   - Run `python3 simulations/cadcad_core/experiments/run_monte_carlo.py` and `python3 simulations/cadcad_core/experiments/run_black_swan_replays.py`.
   - Run `forge test` in `contracts/`.

Deliver your handoff report in `.agents/worker_2/handoff.md`, update `progress.md`, and send a completion message.
</USER_REQUEST>
