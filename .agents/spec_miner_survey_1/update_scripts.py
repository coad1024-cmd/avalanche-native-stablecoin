import re

# Update survey_academic_whitepaper.md
with open('/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/spec_miner_survey_1/survey_academic_whitepaper.md', 'r') as f:
    text = f.read()

# Replace the -52.40% calculation explanation with exact arithmetic
old_text = "3. **Crash from Barrier with Bear Subsidy ($\\tilde{R} = 10\\%, T = 100\\text{ days} = 0.274\\text{ yr}$):**\n   $$\\left(\\frac{\\Delta P}{P}\\right)_{\\text{subsidy}} = \\frac{1}{2} \\left( \\frac{1 + 0.03(0.274) + 0.20(0.274)}{1 + 0.073(0.274) + 0.25} \\right) - 1 = \\mathbf{-52.40\\%}$$"

new_text = "3. **Crash from Barrier with Bear Subsidy ($\\tilde{R} = 10\\%, T = 100\\text{ days} = 0.274\\text{ yr}$):**\n   $$\\left(\\frac{\\Delta P}{P}\\right)_{\\text{subsidy}} = \\frac{1}{2} \\left( \\frac{1 + 0.03(0.274) + 0.20(0.274)}{1 + 0.073(0.274) + 0.25} \\right) - 1 = \\frac{1}{2}\\left(\\frac{1.0630}{1.2700}\\right) - 1 = \\mathbf{-58.15\\%}$$\n   *(Note: SSRN Section 2.5 reports $-52.40\\%$, which corresponds to evaluating at an extended epoch $v_t \\approx 1.2\\text{ yr}$ or slightly different daily compounding conventions; at $v_t = 1.0\\text{ yr}$, the bound is $-53.51\\%$).*"

text = text.replace(old_text, new_text)

# Also update verification command in survey
old_cmd = '   print(f\'Crash Bound (With Subsidy): {bound_with_sub * 100:.2f}% (Expected: -52.40%)\')'
new_cmd = '   print(f\'Crash Bound (With Subsidy, T=100d): {bound_with_sub * 100:.2f}% (Expected: -58.15%)\')'
text = text.replace(old_cmd, new_cmd)

with open('/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/spec_miner_survey_1/survey_academic_whitepaper.md', 'w') as f:
    f.write(text)

# Update handoff.md
with open('/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/spec_miner_survey_1/handoff.md', 'r') as f:
    h_text = f.read()

old_h_cmd = """   b_no_sub = evaluate_single_step_crash_tolerance(0.073, 0.030, 0.25, 0.0, 0.0)
   b_sub = evaluate_single_step_crash_tolerance(0.073, 0.030, 0.25, 100.0/365.0, 0.10)
   assert abs(b_no_sub - (-0.60)) < 1e-4, f'Expected -60.0%, got {b_no_sub}'
   assert abs(b_sub - (-0.524)) < 1e-3, f'Expected -52.4%, got {b_sub}'
   print('Crash bounds independently verified: -60.00% (no subsidy), -52.40% (with subsidy)')"""

new_h_cmd = """   b_no_sub = evaluate_single_step_crash_tolerance(0.073, 0.030, 0.25, 0.0, 0.0)
   b_sub = evaluate_single_step_crash_tolerance(0.073, 0.030, 0.25, 100.0/365.0, 0.10)
   assert abs(b_no_sub - (-0.60)) < 1e-4, f'Expected -60.0%, got {b_no_sub}'
   assert abs(b_sub - (-0.5815)) < 1e-3, f'Expected -58.15%, got {b_sub}'
   print(f'Crash bounds independently verified: {b_no_sub*100:.2f}% (no subsidy), {b_sub*100:.2f}% (with subsidy at T=100d)')"""

h_text = h_text.replace(old_h_cmd, new_h_cmd)

# Also update logic chain text in handoff
old_lc = "returning $-60.00\\%$ (no subsidy) and $-52.40\\%$ (with $10\\%$ subsidy)."
new_lc = "returning $-60.00\\%$ (no subsidy) and $-58.15\\%$ (with $10\\%$ subsidy at $T=100\\text{ days}$; $-53.51\\%$ at $T=1\\text{ yr}$; SSRN reports $-52.4\\%$ at $v \\approx 1.2\\text{ yr}$)."
h_text = h_text.replace(old_lc, new_lc)

with open('/home/hash/Hub/Projects/avalanche-native-stablecoin/.agents/spec_miner_survey_1/handoff.md', 'w') as f:
    f.write(h_text)

print("Updated survey and handoff successfully.")
