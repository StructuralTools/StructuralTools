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

from numpy import pi, sqrt

from structuraltools.aisc import chapter_B
from structuraltools.unit import (Length, Moment, MomentOfInertia,
    SectionModulus, Stress, TorsionalConstant, WarpingConstant)
from structuraltools.utils import fill_template, Result


resources = importlib.resources.files("structuraltools.aisc.resources")
with open(resources.joinpath("chapter_F_templates_processed.json")) as file:
    templates = json.load(file)


def eq_F2_1(F_y: Stress, Z_x: SectionModulus, **string_options) -> Result[Moment]:
    """AISC 360-22 Equation F2-1

    Parameters
    ==========

    F_y : Stress
        Steel yield stress

    Z_x : SectionModulus
        Major axis plastic section modulus"""
    M_p = (F_y*Z_x).to("kipft")
    return fill_template(M_p, templates["eq_F2_1"], locals(), **string_options)

def eq_F2_2(C_b: float, M_p: Moment, F_y: Stress, S_x: SectionModulus,
        L_b: Length, L_p: Length, L_r: Length, **string_options) -> Result[Moment]:
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
    return fill_template(M_ltb, templates["eq_F2_2"], locals(), **string_options)

def eq_F2_3(F_cr: Stress, S_x: SectionModulus, **string_options) -> Result[Moment]:
    """AISC 360-22 Equation F2-3

    Parameters
    ==========

    F_cr : Stress
        Critical stress from AISC 360-22 Equation F2-4

    S_x : SectionModulus
        Major axis elastic section modulus"""
    M_ltb = (F_cr*S_x).to("kipft")
    return fill_template(M_ltb, templates["eq_F2_3"], locals(), **string_options)

def eq_F2_4(C_b: float, E: Stress, L_b: Length, r_ts: Length, J: TorsionalConstant,
        c: float, S_x: SectionModulus, h_o: Length, **string_options) -> Result[Stress]:
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
    return fill_template(F_cr, templates["eq_F2_4"], locals(), **string_options)

def eq_F2_5(r_y: Length, E: Stress, F_y: Stress, **string_options) -> Result[Length]:
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
    return fill_template(L_p, templates["eq_F2_5"], locals(), **string_options)

def eq_F2_6(r_ts: Length, E: Stress, F_y: Stress, J: TorsionalConstant,
        c: float, S_x: SectionModulus, h_o: Length, **string_options) -> Result[Length]:
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
    return fill_template(L_r, templates["eq_F2_6"], locals(), **string_options)

def eq_F2_8b(h_o: Length, I_y: MomentOfInertia, C_w: WarpingConstant,
             **string_options) -> Result[float]:
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
    return fill_template(c, templates["eq_F2_8b"], locals(), **string_options)

def sec_F2_1(shape, **string_options) -> Result[Moment]:
    """Calculate the major axis plastic moment capacity of an I shape with a
    compact web according to AISC 360-22 Section F2.1

    Parameters
    ==========

    shape : aisc.WideFlange
        Shape to calculate the plastic moment capacity of"""
    M_p_str, M_p = eq_F2_1(shape.F_y, shape.Z_x, **string_options)
    return fill_template(M_p, templates["sec_F2_1"], locals(), **string_options)

def sec_F2_2(shape, L_b: Length, M_p: Moment, C_b: float, **string_options) -> Result[Moment]:
    """Calculate the major axis nominal moment capacity of an I shape with a
    compact web based on the limit of lateral torsional buckling according to
    AISC 360-22 Section F2.2.

    Parameters
    ==========

    shape : aisc.WideFlange
        Shape to calculate the lateral-torsional buckling moment of

    L_b : Length
        Compression flange unbraced length

    M_p : Moment
        Major axis plastic moment capacity of the section

    C_b : float
        Lateral-torsional buckling modification factor"""
    if shape.type == "W":
        c_str, c = Result("", 1)
    else:
        c_str, c = eq_F2_8b(shape.h_o, shape.I_y, shape.C_w, **string_options)

    L_p_str, L_p = eq_F2_5(shape.r_y, shape.E, shape.F_y, **string_options)
    L_r_str, L_r = eq_F2_6(shape.r_ts, shape.E, shape.F_y, shape.J, c,
        shape.S_x, shape.h_o, **string_options)
    if L_b <= L_p:
        M_ltb = M_p
        template = templates["sec_F2_2_plastic"]
    elif L_b <= L_r:
        M_ltb_str, M_ltb = eq_F2_2(C_b, M_p, shape.F_y, shape.S_x, L_b, L_p,
            L_r, **string_options)
        template = templates["sec_F2_2_inelastic"]
    else:
        F_cr_str, F_cr = eq_F2_4(C_b, shape.E, L_b, shape.r_ts, shape.J, c,
            shape.S_x, shape.h_o, **string_options)
        M_ltb_str, M_ltb = eq_F2_3(F_cr, shape.S_x, **string_options)
        template = templates["sec_F2_2_elastic"]
    return fill_template(M_ltb, template, locals(), **string_options)

