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


class TestModel:
    def setup_method(self):
        self.model = io.openre.Model("./tests/io/test.oex.xml")

    def test_get_node_reactions(self):
        reactions = self.model.get_node_reactions("1")
        assert reactions.at["DL", "FY"] == 0.025*unit.kip
        assert reactions.at["D2", "MZ"] == 0.212597234696009*unit.kipft
