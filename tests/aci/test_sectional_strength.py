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

from structuraltools.aci import materials, sectional_strength
from structuraltools.unit import unit


def test_calc_a():
    string, a = sectional_strength.calc_a(
        A_st=0.6*unit.inch**2,
        f_y=60*unit.ksi,
        f_prime_c=4*unit.ksi,
        b=8*unit.inch,
        precision=4)
    assert isclose(a, 1.323529412*unit.inch, atol=1e-9*unit.inch)
    assert string == r"a &= \frac{A_{st} \cdot f_y}{0.85 \cdot f'_c \cdot b} = \frac{0.6\ \mathrm{in}^{2} \cdot 60\ \mathrm{ksi}}{0.85 \cdot 4\ \mathrm{ksi} \cdot 8\ \mathrm{in}} &= 1.324\ \mathrm{in}"

def test_calc_M_n():
    string, M_n = sectional_strength.calc_M_n(
        A_st=0.6*unit.inch**2,
        f_y=60*unit.ksi,
        d=12*unit.inch,
        a=1.32353*unit.inch,
        precision=4)
    assert isclose(M_n, 34.014705*unit.kipft, atol=1e-6*unit.kipft)
    assert string == r"M_n &= A_{st} \cdot f_y \cdot \left(d - \frac{a}{2}\right) = 0.6\ \mathrm{in}^{2} \cdot 60\ \mathrm{ksi} \cdot \left(12\ \mathrm{in} - \frac{1.324\ \mathrm{in}}{2}\right) &= 34.01\ \mathrm{kipft}"

def test_calc_epsilon_t():
    string, epsilon_t = sectional_strength.calc_epsilon_t(
        beta_1=0.85,
        d_t=12*unit.inch,
        a=1.32353*unit.inch,
        precision=4)
    assert isclose(epsilon_t, 0.0201199897, atol=1e-10)
    assert string == r"\epsilon_t &= 0.003 \cdot \left(\frac{\beta_1 \cdot d_t}{a} - 1\right) = 0.003 \cdot \left(\frac{0.85 \cdot 12\ \mathrm{in}}{1.324\ \mathrm{in}} - 1\right) &= 0.02012"

def test_moment_capacity():
    concrete = materials.Concrete(4*unit.ksi)
    rebar = materials.Rebar(4)
    string, phiM_n = sectional_strength.moment_capacity(
        b=8*unit.inch,
        d=12*unit.inch,
        concrete=concrete,
        rebar=rebar,
        n=3,
        return_string=True)
    assert isclose(phiM_n[0]*phiM_n[1], 30.61323529*unit.kipft, atol=1e-8*unit.kipft)
    assert string == r"""$$
\begin{aligned}
    a &= \frac{A_{st} \cdot f_y}{0.85 \cdot f'_c \cdot b} = \frac{0.6\ \mathrm{in}^{2} \cdot 6\times 10^{4}\ \mathrm{psi}}{0.85 \cdot 4000\ \mathrm{psi} \cdot 8\ \mathrm{in}} &= 1.324\ \mathrm{in}
    \\[10pt]
    M_n &= A_{st} \cdot f_y \cdot \left(d - \frac{a}{2}\right) = 0.6\ \mathrm{in}^{2} \cdot 6\times 10^{4}\ \mathrm{psi} \cdot \left(12\ \mathrm{in} - \frac{1.324\ \mathrm{in}}{2}\right) &= 34.01\ \mathrm{kipft}
    \\[10pt]
    \epsilon_t &= 0.003 \cdot \left(\frac{\beta_1 \cdot d_t}{a} - 1\right) = 0.003 \cdot \left(\frac{0.85 \cdot 12\ \mathrm{in}}{1.324\ \mathrm{in}} - 1\right) &= 0.02012
\end{aligned}
$$
$$
\begin{aligned}
    & \text{Since, } \left(\epsilon_t \geq \epsilon_{ty} +0.003 \Leftarrow 0.02012 \geq 0.005069\right): & \phi &= 0.9
\end{aligned}
$$"""
