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


calc_phi_compression = Template(r"""$$$$ \begin{aligned}
    & \text{Since, } \left(\epsilon_t \leq \epsilon_{ty} \Leftarrow $epsilon_t \leq $epsilon_ty\right): & \phi &= $phi
\end{aligned} $$$$""")

calc_phi_transition = Template(r"""$$$$ \begin{aligned}
    & \text{Since, } \left(\epsilon_{ty} < \epsilon_t < \epsilon_{ty} + 0.003 \Leftarrow $epsilon_ty < $epsilon_t < $epsilon_ty003\right):
        \\[10pt]
        & \qquad \phi = 0.65 + 0.25 \cdot \frac{\epsilon_t - \epsilon_{ty}}{0.003}
            = 0.65 + 0.25 \cdot \frac{$epsilon_t - $epsilon_ty}{0.003}
            &= $phi
\end{aligned} $$$$""")

calc_phi_tension = Template(r"""$$$$ \begin{aligned}
    & \text {Since, } \left(\epsilon_t \geq \epsilon_{ty} \Leftarrow $epsilon_t \geq $epsilon_ty003\right): & \phi &= $phi
\end{aligned} $$$$""")

moment_capacity = Template(r"""$$$$ \begin{aligned}
    a &= \frac{n \cdot A_b \cdot f_y}{0.85 \cdot f'_c \cdot b}
        = \frac{$n \cdot $A_b \cdot $f_y}{0.85 \cdot $f_prime_c \cdot $b}
        &= $a
    \\[10pt]
    M_n &= n \cdot A_b \cdot f_y \cdot \left(d - \frac{a}{2}\right)
        = $n \cdot $A_b \cdot $f_y \cdot \left($d - \frac{$a}{2}\right)
        &= $M_n
    \\[10pt]
    \epsilon_t &= 0.003 \cdot \left(\frac{\beta_1 \cdot d_t}{a} - 1\right)
        = 0.003 \cdot \left(\frac{$beta_1 \cdot $d_t}{$a} - 1\right)
        &= $epsilon_t
    \\[10pt]
\end{aligned} $$$$
$phi_markdown""")
