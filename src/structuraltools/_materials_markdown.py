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


Concrete = Template(r"""$$$$ \begin{aligned}
    \lambda &= \operatorname{bound}\left(0.75,\ 0.0075 \cdot w_c,\ 1\right)
        = \operatorname{bound}\left(0.75,\ 0.0075 \cdot $w_c,\ 1\right)
        &= $lamb
    \\[10pt]
    E_c &= w_c^{1.5} \cdot 33 \cdot \sqrt{f'_c}
        = \left($w_c\right)^{1.5} \cdot 33 \cdot \sqrt{$f_prime_c}
        &= $E_c
    \\[10pt]
    f_r &= 7.5 \cdot \lambda \cdot \sqrt{f'_c}
        = 7.5 \cdot $lamb \cdot \sqrt{$f_prime_c}
        &= $f_r
    \\[10pt]
    \beta_1 &= \operatorname{bound}\left(0.65,\ 0.85 - \frac{0.05 \cdot \left(f'_c - 4000\ \mathrm{psi}\right)}{1000\ \mathrm{psi}},\ 0.85\right)
        \\
        &= \operatorname{bound}\left(0.65,\ 0.85 - \frac{0.05 \cdot \left($f_prime_c - 4000\ \mathrm{psi}\right)}{1000\ \mathrm{psi}},\ 0.85\right)
        \\
        &= $beta_1
\end{aligned} $$$$""")
