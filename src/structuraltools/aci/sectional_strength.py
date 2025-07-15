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
from typing import Optional

from structuraltools.aci import chapter_21, materials
from structuraltools.unit import Area, Length, Moment, Stress
from structuraltools.utils import fill_template, Result


resources = importlib.resources.files("structuraltools.aci.resources")
with open(resources.joinpath("sectional_strength_templates_processed.json")) as file:
    templates = json.load(file)


def calc_a(A_st: Area, f_y: Stress, f_prime_c: Stress, b: Length,
        **string_options) -> Result[Length]:
    """Calculate the Whitney stress block depth of a section with only tension
    reinforcing.

    Parameters
    ==========

    A_st : Area
        Tension steel area

    f_y : Stress
        Tension reinforcing yield stress

    f_prime_c : Stress
        Specified concrete strength

    b : Length
        Stress block width"""
    a = ((A_st*f_y)/(0.85*f_prime_c*b)).to("inch")
    return fill_template(a, templates["calc_a"], locals(), **string_options)

def calc_M_n(A_st: Area, f_y: Stress, d: Length, a: Length, **string_options
        ) -> Result[Moment]:
    """Calculate the nominal moment capacity of a rectangular concrete section
    with only tension reinforcing.

    Parameters
    ==========

    A_st : Area
        Tension steel area

    f_y : Stress
        Tension reinforcing yield stress

    d : Length
        Total section depth

    a : Length
        Whitney stress block depth"""
    M_n = (A_st*f_y*(d-a/2)).to("kipft")
    return fill_template(M_n, templates["calc_M_n"], locals(), **string_options)

def calc_epsilon_t(beta_1: float, d_t: Length, a: Length, **string_options
        ) -> Result[Moment]:
    """Calculate the strain in the tension reinforcement

    Parameters
    ==========

    beta_1 : float
        Factor relating the depth of the Whitney stress block to the depth of
        the neutral axis

    d_t : Length
        Depth on extreme tension reinforcing

    a : Length
        Whitney stress block depth"""
    epsilon_t = (0.003*((beta_1*d_t)/a-1)).to("dimensionless").magnitude
    return fill_template(epsilon_t, templates["calc_epsilon_t"], locals(), **string_options)

def moment_capacity(
        b: Length,
        d: Length,
        concrete: materials.Concrete,
        rebar: materials.Rebar,
        n: int,
        d_t: Optional[Length] = None,
        **string_options) -> Result[Moment]:
    """Calculate the design moment capacitg of a rectangular concrete member
    with tension reinforcing only.

    Parameters
    ==========

    b : Length
        Beam width or width of slab strip used for analysis

    d : Length
        Depth from extreme compression fiber to centroid of tension steel

    concrete : materials.Concrete
        Concrete to use for the member

    rebar : materials.Rebar
        Rebar to use in the member

    n : int
        Number of reinforcing bars used in the member

    d_t : Length, optional
        Depth from exmreme compression fiber to furthest tensile
        reinforcement. In the case of a single layer of reinforcing
        this is the same as d and does not need to be specified."""
    d_t = d if d_t is None else d_t
    A_st = rebar.A_b*n
    a_str, a = calc_a(A_st, rebar.f_y, concrete.f_prime_c, b, **string_options)
    M_n_str, M_n = calc_M_n(A_st, rebar.f_y, d, a, **string_options)
    epsilon_t_str, epsilon_t = calc_epsilon_t(concrete.beta_1, d_t, a, **string_options)
    phi_str, phi = chapter_21.table_21_2_2(rebar, epsilon_t, **string_options)
    return fill_template((phi, M_n), templates["moment_capacity"], locals(), **string_options)
