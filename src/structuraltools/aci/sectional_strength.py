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

from structuraltools import unit
from structuraltools.aci import _sectional_strength_latex as templates


def calc_phi(rebar, epsilon_t: float, **kwargs) -> float:
    """Calculate the resistance factor for concrete members resisting moment
       and/or axial force according to ACI 318-19 Table 21.2.2

       Parameters
       ==========

       rebar : structuraltools.materials.Rebar instance
           The rebar used in the member

       epsilon_t : float
           Maximum reinforcing strain in the member

       show : bool, optional
           Boolean indicating if the calculations shold be shown in
           Jupyter output

       return_latex : bool, optional
           Boolean indicating if the latex string should be returned

       decimal_points : int, optional
           How many decimal places to use when displaying calculations in
           Jupyter output. Defaults to 3"""
    dec = kwargs.get("decimal_points", 3)

    epsilon_ty = (rebar.f_y/rebar.E_s).to("dimensionless").magnitude
    latex = {
        "epsilon_t": round(epsilon_t, dec),
        "epsilon_ty": round(epsilon_ty, dec),
        "epsilon_ty003": round(epsilon_ty+0.003, dec)
    }
    if epsilon_t <= epsilon_ty:
        phi = 0.65
        latex = templates.calc_phi_compression.substitute(phi=phi, **latex)
    elif epsilon_t < epsilon_ty+0.003:
        phi = 0.65+0.25*(epsilon_t-epsilon_ty)/0.003
        latex = templates.calc_phi_transition.substitute(phi=round(phi, dec), **latex)
    else:
        phi = 0.9
        latex = templates.calc_phi_tension.substitute(phi=phi, **latex)

    if kwargs.get("show"):
        display(Latex(latex))
    if kwargs.get("return_latex"):
        return latex, phi
    return phi

def moment_capacity(b, d, concrete, rebar, n: int, **kwargs):
    """Calculate the design moment capacitg of a rectangular concrete member
    with tension reinforcing only.

    Parameters
    ==========

    b : pint length quantity
        Beam width or width of slab strip used for analysis

    d : pint length quantity
        Depth from extreme compression fiber to centroid of tension steel

    concrete : structuraltools.materials.Concrete instance
        Concrete to use for the member

    rebar : structuraltools.materials.Rebar instance
        Rebar to use in the member

    n : int
        Number of reinforcing bars used in the member

    d_t : pint length quantity, optional
        Depth from exmreme compression fiber to furthest tensile
        reinforcement. In the case of a single layer of reinforcing
        this is the same as d and does not need to be specified.

    show : bool, optional
        Boolean indicating if the calculations shold be shown in
        Jupyter output

    return_latex : bool, optional
        Boolean indicating if the latex string should be returned

    decimal_points : int, optional
        How many decimal places to use when displaying calculations in
        Jupyter output. Defaults to 3"""
    dec = kwargs.get("decimal_points", 3)

    a = ((n*rebar.A_b*rebar.f_y)/(0.85*concrete.f_prime_c*b)).to("inch")
    M_n = (n*rebar.A_b*rebar.f_y*(d-a/2)).to("kipft")
    epsilon_t = (0.003*((concrete.beta_1*kwargs.get("d_t", d))/a-1)).to("dimensionless").magnitude
    phi_latex, phi = calc_phi(rebar, epsilon_t, return_latex=True, decimal_points=dec)

    if kwargs.get("show") or kwargs.get("return_latex"):
        latex = templates.moment_capacity.substitute(
            a=round(a, dec),
            A_b=rebar.A_b,
            b=round(b.to("inch"), dec),
            d=round(d.to("inch"), dec),
            d_t=round(kwargs.get("d_t", d).to("inch"), dec),
            f_prime_c=concrete.f_prime_c,
            f_y=rebar.f_y,
            M_n=round(M_n, dec),
            n=round(n, dec),
            beta_1=round(concrete.beta_1, dec),
            epsilon_t=round(epsilon_t, dec),
            phi_latex=phi_latex)
        if kwargs.get("show"):
            display(Latex(latex))
        if kwargs.get("return_latex"):
            return latex, phi, M_n
    return phi, M_n
