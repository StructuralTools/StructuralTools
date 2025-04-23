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


import csv
from string import Template
import warnings

from IPython.display import display_markdown
from numpy import sign
import pandas as pd
from pint import Quantity
from pint.errors import UndefinedUnitError

from structuraltools import decimal_points, header_level, unit
from structuraltools import Numeric


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

def get_table_entry(filepath: str, index: str) -> dict:
    """Returns the specified row from a csv file as a dict. String values that
    are likely to be numeric or contain Pint quantities are evaluated with
    convert_to_unit. A "with" context handler does not need to be used when
    calling this function.

    Parameters
    ==========

    filepath : str
        Path to the csv file

    index : str
        First value on the row to return"""
    with open(filepath) as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            if tuple(line.values())[0] == index:
                raw_data = line
                break
    data = {key: convert_to_unit(value) for key, value in raw_data.items()}
    return data

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

def fill_template(
        template,
        variables: dict,
        *return_values,
        display: bool = False,
        return_string: bool = False,
        decimal_points: int = decimal_points,
        header_level: int = header_level) -> any:
    """Function to fill out calculation templates and display the result. This
    is designed to be used in the return statement of another function.

    Parameters
    ==========

    template : ShowTemplate
        Template to fill and display

    variables : dict
        Values to fill out the template with

    *return_values : any
        Values to return. If return_string is specified the string will be
        prepended to return_values and the result returned.

    display : bool, Optional
        Whether or not to display the filled template

    return_string : bool, Optional
        Whether or not to return the filled template

    decimal_points : int, Optional
        How many decimal points to round to when writing values into the template

    header_level : int, Optional
        Header level to use when filling in markdown templates"""
    if not (display or return_string):
        if len(return_values) == 1:
            return return_values[0]
        else:
            return return_values

    _ = variables.pop("self", None)
    rounded_variables = {"header": "#"*header_level}
    for key, value in variables.items():
        if isinstance(value, Quantity | float):
            rounded_variables.update({key: round(value, decimal_points)})
        else:
            rounded_variables.update({key: value})

    template.fill(**rounded_variables)
    if display:
        template.display()
    if return_string:
        return_values = (template.string, *return_values)
    if len(return_values) == 1:
        return return_values[0]
    else:
        return return_values

def fill_templates(main_template: Template, variables: dict, *return_vals) -> any:
    """Function to fill out latex templates used for displaying calculations.
    This is designed to be used in the return statement of another function to
    fill out the primary latex template associated with that function.

    Parameters
    ==========

    main_template : Template
        Main template string to fill out and return if requested

    variables : dict
        Dictionary of additional arguments and values to use to fill out the
        template strings. Any template strings in the variables dictionary will
        be filled out and used to fill out the main template.

        The variables dictionary may contain a markdown_options sub-dictionary
        to specify addition arguments for the markdown output.

        show : bool, optional
            Boolean indicating if the calculations should be displayed with
            IPython's display_markdown(). Defaults to False.

        return_markdown : bool, optional
            Boolean indicating if the markdown string should be returned.
            Defaults to False.

        decimal_points : int, optional
            How many decimal places to use when writing variables into the
            markdown template. defaults to the value in
            structuraltools.decimal_points.

    return_vals : Any
        Values to return. If return_markdown is specified in a markdown_options
        sub-dictionary contained in the variables dictionary a new tuple
        consisting of the markdown prepended to returns will be returned"""
    markdown_options = {
        "show": False,
        "return_markdown": False,
        "decimal_points": decimal_points
    }
    markdown_options.update(variables.get("markdown_options", {}))
    if not (markdown_options["show"] or markdown_options["return_markdown"]):
        if len(return_vals) == 1:
            return return_vals[0]
        else:
            return return_vals

    sorted_vars = {}
    subtemplates = {}
    for key, value in variables.items():
        if isinstance(value, Template) and value != main_template:
            subtemplates.update({key: value})
        elif getattr(value, "unpack_for_templates", False):
            sorted_vars.update(vars(value))
        else:
            sorted_vars.update({key: value})

    rounded_vars = {}
    for key, value in sorted_vars.items():
        if isinstance(value, Quantity | float):
            rounded_vars.update({key: round(value, markdown_options["decimal_points"])})
        else:
            rounded_vars.update({key: value})

    filled_subtemplates = {}
    for name, subtemplate in subtemplates.items():
        filled_subtemplates.update({name: subtemplate.substitute(**rounded_vars)})

    markdown = main_template.substitute(**filled_subtemplates, **rounded_vars)
    if markdown_options["show"]:
        display_markdown(markdown, raw=True)
    if markdown_options["return_markdown"]:
        return_vals = (markdown, *return_vals)
    if len(return_vals) == 1:
        return return_vals[0]
    else:
        return return_vals
