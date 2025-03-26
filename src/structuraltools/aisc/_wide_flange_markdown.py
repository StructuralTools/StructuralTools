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


from string import Template


M_ltb_plastic = Template(r"""L_p &= 1.76 \cdot r_y \sqrt{\frac{E}{F_y}}
        = 1.76 \cdot $r_y \sqrt{\frac{$E}{$F_y}}
        &= $L_p
    \\[10pt]
    \text{Since, } & \left(L_b \leq L_p \Leftarrow $L_b \leq $L_p\right):
        \\[10pt]
        M_{ltb} &= M_p
            = $M_p
            &= $M_ltb""")

M_ltb_inelastic = Template(r"""L_p &= 1.76 \cdot r_y \sqrt{\frac{E}{F_y}}
        = 1.76 \cdot $r_y \sqrt{\frac{$E}{$F_y}}
        &= $L_p
    \\[10pt]
    L_r &= \frac{1.95 \cdot r_{ts} \cdot E}{0.7 \cdot F_y} \cdot \sqrt{\frac{J \cdot c}{S_x \cdot h_o} + \sqrt{\left(\frac{J \cdot c}{S_x \cdot h_o}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot F_y}{E}\right)^2}}
        \\
        &= \frac{1.95 \cdot $r_ts \cdot $E}{0.7 \cdot $F_y} \cdot \sqrt{\frac{$J \cdot $c}{$S_x \cdot $h_o} + \sqrt{\left(\frac{$J \cdot $c}{$S_x \cdot $h_o}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot $F_y}{$E}\right)^2}}
        \\
        &= $L_r
    \\[10pt]
    \text{Since, } & \left(L_p < L_b \leq L_r \Leftarrow $L_p < $L_b \leq $L_r\right):
        \\[10pt]
        M_{ltb} &= C_b \cdot \left(M_p - \left(M_p - 0.7 \cdot F_y \cdot S_x\right) \cdot \frac{L_b - L_p}{L_r - L_p}\right)
            \\
            &= $C_b \cdot \left($M_p - \left($M_p - 0.7 \cdot $F_y \cdot $S_x\right) \cdot \frac{$L_b - $L_p}{$L_r - $L_p}\right)
            \\
            &= $M_ltb""")

M_ltb_elastic = Template(r"""L_r &= \frac{1.95 \cdot r_{ts} \cdot E}{0.7 \cdot F_y} \cdot \sqrt{\frac{J \cdot c}{S_x \cdot h_o} + \sqrt{\left(\frac{J \cdot c}{S_x \cdot h_o}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot F_y}{E}\right)^2}}
        \\
        &= \frac{1.95 \cdot $r_ts \cdot $E}{0.7 \cdot $F_y} \cdot \sqrt{\frac{$J \cdot $c}{$S_x \cdot $h_o} + \sqrt{\left(\frac{$J \cdot $c}{$S_x \cdot $h_o}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot $F_y}{$E}\right)^2}}
        \\
        &= $L_r
    \\[10pt]
    \text{Since, } & \left(L_b > L_r \Leftarrow $L_b > $L_r\right):
        \\[10pt]
        M_{ltb} &= \frac{S_x \cdot C_b \cdot \pi^2 \cdot E}{\left(\frac{L_b}{r_{ts}}\right)^2} \cdot \sqrt{1 + \frac{0.078 \cdot J \cdot c}{S_x \cdot h_o} \cdot \left(\frac{L_b}{r_{ts}}\right)^2}
            \\
            &= \frac{$S_x \cdot $C_b \cdot \pi^2 \cdot $E}{\left(\frac{$L_b}{$r_ts}\right)^2} \cdot \sqrt{1 + \frac{0.078 \cdot $J \cdot $c}{$S_x \cdot $h_o} \cdot \left(\frac{$L_b}{$r_ts}\right)^2}
            \\
            &= $M_ltb""")

M_flb_compact = Template(r"""\lambda_{pf} &= 0.38 \cdot \sqrt{\frac{E}{F_y}}
        = 0.38 \cdot \sqrt{\frac{$E}{$F_y}}
        &= $lamb_pf
    \\[10pt]
    \text{Since, } & \left(\lambda_f < \lambda_{pf} \Leftarrow $lamb_f < $lamb_pf\right):
        \\[10pt]
        M_{flb} &= M_p
            = $M_p
            &= $M_flb""")

M_flb_noncompact = Template(r"""\lambda_{pf} &= 0.38 \cdot \sqrt{\frac{E}{F_y}}
        = 0.38 \cdot \sqrt{\frac{$E}{$F_y}}
        &= $lamb_pf
    \\[10pt]
    \lambda_{rf} &= 1 \cdot \sqrt{\frac{E}{F_y}}
        = 1 \cdot \sqrt{\frac{$E}{$F_y}}
        &= $lamb_rf
    \\[10pt]
    \text{Since, } & \left(\lambda_{pf} \leq \lambda_f < \lambda_{rf} \Leftarrow $lamb_pf \leq $lamb_f < $lamb_rf\right):
        \\[10pt]
        M_{flb} &= M_p - \left(M_p - 0.7 \cdot F_y \cdot S_x\right) \cdot \frac{\lambda_f - \lambda_{pf}} {\lambda_{rf} - \lambda_{pf}}
            \\
            &= $M_p - \left($M_p - 0.7 \cdot $F_y \cdot $S_x\right) \cdot \frac{$lamb_f - $lamb_pf}{$lamb_rf - $lamb_pf}
            \\
            &= $M_flb""")

M_flb_slender = Template(r"""\lambda_{rf} &= 1 \cdot \sqrt{\frac{E}{F_y}}
        = 1 \cdot \sqrt{\frac{$E}{$F_y}}
        &= $lamb_rf
    \\[10pt]
    \text {Since, } & \left(\lambda_f \geq \lambda_{rf} \Leftarrow $lamb_f \geq $lamb_rf\right):
        \\[10pt]
        k_c &= \operatorname{min}\left(\operatorname{max}\left(0.35,\ \frac{4}{\sqrt{\lambda_w}}\right),\ 0.76\right)
            = \operatorname{min}\left(\operatorname{max}\left(0.35,\ \frac{4}{\sqrt{$lamb_w}}\right),\ 0.76\right)
            &= $k_c
        \\[10pt]
        M_{flb} &= \frac{0.9 \cdot E \cdot k_c \cdot S_x}{\lambda_f^2}
            = \frac{0.9 \cdot $E \cdot $k_c \cdot $S_x}{$lamb_f^2}
            &= $M_flb""")

moment_capacity = Template(r"""$$$$ \begin{aligned}
    M_p &= F_y \cdot Z_x
        = $F_y \cdot $Z_x
        &= $M_p
    \\[10pt]
    \\[10pt]
    $M_ltb_template
    \\[10pt]
    \\[10pt]
    $M_flb_template
    \\[10pt]
    \\[10pt]
    M_n &= \operatorname{min}\left(M_p,\ M_{ltb},\ M_{flb}\right)
        = \operatorname{min}\left($M_p,\ $M_ltb,\ $M_flb\right)
        &= $M_n
\end{aligned} $$$$""")
