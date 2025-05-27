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
from typing import Annotated, Union

from numpy import ndarray
import pint

from structuraltools.template import Result


resources = importlib.resources.files("structuraltools.resources")

pint.compat.upcast_type_map.update({"structuraltools.template.Result": None})
unit = pint.UnitRegistry(resources.joinpath("units"))
unit.formatter.default_format = "~L"


type Numeric = Union[int, float, Annotated[pint.Quantity, float], Result]
type NumericArray = Union[ndarray, Annotated[pint.Quantity, ndarray], Result]

type Area = Annotated[pint.Quantity, float, "[length]**2]"]
type Force = Annotated[pint.Quantity, float, "[force]"]
type Length = Annotated[pint.Quantity, float, "[length]"]
type LineLoad = Annotated[pint.Quantity, float, "[force]/[length]"]
type Moment = Annotated[pint.Quantity, float, "[moment]"]
type MomentOfInertia = Annotated[pint.Quantity, float, "[length]**4"]
type Pressure = Annotated[pint.Quantity, float, "[pressure]"]
type SectionModulus = Annotated[pint.Quantity, float, "[length]**3"]
type Stress = Annotated[pint.Quantity, float, "[pressure]"]
type TorsionalConstant = Annotated[pint.Quantity, float, "[length]**4"]
type UnitWeight = Annotated[pint.Quantity, float, "[unit_weight]"]
type Velocity = Annotated[pint.Quantity, float, "[velocity]"]
type WarpingConstant = Annotated[pint.Quantity, float, "[length]**6"]
