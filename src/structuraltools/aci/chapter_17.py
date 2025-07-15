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

from structuraltools.unit import unit, Area, Force, Stress
from structuraltools.utils import fill_template, Result


resources = importlib.resources.files("structuraltools.aci.resources")
with open(resources.joinpath("chapter_17_templates_processed.json")) as file:
    templates = json.load(file)


def eq_17_6_1_2(A_seN: Area, f_uta: Stress, f_ya: Stress, **string_options) -> Result[Force]:
    """ACI 318-19 Equation 17.6.1.2

    Parameters
    ==========

    A_seN : Area
        Effective cross-sectional area of an anchor in tension

    f_uta : Stress
        Anchor tensile strength

    f_ya : Stress
        Anchor yield strength"""
    N_sa = (A_seN*min(f_uta, 1.9*f_ya, 125*unit.ksi)).to("lb")
    return fill_template(N_sa, templates["eq_17_6_1_2"], locals(), **string_options)
