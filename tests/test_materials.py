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


from numpy import isclose

from structuraltools import materials, unit


def test_Concrete_init_ultra_lightweight():
    concrete = materials.Concrete(4*unit.ksi, w_c=90*unit.pcf)
    assert concrete.f_prime_c == 4000*unit.psi
    assert concrete.f_prime_c.units == "psi"
    assert isclose(concrete.E_c, 1782000*unit.psi)
    assert concrete.E_c.units == "psi"
    assert concrete.lamb == 0.75
    assert concrete.beta_1 == 0.85
    assert isclose(concrete.f_r, 355.7562368*unit.psi, atol=1e-7)
    assert concrete.f_r.units == "psi"
    assert concrete.markdown == r"""$$ \begin{aligned}
    \lambda &= \operatorname{bound}\left(0.75,\ 0.0075 \cdot w_c,\ 1\right)
        = \operatorname{bound}\left(0.75,\ 0.0075 \cdot 90\ \mathrm{pcf},\ 1\right)
        &= 0.75
    \\[10pt]
    E_c &= w_c^{1.5} \cdot 33 \cdot \sqrt{f'_c}
        = \left(90\ \mathrm{pcf}\right)^{1.5} \cdot 33 \cdot \sqrt{4000\ \mathrm{psi}}
        &= 1782000.0\ \mathrm{psi}
    \\[10pt]
    f_r &= 7.5 \cdot \lambda \cdot \sqrt{f'_c}
        = 7.5 \cdot 0.75 \cdot \sqrt{4000\ \mathrm{psi}}
        &= 355.756\ \mathrm{psi}
    \\[10pt]
    \beta_1 &= \operatorname{bound}\left(0.65,\ 0.85 - \frac{0.05 \cdot \left(f'_c - 4000\ \mathrm{psi}\right)}{1000\ \mathrm{psi}},\ 0.85\right)
        \\
        &= \operatorname{bound}\left(0.65,\ 0.85 - \frac{0.05 \cdot \left(4000\ \mathrm{psi} - 4000\ \mathrm{psi}\right)}{1000\ \mathrm{psi}},\ 0.85\right)
        \\
        &= 0.85
\end{aligned} $$"""

def test_Concrete_init_lightweight():
    concrete = materials.Concrete(5*unit.ksi, w_c=110*unit.pcf)
    assert isclose(concrete.E_c, 2692080.051*unit.psi, atol=1e-3)
    assert concrete.E_c.units == "psi"
    assert isclose(concrete.lamb, 0.825)
    assert isclose(concrete.beta_1, 0.8)
    assert isclose(concrete.f_r, 437.5223209*unit.psi, atol=1e-7)
    assert concrete.f_r.units == "psi"
    assert concrete.markdown == r"""$$ \begin{aligned}
    \lambda &= \operatorname{bound}\left(0.75,\ 0.0075 \cdot w_c,\ 1\right)
        = \operatorname{bound}\left(0.75,\ 0.0075 \cdot 110\ \mathrm{pcf},\ 1\right)
        &= 0.825
    \\[10pt]
    E_c &= w_c^{1.5} \cdot 33 \cdot \sqrt{f'_c}
        = \left(110\ \mathrm{pcf}\right)^{1.5} \cdot 33 \cdot \sqrt{5000\ \mathrm{psi}}
        &= 2692080.051\ \mathrm{psi}
    \\[10pt]
    f_r &= 7.5 \cdot \lambda \cdot \sqrt{f'_c}
        = 7.5 \cdot 0.825 \cdot \sqrt{5000\ \mathrm{psi}}
        &= 437.522\ \mathrm{psi}
    \\[10pt]
    \beta_1 &= \operatorname{bound}\left(0.65,\ 0.85 - \frac{0.05 \cdot \left(f'_c - 4000\ \mathrm{psi}\right)}{1000\ \mathrm{psi}},\ 0.85\right)
        \\
        &= \operatorname{bound}\left(0.65,\ 0.85 - \frac{0.05 \cdot \left(5000\ \mathrm{psi} - 4000\ \mathrm{psi}\right)}{1000\ \mathrm{psi}},\ 0.85\right)
        \\
        &= 0.8
\end{aligned} $$"""

def test_Concrete_init_normalweight():
    concrete = materials.Concrete(8*unit.ksi)
    assert isclose(concrete.E_c, 5422453.319*unit.psi, atol=0.001)
    assert concrete.E_c.units == "psi"
    assert concrete.lamb == 1
    assert concrete.beta_1 == 0.65
    assert concrete.f_r.units == "psi"
    assert isclose(concrete.f_r, 670.8203932*unit.psi, atol=1e-7)
    assert concrete.markdown == r"""$$ \begin{aligned}
    \lambda &= \operatorname{bound}\left(0.75,\ 0.0075 \cdot w_c,\ 1\right)
        = \operatorname{bound}\left(0.75,\ 0.0075 \cdot 150\ \mathrm{pcf},\ 1\right)
        &= 1
    \\[10pt]
    E_c &= w_c^{1.5} \cdot 33 \cdot \sqrt{f'_c}
        = \left(150\ \mathrm{pcf}\right)^{1.5} \cdot 33 \cdot \sqrt{8000\ \mathrm{psi}}
        &= 5422453.319\ \mathrm{psi}
    \\[10pt]
    f_r &= 7.5 \cdot \lambda \cdot \sqrt{f'_c}
        = 7.5 \cdot 1 \cdot \sqrt{8000\ \mathrm{psi}}
        &= 670.82\ \mathrm{psi}
    \\[10pt]
    \beta_1 &= \operatorname{bound}\left(0.65,\ 0.85 - \frac{0.05 \cdot \left(f'_c - 4000\ \mathrm{psi}\right)}{1000\ \mathrm{psi}},\ 0.85\right)
        \\
        &= \operatorname{bound}\left(0.65,\ 0.85 - \frac{0.05 \cdot \left(8000\ \mathrm{psi} - 4000\ \mathrm{psi}\right)}{1000\ \mathrm{psi}},\ 0.85\right)
        \\
        &= 0.65
\end{aligned} $$"""

def test_Rebar_init():
    rebar = materials.Rebar(4, f_y=60*unit.ksi)
    assert rebar.size == 4
    assert isclose(rebar.f_y, 60000*unit.psi)
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
