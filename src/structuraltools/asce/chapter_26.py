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


import json

from numpy import e, sqrt

from structuraltools import resources, unit
from structuraltools import Length, Pressure, Velocity
from structuraltools.asce import _chapter_26_templates as templates
from structuraltools.utils import fill_template, read_data_table


table_26_11_1 = read_data_table(resources.joinpath("ASCE_Table_26-11-1.csv"))

def fig_26_8_1(feature: str, H: Length, L_h: Length, x: Length, z: Length,
        exposure: str, location: str = "downwind", **display_options
        ) -> float | tuple[str, float]:
    """Calculate the topographic factor ($K_zt$) according to
    ASCE 7-22 Figure 26.8-1

    Parameters
    ==========

    feature : str
        Topographic feature causing wind speed-up.
        One of: "ridge", "escarpment", or "hill"

    H : Length
        Height of feature relative to the upwind terrain

    L_h : Length
        Distance upwind of crest to where the difference in ground elevation is
        half of the height of the feature

    x : Length
        Distance (upwind or downwind) from the crest to the site of
        the structure

    z : Length
        Height of the structure above the ground surface at the site

    exposure : str, optional
        Exposure catagory. One of: "B", "C", or "D"

    location : str, optional
        On of: "upwind" or "downwind", indicating the location of the structure
        relative to the feature. Conservatively defaults to "downwind"."""
    with open(resources.joinpath("ASCE_TopoCoefficients.json"), "r") as file:
        topo_coefs = json.load(file)[feature]

    K_1_factor = topo_coefs["K_1/(H/L_h)"][exposure]
    mu = topo_coefs["mu"][location]
    gamma = topo_coefs["gamma"]

    L_h_bounded = max(L_h, 2*H)
    K_1 = (K_1_factor*H/L_h_bounded).to("dimensionless").magnitude
    K_2 = (1-abs(x)/(mu*L_h_bounded)).to("dimensionless").magnitude
    K_3 = e**(-gamma*z/L_h_bounded)
    K_zt = (1+K_1*K_2*K_3)**2
    return fill_template(templates.fig_26_8_1, locals(), K_zt, **display_options)

def table_26_9_1(z_e: Length, **display_options) -> float | tuple[str, float]:
    """Calculate the ground elevation factor ($K_e$) according to
    ASCE 7-22 Table 26.9-1 footnote 2

    Parameters
    ==========

    z_e : Length
        Ground elevation above sea level"""
    z_e = z_e.to("ft")
    K_e = e**(-0.0000362*z_e.magnitude)
    return fill_template(templates.table_26_9_1, locals(), K_e, **display_options)

def table_26_10_1(z: Length, z_g: Length, alpha: float, elevation: str = "z",
        **display_options) -> float | tuple[str, float]:
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
    return fill_template(templates.table_26_10_1, locals(), K_z, **display_options)

def eq_26_10_1(K_z: float, K_zt: float, K_e: float, V: Velocity,
        elevation: str = "z", **display_options) -> Pressure | tuple[str, Pressure]:
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
    return fill_template(templates.eq_26_10_1, locals(), q_z, **display_options)

def eq_26_11_6(I_bar_z: float, Q: float, axis: str = "", g_Q: float = 3.4, g_v:
        float = 3.4, **display_options) -> float | tuple[str, float]:
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
    return fill_template(templates.eq_26_11_6, locals(), G, **display_options)

def eq_26_11_7(c: float, bar_z: Length, **display_options) -> float | tuple[str, float]:
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
    return fill_template(templates.eq_26_11_7, locals(), I_bar_z, **display_options)

def eq_26_11_8(L: Length, h: Length, L_bar_z: Length, axis: str = "",
        **display_options) -> float | tuple[str, float]:
    """ASCE 7-22 Equation 26.11-8

    Parameters
    ==========

    L : Length
        Width of the structure

    h : Length
        Mean roof height

    L_bar_z : Length
        Integral length scale of turbulence from ASCE 7-22 Equation 26.11-9

    axis : str
        Subscript to indicate the axis the gust effect factor is calculated for"""
    Q = sqrt(1/(1+0.63*((L+h)/L_bar_z)**0.63)).to("dimensionless").magnitude
    return fill_template(templates.eq_26_11_8, locals(), Q, **display_options)

def eq_26_11_9(l: Length, bar_z: Length, bar_epsilon: float, **display_options
               ) -> Length | tuple[str, Length]:
    r"""ASCE 7-22 Equation 26.11-9

    Parameters
    ==========

    l : Length
        Terrain exposure constant $l$ from ASCE 7-22 Table 26.11-1

    bar_z : Length
        Equavalent height of the structure as defined in
        ASCE 7-22 Section 26.11.4

    bar_epsilon : float
        Terrain exposure constant $\bar{\epsilon}$ for ASCE 7-22 Table 26.11-1"""
    bar_z = bar_z.to("ft")
    L_bar_z = l*(bar_z.magnitude/33)**bar_epsilon
    return fill_template(templates.eq_26_11_9, locals(), L_bar_z, **display_options)
