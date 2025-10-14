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

from structuraltools.unit import (Force, Length, Moment, MomentOfInertia,
    SectionModulus, Stress)
from structuraltools.utils import fill_template, Result


resources = importlib.resources.files("structuraltools.awc.resources")
with open(resources.joinpath("chapter_3_templates_processed.json")) as file:
    templates = json.load(file)


def eq_3_3_1(
        F_prime_b: Stress,
        S: SectionModulus,
        axis: str,
        **string_options) -> Result[Moment]:
    """AWC NDS-2024 Equation 3.3-1

    Parameters
    ==========

    F_prime_b : Stress
        Adjusted reference design bending stress

    S : SectionModulus
        Elastic section modulus

    axis : str
        String indicating the bending axis. Use "x" for strong axis bending and
        "y" for weak axis bending."""
    phiM_n = (F_prime_b*S).to("lbft")
    return fill_template(phiM_n, templates["eq_3_3_1"], locals(), **string_options)

def eq_3_3_5(l_e: Length, d: Length, b: Length, **string_options) -> Result[float]:
    """AWC NDS-2024 Equation 3.3-5

    Parameters
    ==========

    l_e : Length
        Effective length for bending

    d : Length
        Member depth

    b : Length
        Member thickness"""
    R_B = sqrt(l_e*d/b**2).to("dimensionless").magnitude
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

def sec_3_3_3(section, l_e: Length, F_star_b: Stress, E_prime_min: Stress,
        **string_options) -> Result[float]:
    """Calculate the beam stability factor (C_L) according to NDS 2024 Section 3.3.3

    Parameters
    ==========

    l_e : Length
        Effective length from NDS 2024 Table 3.3.3

    F_star_b : Stress
        Reference bending design value multiplied by all applicable adjustment
        factors except C_fu, C_V (when C_V <= 1), and C_L

    E_prime_min : Stress
        Adjusted lower bound modulus of elasticity"""
    R_B_str, R_B = eq_3_3_5(l_e, section.d, section.b, **string_options)
    assert R_B <= 50  # Slenderness limit. See NDS 2024 Section 3.3.3.7
    F_bE_str, F_bE = eq_3_3_6a(E_prime_min, R_B, **string_options)
    C_L_str, C_L = eq_3_3_6(F_bE, F_star_b, **string_options)
    return fill_template(C_L, templates["sec_3_3_3"], locals(), **string_options)

def eq_3_4_2(F_prime_v: Stress, b: Length, d: Length, **string_options) -> Result[Force]:
    """AWC NDS-2024 Equation 3.4-2

    Parameters
    ==========

    F_prime_v : Stress
        Adjusted reference design shear stress

    b : Length
        Member thickness

    d : Length
        Member depth"""
    V_u = (2*F_prime_v*b*d/3).to("lb")
    return fill_template(V_u, templates["eq_3_4_2"], locals(), **string_options)

def eq_3_7_1(F_cE: Stress, F_star_c: Stress, c: float, **string_options) -> Result[float]:
    """AWC NDS-2024 Equation 3.7-1

    Parameters
    ==========

    F_cE : Stress
        Critical buckling design value for compression members

    F_star_c : Stress
        Reference compression design value multiplied by all applicable
        adjustment factors except C_P

    c : float
        Adjustment factor for wood type"""
    C_P = ((1+F_cE/F_star_c)/(2*c)-sqrt(((1+F_cE/F_star_c)/(2*c))**2-(F_cE/F_star_c)/c))
    C_P = C_P.to("dimensionless").magnitude
    return fill_template(C_P, templates["eq_3_7_1"], locals(), **string_options)
