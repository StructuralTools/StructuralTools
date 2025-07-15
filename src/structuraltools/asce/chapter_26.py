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
from math import e

from numpy import sqrt

from structuraltools.unit import unit, Length, Pressure, Velocity
from structuraltools.utils import fill_template, read_data_table, Result


resources = importlib.resources.files("structuraltools.asce.resources")
table_26_11_1 = read_data_table(resources.joinpath("Table_26-11-1.csv"))
with open(resources.joinpath("chapter_26_templates_processed.json")) as file:
    templates = json.load(file)


def fig_26_8_1_K_1(K_1_factor: float, H: Length, L_prime_h: Length,
        **string_options) -> Result[float]:
    """Calculate K_1 according to ACSE 7-22 Figure 26.8-1

    Parameters
    ==========

    K_1_factor : float
        Factor to from ASCE 7-22 Figure 26.8-1 to use when calculating K_1

    H : Length
        Height of hill or escarpment relative to the upwind terrain

    L_prime_h : Length
        L_h modified acconding to ASCE 7-22 Figure 26.8-1 footnote b"""
    K_1 = (K_1_factor*H/L_prime_h).to("dimensionless").magnitude
    return fill_template(K_1, templates["fig_26_8_1_K_1"], locals(), **string_options)

def fig_26_8_1_K_2(x: Length, mu: float, L_prime_h: Length, **string_options
        ) -> Result[float]:
    """Calculate K_2 according to ASCE 7-22 Figure 26.8-1

    Parameters
    ==========

    x : Length
        Distance from the crest to the site of the building

    mu : float
        Horizontal attenuation factor

    L_prime_h : Length
        L_h modified according to ASCE 7-22 Figure 26.8-1 footnote b"""
    K_2 = (1-abs(x)/(mu*L_prime_h)).to("dimensionless").magnitude
    return fill_template(K_2, templates["fig_26_8_1_K_2"], locals(), **string_options)

def fig_26_8_1_K_3(gamma: float, z: Length, L_prime_h: Length, **string_options
        ) -> Result[float]:
    """Calculate K_3 according to ASCE 7-22 Figure 26.8-1

    Parameters
    ==========

    gamma : float
        Height attenuation factor

    z : Length
        Building height

    L_prime_h : Length
        L_h modified according to ASCE 7-22 Figure 26.8-1 footnote b"""
    K_3 = e**(-gamma*z/L_prime_h)
    return fill_template(K_3, templates["fig_26_8_1_K_3"], locals(), **string_options)

def fig_26_8_1_K_zt(K_1: float, K_2: float, K_3: float, **string_options
        ) -> Result[float]:
    """Calculate K_zt according to ASCE 7-22 Figure 26.8-1

    Parameters
    ==========

    K_1 : float
        Factor to account for shape of topographic feature and maximum speed-up effect

    K_2 : float
        Factor to account for reduction in speed-up with distance upwind or
        downwind of crest

    K_3 : float
        Factor to account for reduction in speed-up with height above local terrain"""
    K_zt = (1+K_1*K_2*K_3)**2
    return fill_template(K_zt, templates["fig_26_8_1_K_zt"], locals(), **string_options)

def table_26_9_1(z_e: Length, **string_options) -> Result[float]:
    """Calculate the ground elevation factor ($K_e$) according to
    ASCE 7-22 Table 26.9-1 footnote 2

    Parameters
    ==========

    z_e : Length
        Ground elevation above sea level"""
    z_e = z_e.to("ft")
    K_e = e**(-0.0000362*z_e.magnitude)
    return fill_template(K_e, templates["table_26_9_1"], locals(), **string_options)

def table_26_10_1(z: Length, z_g: Length, alpha: float, elevation: str = "z",
        **string_options) -> Result[float]:
    """Calculate the velocity pressure exposure coefficient ($K_z$) according to
    ASCE 7-22 Table 26.10-1 Footnote 1

    Parameters
    ==========

    z : Length
        Elevation above site ground level to calculate K_z at

    z_g : Length
        Terrain exposure constant $z_g$ from ASCE 7-22 Table 26.11-1

    alpha : float
        Terrain exposure constant alpha from ASCE 7-22 Table 26.11-1

    elevation : str
        String to use to indicate elevation when displaying the calculation.
        defaults to "z" """
    if z < 0*unit.ft or 3280*unit.ft < z:
        raise ValueError("z is outside of the bounds supported by ASCE 7-22")
    K_z = (2.41*(min(max(15*unit.ft, z), z_g)/z_g)**(2/alpha)).to("dimensionless").magnitude
    return fill_template(K_z, templates["table_26_10_1"], locals(), **string_options)

