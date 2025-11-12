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


from copy import copy
import importlib.resources
import json

from structuraltools.unit import unit, Stress
from structuraltools.utils import fill_template, Result


resources = importlib.resources.files("structuraltools.awc.resources")
with open(resources.joinpath("chapter_4_templates_processed.json")) as file:
    templates = json.load(file)
with open(resources.joinpath("chapter_4_data.json")) as file:
    chapter_4_data = json.load(file)


def sec_4_1_3(t_nom: int, d_nom: int) -> str:
    """Determine the sawn lumber classification according to
    Section 4.1.3 of the 2024 NDS. Classifying wood as decking is not supported.

    Parameters
    ==========

    t_nom : int
        Nominal thickness of the member

    d_nom : int
        Nominal width of the member"""
    if d_nom >= 5 and t_nom >= 5:
        if d_nom > t_nom+2:
            return "Beam"
        else:
            return "Post"
    else:
        return "Dimension"

def table_4_3_1_b(F_b: Stress, C_M: float, C_t: float, C_L: float, C_F: float,
        C_fu: float, C_i: float, C_r: float, lamb: float, **string_options) -> Result[Stress]:
    """Calculate the ultimate bending stress capacity according to NDS 2024 Table 4.3.1

    Parameters
    ==========

    F_b : Stress
        Reference design bending stress

    C_M : float
        Wet service factor

    C_t : float
        Temperature factor

    C_L : float
        Beam stability factor

    C_F : float
        Size factor

    C_fu : float
        Flat use factor

    C_i : float
        Incising factor

    C_r : float
        Repetitive member factor

    lamb : float
        Time effect factor"""
    K_F = 2.54
    phi = 0.85
    F_prime_b = F_b*C_M*C_t*C_L*C_F*C_fu*C_i*C_r*K_F*phi*lamb
    return fill_template(F_prime_b, templates["table_4_3_1_b"], locals(), **string_options)

def table_4_3_1_b_star(F_b: Stress, C_M: float, C_t: float, C_F: float,
        C_i: float, C_r: float, lamb: float, **string_options) -> Result[Stress]:
    """Calculate the reference design bending stress multiplied by all
    applicable adjustment factors according to NDS 2024 Table 4.3.1 except C_fu
    and C_L.

    Parameters
    ==========

    F_b : Stress
        Reference design bending stress

    C_M : float
        Wet service factor

    C_t : float
        Temperature factor

    C_F : float
        Size factor

    C_i : float
        Incising factor

    C_r : float
        Repetitive member factor

    lamb : float
        Time effect factor"""
    K_F = 2.54
    phi = 0.85
    F_star_b = F_b*C_M*C_t*C_F*C_i*C_r*K_F*phi*lamb
    return fill_template(F_star_b, templates["table_4_3_1_b_star"], locals(), **string_options)

def table_4_3_1_t(F_t: Stress, C_M: float, C_t: float, C_F: float, C_i: float,
        lamb: float, **string_options) -> Result[Stress]:
    """Calculate the ultimate tensile stress capacity according to NDS 2024 Table 4.3.1

    Parameters
    ==========

    F_t : Stress
        Reference design tensile stress

    C_M : float
        Wet service factor

    C_t : float
        Temperature factor

    C_F : float
        Size effect factor

    C_i : float
        Incising factor

    lamb : float
        Time effect factor"""
    K_F = 2.7
    phi = 0.8
    F_prime_t = F_t*C_M*C_t*C_F*C_i*K_F*phi*lamb
    return fill_template(F_prime_t, templates["table_4_3_1_t"], locals(), **string_options)

def table_4_3_1_v(F_v: Stress, C_M: float, C_t: float, C_i: float, lamb: float,
        **string_options) -> Result[Stress]:
    """Calculate the ultimate shear stress capacity according to NDS 2024 Table 4.3.1

    Parameters
    ==========

    F_v : Stress
        Reference design shear stress

    C_M : float
        Wet service factor

    C_t : float
        Temperature factor

    C_i : float
        Incising factor

    lamb : float
        Time effect factor"""
    K_F = 2.88
    phi = 0.75
    F_prime_v = F_v*C_M*C_t*C_i*K_F*phi*lamb
    return fill_template(F_prime_v, templates["table_4_3_1_v"], locals(), **string_options)

