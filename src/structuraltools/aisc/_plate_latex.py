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


moment_plastic = Template(r"""
    \end{aligned} $$$$
    $$$$ \begin{aligned}
        & \text{Since, } \left(\frac{L_d \cdot d}{t^2} \leq \frac{0.08 \cdot E}{F_y} \Leftarrow $length \leq $short\right): & M_n &= M_p
    \end{aligned} $$$$
    $$$$ \begin{aligned}
""")

moment_ltb_short = Template(r"""
    & \text{Since, } \left(\frac{0.08 \cdot E}{F_y} < \frac{L_b \cdot d}{t^2} \leq \frac{1.9 \cdot E}{F_y} \Leftarrow $short < $length \leq $long\right):
        \\[10pt]
        & \qquad M_n = \operatorname{min}\left(C_b \cdot \left(1.52 - 0.274 \cdot \frac{L_b \cdot d \cdot F_y}{t^2 \cdot E}\right) \cdot F_y \cdot S_x ,\ M_p\right)
        \\
        & \qquad = \operatorname{min}\left($C_b \cdot \left(1.52 - 0.274 \cdot \frac{$L_b \cdot $d \cdot $F_y}{$t^2 \cdot $E}\right) \cdot $F_y \cdot $S_x ,\ $M_p\right)
        \\
        & \qquad = $M_n
""")

moment_ltb_long = Template(r"""
    & \text{Since, } \left(\frac{L_d \cdot d}{t^2} > \frac{1.9 \cdot E}{F_y} \Leftarrow $length > $long\right):
        \\
        & \qquad M_n = \operatorname{min}\left(\frac{1.9 \cdot E \cdot C_b \cdot t^2 \cdot S_x}{L_b \cdot d} ,\ M_p\right)
        \\
        & \qquad = \operatorname{min}\left(\frac{1.9 \cdot $E \cdot $C_b \cdot $t^2 \cdot $S_x}{$L_b \cdot $d} ,\ M_p\right)
        \\
        & \qquad = $M_n
""")

moment_capacity = Template(r"""
    $$$$ \begin{aligned}
        M_p &= \operatorname{min}\left(F_y \cdot Z_x ,\ 1.5 \cdot F_y \cdot S_x\right) = \operatorname{min}\left($F_y \cdot $Z_x ,\ 1.5 \cdot $F_y \cdot $S_x\right) &= $M_p
        \\[10pt]
        $M_n_str
        \\[10pt]
    \end{aligned} $$$$
""")

moment_minor_plastic = Template(r"""
    \end{aligned} $$$$
    $$$$ \begin{aligned}
        & \text{Since, } \left(\frac{L_d \cdot t}{d^2} \leq \frac{0.08 \cdot E}{F_y} \Leftarrow $length \leq $short\right): & M_n &= M_p
    \end{aligned} $$$$
    $$$$ \begin{aligned}
""")

moment_minor_ltb_short = Template(r"""
    & \text{Since, } \left(\frac{0.08 \cdot E}{F_y} < \frac{L_b \cdot t}{d^2} \leq \frac{1.9 \cdot E}{F_y} \Leftarrow $short < $length \leq $long\right):
        \\[10pt]
        & \qquad M_n = \operatorname{min}\left(C_b \cdot \left(1.52 - 0.274 \cdot \frac{L_b \cdot t \cdot F_y}{d^2 \cdot E}\right) \cdot F_y \cdot S_y ,\ M_p\right)
        \\
        & \qquad = \operatorname{min}\left($C_b \cdot \left(1.52 - 0.274 \cdot \frac{$L_b \cdot $t \cdot $F_y}{$d^2 \cdot $E}\right) \cdot $F_y \cdot $S_y ,\ $M_p\right)
        \\
        & \qquad = $M_n
""")

moment_minor_ltb_long = Template(r"""
    & \text{Since, } \left(\frac{L_d \cdot t}{d^2} > \frac{1.9 \cdot E}{F_y} \Leftarrow $length > $long\right):
        \\
        & \qquad M_n = \operatorname{min}\left(\frac{1.9 \cdot E \cdot C_b \cdot d^2 \cdot S_y}{L_b \cdot t} ,\ M_p\right)
        \\
        & \qquad = \operatorname{min}\left(\frac{1.9 \cdot $E \cdot $C_b \cdot $d^2 \cdot $S_y}{$L_b \cdot $t} ,\ M_p\right)
        \\
        & \qquad = $M_n
""")

moment_capacity_minor = Template(r"""
    $$$$ \begin{aligned}
        M_p &= \operatorname{min}\left(F_y \cdot Z_y ,\ 1.5 \cdot F_y \cdot S_y\right) = \operatorname{min}\left($F_y \cdot $Z_y ,\ 1.5 \cdot $F_y \cdot $S_y\right) &= $M_p
        \\[10pt]
        $M_n_str
        \\[10pt]
    \end{aligned} $$$$
""")

