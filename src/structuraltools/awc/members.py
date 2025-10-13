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

from numpy import ceil, sqrt

from structuraltools.awc import chapter_2, chapter_3, chapter_4
from structuraltools.unit import Length, Moment
from structuraltools.utils import (fill_template, pivot_dict_table,
    read_data_table, Result, round_to)


resources = importlib.resources.files("structuraltools.awc.resources")
with open(resources.joinpath("members_templates_processed.json")) as file:
    templates = json.load(file)


class SawnLumber:
    """Class for calculating solid sawn lumber strength"""
    materials = read_data_table(resources.joinpath("SawnLumber.csv"))

    def __init__(
            self,
            species: str,
            grade: str,
            b: Length,
            d: Length,
            wet_service: bool = False,
            temperature: float = 100,
            incising: bool = False):
        """Create a new sawn lumber member.

        Parameters
        ==========

        species : str
            Member species. Most species names are be the same as in the
            2024 NDS Supplement with only the first letter in each word
            capitalized, but Douglas Fir is notably different with the
            following names: "Douglas Fir", "Douglas Fir (North)", and
            "Douglas Fir (South)"

        grade : str
            Member grade. One of "Select", "1", "2", "3", "Stud",
            "Construction", "Standard", and "Utility". A "+" can be appended to
            the grade designation to indicate "Dense" or "& Btr" and a "-" can
            be appended to indicate "Non-Dense".

        b : Length
            Member thickness

        d : Length
            Member width

        wet_service : bool
            Boolean indicating if the wet service factor should be applied

        temperature : float
            Expected service temperature for applying the temperature factor

        incising : bool
            Boolean indicating if the incising factor should be applied"""
        if d < b:
            raise ValueError(
                f"Specified thickness ({b:~L}) is greater than the specified width ({d:~L})")


        # Calculate section properties
        self.c = 0.8  # Adjustment used when calculating the column stability factor
        self.d = abs(d.to("inch"))
        self.b = abs(b.to("inch"))
        self.d_nom = int(ceil(self.d.magnitude))
        self.b_nom = int(ceil(self.b.magnitude))
        self.A = (self.d*self.b).to("inch**2")
        self.S_x = (self.b*self.d**2/6).to("inch**3")
        self.I_x = (self.b*self.d**3/12).to("inch**4")
        self.r_x = (sqrt(self.I_x/self.A)).to("inch")
        self.S_y = (self.d*self.b**2/6).to("inch**3")
        self.I_y = (self.d*self.b**3/12).to("inch**4")
        self.r_y = (sqrt(self.I_y/self.A)).to("inch")


        # Look up wood properties
        self.species = species
        self.grade = "3" if grade == "Stud" and self.d_nom >= 8 else str(grade)
        self.classification = chapter_4.sec_4_1_3(self.d_nom, self.b_nom)

        try:
            if "Southern Pine" in self.species and self.classification == "Dimension":
                d_nom = max(round_to(self.d_nom, 2), 4)
                index = f"{self.classification}|{self.species}|{self.grade}|{d_nom}"
            else:
                index = f"{self.classification}|{self.species}|{self.grade}"
            material = self.materials.loc[index, :].to_dict()
            for attribute, value in material.items():
                setattr(self, attribute, value)
        except KeyError:
            raise ValueError(f"Unsupported classification/species/grade/width: {index}")


        # Modification factors
        C_F = chapter_4.sec_4_3_6(self.classification, self.species, self.grade,
            self.b_nom, self.d_nom)
        C_M = chapter_4.sec_4_3_3(wet_service, self.F_b, self.F_c, C_F,
            self.classification, self.species)
        C_t = chapter_2.sec_2_3_3(temperature, wet_service)
        C_fu = chapter_4.sec_4_3_7(self.classification, self.grade,
            self.b_nom, self.d_nom)
        C_i = chapter_4.sec_4_3_8(incising)
        self.modifiers = pivot_dict_table(
            {"C_F": C_F, "C_M": C_M, "C_t": C_t, "C_fu": C_fu, "C_i": C_i})

    def moment_capacity(self, lamb: float, C_r: float = 1, C_L: float = 1,
            axis: str = "x", **string_options) -> Result[Moment]:
        """Calculate the nominal moment capacity

        Parameters
        ==========

        lamb : float
            Time effect factor

        C_r : float
            Repetitive member factor

        C_L : float
            Beam stability factor

        axis : str
            Member local axis to calculate the moment capacity about"""
        mods = self.modifiers["F_b"]
        C_fu = 1 if axis == "x" else mods["C_fu"]
        F_prime_b_str, F_prime_b = chapter_4.table_4_3_1_b(self.F_b,
            mods["C_M"], mods["C_t"], C_L, mods["C_F"], C_fu, mods["C_i"], C_r,
            lamb, **string_options)
        phiM_n_str, phiM_n = chapter_3.eq_3_3_1(F_prime_b, self.S_x, axis, **string_options)
        template = templates["SawnLumber_moment_capacity"]
        return fill_template(phiM_n, template, locals(), **string_options)
