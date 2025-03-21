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

from structuraltools import materials, resources, unit, utils
from structuraltools import Length, Moment
from structuraltools.aisc import _wide_flange_markdown as templates


shape_database = utils.read_data_table(resources.joinpath("AISC_WideFlange.csv"))


class WideFlange:
    """Class for calculating section capacity based on AISC 360-22"""
    def __init__(self, size: str, material: materials.Steel):
        """Creates a new member with the specified section and material

        Parameters
        ==========

        size : str
            AISC imperial size designation of the member

        material : materials.Steel
            Material to use for the member"""
        self.size = size
        self.material = material
        dimensions = shape_database.loc[size, :].to_dict()
        for attribute, value in dimensions.items():
            setattr(self, attribute, value)

    def moment_capacity(
        self,
        L_b: Length = 0*unit.inch,
        C_b: int = 1,
        **markdown_options) -> tuple[float, Moment] | tuple[str, float, Moment]:
        """Calculate the major axis moment capacity per
        AISC 360-22 Sections F2 and F3

        Parameters
        ==========

        L_b : Length, optional
            Unbraced length for lateral-torsional buckling

        C_b : float
            Lateral-torsional buckling modification factor"""
        # Raise an exception is the flange is non-compact
        sqrt_E_F_y = sqrt(self.material.E/self.material.F_y)
        if self.lamb_w >= 3.76*sqrt_E_F_y:
            raise NotImplementedError(
                "Moment capacity for beams with non-compact webs is not implemented")

        phi_b = 0.9
        material = self.material

        # Yielding moment
        M_p = (self.material.F_y*self.Z_x).to("kipft")

        # Lateral-torsional buckling moment
        c = 1
        L_p = 1.76*self.r_y*sqrt_E_F_y
        L_r = 1.95*self.r_ts*self.material.E/(0.7*self.material.F_y)*sqrt(
            self.J*c/(self.S_x*self.h_o)+sqrt((self.J*c/(self.S_x*self.h_o))**2 \
            +6.76*(0.7*self.material.F_y/self.material.E)**2))
        if L_b <= L_p:
            M_ltb = M_p
        elif L_b <= L_r:
            M_ltb = C_b*(M_p-(M_p-0.7*self.material.F_y*self.S_x)*(L_b-L_p)/(L_r-L_p))
        else:
            M_ltb = self.S_x*C_b*pi**2*self.material.E/(L_b/self.r_ts)**2*sqrt(
                1+0.078*self.J*c/(self.S_x*self.h_o)*(L_b/self.r_ts)**2)
        M_ltb = M_ltb.to("kipft")

        # Flange local buckling moment
        lamb_pf = 0.38*sqrt_E_F_y
        lamb_rf = sqrt_E_F_y
        if self.lamb_f < lamb_pf:
            M_flb = M_p
        elif self.lamb_f < lamb_rf:
            M_flb = M_p-(M_p-0.7*self.material.F_y*self.S_x) \
                *(self.lamb_f-lamb_pf)/(lamb_rf-lamb_pf)
        else:
            k_c = min(max(0.35, 4/sqrt(self.lamb_w)), 0.76)
            M_flb = 0.9*self.material.E*k_c*self.S_x/self.lamb_f**2
        M_flb = M_flb.to("kipft")

        M_n = min(M_p, M_ltb, M_flb)
        return utils.fill_templates(templates.moment_capacity, locals(), phi_b, M_n)
