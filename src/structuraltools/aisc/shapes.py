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
from typing import Optional

from numpy import sqrt

from structuraltools.aisc import chapter_B, chapter_E, chapter_F
from structuraltools.unit import unit, Force, Length, Moment
from structuraltools.utils import fill_template, read_data_table, Result


resources = importlib.resources.files("structuraltools.aisc.resources")
materials = read_data_table(resources.joinpath("steel_materials.csv"))
with open(resources.joinpath("shapes_templates_processed.json")) as file:
    templates = json.load(file)


class Shape:
    """Base class for AISC steel shapes"""
    def __init__(self, size: str, material: Optional[str] = None):
        """Create an instance from the specified database

        Parameters
        ==========

        size : str
            Name to use when looking up the shape dimensions

        material : str
            Name to use when looking up steel properties"""
        self.size = size
        properties = self.database.loc[size, :].to_dict()
        if not material:
            material = self.default_material
        self.material = material
        material = materials.loc[material, :].to_dict()
        properties.update(material)
        for attribute, value in properties.items():
            setattr(self, attribute, value)


class Angle(Shape):
    """Class to represent angle shapes"""
    database = read_data_table(resources.joinpath("Angle.csv"))
    default_material = "A572Gr50"


class Channel(Shape):
    """Class to represent channel shapes"""
    database = read_data_table(resources.joinpath("Channel.csv"))
    default_material = "A992"


class Plate(Shape):
    """Class for calculating steel plate strength. For consistency with the
    other shapes the x-axis intersects the width of the plate (b) and
    represents the strong axis for bending."""
    default_material = "A572Gr50"

    def __init__(self, d: Length, t: Length, material: str = "A572Gr50"):
        """Create a new steel plate. Major axis bending has d perpendicular to
        the bending axis.

        Parameters
        ==========

        d : pint length quantity
            Plate width

        t : pint length quantity
            Plate thickness

        material : str
            Material to use for the member"""
        self.size = f"Plate {d}X{t}"
        self.d = d.to("inch")
        self.t = t.to("inch")
        self.A = (self.d*self.t).to("inch**2")
        self.S_x = (self.t*self.d**2/6).to("inch**3")
        self.I_x = (self.t*self.d**3/12).to("inch**4")
        self.r_x = (sqrt(self.I_x/self.A)).to("inch")
        self.Z_x = (self.t*self.d**2/4).to("inch**3")
        self.S_y = (self.d*self.t**2/6).to("inch**3")
        self.I_y = (self.d*self.t**3/12).to("inch**4")
        self.r_y = (sqrt(self.I_y/self.A)).to("inch")
        self.Z_y = (self.d*self.t**2/4).to("inch**3")

        self.material = material
        material = materials.loc[material, :].to_dict()
        for attribute, value in material.items():
            setattr(self, attribute, value)

    def compression_capacity(self, L_c: Length, axis: str = "y",
            **string_options) -> Result[Force]:
        """Calculate the nominal compression capacity of a plate according to
        AISC 360-22 Section E3.

        Parameters
        ==========

        L_c : Length
            Effective length for compression

        axis : str
            Member local axis to calculate the compression capacity for"""
        phi_c = 0.9

        P_n_str, P_n = chapter_E.sec_E3(self, L_c, axis, **string_options)
        template = templates["Plate_compression_capacity"]
        return fill_template((phi_c, P_n), template, locals(), **string_options)

    def moment_capacity(self, L_b: Length = 0*unit.ft, axis: str = "x",
            C_b: float = 1, **string_options) -> Result[Moment]:
        """Calculate the nominal moment capacity of a plate according to
        AISC 360-22 Section F11.

        Parameters
        ==========

        L_b : Length
            Compression side unbraced length

        axis : str
            Member local axis to calculate the moment capacity about

        C_b : float
            Lateral-torsional buckling modification factor"""
        phi_b = 0.9

        if axis == "x":
            M_n_str, M_n = chapter_F.sec_F11(self, L_b, C_b, **string_options)
            template = templates["Plate_moment_capacity_x"]
        elif axis == "y":
            F_y = self.F_y
            Z_y = self.Z_y
            S_y = self.S_y
            M_n = min(F_y*Z_y, 1.5*F_y*S_y).to("kipft")
            template = templates["Plate_moment_capacity_y"]
        else:
            raise ValueError(f"Unsupported axis: {axis}")
        return fill_template((phi_b, M_n), template, locals(), **string_options)


class RectHSS(Shape):
    """Class to represent rectangular HSS shapes"""
    database = read_data_table(resources.joinpath("RectHSS.csv"))
    default_material = "A500GrC"


class RoundHSS(Shape):
    """Class to represent round HSS shapes"""
    database = read_data_table(resources.joinpath("RoundHSS.csv"))
    RoundHSS_default_material = "A500GrC"
    Pipe_default_material = "A53GrB"

    def __init__(self, size: str, material: Optional[str] = None):
        """Create an instance from the specified database

        Parameters
        ==========

        size : str
            Name to use when looking up the shape dimensions

        material : materials.Steel
            Material to use for the member"""
        self.size = size
        properties = self.database.loc[size, :].to_dict()
        if not material:
            if properties["type"] == "RoundHSS":
                material = self.RoundHSS_default_material
            else:
                material = self.Pipe_default_material
        self.material = material
        material = materials.loc[material, :].to_dict()
        properties.update(material)
        for attribute, value in properties.items():
            setattr(self, attribute, value)


class WideFlange(Shape):
    """Class to represent wide-flange shapes"""
    database = read_data_table(resources.joinpath("WideFlange.csv"))
    default_material = "A992"

    def moment_capacity(self, L_b: Length = 0*unit.ft, axis: str = "x",
            C_b: float = 1, **string_options) -> Result[Moment]:
        """Calculate the nominal moment capacity of an I shape with a compact
        web according to AISC 360-22 Sections F2 and F3.

        Parameters
        ==========

        L_b : Length
            Compression flange unbraced length

        axis : str
            Member local axis to calculate the moment capacity about

        C_b : float
            Lateral-torsional buckling modification factor"""
        phi_b = 0.9
        _, lamb_pw = chapter_B.table_B4_1b_15_lamb_p(self.E, self.F_y, return_string=False)
        _, lamb_pf = chapter_B.table_B4_1b_10_lamb_p(self.E, self.F_y, return_string=False)

        if self.lamb_w >= lamb_pw:
            raise ValueError("Only sections with compact webs are supported")
        elif self.lamb_f >= lamb_pf:
            M_n_str, M_n = chapter_F.sec_F3(self, L_b, C_b, **string_options)
        else:
            M_n_str, M_n = chapter_F.sec_F2(self, L_b, C_b, **string_options)
        template = templates["WideFlange_moment_capacity_x"]
        return fill_template((phi_b, M_n), template, locals(), **string_options)