def table_4_3_1_c(F_c: Stress, C_M: float, C_t: float, C_F: float, C_i: float,
        C_P: float, lamb: float, **string_options) -> Result[Stress]:
    """Calculate the ultimate compression stress capacity according to NDS 2024 Table 4.3.1

    Parameters
    ==========

    F_c : Stress
        Reference design compression stress

    C_M : float
        Wet service factor

    C_t : float
        Temperature factor

    C_F : float
        Size factor

    C_i : float
        Incising factor

    C_P : float
        Column stability factor

    lamb : float
        Time effect factor"""
    K_F = 2.4
    phi = 0.9
    F_prime_c = F_c*C_M*C_t*C_F*C_i*C_P*K_F*phi*lamb
    return fill_template(F_prime_c, templates["table_4_3_1_c"], locals(), **string_options)

def table_4_3_1_c_star(F_c: Stress, C_M: float, C_t: float, C_F: float, C_i: float,
        lamb: float, **string_options) -> Result[Stress]:
    """Calculate the ultimate compression stress capacity according to NDS 2024 Table 4.3.1

    Parameters
    ==========

    F_c : Stress
        Reference design compression stress

    C_M : float
        Wet service factor

    C_t : float
        Temperature factor

    C_F : float
        Size factor

    C_i : float
        Incising factor

    lamb : float
        Time effect factor"""
    K_F = 2.4
    phi = 0.9
    F_c_star = F_c*C_M*C_t*C_F*C_i*K_F*phi*lamb
    return fill_template(F_c_star, templates["table_4_3_1_c_star"], locals(), **string_options)

def table_4_3_1_c_perp(F_c_perp: Stress, C_M: float, C_t: float, C_i: float,
        C_b: float, **string_options) -> Result[Stress]:
    """Calculate the ultimate compression stress capacity perpendicular to the
    grain according to NDS 2024 Table 4.3.1

    Parameters
    ==========

    F_c_perp : Stress
        Reference design compression stress perpendicular to the grain

    C_M : float
        Wet service factor

    C_t : float
        Temperature factor

    C_i : float
        Incising factor

    C_b : float
        Bearing area factor"""
    K_F = 1.67
    phi = 0.9
    F_prime_c_perp = F_c_perp*C_M*C_t*C_i*C_b*K_F*phi
    template = templates["table_4_3_1_c_perp"]
    return fill_template(F_prime_c_perp, template, locals(), **string_options)

def table_4_3_1_E(E: Stress, C_M: float, C_t: float, C_fu: float, C_i: float,
        **string_options) -> Result[Stress]:
    """Calculate the modulus of elasticity according to NDS 2024 Table 4.3.1

    Parameters
    ==========

    E : Stress
        Reference design modulus of elasticity

    C_M : float
        Wet service factor

    C_t : float
        Temperature factor

    C_fu : float
        Flat use factor

    C_i : float
        Incising factor"""
    E_prime = E*C_M*C_t*C_fu*C_i
    return fill_template(E_prime, templates["table_4_3_1_E"], locals(), **string_options)

def table_4_3_1_E_min(E_min: Stress, C_M: float, C_t: float, C_fu: float,
        C_i: float, C_T: float, **string_options) -> Result[Stress]:
    """Calculate the adjusted lower bound modulus of elasticity according to
    NDS 2024 Table 4.3.1

    Parameters
    ==========

    E_min : Stress
        Reference design lower bound modulus of elasticity

    C_M : float
        Wet service factor

    C_t : float
        Temperature factor

    C_fu : float
        Flat use factor

    C_i : float
        Incising factor

    C_T : float
        Buckling stiffness factor"""
    K_F = 1.76
    phi = 0.85
    E_prime_min = E_min*C_M*C_t*C_fu*C_i*C_T*K_F*phi
    return fill_template(E_prime_min, templates["table_4_3_1_E_min"], locals(), **string_options)

