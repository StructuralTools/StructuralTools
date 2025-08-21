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

from numpy import ceil, sqrt

from structuraltools.awc import chapter_4
from structuraltools.unit import Length
from structuraltools.utils import read_data_table, Result, round_to


resources = importlib.resources.files("structuraltools.awc.resources")


class SawnLumber:
    """Class for calculating solid sawn lumber strength"""
    materials = read_data_table(resources.joinpath("SawnLumber.csv"))

    def __init__(
            self,
            species: str,
            grade: str,
            t: Length,
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

        wet_service : bool
            Boolean indicating if the wet service factor should be applied

        temperature : float
            Expected service temperature for applying the temperature factor

        incising : bool
            Boolean indicating if the incising factor should be applied"""
        if d < t:
            raise ValueError(
                f"Specified thickness ({t:~L}) is greater than the specified width ({d:~L})")


        # Calculate section properties
        self.d = abs(d.to("inch"))
        self.t = abs(t.to("inch"))
        self.d_nom = ceil(self.d.magnitude)
        self.t_nom = ceil(self.t.magnitude)
        self.A = (self.d*self.t).to("inch**2")
        self.S_x = (self.t*self.d**2/6).to("inch**3")
        self.I_x = (self.t*self.d**3/12).to("inch**4")
        self.r_x = (sqrt(self.I_x/self.A)).to("inch")
        self.S_y = (self.d*self.t**2/6).to("inch**3")
        self.I_y = (self.d*self.t**3/12).to("inch**4")
        self.r_y = (sqrt(self.I_y/self.A)).to("inch")


        # Look up wood properties
        self.species = species
        self.grade = "3" if grade == "Stud" and self.d_nom >= 8 else str(grade)
        self.classification = chapter_4.sec_4_1_3(self.d_nom, self.t_nom)

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
