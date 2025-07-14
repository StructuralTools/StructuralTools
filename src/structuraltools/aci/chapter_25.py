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

from structuraltools.aci import materials
from structuraltools.unit import unit, Area, Length, Stress, UnitWeight
from structuraltools.utils import fill_template, Result


resources = importlib.resources.files("structuraltools.aci.resources")
with open(resources.joinpath("chapter_25_templates_processed.json")) as file:
    templates = json.load(file)


def eq_25_4_2_4a(f_y: Stress, psi_t: float, psi_e: float, psi_s: float,
        psi_g: float, lamb: float, f_prime_c: Stress, c_b: Length, K_tr: Length,
        d_b: Length, **string_options) -> Result[Length]:
    """ACI 318-19 Equation 25.4.2.4a

    Parameters
    ==========

    f_y : Stress
        Rebar yield stress

    psi_t : float
        Casting position factor from ACI 318-19 Table 25.4.2.5

    psi_e : float
        Rebar coating factor from ACI 318-19 Table 25.4.2.5

    psi_s : float
        Rebar size factor from ACI 318-19 Table 25.4.2.5

    psi_g : float
        Reinforcment grade factor from ACI 318-19 Table 25.4.2.5

    lamb : float
        Lightweight concrete factor from ACI 318-19 Table 25.4.2.5

    f_prime_c : Stress
        Specified concrete strength

    c_b : Length
        Lesser of: (a) the distance from the center of a bar or wire to the
        nearest concrete surface, and (b) one-half of the center-to-center
        spacing of bars or wires being developed

    K_tr : Length
        Transverse reinforcement index

    d_b : Length
        Rebar diameter"""
    f_prime_c = f_prime_c.to("psi")
    l_prime_d = ((3*f_y*min(psi_t*psi_e, 1.7)*psi_s*psi_g*d_b**2)/ \
                 (40*lamb*sqrt(f_prime_c*unit.psi)*(c_b+K_tr))).to("inch")
    return fill_template(l_prime_d, templates["eq_25_4_2_4a"], locals(), **string_options)

def eq_25_4_2_4b(A_tr: Area, s: Length, n: int, **string_options) -> Result[Length]:
    """ACI 318-19 Equation 25.4.2.4b

    Parameters
    ==========

    A_tr : Area
        Add description

    s : Length
        Add description

    n : int
        Add description"""
    K_tr = ((40*A_tr)/(s*n)).to("inch")
    return fill_template(K_tr, templates["eq_25_4_2_4b"], locals(), **string_options)

def table_25_4_2_5_lamb(w_c: UnitWeight, **string_options) -> Result[float]:
    """ACI 318-19 Table 25.4.2.5 lambda check

    Parameters
    ==========

    w_c : UnitWeight
        Concrete unit weight"""
    normal_weight = 135*unit.pcf
    if w_c < normal_weight:
        lamb = 0.75
        template = templates["table_25_4_2_5_lamb_light"]
    else:
        lamb = 1
        template = templates["table_25_4_2_5_lamb_normal"]
    return fill_template(lamb, template, locals(), **string_options)

def table_25_4_2_5_psi_g(f_y: Stress, **string_options) -> Result[float]:
    """ACI 318-19 Table 25.4.2.5 psi_g check

    Parameters
    ==========

    f_y : Stress
        Rebar yield stress"""
    low_limit = 60*unit.ksi
    high_limit = 80*unit.ksi
    f_y = round(f_y.to("ksi").magnitude)*unit.ksi
    if f_y <= low_limit:
        psi_g = 1
        template = templates["table_25_4_2_5_psi_g_low"]
    elif f_y <= high_limit:
        psi_g = 1.15
        template = templates["table_25_4_2_5_psi_g_mid"]
    else:
        psi_g = 1.3
        template = templates["table_25_4_2_5_psi_g_high"]
    return fill_template(psi_g, template, locals(), **string_options)

def table_25_4_2_5_psi_e(coated: bool, d_b: Length, c_c: Length, s: Length,
        **string_options) -> Result[float]:
    """ACI 318-19 Tble 25.4.2.5 psi_g check

    Parameters
    ==========

    coated : bool
        Boolean indicating if the rebar is epoxy or zing and epoxy dual-coated

    d_b : Length
        Rebar diameter

    c_c : Length
        Rebar clear cover

    s : Length
        Center to center rebar spacing"""
    if coated:
        d_b3 = 3*d_b
        d_b7 = 7*d_b
        if c_c < d_b3:
            psi_e = 1.5
            template = templates["table_25_4_2_5_psi_e_c_c"]
        elif s < d_b7:
            psi_e = 1.5
            template = templates["table_25_4_2_5_psi_e_s"]
        else:
            psi_e = 1.2
            template = templates["table_25_4_2_5_psi_e_true"]
    else:
        psi_e = 1
        template = templates["table_25_4_2_5_psi_e_false"]
    return fill_template(psi_e, template, locals(), **string_options)

