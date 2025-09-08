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

from structuraltools.awc import chapter_3
from structuraltools.unit import unit


def test_eq_3_3_5():
    string, R_B = chapter_3.eq_3_3_5(
        L_e=23.5*unit.ft,
        d=9.25*unit.inch,
        b=1.5*unit.inch,
        precision=4)
    assert isclose(R_B, 34.04898432, atol=1e-8)
    assert string == r"R_B &= \sqrt{\frac{L_e \cdot d}{b^2}} = \sqrt{\frac{23.5\ \mathrm{ft} \cdot 9.25\ \mathrm{in}}{\left(1.5\ \mathrm{in}\right)^2}} &= 34.05"

def test_eq_3_3_6():
    string, C_L = chapter_3.eq_3_3_6(
        F_bE=700*unit.psi,
        F_star_b=4200*unit.psi,
        precision=4)
    assert isclose(C_L, 0.1650356529, atol=1e-10)
    assert string == r"""C_L &= \frac{1 + \frac{F_{bE}}{F_b^*}}{1.9} - \sqrt{\left(\frac{1 + \frac{F_{bE}}{F_b^*}}{1.9}\right)^2 - \frac{\frac{F_{bE}}{F_b^*}}{0.95}}
\\
&= \frac{1 + \frac{700\ \mathrm{psi}}{4200\ \mathrm{psi}}}{1.9} - \sqrt{\left(\frac{1 + \frac{700\ \mathrm{psi}}{4200\ \mathrm{psi}}}{1.9}\right)^2 - \frac{\frac{700\ \mathrm{psi}}{4200\ \mathrm{psi}}}{0.95}}
\\
&= 0.165"""

def test_eq_3_3_6a():
    string, F_bE = chapter_3.eq_3_3_6a(
        E_prime_min=660000*unit.psi,
        R_B=34,
        precision=4)
    assert isclose(F_bE, 685.1211073*unit.psi, atol=1e-7*unit.psi)
    assert string == r"F_{bE} &= \frac{1.2 \cdot E'_{min}}{R_B^2} = \frac{1.2 \cdot 6.6\times 10^{5}\ \mathrm{psi}}{\left(34)\right)^2} &= 685.1\ \mathrm{psi}"
