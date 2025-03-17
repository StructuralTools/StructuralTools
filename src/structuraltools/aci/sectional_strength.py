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


from typing import Optional

from structuraltools import decimal_points, materials, utils
from structuraltools import Length, Moment
from structuraltools.aci import _sectional_strength_markdown as templates


def calc_phi(
    rebar: materials.Rebar,
    epsilon_t: float,
    **markdown_options) -> float | tuple[str, float]:
    """Calculate the resistance factor for concrete members resisting moment
       and/or axial force according to ACI 318-19 Table 21.2.2

       Parameters
       ==========

       rebar : materials.Rebar
           The rebar used in the member

       epsilon_t : float
           Maximum reinforcing strain in the member"""
    epsilon_ty = (rebar.f_y/rebar.E_s).to("dimensionless").magnitude
    epsilon_ty003 = epsilon_ty+0.003
    if epsilon_t <= epsilon_ty:
        phi = 0.65
        template = templates.calc_phi_compression
    elif epsilon_t < epsilon_ty+0.003:
        phi = 0.65+0.25*(epsilon_t-epsilon_ty)/0.003
        template = templates.calc_phi_transition
    else:
        phi = 0.9
        template = templates.calc_phi_tension
    return utils.fill_templates(template, locals(), phi)

def moment_capacity(
    b: Length,
    d: Length,
    concrete: materials.Concrete,
    rebar: materials.Rebar,
    n: int,
    d_t: Optional[Length] = None,
    **markdown_options) -> Moment | tuple[str, Moment]:
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
    if d_t is None:
        d_t = d
    a = ((n*rebar.A_b*rebar.f_y)/(0.85*concrete.f_prime_c*b)).to("inch")
    M_n = (n*rebar.A_b*rebar.f_y*(d-a/2)).to("kipft")
    epsilon_t = (0.003*((concrete.beta_1*d_t)/a-1)).to("dimensionless").magnitude
    phi_markdown, phi = calc_phi(rebar, epsilon_t, return_markdown=True,
        decimal_points=markdown_options.get("decimal_points", decimal_points))
    return utils.fill_templates(templates.moment_capacity, locals(), phi, M_n)
