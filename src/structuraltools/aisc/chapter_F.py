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


import copy

from numpy import pi, sqrt

from structuraltools import (Length, Moment, MomentOfInertia, SectionModulus,
                             Stress, TorsionalConstant, WarpingConstant)
from structuraltools.aisc import chapter_B
from structuraltools.aisc import _chapter_F_templates as templates
from structuraltools.utils import fill_template


def eq_F2_1(F_y: Stress, Z_x: SectionModulus, **display_options
            ) -> Moment | tuple[str, Moment]:
    """AISC 360-22 Equation F2-1

    Parameters
    ==========

    F_y : Stress
        Steel yield stress

    Z_x : SectionModulus
        Major axis plastic section modulus"""
    M_p = (F_y*Z_x).to("kipft")
    return fill_template(templates.eq_F2_1, locals(), M_p, **display_options)

def eq_F2_2(C_b: float, M_p: Moment, F_y: Stress, S_x: SectionModulus,
        L_b: Length, L_p: Length, L_r: Length, **display_options
        ) -> Moment | tuple[str, Moment]:
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
    return fill_template(templates.eq_F2_2, locals(), M_ltb, **display_options)

def eq_F2_3(F_cr: Stress, S_x: SectionModulus, **display_options
            ) -> Moment | tuple[str, Moment]:
    """AISC 360-22 Equation F2-3

    Parameters
    ==========

    F_cr : Stress
        Critical stress from AISC 360-22 Equation F2-4

    S_x : SectionModulus
        Major axis elastic section modulus"""
    M_ltb = (F_cr*S_x).to("kipft")
    return fill_template(templates.eq_F2_3, locals(), M_ltb, **display_options)

def eq_F2_4(C_b: float, E: Stress, L_b: Length, r_ts: Length, J: TorsionalConstant,
        c: float, S_x: SectionModulus, h_o: Length, **display_options
        ) -> Moment | tuple[str, Moment]:
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
    return fill_template(templates.eq_F2_4, locals(), F_cr, **display_options)

def eq_F2_5(r_y: Length, E: Stress, F_y: Stress, **display_options
            ) -> Length | tuple[str, Length]:
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
    return fill_template(templates.eq_F2_5, locals(), L_p, **display_options)

def eq_F2_6(r_ts: Length, E: Stress, F_y: Stress, J: TorsionalConstant,
        c: float, S_x: SectionModulus, h_o: Length, **display_options
        ) -> Length | tuple[str, Length]:
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
    return fill_template(templates.eq_F2_6, locals(), L_r, **display_options)

def eq_F2_8b(h_o: Length, I_y: MomentOfInertia, C_w: WarpingConstant,
             **display_options) -> float | tuple[str, float]:
    """AISC 360-22 Equation F2-8b

    Parameters
    ==========

    h_o : Length
        Distance between the flange centroids

    I_y : MomentOfInertia
        Minor axis moment of moment of inertia

    C_w : WarpingConstant
        Warping constant"""
    c = (h_o/2*sqrt(I_y/C_w)).to("dimensionless").magnitude
    return fill_template(templates.eq_F2_8b, locals(), c, **display_options)

def sec_F2_1(shape, **display_options) -> Moment | tuple[str, Moment]:
    """Calculate the major axis plastic moment capacity of an I shape with a
    compact web according to AISC 360-22 Section F2.2

    Parameters
    ==========

    shape : aisc.WideFlange
        Shape to calculate the plastic moment capacity of"""
    options = copy.copy(display_options)
    options.update({"display": False, "return_string": True})

    M_p_str, M_p = eq_F2_1(shape.material.F_y, shape.Z_x, **options)
    return fill_template(templates.sec_F2_1, locals(), M_p, **display_options)

def sec_F2_2(shape, L_b: Length, M_p: Moment, C_b: float, **display_options
             ) -> Moment | tuple[str, Moment]:
    """Calculate the major axis nominal moment capacity of an I shape with a
    compact web based on the limit of lateral torsional buckling according to
    AISC 360-22 Section F2.2.

    Parameters
    ==========

    shape : aisc.WideFlange
        Shape to calculate the lateral torsional buckling moment of

    L_b : Length
        Compression flange unbraced length

    M_p : Moment
        Major axis nominal plastic moment capacity of the section

    C_b : float
        Lateral-torsional buckling modification factor"""
    options = copy.copy(display_options)
    options.update({"display": False, "return_string": True})

    if shape.type == "W":
        c = 1
        c_str = ""
    else:
        c_str, c = eq_F2_8b(shape.h_o, shape.I_y, shape.C_w, **options)

    L_p_str, L_p = eq_F2_5(shape.r_y, shape.material.E, shape.material.F_y,
        **options)
    L_r_str, L_r = eq_F2_6(shape.r_ts, shape.material.E, shape.material.F_y,
        shape.J, c, shape.S_x, shape.h_o, **options)
    if L_b <= L_p:
        M_ltb = M_p
        template = templates.sec_F2_2_plastic
    elif L_b <= L_r:
        M_ltb_str, M_ltb = eq_F2_2(C_b, M_p, shape.material.F_y, shape.S_x, L_b,
            L_p, L_r, **options)
        template = templates.sec_F2_2_inelastic
    else:
        F_cr_str, F_cr = eq_F2_4(C_b, shape.material.E, L_b, shape.r_ts,
            shape.J, c, shape.S_x, shape.h_o, **options)
        M_ltb_str, M_ltb = eq_F2_3(F_cr, shape.S_x, **options)
        template = templates.sec_F2_2_elastic
    return fill_template(template, locals(), M_ltb, **display_options)