def sec_F2(shape, L_b: Length, C_b: float, **string_options) -> Result[Moment]:
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
    M_p_str, M_p = sec_F2_1(shape, **string_options)
    M_ltb_str, M_ltb = sec_F2_2(shape, L_b, M_p, C_b, **string_options)
    M_n = min(M_p, M_ltb)
    return fill_template(M_n, templates["sec_F2"], locals(), **string_options)

def eq_F3_1(M_p: Moment, F_y: Stress, S_x: SectionModulus, lamb_f: float,
        lamb_pf: float, lamb_rf: float, **string_options) -> Result[Moment]:
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
    return fill_template(M_flb, templates["eq_F3_1"], locals(), **string_options)

def eq_F3_2(E: Stress, k_c: float, S_x: SectionModulus, lamb_f: float,
        **string_options) -> Result[Moment]:
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
    return fill_template(M_flb, templates["eq_F3_2"], locals(), **string_options)

def eq_F3_2a(lamb_w: float, **string_options) -> Result[float]:
    """Calculate k_c according to AISC 360-22 Section F3.2b

    Parameters
    ==========

    lamb_w : float
        Section web slenderness for flexure"""
    k_c = min(max(0.35, 4/sqrt(lamb_w)), 0.76)
    return fill_template(k_c, templates["eq_F3_2a"], locals(), **string_options)

def sec_F3_2(shape, M_p: Moment, **string_options) -> Result[Moment]:
    """Calculate the major axis nominal moment of an I shape with a compact web
    based on the limit of compression flange local buckling according to
    AISC 360-22 Section F3.2.

    Parameters
    ==========

    shape : aisc.WideFlange
        Shape to calculate the compression flange local buckling moment of

    M_p : Moment
        Major axis nominal plastic moment capacity of the section"""
    lamb_f = shape.lamb_f
    lamb_pf_str, lamb_pf = chapter_B.table_B4_1b_10_lamb_p(shape.E, shape.F_y, **string_options)
    lamb_rf_str, lamb_rf = chapter_B.table_B4_1b_10_lamb_r(shape.E, shape.F_y, **string_options)
    if lamb_f < lamb_rf:
        M_flb_str, M_flb = eq_F3_1(M_p, shape.F_y, shape.S_x, shape.lamb_f,
            lamb_pf, lamb_rf, **string_options)
        template = templates["sec_F3_2_noncompact"]
    else:
        k_c_str, k_c = eq_F3_2a(shape.lamb_w, **string_options)
        M_flb_str, M_flb = eq_F3_2(shape.E, k_c, shape.S_x, shape.lamb_f, **string_options)
        template = templates["sec_F3_2_slender"]
    return fill_template(M_flb, template, locals(), **string_options)

def sec_F3(shape, L_b: Length, C_b: float, **string_options) -> Result[Moment]:
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
    M_p_str, M_p = sec_F2_1(shape, **string_options)
    M_ltb_str, M_ltb = sec_F2_2(shape, L_b, M_p, C_b, **string_options)
    M_flb_str, M_flb = sec_F3_2(shape, M_p, **string_options)
    M_n = min(M_ltb, M_flb)
    return fill_template(M_n, templates["sec_F3"], locals(), **string_options)

def eq_F11_1(F_y: Stress, Z_x: SectionModulus, S_x: SectionModulus,
        **string_options) -> Result[Moment]:
    """AISC 360-22 Equation F11-1

    Parameters
    ==========

    F_y : Stress
        Steel yield stress

    Z_x : SectionModulus
        Major axis plastic section modulus

    S : SectionModulus
        Major axis elastic section modulus"""
    M_p = min(F_y*Z_x, 1.5*F_y*S_x).to("kipft")
    return fill_template(M_p, templates["eq_F11_1"], locals(), **string_options)

