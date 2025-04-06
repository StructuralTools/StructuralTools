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

from structuraltools import aisc, materials, unit

from structuraltools.aisc import chapter_F


def test_eq_F2_1():
    string, M_p = chapter_F.eq_F2_1(
        F_y=50*unit.ksi,
        Z_x=20*unit.inch**3,
        return_string=True)
    assert isclose(M_p, 1000/12*unit.kipft)
    assert M_p.units == "kipft"
    assert string == r"M_p &= F_y \cdot Z_x = 50\ \mathrm{ksi} \cdot 20\ \mathrm{in}^{3} &= 83.333\ \mathrm{kipft}"

def test_eq_F2_2():
    string, M_ltb = chapter_F.eq_F2_2(
        C_b=1,
        M_p=83*unit.kipft,
        F_y=50*unit.ksi,
        S_x=15*unit.inch**3,
        L_b=5*unit.ft,
        L_p=3*unit.ft,
        L_r=10*unit.ft,
        return_string=True)
    assert isclose(M_ltb, 71.78571429*unit.kipft, atol=1e-8*unit.kipft)
    assert M_ltb.units == "kipft"
    assert string == r"""M_{ltb} &= C_b \cdot \left(M_p - \left(M_p - 0.7 \cdot F_y \cdot S_x\right) \cdot \left(\frac{L_b - L_p}{L_r - L_p}\right)\right)
    \\
    &= 1 \cdot \left(83\ \mathrm{kipft} - \left(83\ \mathrm{kipft} - 0.7 \cdot 50\ \mathrm{ksi} \cdot 15\ \mathrm{in}^{3}\right) \cdot \left(\frac{5\ \mathrm{ft} - 3\ \mathrm{ft}}{10\ \mathrm{ft} - 3\ \mathrm{ft}}\right)\right)
    \\
    &= 71.786\ \mathrm{kipft}"""

def test_eq_F2_3():
    string, M_ltb = chapter_F.eq_F2_3(
        F_cr=17*unit.ksi,
        S_x=25.4*unit.inch**3,
        return_string=True)
    assert isclose(M_ltb, 35.98333333*unit.kipft, atol=1e-8*unit.kipft)
    assert M_ltb.units == "kipft"
    assert string == r"M_{ltb} &= F_{cr} \cdot S_x = 17\ \mathrm{ksi} \cdot 25.4\ \mathrm{in}^{3} &= 35.983\ \mathrm{kipft}"

def test_eq_F2_4():
    string, F_cr = chapter_F.eq_F2_4(
        C_b=1,
        E=29000*unit.ksi,
        L_b=15*unit.ft,
        r_ts=1.04*unit.inch,
        J=0.293*unit.inch**4,
        c=1,
        S_x=25.4*unit.inch**3,
        h_o=11.9*unit.inch,
        return_string=True)
    assert isclose(F_cr, 17.26466339*unit.ksi, atol=1e-8*unit.ksi)
    assert F_cr.units == "ksi"
    assert string == r"""F_{cr} &= \frac{C_b \cdot \pi^2 \cdot E}{\left(\frac{L_b}{r_{ts}}\right)^2} \cdot \sqrt{1 + 0.078 \cdot \frac{J \cdot c}{S_x \cdot h_o} \cdot \left(\frac{L_b}{r_{ts}}\right)^2}
    \\
    &= \frac{1 \cdot \pi^2 \cdot 29000\ \mathrm{ksi}}{\left(\frac{15\ \mathrm{ft}}{1.04\ \mathrm{in}}\right)^2} \cdot \sqrt{1 + 0.078 \cdot \frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}} \cdot \left(\frac{15\ \mathrm{ft}}{1.04\ \mathrm{in}}\right)^2}
    \\
    &= 17.265\ \mathrm{ksi}"""
