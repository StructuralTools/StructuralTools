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

from structuraltools import awc
from structuraltools.unit import unit


def test_SawnLumber_init_Dimensioned():
    member = awc.SawnLumber(
        species="Douglas Fir",
        grade="Select",
        b=1.5*unit.inch,
        d=7.25*unit.inch,
        temperature=125,
        incising=True)
    assert member.d_nom == 8
    assert member.b_nom == 2
    assert isclose(member.A, 10.875*unit.inch**2)
    assert isclose(member.S_x, 13.140625*unit.inch**3)
    assert isclose(member.I_x, 47.63476563*unit.inch**4, atol=1e-8*unit.inch**4)
    assert isclose(member.r_x, 2.092894726*unit.inch, atol=1e-9*unit.inch)
    assert isclose(member.S_y, 2.71875*unit.inch**3)
    assert isclose(member.I_y, 2.0390625*unit.inch**4)
    assert isclose(member.r_y, 0.4330127019*unit.inch, atol=1e-10*unit.inch)
    assert member.F_b == 1500*unit.psi
    assert member.F_t == 1000*unit.psi
    assert member.F_v == 180*unit.psi
    assert member.F_c_perp == 625*unit.psi
    assert member.F_c == 1700*unit.psi
    assert member.E == 1900000*unit.psi
    assert member.E_min == 690000*unit.psi
    assert member.G == 0.5
    assert member.modifiers == {
        "F_b": {"C_F": 1.2, "C_M": 1, "C_t": 0.8, "C_fu": 1.15, "C_i": 0.8},
        "F_t": {"C_F": 1.2, "C_M": 1, "C_t": 0.9, "C_fu": 1, "C_i": 0.8},
        "F_v": {"C_F": 1, "C_M": 1, "C_t": 0.8, "C_fu": 1, "C_i": 0.8},
        "F_c": {"C_F": 1.05, "C_M": 1, "C_t": 0.8, "C_fu": 1, "C_i": 0.8},
        "F_c_perp": {"C_F": 1, "C_M": 1, "C_t": 0.8, "C_fu": 1, "C_i": 1},
        "E": {"C_F": 1, "C_M": 1, "C_t": 0.9, "C_fu": 1, "C_i": 0.95},
        "E_min": {"C_F": 1, "C_M": 1, "C_t": 0.9, "C_fu": 1, "C_i": 0.95}
    }

def test_SawnLumber_init_Dimensioned_Southern_Pine():
    member = awc.SawnLumber(
        species="Southern Pine",
        grade="1+",
        b=1.5*unit.inch,
        d=5.5*unit.inch,
        wet_service=True)
    assert member.F_b == 1500*unit.psi
    assert member.F_t == 1000*unit.psi
    assert member.F_v == 175*unit.psi
    assert member.F_c_perp == 660*unit.psi
    assert member.F_c == 1650*unit.psi
    assert member.E == 1800000*unit.psi
    assert member.E_min == 660000*unit.psi
    assert member.G == 0.55
    assert member.modifiers == {
        "F_b": {"C_F": 1, "C_M": 0.85, "C_t": 1, "C_fu": 1.15, "C_i": 1},
        "F_t": {"C_F": 1, "C_M": 1, "C_t": 1, "C_fu": 1, "C_i": 1},
        "F_v": {"C_F": 1, "C_M": 0.97, "C_t": 1, "C_fu": 1, "C_i": 1},
        "F_c": {"C_F": 1, "C_M": 0.8, "C_t": 1, "C_fu": 1, "C_i": 1},
        "F_c_perp": {"C_F": 1, "C_M": 0.67, "C_t": 1, "C_fu": 1, "C_i": 1},
        "E": {"C_F": 1, "C_M": 0.9, "C_t": 1, "C_fu": 1, "C_i": 1},
        "E_min": {"C_F": 1, "C_M": 0.9, "C_t": 1, "C_fu": 1, "C_i": 1}
    }

class TestSawnLumber:
    def setup_method(self, method):
        self.sawn_lumber = awc.SawnLumber(
            species="Southern Pine",
            grade="1+",
            b=1.5*unit.inch,
            d=7.25*unit.inch)

    def test_get_E_prime(self):
        string, E_prime = self.sawn_lumber.get_E_prime(axis="y", precision=4)
        assert isclose(E_prime, 1800000*unit.psi)

    def test_moment_capacity(self):
        string, phiM_n = self.sawn_lumber.moment_capacity(
            lamb=0.8,
            C_r=1.15,
            C_L=0.7,
            precision=4)
        assert isclose(phiM_n, 24665.40779*unit.lbin, atol=1e-5*unit.lbin)
