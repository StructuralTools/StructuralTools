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
from typing import Optional

from structuraltools import materials, sections, utils
from structuraltools.aisc import chapter_B, chapter_F
from structuraltools.aisc import _shapes_templates as templates
from structuraltools.template import Result
from structuraltools.unit import unit, Length, Moment
from structuraltools.utils import set_sub_display


resources = importlib.resources.files("structuraltools.resources")


class Shape:
    """Base class for AISC steel shapes"""
    def __init__(self, size: str, material: Optional[materials.Steel] = None):
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
            material = self.default_material
        properties.update(vars(material))
        for attribute, value in properties.items():
            setattr(self, attribute, value)
        delattr(self, "name")


class Angle(Shape):
    """Class to represent angle shapes"""
    database = utils.read_data_table(resources.joinpath("AISC_Angle.csv"))
    default_material = materials.Steel("A572Gr50")


class Channel(Shape):
    """Class to represent channel shapes"""
    database = utils.read_data_table(resources.joinpath("AISC_Channel.csv"))
    default_material = materials.Steel("A992")


class Plate(sections.Rectangle):
    """Class for calculating steel plate strength. For consistency with the
    other shapes the x-axis intersects the width of the plate (b) and
    represents the strong axis for bending."""
    default_material = materials.Steel("A36")

    def __init__(
        self,
        d: Length,
        t: Length,
        material: Optional[materials.Steel] = None):
        """Create a new steel plate.

        Parameters
        ==========

        d : pint length quantity
            Plate width. This is specified at instance initialization to
            make this act more like other shapes.

        t : pint length quantity
            Plate thickness

        material : structuraltools.materials.Steel instance
            Material to use for the member"""
        super().__init__(d, t)
        self.t = self.b
        delattr(self, "b")

        self.Z_x = (self.t*self.d**2/4).to("inch**3")
        self.Z_y = (self.d*self.t**2/4).to("inch**3")

        if not material:
            material = self.default_material
        material = vars(material)
        for attribute, value in material.items():
            setattr(self, attribute, value)
        delattr(self, "name")

    def moment_capacity(self, axis: str = "x", L_b: Length = 0*unit.ft,
            C_b: float = 1, **display_options) -> Result[Moment]:
        """Calculate the nominal moment capacity of a plate according to
        AISC 360-22 Section F11.

        Parameters
        ==========

        axis : str
            Member local axis to calculate the moment capacity about

        L_b : Length
            Compression side unbraced length

        C_b : float
            Lateral-torsional buckling modification factor"""
        sub_options = set_sub_display(display_options)

        phi_b = 0.9

        if axis == "x":
            M_n = chapter_F.sec_F11(self, L_b, C_b, **sub_options)
            template = templates.Plate_moment_capacity_x
        elif axis == "y":
            F_y = self.F_y
            Z_y = self.Z_y
            S_y = self.S_y
            M_n = min(F_y*Z_y, 1.5*F_y*S_y).to("kipft")
            template = templates.Plate_moment_capacity_y
        else:
            raise ValueError(f"Unsupported axis: {axis}")
        return template.fill(locals(), phi_b, M_n, **display_options)


class RectHSS(Shape):
    """Class to represent rectangular HSS shapes"""
    database = utils.read_data_table(resources.joinpath("AISC_RectHSS.csv"))
    default_material = materials.Steel("A500GrC")


class RoundHSS(Shape):
    """Class to represent round HSS shapes"""
    database = utils.read_data_table(resources.joinpath("AISC_RoundHSS.csv"))
    RoundHSS_default_material = materials.Steel("A500GrC")
    Pipe_default_material = materials.Steel("A53GrB")

    def __init__(self, size: str, material: Optional[materials.Steel] = None):
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
        properties.update(vars(material))
        for attribute, value in properties.items():
            setattr(self, attribute, value)
        delattr(self, "name")


class WideFlange(Shape):
    """Class to represent wide-flange shapes"""
    database = utils.read_data_table(resources.joinpath("AISC_WideFlange.csv"))
    default_material = materials.Steel("A992")

    def moment_capacity(self, axis: str = "x", L_b: Length = 0*unit.ft,
            C_b: float = 1, **display_options) -> Result[Moment]:
        """Calculate the nominal moment capacity of an I shape with a compact
        web according to AISC 360-22 Sections F2 and F3.

        Parameters
        ==========

        axis : str
            Member local axis to calculate the moment capacity about

        L_b : Length
            Compression flange unbraced length

        C_b : float
            Lateral-torsional buckling modification factor"""
        sub_options = set_sub_display(display_options)

        phi_b = 0.9

        if self.lamb_w >= chapter_B.table_B4_1b_15_lamb_p(self.E, self.F_y):
            raise ValueError("Only sections with compact webs are supported")
        elif self.lamb_f >= chapter_B.table_B4_1b_10_lamb_p(self.E, self.F_y):
            M_n = chapter_F.sec_F3(self, L_b, C_b, **sub_options)
        else:
            M_n = chapter_F.sec_F2(self, L_b, C_b, **sub_options)
        return templates.WideFlange_moment_capacity.fill(locals(), phi_b, M_n, **display_options)
