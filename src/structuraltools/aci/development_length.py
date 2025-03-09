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
        unconservative.

    show : bool, optional
        Boolean indicating if the calculations should be shown in
        Jupyter output

    return_latex : bool, optional
        Boolean indicating if the latex string should be returned

    decimal_points : int, optional
        How many decimal places to use when displaying calculations in
        Jupyter output. Defaults to 3"""
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
        unconservative.

    show : bool, optional
        Boolean indicating if the calculations should be shown in
        Jupyter output

    return_latex : bool, optional
        Boolean indicating if the latex string should be returned

    decimal_points : int, optional
        How many decimal places to use when displaying calculations in
        Jupyter output. Defaults to 3"""
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

def standard_hook_factors(rebar, concrete, c_c_side, s, **kwargs):
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
        Boolean indicating if the hooked bar terminates inside a column core

    show : bool, optional
        Boolean indicating if the calculations should be shown in
        Jupyter output

    return_latex : bool, optional
        Boolean indicating if the latex string should be returned

    decimal_points : int, optional
        How many decimal places to use when displaying calculations in
        Jupyter output. Defaults to 3"""
    c_c_side = c_c_side.to("inch")
    s = s.to("inch")
    A_th = kwargs.get("A_th", 0*unit.inch**2).to("inch**2")
    dec = kwargs.get("decimal_points", 3)
    factors = {}
    latex = {}

    # Set lamb
    normal = 135*unit.pcf
    if concrete.w_c < normal:
        factors.update({"lamb": 0.75})
        latex.update({"lamb_str": templates.hook_lamb_low.substitute(
            lamb=factors["lamb"], w_c=concrete.w_c, normal=normal)})
    else:
        factors.update({"lamb": 1})
        latex.update({"lamb_str": templates.hook_lamb_high.substitute(
            lamb=factors["lamb"], w_c=concrete.w_c, normal=normal)})

    # Set psi_e
    if rebar.coated:
        factors.update({"psi_e": 1.2})
    else:
        factors.update({"psi_e": 1})
    latex.update({"psi_e_str": templates.hook_psi_e.substitute(
        psi_e=factors["psi_e"], coated=rebar.coated)})

    # Set psi_r
    if rebar.size > 11:
        factors.update({"psi_r": 1.6})
        latex.update({"psi_r_str": templates.hook_psi_r_large.substitute(
            psi_r=factors["psi_r"], size=rebar.size)})
    elif s >= 6*rebar.d_b:
        factors.update({"psi_r": 1})
        latex.update({"psi_r_str": templates.hook_psi_r_s.substitute(
            psi_r=factors["psi_r"], s=round(s, dec), d_b6=round(6*rebar.d_b, dec))})
    elif A_th >= 0.4*rebar.A_b*kwargs.get("n", 1):
        factors.update({"psi_r": 1})
        latex.update({"psi_r_str": templates.hook_psi_r_A_th.substitute(
            psi_r=factors["psi_r"], A_th=round(A_th, dec),
            A_hs04=round(0.4*rebar.A_b*kwargs.get("n", 1), dec))})
    else:
        factors.update({"psi_r": 1.6})
        latex.update({"psi_r_str": templates.hook_psi_r_small.substitute(
            psi_r=factors["psi_r"], s=round(s, dec),  d_b6=round(6*rebar.d_b, dec),
            A_th=round(A_th, dec), A_hs04=round(0.4*rebar.A_b*kwargs.get("n", 1), dec))})

    # Set psi_o
    min_c = 2.5*unit.inch
    if rebar.size > 11:
        factors.update({"psi_o": 1.25})
        latex.update({"psi_o_str": templates.hook_psi_o_large.substitute(
            psi_o=factors["psi_o"], size=rebar.size)})
    elif c_c_side >= 6*rebar.d_b:
        factors.update({"psi_o": 1})
        latex.update({"psi_o_str": templates.hook_psi_o_d_b.substitute(
            psi_o=factors["psi_o"], c_c_side=round(c_c_side, dec), d_b6=round(6*rebar.d_b, dec))})
    elif c_c_side >= min_c and kwargs.get("in_column", False):
        factors.update({"psi_o": 1})
        latex.update({"psi_o_str": templates.hook_psi_o_column.substitute(
            psi_o=factors["psi_o"], c_c_side=round(c_c_side, dec), min_c=min_c)})
    elif kwargs.get("in_column", False):
        factors.update({"psi_o": 1.25})
        latex.update({"psi_o_str": templates.hook_psi_o_column_small.substitute(
            psi_o=factors["psi_o"], c_c_side=round(c_c_side, dec), min_c=min_c)})
    else:
        factors.update({"psi_o": 1.25})
        latex.update({"psi_o_str": templates.hook_psi_o_small.substitute(
            psi_o=factors["psi_o"], c_c_side=round(c_c_side, dec), d_b6=round(6*rebar.d_b, dec))})

    # Set psi_c
    factors.update({"psi_c": min(concrete.f_prime_c.magnitude/15000+0.6, 1)})
    latex.update({"psi_c_str": templates.hook_psi_c.substitute(
        psi_c=round(factors["psi_c"], dec), f_prime_c=concrete.f_prime_c)})

    if kwargs.get("show") or kwargs.get("return_latex"):
        latex = templates.standard_hook_factors.substitute(**latex)
        if kwargs.get("show"):
            display(Latex(latex))
        if kwargs.get("return_latex"):
            return latex, factors
    return factors

def standard_hook(rebar, concrete, c_c_side, s, **kwargs):
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
        Boolean indicating if the hooked bar terminates inside a column core

    show : bool, optional
        Boolean indicating if the calculations should be shown in Jupyter output

    return_latex : bool, optional
        Boolean indicating if the latex string should be returned

    decimal_points : int, optional
        How many decimal places to use when displaying calculations in
        Jupyter output. Defaults to 3"""
    c_c_side = c_c_side.to("inch")
    s = s.to("inch")
    dec = kwargs.get("decimal_points", 3)
    latex = {
        "c_c_side": round(c_c_side, dec),
        "d_b": round(rebar.d_b, dec),
        "f_prime_c": round(concrete.f_prime_c, dec),
        "f_y": round(rebar.f_y, dec),
        "s": round(s, dec)
    }

    factors_latex, factors = standard_hook_factors(
        rebar, concrete, c_c_side, s,
        n=kwargs.get("n", 1),
        A_th=kwargs.get("A_th", 0*unit.inch**2).to("inch**2"),
        in_column=kwargs.get("in_column", False),
        return_latex=True,
        decimal_points=dec)
    lamb, psi_e, psi_r, psi_o, psi_c = factors.values()
    latex.update(factors)
    latex.update({"factors_latex": factors_latex, "psi_c": round(latex["psi_c"], dec)})

    l_prime_dh = (((rebar.f_y*psi_e*psi_r*psi_o*psi_c)/ \
        (55*lamb*sqrt(concrete.f_prime_c*unit.pli)))*rebar.d_b**1.5).to("inch")
    l_dh_limit = 6*unit.inch
    l_dh = max(l_prime_dh, 8*rebar.d_b, l_dh_limit)
    latex.update({
        "l_prime_dh": round(l_prime_dh, dec),
        "d_b8": round(8*rebar.d_b, dec),
        "l_dh_limit": round(l_dh_limit, dec),
        "l_dh": round(l_dh, dec)
    })

    if kwargs.get("show") or kwargs.get("return_latex"):
        latex = templates.standard_hook.substitute(**latex)
        if kwargs.get("show"):
            display(Latex(latex))
        if kwargs.get("return_latex"):
            return latex, l_dh
    return l_dh