def table_25_4_2_5_psi_s(use_psi_s: bool, size: int, **string_options) -> Result[float]:
    """ACI 318-19 Table 25.4.2.5 psi_s check. An additional argument is provided
    to always use a psi_s of 1, since the psi_s factor is unconservative.

    Parameters
    ==========

    use_psi_s : bool
        True if psi_s should be used as shown in ACI 318-19 Table 25.4.2.5.
        False if 1 should always be used

    size : int
        Standard rebar size number"""
    if size >= 7:
        psi_s = 1
        template = templates["table_25_4_2_5_psi_s_big"]
    elif use_psi_s:
        psi_s = 0.8
        template = templates["table_25_4_2_5_psi_s_used"]
    else:
        psi_s = 1
        template = templates["table_25_4_2_5_psi_s_small"]
    return fill_template(psi_s, template, locals(), **string_options)

def table_25_4_2_5_psi_t(concrete_below: bool, **string_options) -> Result[float]:
    """ACI 318-19 Table 25.4.2.5 psi_t check

    Parameters
    ==========

    concrete_below : bool
        Boolean indicating if there is more than 12 inches of fresh concrete
        placed below horizontal reinforcement"""
    limit = 12*unit.inch
    if concrete_below:
        psi_t = 1.3
        template = templates["table_25_4_2_5_psi_t_true"]
    else:
        psi_t = 1
        template = templates["table_25_4_2_5_psi_t_false"]
    return fill_template(psi_t, template, locals(), **string_options)

def table_25_4_2_5(rebar: materials.Rebar, concrete: materials.Concrete,
        c_c: Length, s: Length, use_psi_s: bool, concrete_below: bool,
        **string_options) -> Result[dict[str, float]]:
    """ACI 318-19 Table 25.4.2.5

    Parameters
    ==========

    rebar : materials.Rebar
        Rebar being developed

    concrete : materials.Concrete
        Concrete the rebar is being developed in

    c_c : Length
        Concrete clear cover

    s : Length
        Center to center rebar spacing

    use_psi_s : bool
        True if psi_s should be used as shown in ACI 318-19 Table 25.4.2.5.
        False if 1 should always be used

    concrete_below : bool
        Boolean indicating if there is more than 12 inches of fresh concrete
        placed below horizontal reinforcement"""
    lamb_str, lamb = table_25_4_2_5_lamb(concrete.w_c, **string_options)
    psi_g_str, psi_g = table_25_4_2_5_psi_g(rebar.f_y, **string_options)
    psi_e_str, psi_e = table_25_4_2_5_psi_e(rebar.coated, rebar.d_b, c_c, s, **string_options)
    psi_s_str, psi_s = table_25_4_2_5_psi_s(use_psi_s, rebar.size, **string_options)
    psi_t_str, psi_t = table_25_4_2_5_psi_t(concrete_below, **string_options)
    modifiers = {"lamb": lamb, "psi_g": psi_g, "psi_e": psi_e, "psi_s": psi_s, "psi_t": psi_t}
    return fill_template(modifiers, templates["table_25_4_2_5"], locals(), **string_options)

def eq_25_4_3_1a(f_y: Stress, psi_e: float, psi_r: float, psi_o: float,
        psi_c: float, lamb: float, f_prime_c: Stress, d_b: Length,
        **string_options) -> Result[Length]:
    """ACI 318-19 Equation 25.4.3.1a

    Parameters
    ==========

    f_y: Stress
        Rebar yield stress

    psi_e : float
        Rebar coating factor from ACI 318-19 Table 25.4.3.2

    psi_r : float
        Confining reinforcement factor from ACI 318-19 Table 25.4.3.2

    psi_o : float
        Location factor from ACI 318-19 Table 25.4.3.2

    psi_c : float
        Concrete strength factor from ACI 318-19 Table 25.4.3.2

    lamb : float
        Lightweight concrete factor from ACI 318-19 Table 25.4.3.2

    f_prime_c : Stress
        Specified concrete strength

    d_b : Length
        Rebar diameter"""
    d_b = d_b.to("inch")
    f_prime_c = f_prime_c.to("psi")
    l_prime_dh = (((f_y*psi_e*psi_r*psi_o*psi_c)/ \
        (55*lamb*sqrt(f_prime_c*unit.pli)))*d_b**1.5).to("inch")
    return fill_template(l_prime_dh, templates["eq_25_4_3_1a"], locals(), **string_options)

def table_25_4_3_2_lamb(w_c: UnitWeight, **string_options) -> Result[float]:
    """ACI 318-19 Table 25.4.3.2 lambda check

    Parameters
    ==========

    w_c : UnitWeight
        Concrete unit weight"""
    normal_weight = 135*unit.pcf
    if w_c < normal_weight:
        lamb = 0.75
        template = templates["table_25_4_3_2_lamb_light"]
    else:
        lamb = 1
        template = templates["table_25_4_3_2_lamb_normal"]
    return fill_template(lamb, template, locals(), **string_options)

