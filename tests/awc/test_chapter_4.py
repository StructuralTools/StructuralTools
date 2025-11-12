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

from structuraltools.awc import chapter_4
from structuraltools.unit import unit


def test_sec_4_1_3_Dimension():
    classification = chapter_4.sec_4_1_3(t_nom=4, d_nom=4)
    assert classification == "Dimension"

def test_sec_4_1_3_Beam():
    classification = chapter_4.sec_4_1_3(t_nom=5, d_nom=8)
    assert classification == "Beam"

def test_sec_4_1_3_Post():
    classification = chapter_4.sec_4_1_3(t_nom=5, d_nom=5)
    assert classification == "Post"

def test_table_4_3_1_b():
    string, F_prime_b = chapter_4.table_4_3_1_b(
        F_b=1500*unit.psi,
        C_M=0.9,
        C_t=0.8,
        C_L=0.7,
        C_F=1.1,
        C_fu=1.2,
        C_i=0.6,
        C_r=1.15,
        lamb=1.25,
        precision=4)
    assert isclose(F_prime_b, 1858.264254*unit.psi, atol=1e-6*unit.psi)
    assert string == r"""F'_b &= F_b \cdot C_M \cdot C_t \cdot C_L \cdot C_F \cdot C_{fu} \cdot C_i \cdot C_r \cdot K_F \cdot \phi \cdot \lambda
\\
&= 1500\ \mathrm{psi} \cdot 0.9 \cdot 0.8 \cdot 0.7 \cdot 1.1 \cdot 1.2 \cdot 0.6 \cdot 1.15 \cdot 2.54 \cdot 0.85 \cdot 1.25
\\
&= 1858\ \mathrm{psi}"""

def test_table_4_3_1_b_star():
    string, F_star_b = chapter_4.table_4_3_1_b_star(
        F_b=1500*unit.psi,
        C_M=0.9,
        C_t=0.8,
        C_F=1.1,
        C_i=0.6,
        C_r=1.15,
        lamb=1.25,
        precision=4)
    assert isclose(F_star_b, 2212.21935*unit.psi, atol=1e-5*unit.psi)
    assert string == r"""F^*_b &= F_b \cdot C_M \cdot C_t \cdot C_F \cdot C_i \cdot C_r \cdot K_F \cdot \phi \cdot \lambda
\\
&= 1500\ \mathrm{psi} \cdot 0.9 \cdot 0.8 \cdot 1.1 \cdot 0.6 \cdot 1.15 \cdot 2.54 \cdot 0.85 \cdot 1.25
\\
&= 2212\ \mathrm{psi}"""

def test_table_4_3_1_t():
    string, F_prime_t = chapter_4.table_4_3_1_t(
        F_t=1000*unit.psi,
        C_M=0.9,
        C_t=0.8,
        C_F=1.3,
        C_i=0.7,
        lamb=1.25,
        precision=4)
    assert isclose(F_prime_t, 1769.04*unit.psi)
    assert string == r"""F'_t &= F_t \cdot C_M \cdot C_t \cdot C_F \cdot C_i \cdot K_F \cdot \phi \cdot \lambda
\\
&= 1000\ \mathrm{psi} \cdot 0.9 \cdot 0.8 \cdot 1.3 \cdot 0.7 \cdot 2.7 \cdot 0.8 \cdot 1.25
\\
&= 1769\ \mathrm{psi}"""

def test_table_4_3_1_v():
    string, F_prime_v = chapter_4.table_4_3_1_v(
        F_v=175*unit.psi,
        C_M=0.9,
        C_t=0.8,
        C_i=0.7,
        lamb=1.25,
        precision=4)
    assert isclose(F_prime_v, 238.14*unit.psi)
    assert string == r"""F'_v &= F_v \cdot C_M \cdot C_t \cdot C_i \cdot K_F \cdot \phi \cdot \lambda
\\
&= 175\ \mathrm{psi} \cdot 0.9 \cdot 0.8 \cdot 0.7 \cdot 2.88 \cdot 0.75 \cdot 1.25
\\
&= 238.1\ \mathrm{psi}"""

def test_table_4_3_1_c():
    string, F_prime_c = chapter_4.table_4_3_1_c(
        F_c=1500*unit.psi,
        C_M=0.9,
        C_t=0.8,
        C_F=1.1,
        C_i=0.7,
        C_P=0.6,
        lamb=1.25,
        precision=4)
    assert isclose(F_prime_c, 1347.192*unit.psi)
    assert string == r"""F'_c &= F_c \cdot C_M \cdot C_t \cdot C_F \cdot C_i \cdot C_P \cdot K_F \cdot \phi \cdot \lambda
\\
&= 1500\ \mathrm{psi} \cdot 0.9 \cdot 0.8 \cdot 1.1 \cdot 0.7 \cdot 0.6 \cdot 2.4 \cdot 0.9 \cdot 1.25
\\
&= 1347\ \mathrm{psi}"""

