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


from IPython.display import display, Latex
from numpy import sqrt

from structuraltools import decimal_points, materials, quantities, unit, utils
from structuraltools.aci import _development_length_latex as templates


def straight_bar_factors(
        rebar: materials.Rebar,
        concrete: materials.Concrete,
        c_c: quantities.Length,
        s: quantities.Length,
        concrete_below: bool = False,
        use_psi_s: bool = False,
        **latex_options) -> tuple:
    """Returns the modification factors for straight bar development
    length from ACI 318-19 Table 25.4.2.5

    Parameters
    ==========

    rebar : materials.Rebar instance
        Rebar to return the modification factors for

    concrete : materials.Concrete instance
        Concrete to return the modification factors for

    c_c : pint length quantity
        Minimum rebar clear cover

    s : pint length quantity
        Center to center spacing of bars being developed

    concrete_below : bool, optional
        Boolean indicating if there is 12 inches or more of fresh
        concrete placed below horizontal reinforcement

    use_psi_s : bool, optional
        Boolean indicating if the rebar size factor from
        ACI 318-19 Table 25.4.2.5 should be used. This is not applied by
        default because research indicates that using this factor is
        unconservative."""
    c_c = c_c.to("inch")
    s = s.to("inch")

    # Set lamb
    normal_weight = 135*unit.pcf
    if concrete.w_c < normal_weight:
        lamb = 0.75
        lamb_template = templates.straight_lamb_low
    else:
        lamb = 1
        lamb_template = templates.straight_lamb_high

    # Set psi_g
    psi_g_low_limit = 60*unit.ksi
    psi_g_high_limit = 80*unit.ksi
    f_y = round(rebar.f_y.to("ksi").magnitude)*unit.ksi
    if f_y <= psi_g_low_limit:
        psi_g = 1
        psi_g_template = templates.straight_psi_g_low
    elif f_y <= psi_g_high_limit:
        psi_g = 1.15
        psi_g_template = templates.straight_psi_g_mid
    else:
        psi_g = 1.3
        psi_g_template = templates.straight_psi_g_high

    # Set psi_e
    if rebar.coated:
        d_b3 = 3*rebar.d_b
        d_b7 = 7*rebar.d_b
        if c_c < d_b3:
            psi_e = 1.5
            psi_e_template = templates.straight_psi_e_c_c
        elif s < d_b7:
            psi_e = 1.5
            psi_e_template = templates.straight_psi_e_s
        else:
            psi_e = 1.2
            psi_e_template = templates.straight_psi_e_true
    else:
        psi_e = 1
        psi_e_template = templates.straight_psi_e_false

    # Set psi_s
    if rebar.size >= 7:
        psi_s = 1
        psi_s_template = templates.straight_psi_s_big
    elif use_psi_s:
        psi_s = 0.8
        psi_s_template = templates.straight_psi_s_used
    else:
        psi_s = 1
        psi_s_template = templates.straight_psi_s_small

    # Set psi_t
    limit = 12*unit.inch
    if concrete_below:
        psi_t = 1.3
        psi_t_template = templates.straight_psi_t_true
    else:
        psi_t = 1
        psi_t_template = templates.straight_psi_t_false

    return utils.fill_templates(templates.straight_bar_factors, locals(),
                                lamb, psi_g, psi_e, psi_s, psi_t)

