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

from structuraltools import aisc
from structuraltools.aisc import chapter_E
from structuraltools.unit import unit


def test_eq_E3_1():
    string, P_n = chapter_E.eq_E3_1(50*unit.ksi, 20*unit.inch**2, precision=4)
    assert isclose(P_n, 1000*unit.kip)
    assert string == r"P_n &= F_n \cdot A_g = 50\ \mathrm{ksi} \cdot 20\ \mathrm{in}^{2} &= 1000\ \mathrm{kip}"

def test_eq_E3_2():
    string, F_n = chapter_E.eq_E3_2(50*unit.ksi, 40*unit.ksi, precision=4)
    assert isclose(F_n, 29.63141366*unit.ksi, atol=1e-8*unit.ksi)
    assert string == r"F_n &= \left(0.658^{\frac{F_y}{F_e}}\right) \cdot F_y = \left(0.658^{\frac{50\ \mathrm{ksi}}{40\ \mathrm{ksi}}}\right) \cdot 50\ \mathrm{ksi} &=  29.63\ \mathrm{ksi}"

def test_eq_E3_3():
    string, F_n = chapter_E.eq_E3_3(40*unit.ksi, precision=4)
    assert isclose(F_n, 35.08*unit.ksi)
    assert string == r"F_n &= 0.877 \cdot F_e = 0.877 \cdot 40\ \mathrm{ksi} &= 35.08\ \mathrm{ksi}"

def test_eq_E3_4():
    string, F_e = chapter_E.eq_E3_4(
        E=29000*unit.ksi,
        L_c=120*unit.inch,
        r=5*unit.inch,
        axis="y",
        precision=4)
    assert isclose(F_e, 496.907166*unit.ksi, atol=1e-6*unit.ksi)
    assert string == r"F_e &= \frac{\pi^2 \cdot E}{\left(\frac{L_{c_{y}}}{r_{y}}\right)^2} = \frac{\pi^2 \cdot 2.9\times 10^{4}\ \mathrm{ksi}}{\left(\frac{120\ \mathrm{in}}{5\ \mathrm{in}}\right)^2} &= 496.9\ \mathrm{ksi}"

def test_sec_E3_inelastic():
    shape = aisc.Plate(12*unit.inch, 1*unit.inch, "A36")
    string, P_n = chapter_E.sec_E3(shape, 3*unit.ft, "y", precision=4)
    assert isclose(P_n, 190.50898212391965*unit.kip)
    assert string == r"""\begin{aligned}
    F_e &= \frac{\pi^2 \cdot E}{\left(\frac{L_{c_{y}}}{r_{y}}\right)^2} = \frac{\pi^2 \cdot 2.9\times 10^{4}\ \mathrm{ksi}}{\left(\frac{3\ \mathrm{ft}}{0.2887\ \mathrm{in}}\right)^2} &= 18.4\ \mathrm{ksi}
    \\[10pt]
    \text{Since, } & \left(\frac{F_y}{F_e} \leq 2.25 \Leftarrow \frac{36\ \mathrm{ksi}}{18.4\ \mathrm{ksi}} \leq 2.25\right):
    \\[10pt]
    F_n &= \left(0.658^{\frac{F_y}{F_e}}\right) \cdot F_y = \left(0.658^{\frac{36\ \mathrm{ksi}}{18.4\ \mathrm{ksi}}}\right) \cdot 36\ \mathrm{ksi} &=  15.88\ \mathrm{ksi}
    \\[10pt]
    P_n &= F_n \cdot A_g = 15.88\ \mathrm{ksi} \cdot 12\ \mathrm{in}^{2} &= 190.5\ \mathrm{kip}
\end{aligned}"""

def test_sec_E3_elastic():
    shape = aisc.Plate(12*unit.inch, 1*unit.inch, "A36")
    string, P_n = chapter_E.sec_E3(shape, 4*unit.ft, "y", precision=4)
    assert isclose(P_n, 108.94689615143473*unit.kip)
    assert string == r"""\begin{aligned}
    F_e &= \frac{\pi^2 \cdot E}{\left(\frac{L_{c_{y}}}{r_{y}}\right)^2} = \frac{\pi^2 \cdot 2.9\times 10^{4}\ \mathrm{ksi}}{\left(\frac{4\ \mathrm{ft}}{0.2887\ \mathrm{in}}\right)^2} &= 10.35\ \mathrm{ksi}
    \\[10pt]
    \text{Since, } & \left(\frac{F_y}{F_e} > 2.25 \Leftarrow \frac{36\ \mathrm{ksi}}{10.35\ \mathrm{ksi}} > 2.25\right):
    \\[10pt]
    F_n &= 0.877 \cdot F_e = 0.877 \cdot 10.35\ \mathrm{ksi} &= 9.079\ \mathrm{ksi}
    \\[10pt]
    P_n &= F_n \cdot A_g = 9.079\ \mathrm{ksi} \cdot 12\ \mathrm{in}^{2} &= 108.9\ \mathrm{kip}
\end{aligned}"""
