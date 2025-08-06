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
from structuraltools.utils import read_data_table


resources = importlib.resources.files("structuraltools.awc.resources")
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


def sec_4_3_3(wet_service: bool, F_b: Stress, F_c: Stress, C_F: float,
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

    C_F : float
        Size factor for flexure

    classification : str
        One of "Dimension", "Beam", or "Post" indicating the lumber classification

    species : str
        Wood species"""
    C_M = copy(chapter_4_data["C_M"][classification])
    if classification == "Dimension" and F_b*C_f <= 1150*unit.psi:
        C_M.update({"F_b": 1})
    if classification == "Dimension" and F_c <= 750*unit.psi:
        C_M.update({"F_c": 1})
    if classification in ["Beam", "Post"] and "Southern Pine" in species:
        C_M.update({"F_c": 1, "F_c_perp": 1})
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
            C_F.update(copy(chapter_4_data["C_F"][grade][t_nom][d_nom]))
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
            C_fu = copy(chapter_4_data["C_fu"][classification][t_nom][d_nom])
        except KeyError:
            raise ValueError(f"Unsupported dimensions: {t_nom}x{d_nom}")
    else:
        grade = grade.replace("+", "").replace("-", "")
        try:
            C_fu = copy(chapter_4_data["C_fu"][classification][grade])
        except KeyError:
            raise ValueError(f"Unsupported grade ({grade}) for classification {classification}")
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
