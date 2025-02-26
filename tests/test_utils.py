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


import pytest

from structuraltools import resources, unit, utils


def test_linterp():
    y_3 = utils.linterp(1, 1, 3, 3, 2)
    assert y_3 == 2

def test_convert_to_unit_1():
    result = utils.convert_to_unit("1 ft")
    assert result == 1*unit.ft

def test_convert_to_unit_2():
    result = utils.convert_to_unit(1)
    assert result == 1

def test_convert_to_unit_3():
    result = utils.convert_to_unit("1")
    assert result == 1

def test_convert_to_unit_4():
    result = utils.convert_to_unit("ft")
    assert result == "ft"

def test_convert_to_unit_5():
    with pytest.warns(UserWarning) as record:
        result = utils.convert_to_unit("1 xyz")
    assert result == "1 xyz"
    assert record[0].message.args[0] == "1 xyz was not evaluated as a unit"

def test_get_table_entry():
    filepath = resources.joinpath("steel_materials.csv")
    data = utils.get_table_entry(filepath, "A36")
    expected_data = {
        "name": "A36",
        "F_y": 36*unit.ksi,
        "F_u": 58*unit.ksi,
        "E": 29000*unit.ksi,
        "G": 11200*unit.ksi,
        "v": 0.3,
        "w_s": 490*unit.pcf
    }
    assert data == expected_data
