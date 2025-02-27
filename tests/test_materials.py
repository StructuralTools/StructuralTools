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

from structuraltools import materials, unit


def test_Concrete_init_ultra_lightweight():
    concrete = materials.Concrete(4*unit.ksi, w_c=90*unit.pcf)
    assert concrete.f_prime_c == 4000*unit.psi
    assert isclose(concrete.E_c.magnitude, 1782000)
    assert concrete.E_c.units == "psi"
    assert concrete.lamb == 0.75
    assert concrete.beta_1 == 0.85
    assert isclose(concrete.f_r.magnitude, 355.7562368, abs_tol=1e-7)
    assert concrete.f_r.units == "psi"
    assert concrete.latex == r"""
    $$ \begin{aligned}
        
    \end{aligned} $$
    $$ \begin{aligned}
    & \text{Since, } \left(w_c \leq 100\ \mathrm{pcf} \Leftarrow 90\ \mathrm{pcf} \leq 100\ \mathrm{pcf}\right): & \lambda &= 0.75
    \end{aligned} $$
    $$ \begin{aligned}

        \\[10pt]
        
    \end{aligned} $$
    $$ \begin{aligned}
    & \text{Since, } \left(f'_c \leq 4000\ \mathrm{psi} \Leftarrow 4000\ \mathrm{psi} \leq 4000\ \mathrm{psi}\right): & \beta_1 &= 0.85
    \end{aligned} $$
    $$ \begin{aligned}

        \\[10pt]
        E_c &= \left(\frac{w_c}{\mathrm{pcf}}\right)^{1.5} \cdot 33 \cdot \sqrt{f'_c \cdot \mathrm{psi}} = \left(\frac{90\ \mathrm{pcf}}{\mathrm{pcf}}\right)^{1.5} \cdot 33 \cdot \sqrt{4000\ \mathrm{psi} \cdot \mathrm{psi}} &= 1782000.0\ \mathrm{psi}
        \\[10pt]
        f_r &= 7.5 \cdot \lambda \cdot \sqrt{f'_c \cdot \mathrm{psi}} = 7.5 \cdot 0.75 \cdot \sqrt{4000\ \mathrm{psi} \cdot \mathrm{psi}} &= 355.756\ \mathrm{psi}
        \\[10pt]
    \end{aligned} $$
"""

def test_Concrete_init_lightweight():
    concrete = materials.Concrete(5*unit.ksi, w_c=110*unit.pcf)
    assert isclose(concrete.E_c.magnitude, 2692080.051, abs_tol=1e-3)
    assert concrete.E_c.units == "psi"
    assert isclose(concrete.lamb, 0.825)
    assert isclose(concrete.beta_1, 0.8)
    assert isclose(concrete.f_r.magnitude, 437.5223209, abs_tol=1e-7)
    assert concrete.f_r.units == "psi"
    assert concrete.latex == r"""
    $$ \begin{aligned}
        
    &  \text{Since, } \left(100\ \mathrm{pcf} < w_c \leq 135\ \mathrm{pcf} \Leftarrow 100\ \mathrm{pcf} < 110\ \mathrm{pcf} \leq 135\ \mathrm{pcf}\right):
    \\[10pt]
    & \qquad \lambda = \operatorname{min}\left(0.0075 \cdot \frac{w_c}{\mathrm{pcf}} ,\ 1\right) = \operatorname{min}\left(0.0075 \cdot \frac{110\ \mathrm{pcf}}{\mathrm{pcf}} ,\ 1\right) &= 0.825

        \\[10pt]
        
    & \text{Since, } \left(4000\ \mathrm{psi} < f'_c < 8000\ \mathrm{psi} \Leftarrow 4000\ \mathrm{psi} < 5000\ \mathrm{psi} < 8000\ \mathrm{psi}\right):
    \\[10pt]
    & \qquad \beta_1 = 0.85 - \frac{0.05 \cdot \left(f'_c - 4000\ \mathrm{psi}\right)}{1000\ \mathrm{psi}} &= 0.8

        \\[10pt]
        E_c &= \left(\frac{w_c}{\mathrm{pcf}}\right)^{1.5} \cdot 33 \cdot \sqrt{f'_c \cdot \mathrm{psi}} = \left(\frac{110\ \mathrm{pcf}}{\mathrm{pcf}}\right)^{1.5} \cdot 33 \cdot \sqrt{5000\ \mathrm{psi} \cdot \mathrm{psi}} &= 2692080.051\ \mathrm{psi}
        \\[10pt]
        f_r &= 7.5 \cdot \lambda \cdot \sqrt{f'_c \cdot \mathrm{psi}} = 7.5 \cdot 0.825 \cdot \sqrt{5000\ \mathrm{psi} \cdot \mathrm{psi}} &= 437.522\ \mathrm{psi}
        \\[10pt]
    \end{aligned} $$
"""

