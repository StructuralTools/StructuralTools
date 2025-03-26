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


from structuraltools import io, unit


def test_model_init():
    model = io.openre.Model("./tests/io/test.oex.xml")
    assert model.force_unit == unit.kip
    assert model.length_unit == unit.ft
    assert model.load_cases == {"DL": "DL", "LL": "LL"}
    assert model.design_combs == {"D1", "D2"}
    assert model.service_combs == {"S2"}


class TestModel:
    def setup_method(self):
        self.model = io.openre.Model("./tests/io/test.oex.xml")

    def test_get_node_location(self):
        location = self.model.get_node_location(3)
        expected_location = {
            "X": 0.833333333333333*unit.ft,
            "Y": 0.833333333333333*unit.ft,
            "Z": 0*unit.ft
        }
        assert location == expected_location


    def test_get_node_reactions_load_cases(self):
        reactions = self.model.get_node_reactions(1, "load_cases")
        assert reactions.at["DL", "FY"] == 0.025*unit.kip
        assert reactions.at["LL", "MZ"] == 0.132969434963536*unit.kipft

    def test_get_node_reactions_design_combinations(self):
        reactions = self.model.get_node_reactions(2, "design_combs")
        assert reactions.at["D1", "FY"] == 0.035*unit.kip
        assert reactions.at["D2", "MZ"] == 0.235493482898162*unit.kipft

    def test_get_node_reactions_service_combinations(self):
        reactions = self.model.get_node_reactions(1, "service_combs")
        assert reactions.at["S2", "FX"] == -0.234979829085838*unit.kip
        assert reactions.at["S2", "MX"] == 0*unit.kipft

    def test_get_member_end_forces_start_load_cases(self):
        end_forces = self.model.get_member_end_forces(1, 1, "load_cases")
        assert end_forces.at["DL", "Axial"] == 0.025*unit.kip
        assert end_forces.at["LL", "V2"] == 0.237293954287643*unit.kip

    def test_get_member_end_forces_end_design_combinations(self):
        end_forces = self.model.get_member_end_forces(3, 3, "design_combs")
        assert end_forces.at["D1", "Axial"] == -0.035*unit.kip
        assert end_forces.at["D2", "M33"] == 0.117095369920119*unit.kipft
