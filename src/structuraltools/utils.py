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

from IPython import display, Latex
from pint.errors import UndefinedUnitError

from structuraltools import unit

def linterp(x_1, y_1, x_2, y_2, x_3):
    """Linear interpolation between two points

    Parameters
    ==========

    x1 : int, float, or pint quantity
        x value of first point for interpolation

    y1 : int, float, or pint quantity
        y value of first point for interpolation

    x2 : int, float, or pint quantity
        x value of second point for interpolation

    y2 : int, float, or pint quantity
        y value of second point for interpolation

    x3 : int, float, or pint quantity
        x value of point to interpolate y value for."""
    y_3 = y_1+(y_2-y_1)/(x_2-x_1)*(x_3-x_1)
    return y_3

def linterp_dicts(x_1, dict_1: dict, x_2, dict_2: dict, x_3) -> dict:
    """Returns a dictionary that is a linear interpolation between two provided
    dictionaries of dictionaries with the same keys. Integer and float values
    are interpolated all other values are taken from dict_1.

    Parameters
    ==========

    x_1 : float
        Value to associate with dict_1 for interpolation

    dict_1 : dict
        First dictionary of values to interpolate

    x_2 : float
        Value to associate with dict_2 for interpolation

    dict_2 : dict
        Second dictionary of values to interpolate

    x_3 : float
        Interpolation value to associate with the new dictionary"""
    dict_3 = {}
    for key_1 in dict_1.keys():
        dict_3.update({key_1: {}})
        for key_2 in dict_1[key_1].keys():
            if isinstance(dict_1[key_1][key_2], int | float):
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

def convert_to_unit(value):
    """Checks if the given value is likely to be a string of a pint
    quantity and attempts to read with the set unit registry. This
    is designed to help with reading .csv data tables."""

    if isinstance(value, str):
        if value.split(" ")[0].replace(".", "").replace("-", "").isdigit():
            try:
                value = unit(value)
            except UndefinedUnitError:
                warnings.warn(f"{value} was not evaluated as a unit")
    return value

def get_table_entry(filepath, index: str) -> dict:
    """Returns the specified row from a csv file as a dict. String values that
    are likely to be numeric or contain Pint quantities are evaluated with
    convert_to_unit. A "with" context handler does not need to be used when
    calling this function.

    Parameters
    ==========

    filepath
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

def fill_templates(return_vals: tuple, main_template: Template, variables: dict):
    """Add docstring

    Parameters
    ==========

    returns : tuple
        Tuple of values to return

    main_template : Template
        Main template string to fill out and return if requested

    variables : dict
        Dictionary of additional arguments and values to use to fill out the
        template strings"""
    if not (variables.get("show") or variables.get("return_latex")):
        return return_vals

    sorted_vars = {}
    subtemplates = {}
    for key, value in variables.items():
        if isinstance(value, Template):
            subtemplates.update({key: value})
        elif getattr(value, "unpack_for_templates", False):
            sorted_vars.update(vars(value))
        else:
            sorted_vars.update({key: value})

    rounded_vars = {}
    dec = sorted_vars.get("decimal_points", 3)
    for key, value in sorted_vars.items():
        try:
            rounded_vars.update({key: round(value, dec)})
        except TypeError:
            rounded_vars.update({key: value})

    filled_subtemplates = {}
    for name, subtemplate in subtemplates.items():
        filled_subtemplates.update({name: subtemplate.substitute(**rounded_vars)})

    latex = main_template.substitute(**filled_subtemplates, **rounded_vars)
    if rounded_vars.get("show"):
        display(Latex(latex))
    if rounded_vars.get("return_latex"):
        return (latex, *return_vals)
    return return_vals
