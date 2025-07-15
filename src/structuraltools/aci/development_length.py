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

from structuraltools.aci import chapter_25, materials
from structuraltools.unit import unit, Area, Length
from structuraltools.utils import fill_template, Result


resources = importlib.resources.files("structuraltools.aci.resources")
with open(resources.joinpath("development_length_templates_processed.json")) as file:
    templates = json.load(file)


def straight(
        rebar: materials.Rebar,
        concrete: materials.Concrete,
        c_c: Length,
        s: Length,
        n: int = 1,
        A_tr: Area = 0*unit.inch**2,
        concrete_below: bool = False,
        use_psi_s: bool = False,
        **string_options) -> Result[Length]:
    """Calculate the development length of deformed bars in tension according
    to ACI 318-19 Section 25.4.2

    Parameters
    ==========

    rebar : structuraltools.aci.materials.Rebar
        Rebar to calculate the development length for

    concrete : structuraltools.aci.materials.Concrete
        Concrete that the rebar is embedded in

    c_c : Length
        Minimum rebar clear cover

    s : Length
        Center to center spacing of bars being developed

    n : int, optional
        Number of bars being developed

    A_tr : Area, optional
        Total cross-sectional area of all transverse reinforcment within
        spacing $s$ that crosses the potential plane of splitting through
        the reinforcement being developed. This can be taken as 0 as a
        design simplification, and is set to 0 if $n$ is not also set.

    concrete_below : bool, optional
        Boolean indicating if there is 12 inches or more of fresh concrete
        placed below horizontal reinforcement

    use_psi_s : bool, optional
        Boolean indicating if the rebar size factor from
        ACI 318-19 Table 25.4.2.5 should be used. This is not applied by
        default because reseach indicates that using this factor is
        unconservative."""
    d_b = rebar.d_b
    modifiers_str, modifiers = chapter_25.table_25_4_2_5(rebar, concrete, c_c,
        s, use_psi_s, concrete_below, **string_options)
    K_tr_str, K_tr = chapter_25.eq_25_4_2_4b(A_tr, s, n, **string_options)
    c_b = min(c_c+rebar.d_b/2, s/2)
    l_prime_d_str, l_prime_d = chapter_25.eq_25_4_2_4a(f_y=rebar.f_y,
        f_prime_c=concrete.f_prime_c, c_b=c_b, K_tr=K_tr, d_b=rebar.d_b,
        **modifiers, **string_options)
    l_d_min = 12*unit.inch
    l_d = max(l_prime_d, l_d_min)
    modifiers.update(locals())
    return fill_template(l_d, templates["straight"], modifiers, **string_options)

def hook(
        rebar: materials.Rebar,
        concrete: materials.Concrete,
        c_c_side: Length,
        s: Length,
        n: int = 1,
        A_th: Area = 0*unit.inch**2,
        in_column: bool = False,
        **string_options) -> Result[Length]:
    """Calculate the development length ($l_{dh}$) for a deformed bar in tension
    terminating in a standard hook according to ACI 318-19 Section 25.4.3

    Parameters
    ==========

    rebar : structuraltools.aci.materials.Rebar
        Rebar to calculate the development length for

    concrete : structuraltools.aci.materials.Concrete
        Concrete that the rebar is embedded in

    c_c_side : Length
        Rebar clear cover normal to the plane of the hook

    s : Length
        Center to center spacing of bars being developed

    n : int, optional
        Number of hooked bars being developed. Defaults to 1.

    A_th : Area, optional
        Total cross-sectional area of ties or stirrups confining hooked bars.
        Defaults to 0.

    in_column : bool
        Boolean indicating if the hooked bar terminates inside a column core"""
    d_b = rebar.d_b
    modifiers_str, modifiers = chapter_25.table_25_4_3_2(rebar, concrete,
        c_c_side, s, n, A_th, in_column, **string_options)
    l_prime_dh_str, l_prime_dh = chapter_25.eq_25_4_3_1a(f_y=rebar.f_y,
        f_prime_c=concrete.f_prime_c, d_b=d_b, **modifiers, **string_options)
    l_dh_min = 6*unit.inch
    l_dh = max(l_prime_dh, 8*d_b, l_dh_min)
    modifiers.update(locals())
    return fill_template(l_dh, templates["hook"], modifiers, **string_options)