def straight_bar(
        rebar: materials.Rebar,
        concrete: materials.Concrete,
        c_c: quantities.Length,
        s: quantities.Length,
        n: int = 1,
        A_tr: quantities.Area | None = None,
        concrete_below: bool = False,
        use_psi_s: bool = False,
        **latex_options) -> quantities.Length | tuple[str, quantities.Length]:
    """Calculate the development length of deformed bars in tension according
    to ACI 318-19 Section 25.4.2

    Parameters
    ==========

    rebar : structuraltools.materials.rebar instance
        Rebar to calculate the development length for

    concrete : structuraltools.materials.concrete instance
        Concrete that the rebar is embedded in

    c_c : pint length quantity
        Minimum rebar clear cover

    s : pint length quantity
        Center to center spacing of bars being developed

    n : int, optional
        Number of bars being developed

    A_tr : pint area quantity, optional
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
    c_c = c_c.to("inch")
    s = s.to("inch")

    factors_latex, lamb, psi_g, psi_e, psi_s, psi_t = straight_bar_factors(
        rebar, concrete, c_c, s, concrete_below, use_psi_s, return_latex=True,
        decimal_points=latex_options.get("dec", decimal_points))

    if A_tr:
        A_tr = A_tr.to("inch**2")
        K_tr = ((40*A_tr)/(s*n)).to("inch")
        K_tr_template = templates.straight_K_tr
    else:
        K_tr = 0*unit.inch
        K_tr_template = ""

    c_b = min(c_c+rebar.d_b/2, s/2)
    l_prime_d = ((3*rebar.f_y*min(psi_t*psi_e, 1.7)*psi_s*psi_g*rebar.d_b**2)/ \
                 (40*lamb*sqrt(concrete.f_prime_c*unit.psi)*(c_b+K_tr))).to("inch")
    l_d_limit = 12*unit.inch
    l_d = max(l_prime_d, l_d_limit)
    return utils.fill_templates(templates.straight_bar, locals(), l_d)

def standard_hook_factors(
    rebar: materials.Rebar,
    concrete: materials.Concrete,
    c_c_side: quantities.Length,
    s: quantities.Length,
    n: int = 1,
    A_th: quantities.Area = 0*unit.inch**2,
    in_column: bool = False,
    **latex_options) -> tuple:
    """Returns the modification factors for standard hook development length
    from ACI 318-19 Table 25.4.3.2

    Parameters
    ==========

    rebar : structuraltools.materials.Rebar instance
        Rebar to return the modification factors for

    concrete : structuraltools.materials.Concrete instance
        Concrete to return the modification factors for

    c_c_side : pint length quantity
        Rebar clear cover normal to the plane of the hook

    s : pint length quantity
        Center to center spacing of bars being developed

    n : int, optional
        Number of hooked bars being developed. Defaults to 1.

    A_th : pint area quantity, optional
        Total cross-sectional area of ties or stirrups confining the hooked
        bars. Defaults to 0

    in_column : bool, optional
        Boolean indicating if the hooked bar terminates inside a column core"""
    c_c_side = c_c_side.to("inch")
    s = s.to("inch")
    A_th = A_th.to("inch**2")

    # Set lamb
    normal_weight = 135*unit.pcf
    if concrete.w_c < normal_weight:
        lamb = 0.75
        lamb_template = templates.hook_lamb_low
    else:
        lamb = 1
        lamb_template = templates.hook_lamb_high

    # Set psi_e
    if rebar.coated:
        psi_e = 1.2
    else:
        psi_e = 1
    psi_e_template = templates.hook_psi_e

    # Set psi_r
    d_b6 = 6*rebar.d_b
    A_hs04 = 0.4*rebar.A_b*n
    if rebar.size > 11:
        psi_r = 1.6
        psi_r_template = templates.hook_psi_r_large
    elif s >= d_b6:
        psi_r = 1
        psi_r_template = templates.hook_psi_r_s
    elif A_th >= A_hs04:
        psi_r = 1
        psi_r_template = templates.hook_psi_r_A_th
    else:
        psi_r = 1.6
        psi_r_template = templates.hook_psi_r_small

    # Set psi_o
    min_c_c_side = 2.5*unit.inch
    if rebar.size > 11:
        psi_o = 1.25
        psi_o_template = templates.hook_psi_o_large
    elif c_c_side >= d_b6:
        psi_o = 1
        psi_o_template = templates.hook_psi_o_d_b
    elif c_c_side >= min_c_c_side and in_column:
        psi_o = 1
        psi_o_template = templates.hook_psi_o_column
    elif in_column:
        psi_o = 1.25
        psi_o_template = templates.hook_psi_o_column_small
    else:
        psi_o = 1.25
        psi_o_template = templates.hook_psi_o_small

    # Set psi_c
    psi_c = min(concrete.f_prime_c.magnitude/15000+0.6, 1)
    psi_c_template = templates.hook_psi_c

    return utils.fill_templates(templates.standard_hook_factors, locals(),
                                lamb, psi_e, psi_r, psi_o, psi_c)

def standard_hook(
    rebar: materials.Rebar,
    concrete: materials.Concrete,
    c_c_side: quantities.Length,
    s: quantities.Length,
    n: int = 1,
    A_th: quantities.Area = 0*unit.inch**2,
    in_column: bool = False,
    **latex_options) -> quantities.Length | tuple[str, quantities.Length]:
    """Calculate the development length ($l_{dh}$) for a deformed bar in tension
    terminating in a standard hook according to ACI 318-19 Section 25.4.3

    Parameters
    ==========

    rebar : structuraltools.materials.rebar instance
        Rebar to calculate the development length for

    concrete : structuraltools.materials.concrete instance
        Concrete that the rebar is embedded in

    c_c_side : pint length quantity
        Rebar clear cover normal to the plane of the hook

    s : pint length quantity
        Center to center spacing of bars being developed

    n : int, optional
        Number of hooked bars being developed. Defaults to 1.

    A_th : pint area quantity, optional
        Total cross-sectional area of ties or stirrups confining hooked bars.
        Defaults to 0.

    in_column : bool
        Boolean indicating if the hooked bar terminates inside a column core"""
    c_c_side = c_c_side.to("inch")
    s = s.to("inch")
    A_th = A_th.to("inch**2")

    factors_latex, lamb, psi_e, psi_r, psi_o, psi_c = standard_hook_factors(
        rebar, concrete, c_c_side, s, n, A_th, in_column, return_latex=True,
        decimal_points=latex_options.get("decimal_points", decimal_points))

    l_prime_dh = (((rebar.f_y*psi_e*psi_r*psi_o*psi_c)/ \
        (55*lamb*sqrt(concrete.f_prime_c*unit.pli)))*rebar.d_b**1.5).to("inch")
    d_b8 = 8*rebar.d_b
    l_dh_limit = 6*unit.inch
    l_dh = max(l_prime_dh, d_b8, l_dh_limit)
    return utils.fill_templates(templates.standard_hook, locals(), l_dh)
