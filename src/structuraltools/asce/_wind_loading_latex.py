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

calc_K_z = Template(r"""
    $$$$ \begin{aligned}
        K_z &= 2.41 \cdot \frac{\operatorname{max}\left(z, 15 \mathrm{ft}\right)}{z_g}^{\frac{2}{\alpha}} = 2.41 \cdot \frac{\operatorname{max}\left($z , 15 \mathrm{ft}\right)}{$z_g}^{\frac{2}{$alpha}} &= $K_z
    \end{aligned} $$$$
""")

calc_K_z_high = Template(r"""
    $$$$ \begin{aligned}
        & \text{Since, } \left(z > z_g \Leftarrow $z > $z_g\right): & K_z &= $K_z
    \end{aligned} $$$$
""")

calc_q_z = Template(r"q_z &= 0.00256 \cdot K_z \cdot K_{zt} \cdot K_e \cdot V^2 = 0.00256 \cdot $K_z \cdot $K_zt \cdot $K_e \cdot $V^2 &= $q_z")
