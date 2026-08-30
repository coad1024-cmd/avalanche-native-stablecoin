# 17-Point Preflight Quality Checklist for Stablecoin Deliverables

**Governing Standard:** BCRG Memo & Report Preflight Standard  
**Owner:** Bonding Curve Research Group (BCRG)  
**Status:** Canonical Checklist · August 2026  

---

## The 17-Point Preflight Checklist

Before any memo, whitepaper revision, or simulation report is promoted to production, it must satisfy all 17 preflight checks:

```
====================================================================================================
                        17-POINT PREFLIGHT VERIFICATION CHECKLIST
====================================================================================================
  [X] 01. Title & Headings      : Concise noun-phrase labels only (no sentence claims).
  [X] 02. Authorship            : Attributed strictly to Bonding Curve Research Group (BCRG).
  [X] 03. Abstract / Executive  : 200-300 words with explicit substantive findings and metrics.
  [X] 04. Prime Directive       : Every parameter traces to SSRN-3856569, ACP-67, or sweep list.
  [X] 05. Zero Magic Numbers    : Zero bare numeric literals in prose or code without citations.
  [X] 06. Exhibit Density       : Exactly one complete exhibit (table, chart, or Mermaid) per section.
  [X] 07. Math-Prose Pairing    : Every display equation motivated above and paraphrased below.
  [X] 08. Bold-First Terms      : Key terms bolded inline upon their first introduction.
  [X] 09. Substance-First Prose : Zero meta-commentary ("This section will show...").
  [X] 10. Voice & Tone          : First-person plural ("we"), active voice, objective academic stance.
  [X] 11. Banned Constructions  : Zero em-dashes, section signs (§), negative pivots, or filler buzzwords.
  [X] 12. Units & Percentages   : Rates as annualized decimals/percentages; no bare "yield" or "pp".
  [X] 13. Solvency Invariant    : |V_A + V_B - 2S| <= 1e-12 verified at machine precision.
  [X] 14. Crash Proof (Thm 1)   : Single-step crash tolerance verified >= 60.00% without loss.
  [X] 15. Control Damping       : PI secondary controller verified overdamped (zeta >= 1.0).
  [X] 16. LaTeX / PDF Sync      : WHITEPAPER.tex compiles via Tectonic with zero fatal errors.
  [X] 17. Lineage Tracking      : Git SHA and dataset hash recorded in data/_lineage.jsonl.
====================================================================================================
```
