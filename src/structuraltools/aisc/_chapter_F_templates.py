# Copyright 2025 Joe Bears
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from structuraltools import LatexTemplate, MarkdownTemplate, MathTemplate


eq_F2_1 = MathTemplate(r"M_p &= F_y \cdot Z_x = $F_y \cdot $Z_x &= $M_p")

eq_F2_2 = MathTemplate(r"""M_{ltb} &= C_b \cdot \left(M_p - \left(M_p - 0.7 \cdot F_y \cdot S_x\right) \cdot \left(\frac{L_b - L_p}{L_r - L_p}\right)\right)
    \\
    &= $C_b \cdot \left($M_p - \left($M_p - 0.7 \cdot $F_y \cdot $S_x\right) \cdot \left(\frac{$L_b - $L_p}{$L_r - $L_p}\right)\right)
    \\
    &= $M_ltb""")

eq_F2_3 = MathTemplate(r"M_{ltb} &= F_{cr} \cdot S_x = $F_cr \cdot $S_x &= $M_ltb")

eq_F2_4 = MathTemplate(r"""F_{cr} &= \frac{C_b \cdot \pi^2 \cdot E}{\left(\frac{L_b}{r_{ts}}\right)^2} \cdot \sqrt{1 + 0.078 \cdot \frac{J \cdot c}{S_x \cdot h_o} \cdot \left(\frac{L_b}{r_{ts}}\right)^2}
    \\
    &= \frac{$C_b \cdot \pi^2 \cdot $E}{\left(\frac{$L_b}{$r_ts}\right)^2} \cdot \sqrt{1 + 0.078 \cdot \frac{$J \cdot $c}{$S_x \cdot $h_o} \cdot \left(\frac{$L_b}{$r_ts}\right)^2}
    \\
    &= $F_cr""")

eq_F2_5 = MathTemplate(r"L_p &= 1.76 \cdot r_y \cdot \sqrt{\frac{E}{F_y}} = 1.76 \cdot $r_y \cdot \sqrt{\frac{$E}{$F_y}} &= $L_p")

eq_F2_6 = MathTemplate(r"""L_r &= 1.95 \cdot r_{ts} \cdot \frac{E}{0.7 \cdot F_y} \cdot \sqrt{\frac{J \cdot c}{S_x \cdot h_o} + \sqrt{\left(\frac{J \cdot c}{S_x \cdot h_o}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot F_y}{E}\right)^2}}
    \\
    &= 1.95 \cdot $r_ts \frac{$E}{0.7 \cdot $F_y} \cdot \sqrt{\frac{$J \cdot $c}{$S_x \cdot $h_o} + \sqrt{\left(\frac{$J \cdot $c}{$S_x \cdot $h_o}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot $F_y}{$E}\right)^2}}
    \\
    &= $L_r""")

eq_F2_8b = MathTemplate(r"c &= \frac{h_o}{2} \cdot \sqrt{\frac{I_y}{C_w}} = \frac{$h_o}{2} \cdot \sqrt{\frac{$I_y}{$C_w}} &= $c")

sec_F2_1 = LatexTemplate(r"""\begin{aligned}
    $M_p_str
\end{aligned}""")

sec_F2_2_plastic = LatexTemplate(r"""\begin{aligned}
    $L_p_str
    \\[10pt]
    \text{Since, } & \left(L_b \leq L_p \Leftarrow $L_b \leq $L_p\right):
        \\[10pt]
        M_{ltb} &= M_p = $M_p &= $M_ltb
\end{aligned}""")

sec_F2_2_inelastic = LatexTemplate(r"""\begin{aligned}
    $L_p_str
    \\[10pt]
    $L_r_str
    \\[10pt]
    \text{Since, } & \left(L_p < L_b \leq L_r \Leftarrow $L_p < $L_b \leq $L_r\right):
        \\[10pt]
        $M_ltb_str
\end{aligned}""")

sec_F2_2_elastic = LatexTemplate(r"""\begin{aligned}
    $L_r_str
    \\[10pt]
    \text{Since, } & \left(L_b > L_r \Leftarrow $L_b > $L_r\right):
        \\[10pt]
        $F_cr_str
        \\[10pt]
        $M_ltb_str
\end{aligned}""")

sec_F2 = MarkdownTemplate(r"""$header Plastic Moment Capacity
$$$$ $M_p_str $$$$
<br/>
$header Lateral-Torsional Buckling Moment Capacity
$$$$ $M_ltb_str $$$$
<br/>
$header Nominal Moment Capacity
$$$$ \begin{aligned}
    M_n &= \operatorname{min}\left(M_p,\ M_{ltb}\right) = \operatorname{min}\left($M_p,\ $M_ltb\right) &= $M_n
\end{aligned} $$$$""")

eq_F3_1 = MathTemplate(r"""M_flb &= M_p - \left(M_p - 0.7 \cdot F_y \cdot S_x\right) \left(\frac{\lambda_f - \lambda_{pf}}{\lambda_{rf} - \lambda_{pf}}\right)
    \\
    &= $M_p - \left($M_p - 0.7 \cdot $F_y \cdot $S_x\right) \left(\frac{$lamb_f - $lamb_pf}{$lamb_rf - $lamb_pf}\right)
    &= $M_flb""")