def table_25_4_3_2_psi_e(coated: bool, **string_options) -> Result[float]:
    """ACI 318-19 Table 25.4.3.2 psi_e check

    Parameters
    ==========

    coated : bool
        Whether the rebar is epoxy coated or zinc and epoxy dual coated"""
    psi_e = 1.2 if coated else 1
    return fill_template(psi_e, templates["table_25_4_3_2_psi_e"], locals(), **string_options)

def table_25_4_3_2_psi_r(d_b: Length, A_hs: Area, size: int, s: Length,
        A_th: Area, **string_options) -> Result[float]:
    """ACI 318-19 Table 25.4.3.2 psi_r check

    Parameters
    ==========

    d_b : Length
        Diameter of rebar being developed

    A_hs : Area
        Area of bars being developed at the location

    size : int
        Size of rebar being developed

    s : Length
        Minimum center to center spacing of bars being developed

    A_th : Area
        Total cross-sectional area of ties or stirrups confining hooked bars"""
    d_b6 = 6*d_b
    A_hs04 = 0.4*A_hs
    if size > 11:
        psi_r = 1.6
        template = templates["table_25_4_3_2_psi_r_large"]
    elif s >= d_b6:
        psi_r = 1
        template = templates["table_25_4_3_2_psi_r_s"]
    elif A_th >= A_hs04:
        psi_r = 1
        template = templates["table_25_4_3_2_psi_r_A_th"]
    else:
        psi_r = 1.6
        template = templates["table_25_4_3_2_psi_r_small"]
    return fill_template(psi_r, template, locals(), **string_options)

def table_25_4_3_2_psi_o(d_b: Length, size: int, c_c_side: Length,
        in_column: bool, **string_options) -> Result[float]:
    """ACI 318-19 Table 25.4.3.2 psi_o check

    Parameters
    ==========

    d_b : Length
        Diameter of rebar being developed

    size : int
        Size of rebar being developed

    c_c_side : Length
        Side cover normal to the plane of the hook

    in_column : bool
        Whether or not the hook is inside a column core"""
    d_b6 = 6*d_b
    min_c_c_side = 2.5*unit.inch
    if size > 11:
        psi_o = 1.25
        template = templates["table_25_4_3_2_psi_o_large"]
    elif c_c_side >= d_b6:
        psi_o = 1
        template = templates["table_25_4_3_2_psi_o_d_b"]
    elif c_c_side >= min_c_c_side and in_column:
        psi_o = 1
        template = templates["table_25_4_3_2_psi_o_column"]
    elif in_column:
        psi_o = 1.25
        template = templates["table_25_4_3_2_psi_o_column_small"]
    else:
        psi_o = 1.25
        template = templates["table_25_4_3_2_psi_o_small"]
    return fill_template(psi_o, template, locals(), **string_options)

def table_25_4_3_2_psi_c(f_prime_c: Stress, **string_options) -> Result[float]:
    """ACI 318-19 Table 25.4.3.2 psi_c calculation

    Parameters
    ==========

    f_prime_c : Stress
        Specified concrete strength"""
    psi_c = min(f_prime_c.to("psi").magnitude/15000+0.6, 1)
    return fill_template(psi_c, templates["table_25_4_3_2_psi_c"], locals(), **string_options)

def table_25_4_3_2(rebar: materials.Rebar, concrete: materials.Concrete,
        c_c_side: Length, s: Length, n: int, A_th: Area, in_column: bool,
        **string_options) -> Result[dict[str, float]]:
    """ACI 318-19 Table 25.4.3.2

    Parameters
    ==========

    rebar : materials.Rebar
        Rebar being developed

    concrete : materials.Concrete
        Concrete the rebar is being developed in

    c_c_side : Length
        Minimum concrete cover normal to the plane of the hook

    s : Length
        Center to center spacing of bars being developed

    n : int
        Number of hooked bars being developed

    A_th : Area
        Total cross-sectional area of ties or stirrups confining the hooked bars

    in_column : bool
        Whether or not the hook is inside a column core"""
    lamb_str, lamb = table_25_4_3_2_lamb(concrete.w_c, **string_options)
    psi_e_str, psi_e = table_25_4_3_2_psi_e(rebar.coated, **string_options)
    psi_r_str, psi_r = table_25_4_3_2_psi_r(rebar.d_b, rebar.A_b*n, rebar.size,
        s, A_th, **string_options)
    psi_o_str, psi_o = table_25_4_3_2_psi_o(rebar.d_b, rebar.size, c_c_side,
        in_column, **string_options)
    psi_c_str, psi_c = table_25_4_3_2_psi_c(concrete.f_prime_c, **string_options)
    modifiers = {"lamb": lamb, "psi_e": psi_e, "psi_r": psi_r, "psi_o": psi_o, "psi_c": psi_c}
    return fill_template(modifiers, templates["table_25_4_3_2"], locals(), **string_options)
