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


from math import isclose

from structuraltools import aci, materials, unit


def test_calc_phi_compression_controlled():
    rebar = materials.Rebar(4)
    latex, phi = aci.sectional_strength.calc_phi(rebar, 0.002, return_latex=True)
    assert phi == 0.65
    assert latex == r"""$$ \begin{aligned}
    & \text{Since, } \left(\epsilon_t \leq \epsilon_{ty} \Leftarrow 0.002 \leq 0.002\right): & \phi &= 0.65
\\[10pt] \end{aligned} $$"""

def test_calc_phi_transition():
    rebar = materials.Rebar(4)
    latex, phi = aci.sectional_strength.calc_phi(rebar, 0.003, return_latex=True)
    assert isclose(phi, 0.7275862083, abs_tol=1e-8)
    assert latex == r"""$$ \begin{aligned}
    & \text{Since, } \left(\epsilon_{ty} < \epsilon_t < \epsilon_{ty} + 0.003 \Leftarrow 0.002 < 0.003 < 0.005\right):
        \\[10pt]
        & \qquad \phi = 0.65 + 0.25 \cdot \frac{\epsilon_t - \epsilon_{ty}}{0.003} = 0.65 + 0.25 \cdot \frac{0.003 - 0.002}{0.003} &= 0.728
\\[10pt] \end{aligned} $$"""

def test_calc_phi_tension_controlled():
    rebar = materials.Rebar(4)
    latex, phi = aci.sectional_strength.calc_phi(rebar, 0.006, return_latex=True)
    assert phi == 0.9
    assert latex == r"""$$ \begin{aligned}
    & \text {Since, } \left(\epsilon_t \geq \epsilon_{ty} \Leftarrow 0.006 \geq 0.005\right): & \phi &= 0.9
\\[10pt] \end{aligned} $$"""

def test_moment_capacity():
    concrete = materials.Concrete(4*unit.ksi)
    rebar = materials.Rebar(4)
    latex, phi, M_n = aci.sectional_strength.moment_capacity(
        b=8*unit.inch,
        d=12*unit.inch,
        concrete=concrete,
        rebar=rebar,
        n=3,
        return_latex=True)
    assert isclose((phi*M_n).to("kipft").magnitude, 30.61323529, abs_tol=1e-8)
    print(latex)
    assert latex == r"""
    $$ \begin{aligned}
        a &= \frac{n \cdot A_b \cdot f_y}{0.85 \cdot f'_c \cdot b} = \frac{3 \cdot 0.2\ \mathrm{in}^{2} \cdot 60000\ \mathrm{psi}}{0.85 \cdot 4000\ \mathrm{psi} \cdot 8\ \mathrm{in}} &= 1.324\ \mathrm{in}
        \\[10pt]
        M_n &= n \cdot A_b \cdot f_y \cdot \left(d - \frac{a}{2}\right) = 3 \cdot 0.2\ \mathrm{in}^{2} \cdot 60000\ \mathrm{psi} \cdot \left(12\ \mathrm{in} - \frac{1.324\ \mathrm{in}}{2}\right) &= 34.015\ \mathrm{kipft}
        \\[10pt]
        \epsilon_t &= 0.003 \cdot \left(\frac{\beta_1 \cdot d_t}{a} - 1\right) = 0.003 \cdot \left(\frac{0.85 \cdot 12\ \mathrm{in}}{1.324\ \mathrm{in}} - 1\right) &= 0.02
    \\[10pt] \end{aligned} $$
    $$ \begin{aligned}
    & \text {Since, } \left(\epsilon_t \geq \epsilon_{ty} \Leftarrow 0.02 \geq 0.005\right): & \phi &= 0.9
\\[10pt] \end{aligned} $$
"""

