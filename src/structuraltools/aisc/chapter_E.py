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

from numpy import pi, sqrt

from structuraltools.unit import Area, Force, Length, Stress
from structuraltools.utils import fill_template, Result


resources = importlib.resources.files("structuraltools.aisc.resources")
with open(resources.joinpath("chapter_E_templates_processed.json")) as file:
    templates = json.load(file)


def eq_E3_1(F_n: Stress, A_g: Area, **string_options) -> Result[Force]:
    """AISC 360-22 Equation E3-1

    Parameters
    ==========

    F_n : Stress
        Nominal stress from Equation E3-2 or E3-3

    A_g : Area
        Gross area of member"""
    P_n = (F_n*A_g).to("kip")
    return fill_template(P_n, templates["eq_E3_1"], locals(), **string_options)

def eq_E3_2(F_y: Stress, F_e: Stress, **string_options) -> Result[Stress]:
    """AISC 360-22 Equation E3-2

    Parameters
    ==========

    F_y : Stress
        Steel yield stress

    F_e : Stress
        Elastic buckling stress"""
    F_n = (0.658**(F_y/F_e)*F_y).to("ksi")
    return fill_template(F_n, templates["eq_E3_2"], locals(), **string_options)

def eq_E3_3(F_e: Stress, **string_options) -> Result[Stress]:
    """AISC 360-22 Equation E3-3

    Parameters
    ==========

    F_e : Stress
        Elastic buckling stress"""
    F_n = (0.877*F_e).to("ksi")
    return fill_template(F_n, templates["eq_E3_3"], locals(), **string_options)

def eq_E3_4(E: Stress, L_c: Length, r: Length, axis: str, **string_options
        ) -> Result[Stress]:
    """AISC 360-22 Equation E3-4

    Parameters
    ==========

    E : Stress
        Steel modulus of elasticity

    L_c : Length
        Member effective length

    r : Length
        Member radius of gyration

    axis : str
        String indicating which member axis is being considered"""
    F_e = ((pi**2*E)/((L_c/r)**2)).to("ksi")
    return fill_template(F_e, templates["eq_E3_4"], locals(), **string_options)

def sec_E3(shape, L_c: Length, axis: str, **string_options) -> Result[Force]:
    """AISC 360-22 Section E3

    Parameters
    ==========

    shape : aisc.Shape
        Shape to calculate the flexural buckling capacity of

    L_c : Length
        Member effective length

    axis : str
        String inicating which member axis is being considered"""
    F_y = shape.F_y
    r = shape.r_x if axis == "x" else shape.r_y

    F_e_str, F_e = eq_E3_4(shape.E, L_c, r, axis, **string_options)
    if F_y/F_e <= 2.25:
        F_n_str, F_n = eq_E3_2(F_y, F_e, **string_options)
        template = templates["sec_E3_inelastic"]
    else:
        F_n_str, F_n = eq_E3_3(F_e, **string_options)
        template = templates["sec_E3_elastic"]
    P_n_str, P_n = eq_E3_1(F_n, shape.A, **string_options)
    return fill_template(P_n, template, locals(), **string_options)
