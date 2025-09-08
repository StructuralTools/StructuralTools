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

from numpy import sqrt

from structuraltools.unit import Length, Moment, MomentOfInertia, SectionModulus, Stress
from structuraltools.utils import fill_template, Result


resources = importlib.resources.files("structuraltools.awc.resources")
with open(resources.joinpath("chapter_3_templates_processed.json")) as file:
    templates = json.load(file)


def eq_3_3_5(L_e: Length, d: Length, b: Length, **string_options) -> Result[float]:
    """AWC NDS-2024 Equation 3.3-5

    Parameters
    ==========

    L_e : Length
        Effective length for bending

    d : Length
        Member depth

    b : Length
        Member thickness"""
    R_B = sqrt(L_e*d/b**2).to("dimensionless").magnitude
    return fill_template(R_B, templates["eq_3_3_5"], locals(), **string_options)

def eq_3_3_6(F_bE: Stress, F_star_b: Stress, **string_options) -> Result[float]:
    """AWC NDS-2024 Equation 3.3-6

    Parameters
    ==========

    F_bE : Stress
        Critical buckling design value for bending members

    F_star_b : Stress
        Reference bending design value multiplied by all applicable adjustment
        factors except C_fu, C_V (when C_V <= 1), and C_L"""
    C_L = ((1+F_bE/F_star_b)/1.9-sqrt(((1+F_bE/F_star_b)/1.9)**2-(F_bE/F_star_b)/0.95))
    C_L = C_L.to("dimensionless").magnitude
    return fill_template(C_L, templates["eq_3_3_6"], locals(), **string_options)

def eq_3_3_6a(E_prime_min: Stress, R_B: float, **string_options) -> Result[Stress]:
    """AWC NDS-2024 Equation 3.3-6 supporting function a

    Parameters
    ==========

    E_prime_min : Stress
        Lower bound elastic modulus

    R_B : float
        Slenderness ratio for bending"""
    F_bE = 1.2*E_prime_min/R_B**2
    return fill_template(F_bE, templates["eq_3_3_6a"], locals(), **string_options)