def sec_F2(shape, L_b: Length, C_b: float, **display_options) -> Moment | tuple[str, Moment]:
    """Calculate the major axis nominal moment capacity of a compact I shape
    according to AISC 360-22 Section F2.

    Parameters
    ==========

    shape : aisc.WideFlange
        Shape to calculate the nominal moment capacity of

    L_b : Length
        Compression flange unbraced length

    C_b : float
        Lateral-torsional buckling modification factor"""
    options = copy.copy(display_options)
    options.update({"display": False, "return_string": True})

    M_p_str, M_p = sec_F2_1(shape, **options)
    M_ltb_str, M_ltb = sec_F2_2(shape, L_b, M_p, C_b, **options)
    M_n = min(M_p, M_ltb)
    return fill_template(templates.sec_F2, locals(), M_n, **display_options)

def eq_F3_1(M_p: Moment, F_y: Stress, S_x: SectionModulus, lamb_f: float,
        lamb_pf: float, lamb_rf: float, **display_options) -> Moment | tuple[str, Moment]:
    """AISC 360-22 Equation F3-1

    Parameters
    ==========

    M_p : Moment
        Major axis nominal plastic moment capacity of the section

    F_y : Stress
        Steel yield stress

    S_x : SectionModulus
        Major axis elastic section modulus

    lamb_f : float
        Section flange slenderness for flexure

    lamb_pf : float
        Compact section flange slenderness limit for flexure

    lamb_rf : float
        Noncompact section flange slenderness limit for flexure"""
    M_flb = (M_p-(M_p-0.7*F_y*S_x)*(lamb_f-lamb_pf)/(lamb_rf-lamb_pf)).to("kipft")
    return fill_template(templates.eq_F3_1, locals(), M_flb, **display_options)

def eq_F3_2(E: Stress, k_c: float, S_x: SectionModulus, lamb_f: float,
        **display_options) -> Moment | tuple[str, Moment]:
    """AISC 360-22 Equation F3-2

    Parameters
    ==========

    E : Stress
        Steel elastic modulus

    k_c : float
        k_c for AISC 360-22 Section F3.2b

    S_x : SectionModulus
        Major axis elastic section modulus

    lamb_f : float
        Section flange slenderness for flexure"""
    M_flb = (0.9*E*k_c*S_x/lamb_f**2).to("kipft")
    return fill_template(templates.eq_F3_2, locals(), M_flb, **display_options)

def eq_F3_2a(lamb_w: float, **display_options) -> float | tuple[str, float]:
    """Calculate k_c according to AISC 360-22 Section F3.2b

    Parameters
    ==========

    lamb_w : float
        Section web slenderness for flexure"""
    k_c = min(max(0.35, 4/sqrt(lamb_w)), 0.76)
    return fill_template(templates.eq_F3_2a, locals(), k_c, **display_options)

def sec_F3_2(shape, M_p: Moment, **display_options) -> Moment | tuple[str, Moment]:
    """Calculate the major axis nominal moment of an I shape with a compact web
    based on the limit of compression flange local buckling according to
    AISC 360-22 Section F3.2.

    Parameters
    ==========

    shape : aisc.WideFlange
        Shape to calculate the compression flange local buckling moment of

    M_p : Moment
        Major axis nominal plastic moment capacity of the section"""
    options = copy.copy(display_options)
    options.update({"display": False, "return_string": True})

    lamb_f = shape.lamb_f
    lamb_pf_str, lamb_pf = chapter_B.table_B4_1b_10_lamb_p(
        shape.material.E, shape.material.F_y, **options)
    lamb_rf_str, lamb_rf = chapter_B.table_B4_1b_10_lamb_r(
        shape.material.E, shape.material.F_y, **options)
    if lamb_f < lamb_rf:
        M_flb_str, M_flb = eq_F3_1(M_p, shape.material.F_y, shape.S_x,
            shape.lamb_f, lamb_pf, lamb_rf, **options)
        template = templates.sec_F3_2_noncompact
    else:
        k_c_str, k_c = eq_F3_2a(shape.lamb_w, **options)
        M_flb_str, M_flb = eq_F3_2(shape.material.E, k_c, shape.S_x,
            shape.lamb_f, **options)
        template = templates.sec_F3_2_slender
    return fill_template(template, locals(), M_flb, **display_options)

def sec_F3(shape, L_b: Length, C_b: float, **display_options):
    """Calculate the major axis nominal moment capacity of a compact I shape
    according to AISC 360-22 Section F3.

    Parameters
    ==========

    shape : aisc.WideFlange
        Shape to calculate the nominal moment capaciy of

    L_b : Length
        Compression flange unbraced length

    C_b : float
        Lateral-torsional buckling modification factor"""
    options = copy.copy(display_options)
    options.update({"display": False, "return_string": True})

    M_p_str, M_p = sec_F2_1(shape, **options)
    M_ltb_str, M_ltb = sec_F2_2(shape, L_b, M_p, C_b, **options)
    M_flb_str, M_flb = sec_F3_2(shape, M_p, **options)
    M_n = min(M_ltb, M_flb)
    return fill_template(templates.sec_F3, locals(), M_n, **display_options)
