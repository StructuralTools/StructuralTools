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

import importlib.resources
import json
from typing import NamedTuple
import warnings

from numpy import sign
import pandas as pd
from pint import Quantity
from pint.errors import UndefinedUnitError

from structuraltools.unit import unit, Numeric


class Result[ValueType](NamedTuple):
    string: str
    value: ValueType


def fill_template(
        value: any,
        template: str,
        variables: dict[str: any],
        return_string: bool = True,
        precision: int = 4,
        header_level: int = 4,
        header_type: str = "markdown",
        general_format: str = "g",
        quantity_format: str = "~L") -> Result[any]:
    """Pass the return value through and fill the representation string if
    desired. This is designed to be used in the return statement of a function.

    Parameters
    ==========

    value : any
        Value to return as the result value

    template : str
        String to use as the template for the result string

    variables : dict[str: any]
        Values to use when filling out the template

    return_string : bool
        Whether to fill the provided template or return an empty string

    precision : int
        Precision value to use when filling the template

    header_level : int
        Header level to use when filling in templates

    header_type : str
        Type of headers to use. One of: "markdown" or "html"

    general_format : str
        Format code to use when filling the template

    quantity_format : str
        Additional format code to use for quantities when filling the template"""
    if not return_string:
        return Result("", value)

    if header_type == "markdown":
        headers = {"_header_": f"{"#"*header_level} ", "_h_start_": "", "_h_end_": ""}
    elif header_type == "html":
        headers = {
            "_header_": "",
            "_h_start_": f"<h{header_level}>",
            "_h_end_": f"</h{header_level}>"
        }
    else:
        raise ValueError(f"Unrecognized header type: {header_type}")

    string = template.format(
        _precision_=precision,
        _gformat_=general_format,
        _qformat_=quantity_format,
        **headers,
        **variables)
    return Result(string, value)

def process_templates( module: str, filename: str) -> None:
    """Function to process template files into the form used by python functions

    Parameters
    ==========

    module : str
        Module the template file is in

    filename : str
        Template file name"""
    directory = importlib.resources.files(module)
    with open(directory.joinpath(filename)) as file:
        templates = json.load(file)

    processed_templates = {}
    for name, data in templates.items():
        print(f"processing {name}")
        mapping = {}
        for variable, kind in data["types"].items():
            if kind == "str":
                mapping.update({variable: f"{{{variable}}}"})
            elif kind == "int" or kind == "float":
                mapping.update({variable: f"{{{variable}:.{{_precision_}}{{_gformat_}}}}"})
            elif kind == "unit":
                mapping.update({
                    variable: f"{{{variable}:{{_qformat_}}.{{_precision_}}{{_gformat_}}}}"
                })
            else:
                raise ValueError(f"Unrecognized type code: {kind}")
        processed_templates.update({name: data["string"].format(**mapping)})

    out_file = f"{filename.split(".")[0]}_processed.json"
    with open(directory.joinpath(out_file), mode="w", encoding="utf-8") as file:
        json.dump(processed_templates, file, indent=4)

def linterp(
        x_1: Numeric,
        y_1: Numeric,
        x_2: Numeric,
        y_2: Numeric,
        x_3: Numeric) -> Numeric:
    """Linear interpolation between two points

    Parameters
    ==========

    x1 : Numeric
        x value of first point for interpolation

    y1 : Numeric
        y value of first point for interpolation

    x2 : Numeric
        x value of second point for interpolation

    y2 : Numeric
        y value of second point for interpolation

    x3 : Numeric
        x value of point to interpolate y value for."""
    y_3 = y_1+(y_2-y_1)/(x_2-x_1)*(x_3-x_1)
    return y_3

def linterp_dicts(
        x_1: Numeric,
        dict_1: dict[any, dict],
        x_2: Numeric,
        dict_2: dict[any, dict],
        x_3: Numeric) -> dict[any, dict]:
    """Returns a dictionary that is a linear interpolation between two provided
    dictionaries of dictionaries with the same keys. Numeric value are
    interpolated all other values are taken from dict_1.

    Parameters
    ==========

    x_1 : Numeric
        Value to associate with dict_1 for interpolation

    dict_1 : dict[any, dict]
        First dictionary of values to interpolate

    x_2 : Numeric
        Value to associate with dict_2 for interpolation

    dict_2 : dict[any, dict]
        Second dictionary of values to interpolate

    x_3 : Numeric
        Interpolation value to associate with the new dictionary"""
    dict_3 = {}
    for key_1 in dict_1.keys():
        dict_3.update({key_1: {}})
        for key_2 in dict_1[key_1].keys():
            if isinstance(dict_1[key_1][key_2], int | float | Quantity):
                dict_3[key_1].update({
                    key_2: linterp(
                        x_1,
                        dict_1[key_1][key_2],
                        x_2,
                        dict_2[key_1][key_2],
                        x_3)
                    })
            else:
                dict_3[key_1].update({key_2: dict_1[key_1][key_2]})
    return dict_3

def round_to(value: Numeric, to: Numeric) -> Numeric:
    """Round the provided value away from 0 to the nearest multiple of to

    Parameters
    ==========

    value : Numeric
        Value to round

    to : Numeric
        Rounding target"""
    to = abs(to)
    if isinstance(value, Quantity):
        return to*(abs(value.to(to.units).magnitude)//to.magnitude+1)*sign(value)
    return to*(abs(value)//to+1)*sign(value)

def convert_to_unit(value: any) -> any:
    """Attempts to convert the given value to a Quantity if it is a string.
    The value is returned unmodified if it cannot be converted.

    Parameters
    ==========

    value : any
        Value to convert"""
    if isinstance(value, str):
        first_value = value.split(" ")[0]
        for character in ".-eE":
            first_value = first_value.replace(character, "")
        if first_value.isdigit():
            try:
                value = unit(value)
            except UndefinedUnitError:
                warnings.warn(f"'{value}' was not evaluated as a unit")
    return value

def read_data_table(filepath: str) -> pd.DataFrame:
    """Reads a .csv file and returns a pandas DataFrame with the first column
    set as the index and convert_to_unit run on all values

    Parameters
    ==========

    filepath : str
        Path to the file"""
    data_table = pd.read_csv(filepath)
    data_table = data_table.map(convert_to_unit)
    data_table = data_table.set_index(data_table.columns[0], drop=True)
    return data_table
