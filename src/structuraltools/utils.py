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
import warnings

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

def get_table_entry(filepath, index) -> dict:
    """Returns the specified row from a csv file as a dict. String values that
    are likely to be numeric or contain Pint quantities are evaluated with
    convert_to_unit. A "with" context handler does not need to be used when
    calling this function.

    Parameters
    ==========

    filepath
        Path to the csv file

    index
        First value on the row to return"""
    with open(filepath) as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            if tuple(line.values())[0] == index:
                raw_data = line
                break
    data = {key: convert_to_unit(value) for key, value in raw_data.items()}
    return data