def eq_26_10_1(K_z: float, K_zt: float, K_e: float, V: Velocity,
        elevation: str = "z", **string_options) -> Result[Pressure]:
    """ASCE 7-22 Equation 26.10-1

    Parameters
    ==========

    K_z : float
        Velocity pressure exposure coefficient from ASCE 7-22 Table 26.10-1

    K_zt : float
        Topographic factor from ASCE 7-22 Figure 26.8-1

    K_e : float
        Ground elevation factor from ASCE 7-22 Table 26.9-1

    V : Velocity
        Basic wind speed from the ASCE 7 Hazard tool

    elevation : str
        String to use to indicate elevation when displaying the calculation.
        defaults to "z" """
    V = V.to("mph")
    q_z = 0.00256*K_z*K_zt*K_e*((V.magnitude)**2)*unit.psf
    return fill_template(q_z, templates["eq_26_10_1"], locals(), **string_options)

def eq_26_11_6(I_bar_z: float, Q: float, axis: str = "", g_Q: float = 3.4, g_v:
        float = 3.4, **string_options) -> Result[float]:
    """ASCE 7-22 Equation 26.11-6

    Parameters
    ==========

    I_bar_z : float
        Intensity of turbulence at hight $\bar{z}$ from ASCE 7-22 Equation 26.11-7

    Q : float
        Background response from ASCE 7-22 Equation 26.11-8

    axis : str
        Subscript to indicate the axis the gust effect factor is calculated for

    g_Q : float
        Factor defined in ASCE 7-22 Section 26.22.4. This can always be left as
        the default value.

    g_v : float
        Factor defined in ASCE 7-22 Section 26.22.4. This can always be left as
        the default value."""
    G = 0.925*(1+1.7*g_Q*I_bar_z*Q)/(1+1.7*g_v*I_bar_z)
    return fill_template(G, templates["eq_26_11_6"], locals(), **string_options)

def eq_26_11_7(c: float, bar_z: Length, **string_options) -> Result[float]:
    """ASCE 7-22 Equation 26.11-7

    Parameters
    ==========

    c : float
        Terrain exposure constant $c$ from ASCE 7-22 Table 26.11-1

    bar_z : Length
        Equivalent height of the structure as defined in
        ASCE 7-22 Section 26.11.4"""

    bar_z = bar_z.to("ft")
    I_bar_z = c*(33/bar_z.magnitude)**(1/6)
    return fill_template(I_bar_z, templates["eq_26_11_7"], locals(), **string_options)

def eq_26_11_8(L: Length, h: Length, L_bar_z: Length, axis_1: str = "",
        axis_2: str = "", **string_options) -> Result[float]:
    """ASCE 7-22 Equation 26.11-8

    Parameters
    ==========

    L : Length
        Width of the structure

    h : Length
        Mean roof height

    L_bar_z : Length
        Integral length scale of turbulence from ASCE 7-22 Equation 26.11-9

    axis_1 : str
        Subscript to indicate the axis the gust effect factor is calculated for

    axis_2 : str
        Subscript to indicate the axis perpendicular to the axis the gust effect
        factor is calculated for"""
    Q = sqrt(1/(1+0.63*((L+h)/L_bar_z)**0.63)).to("dimensionless").magnitude
    return fill_template(Q, templates["eq_26_11_8"], locals(), **string_options)

def eq_26_11_9(L: Length, bar_z: Length, bar_epsilon: float, **string_options
               ) -> Result[Length]:
    r"""ASCE 7-22 Equation 26.11-9

    Parameters
    ==========

    L : Length
        Terrain exposure constant $l$ from ASCE 7-22 Table 26.11-1

    bar_z : Length
        Equavalent height of the structure as defined in
        ASCE 7-22 Section 26.11.4

    bar_epsilon : float
        Terrain exposure constant $\bar{\epsilon}$ for ASCE 7-22 Table 26.11-1"""
    bar_z = bar_z.to("ft")
    L_bar_z = L*(bar_z.magnitude/33)**bar_epsilon
    return fill_template(L_bar_z, templates["eq_26_11_9"], locals(), **string_options)
