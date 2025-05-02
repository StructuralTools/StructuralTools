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


from structuraltools.template import Template


eq_F2_1 = Template("Math", r"M_p &= F_y \cdot Z_x = $F_y \cdot $Z_x &= $M_p")

eq_F2_2 = Template("Math", r"""M_{ltb} &= C_b \cdot \left(M_p - \left(M_p - 0.7 \cdot F_y \cdot S_x\right) \cdot \left(\frac{L_b - L_p}{L_r - L_p}\right)\right)
    \\
    &= $C_b \cdot \left($M_p - \left($M_p - 0.7 \cdot $F_y \cdot $S_x\right) \cdot \left(\frac{$L_b - $L_p}{$L_r - $L_p}\right)\right)
    \\
    &= $M_ltb""")

eq_F2_3 = Template("Math", r"M_{ltb} &= F_{cr} \cdot S_x = $F_cr \cdot $S_x &= $M_ltb")

eq_F2_4 = Template("Math", r"""F_{cr} &= \frac{C_b \cdot \pi^2 \cdot E}{\left(\frac{L_b}{r_{ts}}\right)^2} \cdot \sqrt{1 + 0.078 \cdot \frac{J \cdot c}{S_x \cdot h_o} \cdot \left(\frac{L_b}{r_{ts}}\right)^2}
    \\
    &= \frac{$C_b \cdot \pi^2 \cdot $E}{\left(\frac{$L_b}{$r_ts}\right)^2} \cdot \sqrt{1 + 0.078 \cdot \frac{$J \cdot $c}{$S_x \cdot $h_o} \cdot \left(\frac{$L_b}{$r_ts}\right)^2}
    \\
    &= $F_cr""")

eq_F2_5 = Template("Math", r"L_p &= 1.76 \cdot r_y \cdot \sqrt{\frac{E}{F_y}} = 1.76 \cdot $r_y \cdot \sqrt{\frac{$E}{$F_y}} &= $L_p")

eq_F2_6 = Template("Math", r"""L_r &= 1.95 \cdot r_{ts} \cdot \frac{E}{0.7 \cdot F_y} \cdot \sqrt{\frac{J \cdot c}{S_x \cdot h_o} + \sqrt{\left(\frac{J \cdot c}{S_x \cdot h_o}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot F_y}{E}\right)^2}}
    \\
    &= 1.95 \cdot $r_ts \frac{$E}{0.7 \cdot $F_y} \cdot \sqrt{\frac{$J \cdot $c}{$S_x \cdot $h_o} + \sqrt{\left(\frac{$J \cdot $c}{$S_x \cdot $h_o}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot $F_y}{$E}\right)^2}}
    \\
    &= $L_r""")

eq_F2_8b = Template("Math", r"c &= \frac{h_o}{2} \cdot \sqrt{\frac{I_y}{C_w}} = \frac{$h_o}{2} \cdot \sqrt{\frac{$I_y}{$C_w}} &= $c")

sec_F2_1 = Template("Latex", r"""\begin{aligned}
    $M_p_str
\end{aligned}""")

sec_F2_2_plastic = Template("Latex", r"""\begin{aligned}
    $L_p_str
    \\[10pt]
    \text{Since, } & \left(L_b \leq L_p \Leftarrow $L_b \leq $L_p\right):
        \\[10pt]
        M_{ltb} &= M_p = $M_p &= $M_ltb
\end{aligned}""")

sec_F2_2_inelastic = Template("Latex", r"""\begin{aligned}
    $L_p_str
    \\[10pt]
    $L_r_str
    \\[10pt]
    \text{Since, } & \left(L_p < L_b \leq L_r \Leftarrow $L_p < $L_b \leq $L_r\right):
        \\[10pt]
        $M_ltb_str
\end{aligned}""")

sec_F2_2_elastic = Template("Latex", r"""\begin{aligned}
    $L_r_str
    \\[10pt]
    \text{Since, } & \left(L_b > L_r \Leftarrow $L_b > $L_r\right):
        \\[10pt]
        $F_cr_str
        \\[10pt]
        $M_ltb_str
\end{aligned}""")

sec_F2 = Template("Markdown", r"""$header Plastic Moment Capacity
$$$$ $M_p_str $$$$
<br/>
$header Lateral-Torsional Buckling Moment Capacity
$$$$ $M_ltb_str $$$$
<br/>
$header Nominal Moment Capacity
$$$$ \begin{aligned}
    M_n &= \operatorname{min}\left(M_p,\ M_{ltb}\right) = \operatorname{min}\left($M_p,\ $M_ltb\right) &= $M_n
\end{aligned} $$$$""")

eq_F3_1 = Template("Math", r"""M_{flb} &= M_p - \left(M_p - 0.7 \cdot F_y \cdot S_x\right) \left(\frac{\lambda_f - \lambda_{pf}}{\lambda_{rf} - \lambda_{pf}}\right)
    \\
    &= $M_p - \left($M_p - 0.7 \cdot $F_y \cdot $S_x\right) \left(\frac{$lamb_f - $lamb_pf}{$lamb_rf - $lamb_pf}\right)
    \\
    &= $M_flb""")

eq_F3_2 = Template("Math", r"M_{flb} &= \frac{0.9 \cdot E \cdot k_c \cdot S_x}{\lambda_f^2} = \frac{0.9 \cdot $E \cdot $k_c \cdot $S_x}{$lamb_f^2} &= $M_flb")

