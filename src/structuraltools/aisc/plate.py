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

from structuraltools import materials, unit, utils
from structuraltools import Force, Length, Moment
from structuraltools.aisc import _plate_markdown as templates

class Plate:
    """Class for calculating steel plate strength. For consistency with the
    other shapes the x-axis intersects the width of the plate (b) and
    represents the strong axis for bending."""
    def __init__(
        self,
        d: Length,
        t: Length,
        material: materials.Steel):
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
        self.material = material
        self.unpack_for_templates = True

        self.A = (self.d*self.t).to("inch**2")
        self.W = (self.A*material.w_s).to("plf")
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
        material = self.material

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
            M_n_template = templates.moment_plastic
        elif length <= long:
            M_n = min(C_b*(1.52-0.274*(L_b*self.d*self.material.F_y)/
                (self.t**2*self.material.E))*self.material.F_y*self.S_x, M_p).to("kipft")
            M_n_template = templates.moment_ltb_short
        else:
            M_n = min((1.9*self.material.E*C_b*self.t**2*self.S_x)/(L_b*self.d), M_p).to("kipft")
            M_n_template = templates.moment_ltb_long
        return utils.fill_templates(templates.moment_capacity, locals(), phi_b, M_n)

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
            M_n_template = templates.moment_minor_plastic
        elif length <= long:
            M_n = min(C_b*(1.52-0.274*(L_b*self.t*self.material.F_y)/
                (self.d**2*self.material.E))*self.material.F_y*self.S_y, M_p).to("kipft")
            M_n_template = templates.moment_minor_ltb_short
        else:
            M_n = min((1.9*self.material.E*C_b*self.d**2*self.S_y)/(L_b*self.t), M_p).to("kipft")
            M_n_template = templates.moment_minor_ltb_long
        return utils.fill_templates(templates.moment_capacity_minor, locals(), phi_b, M_n)
