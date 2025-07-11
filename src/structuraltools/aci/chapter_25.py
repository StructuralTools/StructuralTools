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
from structuraltools.utils import Result


resources = importlib.resources.files("structuraltools.aci.resources")
with open(resources.joinpath("chapter_25_templates_processed.json")) as file:
    templates = json.load(file)


def eq_25_4_2_4a(f_y: Stress, psi_t: float, psi_e: float, psi_s: float,
        psi_g: float, lamb: float, f_prime_c: Stress, c_b: Length, K_tr: Length,
        d_b: Length, **display_options) -> Result[Length]:
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
    l_prime_d = ((3*f_y*min(psi_t*psi_e, 1.7)*psi_s*psi_g*d_b**2)/ \
                 (40*lamb*sqrt(f_prime_c.to("psi")*unit.psi)*(c_b+K_tr))).to("inch")
    return templates.eq_25_4_2_4a.fill(locals(), l_prime_d, **display_options)

def eq_25_4_2_4b(A_tr: Area, s: Length, n: int, **display_options) -> Result[Length]:
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
    return templates.eq_25_4_2_4b.fill(locals(), K_tr, **display_options)

def table_25_4_2_5_lamb(w_c: UnitWeight, **display_options) -> Result[float]:
    """ACI 318-19 Table 25.4.2.5 lambda check

    Parameters
    ==========

    w_c : UnitWeight
        Concrete unit weight"""
    normal_weight = 135*unit.pcf
    if w_c < normal_weight:
        lamb = 0.75
        template = templates.table_25_4_2_5_lamb_light
    else:
        lamb = 1
        template = templates.table_25_4_2_5_lamb_normal
    return template.fill(locals(), lamb, **display_options)

def table_25_4_2_5_psi_g(f_y: Stress, **display_options) -> Result[float]:
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
        template = templates.table_25_4_2_5_psi_g_low
    elif f_y <= high_limit:
        psi_g = 1.15
        template = templates.table_25_4_2_5_psi_g_mid
    else:
        psi_g = 1.3
        template = templates.table_25_4_2_5_psi_g_high
    return template.fill(locals(), psi_g, **display_options)

def table_25_4_2_5_psi_e(coated: bool, d_b: Length, c_c: Length, s: Length,
        **display_options) -> Result[float]:
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
            template = templates.table_25_4_2_5_psi_e_c_c
        elif s < d_b7:
            psi_e = 1.5
            template = templates.table_25_4_2_5_psi_e_s
        else:
            psi_e = 1.2
            template = templates.table_25_4_2_5_psi_e_true
    else:
        psi_e = 1
        template = templates.table_25_4_2_5_psi_e_false
    return template.fill(locals(), psi_e, **display_options)

def table_25_4_2_5_psi_s(use_psi_s: bool, size: int, **display_options) -> Result[float]:
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
        template = templates.table_25_4_2_5_psi_s_big
    elif use_psi_s:
        psi_s = 0.8
        template = templates.table_25_4_2_5_psi_s_used
    else:
        psi_s = 1
        template = templates.table_25_4_2_5_psi_s_small
    return template.fill(locals(), psi_s, **display_options)

def table_25_4_2_5_psi_t(concrete_below: bool, **display_options) -> Result[float]:
    """ACI 318-19 Table 25.4.2.5 psi_t check

    Parameters
    ==========

    concrete_below : bool
        Boolean indicating if there is more than 12 inches of fresh concrete
        placed below horizontal reinforcement"""
    limit = 12*unit.inch
    if concrete_below:
        psi_t = 1.3
        template = templates.table_25_4_2_5_psi_t_true
    else:
        psi_t = 1
        template = templates.table_25_4_2_5_psi_t_false
    return template.fill(locals(), psi_t, **display_options)

def table_25_4_2_5(rebar: materials.Rebar, concrete: materials.Concrete,
        c_c: Length, s: Length, use_psi_s: bool, concrete_below: bool,
        **display_options) -> Result[tuple[float]]:
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
    display = display_options.pop("display", False)

    lamb = table_25_4_2_5_lamb(concrete.w_c, **display_options)
    psi_g = table_25_4_2_5_psi_g(rebar.f_y, **display_options)
    psi_e = table_25_4_2_5_psi_e(rebar.coated, rebar.d_b, c_c, s, **display_options)
    psi_s = table_25_4_2_5_psi_s(use_psi_s, rebar.size, **display_options)
    psi_t = table_25_4_2_5_psi_t(concrete_below, **display_options)
    return templates.table_25_4_2_5.fill(locals(), lamb, psi_g, psi_e, psi_s,
        psi_t, display=display, **display_options)

def eq_25_4_3_1a(f_y: Stress, psi_e: float, psi_r: float, psi_o: float,
        psi_c: float, lamb: float, f_prime_c: Stress, **display_options) -> Result[Length]:
    pass
