import os

tex_path = "/home/hash/Hub/Projects/avalanche-native-stablecoin/docs/WHITEPAPER.tex"

with open(tex_path, "r", encoding="utf-8") as f:
    content = f.read()

target = r"""\begin{table}[H]
\centering
\caption{Governance Parameter Choices and Structural Trade-Offs}
\label{tab:governance_tradeoffs}
\resizebox{\textwidth}{!}{%
\begin{tabular}{@{}lccl@{}}
\toprule
\textbf{Decision Parameter} & \textbf{Proposed Default} & \textbf{Alternative Option} & \textbf{Primary Economic Trade-Off} \\ \midrule
\textbf{Downward Barrier ($H_d$)} & \$0.25 NAV & \$0.35 NAV & Lower barrier reduces reset frequency; higher barrier increases crash buffer \\
\textbf{Senior Coupon ($R$)}      & 7.30\% p.a. & 6.00\% p.a. & Higher coupon attracts Class A capital; lower coupon reduces leverage cost \\
\textbf{ACP-67 Burn Share}        & 65.00\%     & 50.00\%     & Higher burn accelerates AVAX deflation; lower burn expands validator rewards \\ \bottomrule
\end{tabular}%
}
\end{table}"""

replacement = r"""\begin{table}[H]
\centering
\caption{The 20-Dimensional Protocol Governance Parameter Surface ($\Theta \subset \mathbb{R}^{23}$)}
\label{tab:governance_tradeoffs}
\resizebox{\textwidth}{!}{%
\begin{tabular}{@{}llllcl@{}}
\toprule
\textbf{Subsystem} & \textbf{Parameter Name} & \textbf{Code Symbol} & \textbf{Baseline} & \textbf{Corridor} & \textbf{Economic Role \& Trade-Off} \\ \midrule
\textbf{1. Tranching} & Senior Coupon Rate & $R$ & \textbf{7.30\%} & $[4.0\%, 12.0\%]$ & Determines Class A bond yield; drives senior capital inflows. \\
& anUSD Benchmark Coupon & $R'$ & \textbf{3.00\%} & $[1.0\%, 5.0\%]$ & Baseline money-market yield paid to anUSD transactors. \\
& Bear Market Subsidy & $\tilde{R}$ & \textbf{10.00\%} & $[0.0\%, 20.0\%]$ & Subsidy from A to B on downward reset to retain equity capital. \\
& Tranche Split Ratio & $\chi$ & \textbf{1.00} & $[0.50, 2.00]$ & Initial ratio of Class A to Class B minted per collateral deposit. \\
& Contract Maturity Horizon & $T$ & \textbf{365 d} & $[90, 730\text{ d}]$ & Maximum elapsed time before scheduled contractual renewal. \\ \midrule
\textbf{2. Dynamic Resets} & Upward Split Barrier & $H_u$ & \textbf{\$2.00} & $[\$1.50, \$3.00]$ & NAV threshold executing $1.50\times$ share split to de-leverage Class B. \\
& Downward Merger Barrier & $H_d$ & \textbf{\$0.25} & $[\$0.15, \$0.40]$ & NAV threshold executing $0.75\times$ reverse split to preserve solvency. \\
& Upward Split Multiplier & $\mu_{\text{split}}$ & \textbf{1.50$\times$} & $[1.20, 2.00]$ & Share balance expansion multiplier during upward reset. \\
& Downward Merge Multiplier & $\mu_{\text{merge}}$ & \textbf{0.75$\times$} & $[0.50, 0.90]$ & Share balance contraction multiplier during downward reset. \\
& MEV Proximity Band & $\delta_{\text{lock}}$ & \textbf{$\pm 1.50\%$} & $[\pm 0.5\%, \pm 3.0\%]$ & Proximity band around $H_u, H_d$ triggering 1-block delay lock. \\ \midrule
\textbf{3. Feedback Control}& Proportional Gain & $K_p$ & \textbf{0.150} & $[0.01, 1.00]$ & Primary responsiveness to instantaneous secondary AMM price spread. \\
& Integral Gain & $K_i$ & \textbf{0.020} & $[0.001, 0.10]$ & Integrates error to eliminate persistent secondary peg offsets. \\
& Derivative Gain & $K_d$ & \textbf{0.005} & $[0.000, 0.05]$ & Damps high-frequency secondary DEX price oscillations. \\
& Max Dynamic Rate Clamp & $\Delta R'_{\max}$ & \textbf{$\pm 5.00\%$} & $[\pm 2.0\%, \pm 10.0\%]$ & Anti-windup ceiling preventing excessive rate fluctuations. \\
& DEX TWAP Window Length & $\Delta t_{\text{sample}}$ & \textbf{1800 s} & $[600, 7200\text{ s}]$ & Sampling duration for secondary market price filtering (30 min). \\ \midrule
\textbf{4. ACP-67 Waterfall}& AVAX Buyback \& Burn Share & $\omega_{\text{burn}}$ & \textbf{65.00\%} & $[40.0\%, 80.0\%]$ & Staking yield allocated to programmatic open-market AVAX burns. \\
& Validator Incentive Boost & $\omega_{\text{val}}$ & \textbf{20.00\%} & $[10.0\%, 35.0\%]$ & Staking yield allocated to active Avalanche validator rewards. \\
& Sovereign L1 Grants & $\omega_{\text{l1}}$ & \textbf{15.00\%} & $[5.0\%, 25.0\%]$ & Staking yield allocated to cross-L1 Teleporter bridge incentives. \\
& Primary Mint Fee & $f_{\text{mint}}$ & \textbf{10 bps} & $[0, 50\text{ bps}]$ & Protocol issuance fee ($0.10\%$) routed to revenue waterfall. \\
& Primary Redemption Fee & $f_{\text{redeem}}$ & \textbf{10 bps} & $[0, 50\text{ bps}]$ & Protocol redemption fee ($0.10\%$) routed to revenue waterfall. \\ \midrule
\textbf{5. Circuit Breakers}& Max Spot/TWAP Divergence & $\Delta P_{\max}$ & \textbf{$\pm 8.00\%$} & $[\pm 3.0\%, \pm 15.0\%]$ & Circuit breaker threshold pausing vault operations during manipulation. \\
& Max Oracle Staleness & $\tau_{\text{heart}}$ & \textbf{300 s} & $[60, 900\text{ s}]$ & Maximum allowable Chainlink oracle heartbeat delay. \\
& Daily Gross Mint Throttle & $L_{\text{cap}}$ & \textbf{\$50M/d} & $[\$10\text{M}, \$500\text{M}]$ & Maximum daily gross deposit inflow throttle during bootstrap. \\ \bottomrule
\end{tabular}%
}
\end{table}"""

if target in content:
    content = content.replace(target, replacement)
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully updated Table 4 with 20-Dimensional Governance Registry in WHITEPAPER.tex")
else:
    print("Target string not found in WHITEPAPER.tex")