def sec_4_3_3(wet_service: bool, F_b: Stress, F_c: Stress, C_F: dict[str, float],
        classification: str, species: str) -> dict[str: float]:
    """Determine the wet service factors for sawn lumber according to
    Section 4.3.3 of the 2024 NDS

    Parameters
    ==========

    wet_service : bool
        Boolean indicating if the wet service factor should be applied

    F_b : Stress
        Unmodified flexural stress of the wood

    F_c : Stress
        Unmodified compression stress of the wood

    C_F : dict[str, float]
        Size factor dictionary

    classification : str
        One of "Dimension", "Beam", or "Post" indicating the lumber classification

    species : str
        Wood species"""
    if wet_service:
        C_M = copy(chapter_4_data["C_M"][classification])
        if classification == "Dimension" and F_b*C_F["F_b"] <= 1150*unit.psi:
            C_M.update({"F_b": 1})
        if classification == "Dimension" and F_c*C_F["F_c"] <= 750*unit.psi:
            C_M.update({"F_c": 1})
        if classification in ["Beam", "Post"] and "Southern Pine" in species:
            C_M.update({"F_c": 1, "F_c_perp": 1})
    else:
        C_M = {"F_b": 1, "F_t": 1, "F_v": 1, "F_c": 1, "F_c_perp": 1, "E": 1, "E_min": 1}
    return C_M

def sec_4_3_6(
        classification: str,
        species: str,
        grade: str,
        t_nom: int,
        d_nom: int) -> dict[str: float]:
    """Determine the size factor for sawn lumber according to
    Section 4.3.6 of the 2024 NDS

    Parameters
    ==========

    classification : str
        Sawn lumber classification from Section 4.1.3 of the 2024 NDS

    species : str
        Wood species

    grade : str
        Wood grade

    t_nom : int
        Nominal thickness of the member

    d_nom : int
        Nominal width of the member"""
    C_F = {"F_b": 1, "F_t": 1, "F_v": 1, "F_c": 1, "F_c_perp": 1, "E": 1, "E_min": 1}
    if classification in ["Beam", "Post"] and d_nom > 12:
        C_F.update({"F_b": min((12/d_nom)**(1/9), 1)})
    elif classification == "Dimension" and "Southern Pine" in species:
        if t_nom == 4 and d_nom >= 8:
            C_F.update({"F_b": C_F["F_b"]*1.1})
        if  d_nom > 12:
            C_F.update({"F_b": C_F["F_b"]*0.9})
    elif classification == "Dimension":
        grade = grade.replace("+", "").replace("-", "")
        try:
            C_F.update(copy(chapter_4_data["C_F"][grade][str(t_nom)][str(d_nom)]))
        except KeyError:
            raise ValueError(f"Unsupported grade ({grade})/width ({d_nom}) combination")
    return C_F

def sec_4_3_7(classification: str, grade: str, t_nom: int, d_nom: int) -> dict[str: float]:
    """Determine the flat use factor for sawn lumber according to
    Section 4.3.7 of the 2024 NDS

    Parameters
    ==========

    classification : str
        Sawn lumber classification from Section 4.1.3 of the 2024 NDS

    grade : str
        Wood grade

    t_nom : int
        Nominal thickness of the member

    d_nom : int
        Nominal width of the member"""
    if classification == "Dimension":
        try:
            C_fu = copy(chapter_4_data["C_fu"][classification][str(t_nom)][str(d_nom)])
        except KeyError:
            raise ValueError(f"Unsupported dimensions: {t_nom}x{d_nom}")
    elif classification == "Beam":
        grade = grade.replace("+", "").replace("-", "")
        try:
            C_fu = copy(chapter_4_data["C_fu"][classification][grade])
        except KeyError:
            raise ValueError(f"Unsupported grade ({grade}) for classification {classification}")
    else:
        C_fu = {"F_b": 1, "F_t": 1, "F_v": 1, "F_c": 1, "F_c_perp": 1, "E": 1, "E_min": 1}
    return C_fu

def sec_4_3_8(incising: bool) -> dict[str: float]:
    """Determine the incising factor for sawn lumber according to
    Section 4.3.8 of the 2024 NDS

    Parameters
    ==========

    incising : bool
        Boolean indicating if the incising factor should be used"""
    incising = str(bool(incising))
    C_i = copy(chapter_4_data["C_i"][incising])
    return C_i
