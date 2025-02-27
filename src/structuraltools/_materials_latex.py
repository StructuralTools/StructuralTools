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


Concrete_lamb_low = Template(r"""
    \end{aligned} $$$$
    $$$$ \begin{aligned}
    & \text{Since, } \left(w_c \leq $low \Leftarrow $w_c \leq $low\right): & \lambda &= $lamb
    \end{aligned} $$$$
    $$$$ \begin{aligned}
""")

Concrete_lamb_mid = Template(r"""
    &  \text{Since, } \left($low < w_c \leq $high \Leftarrow $low < $w_c \leq $high\right):
    \\[10pt]
    & \qquad \lambda = \operatorname{min}\left(0.0075 \cdot \frac{w_c}{\mathrm{pcf}} ,\ 1\right) = \operatorname{min}\left(0.0075 \cdot \frac{$w_c}{\mathrm{pcf}} ,\ 1\right) &= $lamb
""")

Concrete_lamb_high = Template(r"""
    \end{aligned} $$$$
    $$$$ \begin{aligned}
    & \text{Since, } \left(w_c > $high \Leftarrow $w_c > $high\right): & \lambda &= $lamb
    \end{aligned} $$$$
    $$$$ \begin{aligned}
""")

Concrete_beta_1_low = Template(r"""
    \end{aligned} $$$$
    $$$$ \begin{aligned}
    & \text{Since, } \left(f'_c \leq $low \Leftarrow $f_prime_c \leq $low\right): & \beta_1 &= $beta_1
    \end{aligned} $$$$
    $$$$ \begin{aligned}
""")

Concrete_beta_1_mid = Template(r"""
    & \text{Since, } \left($low < f'_c < $high \Leftarrow $low < $f_prime_c < $high\right):
    \\[10pt]
    & \qquad \beta_1 = 0.85 - \frac{0.05 \cdot \left(f'_c - $low\right)}{1000\ \mathrm{psi}} &= $beta_1
""")

Concrete_beta_1_high = Template(r"""
    \end{aligned} $$$$
    $$$$ \begin{aligned}
    & \text{Since, } \left(f'_c \geq $high \Leftarrow $f_prime_c \geq $high\right): & \beta_1 &= $beta_1
    \end{aligned}$$$$
    $$$$ \begin{aligned}
""")

Concrete = Template(r"""
    $$$$ \begin{aligned}
        $lamb_str
        \\[10pt]
        $beta_1_str
        \\[10pt]
        E_c &= \left(\frac{w_c}{\mathrm{pcf}}\right)^{1.5} \cdot 33 \cdot \sqrt{f'_c \cdot \mathrm{psi}} = \left(\frac{$w_c}{\mathrm{pcf}}\right)^{1.5} \cdot 33 \cdot \sqrt{$f_prime_c \cdot \mathrm{psi}} &= $E_c
        \\[10pt]
        f_r &= 7.5 \cdot \lambda \cdot \sqrt{f'_c \cdot \mathrm{psi}} = 7.5 \cdot $lamb \cdot \sqrt{$f_prime_c \cdot \mathrm{psi}} &= $f_r
        \\[10pt]
    \end{aligned} $$$$
""")
