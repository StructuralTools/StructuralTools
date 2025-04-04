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


from numpy import pi, sqrt

from structuraltools import aisc, unit, utils
from structuraltools import (Length, Moment, MomentOfInertia, SectionModulus,
                             Stress, TorsionalConstant, WarpingConstant)
from structuraltools.aisc import _chapter_F_templates as templates


def eq_F2_1(F_y: Stress, Z_x: SectionModulus, **display_options) -> Moment:
    """AISC 360-22 Equation F2-1

    Parameters
    ==========

    F_y : Stress
        Steel yield stress

    Z_x : SectionModulus
        Major axis plastic section modulus"""
    M_p = (F_y*Z_x).to("kipft")
    return utils.fill_templates(templates.eq_F2_1, locals(), M_p)

def eq_F2_2(C_b: float, M_p: Moment, F_y: Stress, S_x: SectionModulus,
            L_b: Length, L_p: Length, L_r: Length, **display_options) -> Moment:
    """AISC 360-22 Equation F2-2

    Parameters
    ==========

    C_b : float
        Lateral-torsional buckling modification factor

    M_p : Moment
        Plastic moment capacity

    F_y : Stress
        Steel yield stress

    S_x : SectionModulus
        Major axis elastic section modulus

    L_b : Length
        Distance between compression flange bracing points

    L_p : Length
        Limiting length for inelastic lateral-torsional buckling

    L_r : Length
        Limiting length for elastic lateral-torsional buckling"""
    M_ltb = (C_b*(M_p-(M_p-0.7*F_y*S_x)*(L_b-L_p)/(L_r-L_p))).to("kipft")
    return utils.fill_templates(templates.eq_F2_2, locals(), M_ltb)

def eq_F2_3(F_cr: Stress, S_x: SectionModulus, **display_options) -> Moment:
    """AISC 360-22 Equation F2-3

    Parameters
    ==========

    F_cr : Stress
        Critical stress from AISC 360-22 Equation F2-4

    S_x : SectionModulus
        Major axis elastic section modulus"""
    M_ltb = (F_cr*S_x).to("kipft")
    return utils.fill_templates(templates.eq_F2_3, locals(), M_ltb)

def eq_F2_4(C_b: float, E: Stress, L_b: Length, r_ts: Length, J: TorsionalConstant,
            c: float, S_x: SectionModulus, h_o: Length, **display_options) -> Moment:
    """AISC 360-22 Equation F2-4

    Parameters
    ==========

    C_b : float
        Lateral-torsional buckling modification factor

    E : Stress
        Steel modulus of elasticity

    L_b : Length
        Distance between compression flange bracing points

    r_ts : Length
        Effective radius of gyration

    J : TorsionalConstant
        Torsional torsional

    c : float
        Modification coefficient for channels

    S_x : SectionModulus
        Major axis elastic section modulus

    h_o : Length
        Distance between the flange centroids"""
    F_cr = (C_b*E*pi**2/(L_b/r_ts)**2*sqrt(1+0.078*J*c/(S_x*h_o)*(L_b/r_ts)**2)).to("ksi")
    return utils.fill_templates(templates.eq_F2_4, locals(), F_cr)

def eq_F2_5(r_y: Length, E: Stress, F_y: Stress, **display_options) -> Length:
    """AISC 360-22 Equation F2-5

    Parameters
    ==========

    r_y : Length
        Minor axis radius of gyration

    E : Stress
        Steel elastic modulus

    F_y : Stress
        Steel yield stress"""
    L_p = (1.76*r_y*sqrt(E/F_y)).to("ft")
    return utils.fill_templates(templates.eq_F2_5, locals(), L_p)

def eq_F2_6(r_ts: Length, E: Stress, F_y: Stress, J: TorsionalConstant, c: float,
            S_x: SectionModulus, h_o: Length, **display_options) -> Length:
    """AISC 360-22 Equation F2-6

    Parameters
    ==========

    r_ts : Length
        Effective radius of gyration

    E : Stress
        Steel elastic modulus

    F_y : Stress
        Steel yield stress

    J : TorsionalConstant
        Torsional constant

    c : float
        Modification coefficient for channels

    S_x : SectionModulus
        Major axis elastic section modulus

    h_o : Length
        Distance between the flange centroids"""
    L_r = (1.95*r_ts*E/(0.7*F_y)*sqrt(J*c/(S_x*h_o) \
        +sqrt((J*c/(S_x*h_o))**2+6.76*(0.7*F_y/E)**2))).to("ft")
    return utils.fill_templates(templates.eq_F2_6, locals(), L_p)

def eq_F2_8b(h_o: Length, I_y: MomentOfInertia, C_w: WarpingConstant,
             **display_options) -> float:
    """AISC 360-22 Equation F2-8b

    Parameters
    ==========

    h_o : Length
        Distance between the flange centroids

    I_y : MomentOfInertia
        Minor axis moment of moment of inertia

    C_w : WarpingConstant
        Warping constant"""
    c = h_o/2*sqrt(I_y/C_w)
    return utils.fill_templates(templates.eq_F2_8b, locals(), c)

def sec_F2_2(shape, M_p: Moment, **display_options) -> Moment:
    pass