def eq_F11_3(C_b: float, L_b: Length, d: Length, t: Length, F_y: Stress,
        E: Stress, S_x: SectionModulus, **string_options) -> Result[Moment]:
    """AISC 360-22 Equation F11-3

    Parameters
    ==========

    C_b : float
        Lateral-torsional buckling modification factor

    L_b : Length
        Compression side unbraced length

    d : Length
        Section depth relative to the bending axis

    t : Length
        Section width relative to the bending axis

    F_y : Stress
        Steel yield stress

    E : Stress
        Steel elastic modulus

    S_x : Section modulus
        Major axis elastic section modulus"""
    M_ltb = (C_b*(1.52-0.274*(L_b*d*F_y)/(E*t**2))*F_y*S_x).to("kipft")
    return fill_template(M_ltb, templates["eq_F11_3"], locals(), **string_options)

def eq_F11_4(F_cr: Stress, S_x: SectionModulus, **string_options) -> Result[Moment]:
    """AISC 360-22 Equation F11-4

    Parameters
    ==========

    F_cr : Stress
        Critical stress for elastic lateral-torsional buckling

    S_x : SectionModulus
        Major axis elastic section modulus"""
    M_ltb = (F_cr*S_x).to("kipft")
    return fill_template(M_ltb, templates["eq_F11_4"], locals(), **string_options)

def eq_F11_5(E: Stress, C_b: float, L_b: Length, d: Length, t: Length,
        **string_options) -> Result[Stress]:
    """AISC 360-22 Equation F11-5

    Parameters
    ==========

    E : Stress
        Steel elastic modulus

    C_b : float
        Lateral-torsional buckling modification factor

    L_b : Length
        Compression side unbraced length

    d : Length
        Section depth

    t : Length
        Section width"""
    F_cr = (1.9*E*C_b)/(L_b*d/t**2)
    return fill_template(F_cr, templates["eq_F11_5"], locals(), **string_options)

def sec_F11_1(shape, **string_options) -> Result[Moment]:
    """Calculate the plastic moment capacity of a rectangular bar according to
    AISC 360-22 Section F11.1

    Parameters
    ==========

    shape : aisc.Plate
        Shape to calculate the plastic moment capacity of"""
    M_p_str, M_p = eq_F11_1(shape.F_y, shape.Z_x, shape.S_x, **string_options)
    return fill_template(M_p, templates["sec_F11_1_rect"], locals(), **string_options)

def sec_F11_2(shape, L_b: Length, M_p: Moment, C_b: float, **string_options) -> Result[Moment]:
    """Calculate the major axis nominal moment capacity of a rectangular bar
    base on the limit of lateral-torsional buckling according to
    AISC 360-22 Section F11.2.

    Parameters
    ==========

    shape : aisc.Plate
        Shape to calculate the lateral-torsional buckling moment of

    L_b : Length
        Copression side unbraced length

    M_p : Moment
        Major axis plastic moment capacity of the section

    C_b : float
        Lateral-torsional buckling modification factor"""
    E = shape.E
    F_y = shape.F_y
    d = shape.d
    t = shape.t

    lamb_p = 0.08*E/F_y
    lamb_r = 1.9*E/F_y
    lamb = L_b*d/t**2
    if lamb <= lamb_p:
        M_ltb = M_p
        template = templates["sec_F11_2_plastic"]
    elif lamb <= lamb_r:
        M_ltb_str, M_ltb = eq_F11_3(C_b, L_b, d, t, F_y, E, shape.S_x, **string_options)
        template = templates["sec_F11_2_inelastic"]
    else:
        F_cr_str, F_cr = eq_F11_5(E, C_b, L_b, d, t, **string_options)
        M_ltb_str, M_ltb = eq_F11_4(F_cr, shape.S_x, **string_options)
        template = templates["sec_F11_2_elastic"]
    return fill_template(M_ltb, template, locals(), **string_options)

def sec_F11(shape, L_b: Length, C_b: float, **string_options) -> Result[Moment]:
    """Calculate the moment capacity of a rectangular bar according to
    AISC 360-22 Section F11

    Parameters
    ==========

    shape : aisc.Plate
        Shape to calculate the nominal moment capacity of

    L_b : Length
        Compression side unbraced length

    C_b : float
        Lateral-torsional buckling modification factor"""
    M_p_str, M_p = sec_F11_1(shape, **string_options)
    M_ltb_str, M_ltb = sec_F11_2(shape, L_b, M_p, C_b, **string_options)
    M_n = min(M_p, M_ltb)
    return fill_template(M_n, templates["sec_F11"], locals(), **string_options)

