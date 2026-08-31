# Behavioral Parameter Audit (BPA)

## Objective

The Behavioral Parameter Audit (BPA) skill provides a systematic protocol for auditing behavioral parameters in simulation models, digital twins, and economic specifications. It prevents misinterpreting parameter roles (such as confusing static response magnitude with dynamic adjustment speed) by tracing every parameter from economic theory to mathematical definitions, source code implementation, and empirical identification.

---

## Core Philosophy

Never trust:
* parameter names,
* documentation prose,
* code comments,
* variable names,

until verified against the actual source code implementation and governing equations.

Treat the **source code and governing mathematical equations** as the ground truth.

The purpose of this skill is to ensure that economics, mathematics, code implementation, calibration, and empirical claims remain strictly consistent.

---

## Standard Audit Workflow

When auditing any behavioral parameter, perform the following 10-step evaluation:

### Step 1: Economic Interpretation
Determine the underlying economic decision:
* What real-world decision does this parameter represent?
* Which agent archetype does it belong to (validator, delegator, governance, market)?
* What behavioral margin does it influence (entry, exit, renewal, duration choice, commission choice, stake allocation, liquidity preference, risk aversion)?

### Step 2: Mathematical Definition
Locate the governing equation. Write the equation explicitly and identify:
* dependent variable
* independent variables
* functional form (linear, logit, hazard, utility, state transition, difference equation, ODE)

### Step 3: Parameter Classification
Determine the parameter class:
* utility coefficient, elasticity, regression coefficient, correlation, sensitivity coefficient, adjustment speed, learning rate, discount factor, probability, threshold, state transition coefficient, diffusion coefficient, interaction term.
* Never infer parameter class from variable names.

### Step 4: Code Trace
Locate every occurrence of the parameter in the codebase. For every occurrence:
* show the code snippet and equation
* explain what quantity it multiplies or modifies
* determine whether it alters magnitude, timing, probability, utility, state, transition, or payoff.

### Step 5: Dynamic vs. Static Classification
Determine whether the parameter is:
* Static: $y = a + b \cdot x$
* Dynamic: $x_{t+1} = x_t + \alpha \cdot (x^* - x_t)$

Never confuse response magnitude ($b = \frac{\partial y}{\partial x}$) with adjustment speed ($\alpha$).

### Step 6: Units Audit
Identify explicit physical and economic units (for example: probability, utility, percentage points, log(APY), days, weeks, AVAX, or dimensionless).

### Step 7: Identification Audit
Evaluate empirical identifiability against available data:
* Can the dataset identify this parameter?
* Check for insufficient variation, multicollinearity, flat objective surfaces, weak excitation, sparse observations, single-regime data, or parameter redundancy.

### Step 8: Calibration Audit
Explain the calibration decision:
* Why was this parameter fitted, or why was it fixed/pinned?
* If fixed, document whether it was due to theoretical requirements, lack of data identification, pre-registration design, or simplifying assumptions.

### Step 9: Documentation Consistency
Compare report prose, mathematical equations, software implementation, and variable names. Identify any discrepancies and recommend corrected prose or parameter names.

### Step 10: Scientific Claims Audit
Review every scientific claim involving the parameter:
* Differentiate clearly between descriptive statistics, structural parameters, causal estimates, and validation targets.
* Replace overstatements (such as "validated") with precise descriptions (such as "consistent with").

---

## Output Format

Every parameter audit output must include the following 11 sections:

1. **Economic Meaning**
2. **Mathematical Definition**
3. **Parameter Type**
4. **Code Implementation**
5. **Dynamic Behaviour**
6. **Units**
7. **Identifiability**
8. **Calibration Decision**
9. **Documentation Consistency**
10. **Scientific Interpretation**
11. **Recommended Improvements**

---

## General Principles

Always distinguish between:
* Correlation vs. Causation
* Elasticity vs. Utility Coefficient
* Sensitivity vs. Adjustment Speed
* Static Mapping vs. Dynamic Process
* Calibration vs. Validation
* Structural Model vs. Reduced-Form Model
* Prediction vs. Explanation
* Parameter Estimate vs. Validation Metric
* Model Assumption vs. Empirical Finding

Never infer semantics from variable names. Always verify using equations and code implementation.
