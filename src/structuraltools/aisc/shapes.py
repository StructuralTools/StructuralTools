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
from math import pi
from typing import Optional

from structuraltools import materials, utils
from structuraltools.aisc import chapter_B, chapter_F
from structuraltools.aisc import _shapes_templates as templates
from structuraltools.unit import unit, Force, Length, Moment
from structuraltools.utils import sqrt


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
        self.material = material.name
        properties.update(vars(material))
        for attribute, value in properties.items():
            setattr(self, attribute, value)


class Angle(Shape):
    """Class to represent angle shapes"""
    database = utils.read_data_table(resources.joinpath("AISC_Angle.csv"))
    default_material = materials.Steel("A572Gr50")


class Channel(Shape):
    """Class to represent channel shapes"""
    database = utils.read_data_table(resources.joinpath("AISC_Channel.csv"))
    default_material = materials.Steel("A992")


class Plate:
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

        b : pint length quantity
            Plate width. This is specified at instance initialization to
            make this act more like other shapes.

        t : pint length quantity
            Plate thickness

        material : structuraltools.materials.Steel instance
            Material to use for the member"""
        self.d = d.to("inch")
        self.t = t.to("inch")
        if not material:
            self.material = self.default_material
        else:
            self.material = material
        self.unpack_for_templates = True

        self.A = (self.d*self.t).to("inch**2")
        self.W = (self.A*self.material.w_s).to("plf")
        self.S_x = (self.t*self.d**2/6).to("inch**3")
        self.Z_x = (self.t*self.d**2/4).to("inch**3")
        self.I_x = (self.t*self.d**3/12).to("inch**4")
        self.r_x = (sqrt(self.I_x/self.A)).to("inch")
        self.S_y = (self.d*self.t**2/6).to("inch**3")
        self.Z_y = (self.d*self.t**2/4).to("inch**3")
        self.I_y = (self.d*self.t**3/12).to("inch**4")
        self.r_y = (sqrt(self.I_y/self.A)).to("inch")

    def compression_capacity(
        self,
        L_x: Length,
        L_y: Length,
        **markdown_options) -> tuple[float, Force] | tuple[str, float, Force]:
        """Calculate the axial compression capacity according to
        AISC 360-22 Section E3

        Parameters
        ==========

        L_x : Length
            Critical length with respect to r_x

        L_x : Length
            Critical length with respect to r_y"""
        phi_c = 0.9

        F_e_x = (self.material.E*pi**2)/((L_x/self.r_x)**2)
        if self.material.F_y/F_e_x <= 2.25:
            F_n_x = (0.658**(self.material.F_y/F_e_x))*self.material.F_y
        else:
            F_n_x = 0.877*F_e_x

        F_e_y = (self.material.E*pi**2)/((L_y/self.r_y)**2)
        if self.material.F_y/F_e_y <= 2.25:
            F_n_y = (0.658**(self.material.F_y/F_e_y))*self.material.F_y
        else:
            F_n_y = 0.877*F_e_y

        P_n = min(F_n_x, F_n_y)*self.A
        return phi_c, P_n


    def moment_capacity(
        self,
        L_b: Length = 0*unit.inch,
        C_b: int = 1,
        **markdown_options) -> tuple[float, Moment] | tuple[str, float, Moment]:
        """Calculate the major axis moment capacity according to
        AISC 360-22 Section F11

        Parameters
        ==========

        L_b : pint length quantity, optional
            Unbraced length for lateral-torsional buckling

        C_b : float
            Lateral-torsional buckling modification factor. Defaults to 1."""
        phi_b = 0.9
        material = self.material

        short = 0.08*self.material.E/self.material.F_y
        long = 1.9*self.material.E/self.material.F_y
        length = L_b*self.d/self.t**2
        M_p = min(self.material.F_y*self.Z_x, 1.5*self.material.F_y*self.S_x).to("kipft")

        if length <= short:
            M_n = M_p
            M_n_template = plate_templates.moment_plastic
        elif length <= long:
            M_n = min(C_b*(1.52-0.274*(L_b*self.d*self.material.F_y)/
                (self.t**2*self.material.E))*self.material.F_y*self.S_x, M_p).to("kipft")
            M_n_template = plate_templates.moment_ltb_short
        else:
            M_n = min((1.9*self.material.E*C_b*self.t**2*self.S_x)/(L_b*self.d), M_p).to("kipft")
            M_n_template = plate_templates.moment_ltb_long
        return utils.fill_templates(plate_templates.moment_capacity, locals(), phi_b, M_n)

    def moment_capacity_minor(
        self,
        L_b: Length = 0*unit.inch,
        C_b: int = 1,
        **markdown_options) -> tuple[float, Moment] | tuple[str, float, Moment]:
        """Calculate the minor axis moment capacity according to
        AISC 360-22 Section F11

        Parameters
        ==========

        L_b : pint length quantity, optional
            Unbraced length for lateral-torsional buckling

        C_b : float
            Lateral-torsional buckling modification factor. Defaults to 1."""
        phi_b = 0.9
        material = self.material

        short = 0.08*self.material.E/self.material.F_y
        long = 1.9*self.material.E/self.material.F_y
        length = L_b*self.t/self.d**2
        M_p = min(self.material.F_y*self.Z_y, 1.5*self.material.F_y*self.S_y).to("kipft")

        if length <= short:
            M_n = M_p
            M_n_template = plate_templates.moment_minor_plastic
        elif length <= long:
            M_n = min(C_b*(1.52-0.274*(L_b*self.t*self.material.F_y)/
                (self.d**2*self.material.E))*self.material.F_y*self.S_y, M_p).to("kipft")
            M_n_template = plate_templates.moment_minor_ltb_short
        else:
            M_n = min((1.9*self.material.E*C_b*self.d**2*self.S_y)/(L_b*self.t), M_p).to("kipft")
            M_n_template = plate_templates.moment_minor_ltb_long
        return utils.fill_templates(plate_templates.moment_capacity_minor, locals(), phi_b, M_n)


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
        self.material = material.name
        properties.update(vars(material))
        for attribute, value in properties.items():
            setattr(self, attribute, value)


class WideFlange(Shape):
    """Class to represent wide-flange shapes"""
    database = utils.read_data_table(resources.joinpath("AISC_WideFlange.csv"))
    default_material = materials.Steel("A992")

    def moment_capacity(self, L_b: Length = 0*unit.ft, C_b: float = 1, **display_options
                        ) -> tuple[float, Moment] | tuple[str, float, Moment]:
        """Calculate the major axis nominal moment capacity of an I shape with
        a compact web according to AISC 360-22 Sections F2 and F3.

        Parameters
        ==========

        L_b : Length
            Compression flange unbraced length

        C_b : float
            Lateral-torsional buckling modification factor"""
        options = copy.copy(display_options)
        options.update({"display": False, "return_string": True})

        phi_b = 0.9

        if self.lamb_w >= chapter_B.table_B4_1b_15_lamb_p(self.E, self.F_y):
            raise ValueError("Only sections with compact webs are supported")
        elif self.lamb_f >= chapter_B.table_B4_1b_10_lamb_p(self.E, self.F_y):
            M_n_str, M_n = chapter_F.sec_F3(self, L_b, C_b, **options)
        else:
            M_n_str, M_n = chapter_F.sec_F2(self, L_b, C_b, **options)
        return utils.fill_template(templates.WideFlange_moment_capacity,
                                   locals(), phi_b, M_n, **display_options)
