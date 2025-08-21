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

def test_sec_4_3_3():
    C_M = chapter_4.sec_4_3_3(
        wet_service=True,
        F_b=1000*unit.psi,
        F_c=600*unit.psi,
        C_F=1.1,
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
