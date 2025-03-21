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


def test_WideFlange_init():
    steel = materials.Steel("A992")
    wide_flange = aisc.WideFlange("W10X12", steel)
    assert wide_flange.W == 12*unit.plf


class TestWideFlange:
    def setup_method(self, method):
        self.steel = materials.Steel("A992")

    def test_moment_capacity_plastic(self):
        wide_flange = aisc.WideFlange("W12X22", self.steel)
        phi_b, M_n = wide_flange.moment_capacity()
        assert isclose(phi_b*M_n, 110*unit.kipft, atol=1*unit.kipft)

    def test_moment_capacity_inelastic_ltb(self):
        wide_flange = aisc.WideFlange("W12X22", self.steel)
        phi_b, M_n = wide_flange.moment_capacity(L_b=7*unit.ft)
        assert isclose(phi_b*M_n, 81.7*unit.kipft, atol=1*unit.kipft)

    def test_moment_capacity_elastic_ltb(self):
        wide_flange = aisc.WideFlange("W12X22", self.steel)
        phi_b, M_n = wide_flange.moment_capacity(L_b=15*unit.ft)
        assert isclose(phi_b*M_n, 32.9*unit.kipft, atol=1*unit.kipft)

    def test_moment_capacity_flange_local_buckling(self):
        wide_flange = aisc.WideFlange("W10X12", self.steel)
        phi_b, M_n = wide_flange.moment_capacity()
        assert isclose(phi_b*M_n, 46.9*unit.kipft, atol=1*unit.kipft)