def test_Concrete_init_normalweight():
    concrete = materials.Concrete(8*unit.ksi)
    assert isclose(concrete.E_c.magnitude, 5422453.319, abs_tol=0.001)
    assert concrete.E_c.units == "psi"
    assert concrete.lamb == 1
    assert concrete.beta_1 == 0.65
    assert isclose(concrete.f_r.magnitude, 670.8203932, abs_tol=1e-7)
    assert concrete.f_r.units == "psi"
    assert concrete.latex == r"""
    $$ \begin{aligned}
        
    \end{aligned} $$
    $$ \begin{aligned}
    & \text{Since, } \left(w_c > 135\ \mathrm{pcf} \Leftarrow 150\ \mathrm{pcf} > 135\ \mathrm{pcf}\right): & \lambda &= 1
    \end{aligned} $$
    $$ \begin{aligned}

        \\[10pt]
        
    \end{aligned} $$
    $$ \begin{aligned}
    & \text{Since, } \left(f'_c \geq 8000\ \mathrm{psi} \Leftarrow 8000\ \mathrm{psi} \geq 8000\ \mathrm{psi}\right): & \beta_1 &= 0.65
    \end{aligned}$$
    $$ \begin{aligned}

        \\[10pt]
        E_c &= \left(\frac{w_c}{\mathrm{pcf}}\right)^{1.5} \cdot 33 \cdot \sqrt{f'_c \cdot \mathrm{psi}} = \left(\frac{150\ \mathrm{pcf}}{\mathrm{pcf}}\right)^{1.5} \cdot 33 \cdot \sqrt{8000\ \mathrm{psi} \cdot \mathrm{psi}} &= 5422453.319\ \mathrm{psi}
        \\[10pt]
        f_r &= 7.5 \cdot \lambda \cdot \sqrt{f'_c \cdot \mathrm{psi}} = 7.5 \cdot 1 \cdot \sqrt{8000\ \mathrm{psi} \cdot \mathrm{psi}} &= 670.82\ \mathrm{psi}
        \\[10pt]
    \end{aligned} $$
"""

def test_Rebar_init():
    rebar = materials.Rebar(4, f_y=60*unit.ksi)
    assert rebar.size == 4
    assert isclose(rebar.f_y.magnitude, 60000)
    assert rebar.f_y.units == "psi"
    assert rebar.A_b.magnitude == 0.2
    assert rebar.A_b.units == "inch ** 2"
    assert rebar.w.magnitude == 0.668
    assert rebar.w.units == "plf"
    assert rebar.d_b.magnitude == 0.5
    assert rebar.d_b.units == "inch"
    assert rebar.D.magnitude == 3
    assert rebar.D.units == "inch"
    assert rebar.G.magnitude == 8
    assert rebar.G.units == "inch"
    assert rebar.J.magnitude == 4
    assert rebar.J.units == "inch"

def test_Steel_init():
    steel = materials.Steel("A36")
    assert steel.name == "A36"
    assert steel.F_y == 36*unit.ksi
    assert steel.F_u == 58*unit.ksi
    assert steel.E == 29000*unit.ksi
    assert steel.G == 11200*unit.ksi
    assert steel.v == 0.3
    assert steel.w_s == 490*unit.pcf
