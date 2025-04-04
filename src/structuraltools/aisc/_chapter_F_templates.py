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


from structuraltools import MathTemplate


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
