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
from string import Template
from typing import Annotated, Union

from IPython.display import display, Latex, Markdown
from numpy import ndarray
import pint


resources = importlib.resources.files("structuraltools.resources")

unit = pint.UnitRegistry(resources.joinpath("units"))
unit.formatter.default_format = "~L"

with open(resources.joinpath("ASCE_combinations.json")) as file:
    combs = json.load(file)

decimal_points = 3
header_level = 4

type Numeric = Union[int, float, pint.Quantity]
type NumericArray = Union[ndarray, Annotated[pint.Quantity, ndarray]]

type Area = Annotated[pint.Quantity, float, "[length]**2]"]
type Force = Annotated[pint.Quantity, float, "[force]"]
type Length = Annotated[pint.Quantity, float, "[length]"]
type Moment = Annotated[pint.Quantity, float, "[moment]"]
type MomentOfInertia = Annotated[pint.Quantity, float, "[length]**4"]
type Pressure = Annotated[pint.Quantity, float, "[pressure]"]
type SectionModulus = Annotated[pint.Quantity, float, "[length]**3"]
type Stress = Annotated[pint.Quantity, float, "[pressure]"]
type TorsionalConstant = Annotated[pint.Quantity, float, "[length]**4"]
type UnitWeight = Annotated[pint.Quantity, float, "[unit_weight]"]
type Velocity = Annotated[pint.Quantity, float, "[velocity]"]
type WarpingConstant = Annotated[pint.Quantity, float, "[length]**6"]


class DisplayTemplate(Template):
    """Subclass of Template from the string module that can fill in place. This
    is supposed to be a base class for templates that can display themselves."""
    def fill(self, **variables):
        """Fill the template using the Template.substitute method"""
        self.string = self.substitute(**variables)

    def display(self):
        """Display the filled template"""
        display(Latex(self.string))


class LatexTemplate(DisplayTemplate):
    """General LaTeX template class that can display the filled template"""


class MarkdownTemplate(DisplayTemplate):
    """General markdown template class that can display the filled template"""
    def display(self):
        """Display the filled template"""
        display(Markdown(self.string))


class MathTemplate(DisplayTemplate):
    """Template for single LaTeX equations"""
    def display(self):
        """Display the filled template in a LaTeX equation alignment"""
        display(Latex(rf"\begin{{aligned}} {self.string} \end{{aligned}}"))
