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


from string import Template

from numpy import isclose
import pytest

from structuraltools import materials, MathTemplate, resources, unit, utils


def test_linterp():
    assert utils.linterp(1, 1, 3, 3, 2) == 2

def test_linterp_dicts():
    dict_3 = utils.linterp_dicts(
        x_1=1,
        dict_1={11: {21: 1, 22: 1, "text": "text"}, 12: {21: 1, 22: 1}},
        x_2=3,
        dict_2={11: {21: 3, 22: 3, "text": "text"}, 12: {21: 3, 22: 3}},
        x_3=2)
    assert dict_3 == {11: {21: 2, 22: 2, "text": "text"}, 12: {21: 2, 22: 2}}

def test_round_to_float():
    assert utils.round_to(3.5, 5) == 5

def test_round_to_Quantity():
    assert isclose(utils.round_to(-0.1713*unit.kip, 10*unit.lb), -180*unit.lb)

def test_convert_to_unit_Quantity_string():
    assert utils.convert_to_unit("1 ft") == 1*unit.ft

def test_convert_to_unit_int():
    assert utils.convert_to_unit(1) == 1

def test_convert_to_unit_number_string():
    assert utils.convert_to_unit("1") == 1

def test_convert_to_unit_alpha_string():
    assert utils.convert_to_unit("ft") == "ft"

def test_convert_to_unit_scientific_Quantity_string():
    assert utils.convert_to_unit("-9.5e-05 ft") == -9.5e-5*unit.ft

def test_convert_to_unit_Quantity_like_string():
    with pytest.warns(UserWarning) as record:
        result = utils.convert_to_unit("1 xyz")
    assert result == "1 xyz"
    assert record[0].message.args[0] == "'1 xyz' was not evaluated as a unit"

def test_read_data_table():
    filepath = resources.joinpath("AISC_steel_materials.csv")
    steel_table = utils.read_data_table(filepath)
    assert steel_table.at["A36", "F_y"] == 36*unit.ksi

def test_get_table_entry():
    filepath = resources.joinpath("AISC_steel_materials.csv")
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

def test_fill_templates():
    main_template = Template("""
        Sub-template: $sub_template
        Test string: $test_string
        Test class attribute: $f_y
        Test quantity: $length""")
    sub_template = Template("Sub-template value: $length")
    rebar = materials.Rebar(4)
    test_string = "Test string"
    length = 3.66667*unit.ft
    markdown_options = {"return_markdown": True, "decimal_points": 2}
    markdown, returned = utils.fill_templates(main_template, locals(), length)
    assert returned == length
    assert markdown == r"""
        Sub-template: Sub-template value: 3.67\ \mathrm{ft}
        Test string: Test string
        Test class attribute: 60000\ \mathrm{psi}
        Test quantity: 3.67\ \mathrm{ft}"""

def test_fill_templates_single_return():
    assert utils.fill_templates("", {}, "test") == "test"

def test_fill_templates_return_markdown_only():
    values = {"markdown_options": {"return_markdown": True}}
    assert utils.fill_templates(Template("test"), values) == "test"