def test_table_4_3_1_c_star():
    string, F_c_star = chapter_4.table_4_3_1_c_star(
        F_c=1500*unit.psi,
        C_M=0.9,
        C_t=0.8,
        C_F=1.1,
        C_i=0.7,
        lamb=1.25,
        precision=4)
    assert isclose(F_c_star, 2245.32*unit.psi)
    assert string == r"""F^*_c &= F_c \cdot C_M \cdot C_t \cdot C_F \cdot C_i \cdot K_F \cdot \phi \cdot \lambda
\\
&= 1500\ \mathrm{psi} \cdot 0.9 \cdot 0.8 \cdot 1.1 \cdot 0.7 \cdot 2.4 \cdot 0.9 \cdot 1.25
\\
&= 2245\ \mathrm{psi}"""

def test_table_4_3_1_c_perp():
    string, F_prime_c_perp = chapter_4.table_4_3_1_c_perp(
        F_c_perp=660*unit.psi,
        C_M=0.9,
        C_t=0.8,
        C_i=0.7,
        C_b=0.6,
        precision=4)
    assert isclose(F_prime_c_perp, 299.974752*unit.psi, atol=1e-6*unit.psi)
    assert string == r"""F'_{c_{perp}} &= F_{c_{perp}} \cdot C_M \cdot C_t \cdot C_i \cdot C_b \cdot K_F \cdot \phi
\\
&= 660\ \mathrm{psi} \cdot 0.9 \cdot 0.8 \cdot 0.7 \cdot 0.6 \cdot 1.67 \cdot 0.9
\\
&= 300\ \mathrm{psi}"""

def test_table_4_3_1_E():
    string, E_prime = chapter_4.table_4_3_1_E(
        E=1600000*unit.psi,
        C_M=0.9,
        C_t=0.8,
        C_fu=0.7,
        C_i=0.6,
        precision=4)
    assert isclose(E_prime, 483840*unit.psi)
    assert string == r"""E' &= E \cdot C_M \cdot C_t \cdot C_{fu} \cdot C_i
\\
&= 1.6\times 10^{6}\ \mathrm{psi} \cdot 0.9 \cdot 0.8 \cdot 0.7 \cdot 0.6
\\
&= 4.838\times 10^{5}\ \mathrm{psi}"""

def test_table_4_3_1_E_min():
    string, E_prime_min = chapter_4.table_4_3_1_E_min(
        E_min=580000*unit.psi,
        C_M=0.9,
        C_t=0.8,
        C_fu=0.7,
        C_i=0.6,
        C_T=1.1,
        precision=4)
    assert isclose(E_prime_min, 288625.0752*unit.psi, atol=1e-4*unit.psi)
    assert string == r"""E'_{min} &= E_{min} \cdot C_M \cdot C_t \cdot C_{fu} \cdot C_i \cdot C_T \cdot K_F \cdot \phi
\\
&= 5.8\times 10^{5}\ \mathrm{psi} \cdot 0.9 \cdot 0.8 \cdot 0.7 \cdot 0.6 \cdot 1.1 \cdot 1.76 \cdot 0.85
\\
&= 2.886\times 10^{5}\ \mathrm{psi}"""

def test_sec_4_3_3():
    C_M = chapter_4.sec_4_3_3(
        wet_service=True,
        F_b=1000*unit.psi,
        F_c=600*unit.psi,
        C_F={"F_b": 1.1, "F_c": 1.1},
        classification="Dimension",
        species="Southern Pine")
    assert C_M == {"F_b": 1, "F_t": 1, "F_v": 0.97, "F_c": 1,
                   "F_c_perp": 0.67, "E": 0.9, "E_min": 0.9}

def test_sec_4_3_6_Dimension():
    C_F = chapter_4.sec_4_3_6(
        classification="Dimension",
        species="Alaska Cedar",
        grade="1",
        t_nom=2,
        d_nom=6)
    assert C_F == {"F_b": 1.3, "F_t": 1.3, "F_v": 1, "F_c": 1.1, "F_c_perp": 1, "E": 1, "E_min": 1}

def test_sec_4_3_6_Dimension_Southern_Pine():
    C_F = chapter_4.sec_4_3_6(
        classification="Dimension",
        species="Southern Pine",
        grade="Select",
        t_nom=4,
        d_nom=4)
    assert all(value == 1 for value in C_F.values())

def test_sec_4_3_6_Timber():
    C_F = chapter_4.sec_4_3_6(
        classification="Beam",
        species="Douglas Fir",
        grade="2",
        t_nom=8,
        d_nom=14)
    assert isclose(C_F.pop("F_b"), 0.9830179945, atol=1e-10)
    assert all(value == 1 for value in C_F.values())

def test_sec_4_3_7_Dimension():
    C_fu = chapter_4.sec_4_3_7(
        classification="Dimension",
        grade="Select",
        t_nom=2,
        d_nom=8)
    assert C_fu.pop("F_b") == 1.15
    assert all(value == 1 for value in C_fu.values())

def test_sec_4_3_7_Beam():
    C_fu = chapter_4.sec_4_3_7(
        classification="Beam",
        grade="1",
        t_nom=6,
        d_nom=10)
    assert C_fu == {"F_b": 0.74, "F_t": 1, "F_v": 1, "F_c": 1,
                    "F_c_perp": 1, "E": 0.9, "E_min": 0.9}

def test_sec_4_3_8():
    C_i = chapter_4.sec_4_3_8(incising=True)
    assert C_i == {"F_b": 0.8, "F_t": 0.8, "F_v": 0.8, "F_c": 0.8,
                  "F_c_perp": 1, "E": 0.95, "E_min": 0.95}