eq_F3_2a = Template("Math", r"k_c &= \operatorname{min}\left(\operatorname{max}\left(0.35,\ \frac{4}{\sqrt{\lambda_w}}\right),\ 0.76\right) = \operatorname{min}\left(\operatorname{max}\left(0.35,\ \frac{4}{\sqrt{$lamb_w}}\right),\ 0.76\right) &= $k_c")

sec_F3_2_noncompact = Template("Latex", r"""\begin{aligned}
    $lamb_pf_str
    \\[10pt]
    $lamb_rf_str
    \\[10pt]
    \text{Since, } & \left(\lambda_{pf} \leq \lambda_f < \lambda_{rf} \Leftarrow $lamb_pf \leq $lamb_f < $lamb_rf\right):
        \\[10pt]
        $M_flb_str
\end{aligned}""")

sec_F3_2_slender = Template("Latex", r"""\begin{aligned}
    $lamb_rf_str
    \\[10pt]
    \text{Since, } & \left(\lambda_f \geq \lambda_{rf} \Leftarrow $lamb_f \geq $lamb_rf\right):
        \\[10pt]
        $k_c_str
        \\[10pt]
        $M_flb_str
\end{aligned}""")

sec_F3 = Template("Markdown", r"""$header Plastic Moment
$$$$ $M_p_str $$$$
<br/>
$header Lateral-Torsional Buckling Moment Capacity
$$$$ $M_ltb_str $$$$
<br/>
$header Compression Flange Local Buckling Moment Capacity
$$$$ $M_flb_str $$$$
<br/>
$header Nominal Moment Capacity
$$$$ \begin{aligned}
    M_n &= \operatorname{min}\left(M_{ltb},\ M_{flb}\right) = \operatorname{min} \left($M_ltb,\ $M_flb\right) &= $M_n
\end{aligned} $$$$""")

eq_F11_1 = Template("Math", r"M_p &= \operatorname{min}\left(F_y \cdot Z_x,\ 1.5 \cdot F_y \cdot S_x\right) = \operatorname{min}\left($F_y \cdot $Z_x,\ 1.5 \cdot $F_y \cdot $S_x\right) &= $M_p")

eq_F11_3 = Template("Math", r"""M_{ltb} &= C_b \cdot \left(1.52 - 0.274 \cdot \left(\frac{L_b \cdot d}{t^2}\right) \cdot \frac{F_y}{E}\right) \cdot F_y \cdot S_x
    \\
    &= $C_b \cdot \left(1.52 - 0.274 \cdot \left(\frac{$L_b \cdot $d}{\left($t\right)^2}\right) \cdot \frac{$F_y}{$E}\right) \cdot $F_y \cdot $S_x
    \\
    &= $M_ltb""")

eq_F11_4 = Template("Math", r"M_{ltb} &= F_{cr} \cdot S_x = $F_cr \cdot $S_x &= $M_ltb")

eq_F11_5 = Template("Math", r"F_{cr} &= \frac{1.9 \cdot E \cdot C_b}{\frac{L_b \cdot d}{t^2}} = \frac{1.9 \cdot $E \cdot $C_b}{\frac{$L_b \cdot $d}{\left($t\right)^2}} &= $F_cr")

sec_F11_1_rect = Template("Latex", r"""\begin{aligned}
    $M_p_str
\end{aligned}""")

sec_F11_2_plastic = Template("Latex", r"""\begin{aligned}
    \text{Since, } & \left(\frac{L_b \cdot d}{t^2} \leq \frac{0.08 \cdot E}{F_y} \Leftarrow \frac{$L_b \cdot $d}{\left($t\right)^2} \leq \frac{0.08 \cdot $E}{$F_y}\right):
        \\[10pt]
        M_{ltb} &= M_p = $M_p &= $M_ltb
\end{aligned}""")

sec_F11_2_inelastic = Template("Latex", r"""\begin{aligned}
    \text{Since, } & \left(\frac{0.08 \cdot E}{F_y} < \frac{L_b \cdot d}{t^2} \leq \frac{1.9 \cdot E}{F_y} \Leftarrow \frac{0.08 \cdot $E}{$F_y} < \frac{$L_b \cdot $d}{\left($t\right)^2} \leq \frac{1.9 \cdot $E}{$F_y}\right):
        \\[10pt]
        $M_ltb_str
\end{aligned}""")

sec_F11_2_elastic = Template("Latex", r"""\begin{aligned}
    \text{Since, } & \left(\frac{L_b \cdot d}{t^2} > \frac{1.9 \cdot E}{F_y} \Leftarrow \frac{$L_b \cdot $d}{\left($t\right)^2} > \frac{1.9 \cdot $E}{$F_y}\right):
        \\[10pt]
        $F_cr_str
        \\[10pt]
        $M_ltb_str
\end{aligned}""")

sec_F11 = Template("Markdown", r"""$header Plastic Moment Capacity
$$$$ $M_p_str $$$$
<br/>
$header Lateral-Torsional Buckling Moment Capacity
$$$$ $M_ltb_str $$$$
<br/>
$header Nominal Moment Capacity
$$$$ \begin{aligned}
    M_n &= \operatorname{min}\left(M_p,\ M_{ltb}\right) = \operatorname{min}\left($M_p,\ $M_ltb\right) &= $M_n
\end{aligned} $$$$""")
