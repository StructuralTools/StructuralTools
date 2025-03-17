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


from numpy import isclose, sqrt

from structuraltools import resources, unit, utils
from structuraltools import Length, Stress, UnitWeight
from structuraltools import _materials_markdown as templates


rebar_database = utils.read_data_table(resources.joinpath("ACI_rebar_sizes.csv"))
steel_database = utils.read_data_table(resources.joinpath("AISC_steel_materials.csv"))


class Concrete:
    """Class to store data for concrete materials and calculate basic material
    properties."""
    def __init__(
        self,
        f_prime_c: Stress,
        w_c: UnitWeight = 150*unit.pcf,
        max_agg: Length = 1*unit.inch,
        v: float = 0.2,
        **markdown_options):
        """Create a new concrete material instance, calculate the modulus of
        elasticity, and optionally show the any calculations made.

        Parameters
        ==========

        f_prime_c : pint pressure quantity
            Specified compressive strength of the concrete

        w_c : pint unit weight quantity, optional
            Concrete unit weight

        max_agg : pint length quantity, optional
            Nominal maximum aggregate size

        v : float, optional
            Poisson's ration of the concrete"""
        self.max_agg = max_agg.to("inch")
        self.v = v
        self.unpack_for_templates = True

        if isclose(f_prime_c.to("psi"), round(f_prime_c.to("psi"))):
            f_prime_c = round(f_prime_c.to("psi").magnitude)*unit.psi
        self.f_prime_c = min(f_prime_c.to("psi"), 10000*unit.psi)

        if isclose(w_c.to("pcf"), round(w_c.to("pcf"))):
            self.w_c = round(w_c.to("pcf").magnitude)*unit.pcf
        else:
            self.w_c = w_c.to("pcf")

        self.E_c = (self.w_c.magnitude)**1.5*33*sqrt(self.f_prime_c*unit.psi)
        self.lamb = utils.bound(0.75, 0.0075*w_c.magnitude, 1)
        self.f_r = 7.5*self.lamb*sqrt(self.f_prime_c*unit.psi)
        self.beta_1 = utils.bound(0.65, 0.85-0.05*(self.f_prime_c.magnitude-4000)/1000, 0.85)

        markdown_options.update({"return_markdown": True})
        self.markdown = utils.fill_templates(templates.Concrete, locals())


class Rebar:
    """Class to store data for rebar"""
    def __init__(
        self,
        size: int,
        f_y: Stress = 60000*unit.psi,
        coated: bool = False,
        E_s: Stress = 29e6*unit.psi):
        """Create a new rebar class instance

        Parameters
        ==========

        size : int
            Integer indicating common rebar size

        f_y : Pint Pressure Quantity, Optional
            Rebar yield strength. Defaults to 60 ksi

        coated : boolean, Optional
            Boolean indicating if the rebar is epoxy-coated or zinc and epoxy
            dual-coated

        E_s : pint pressure quantity optional
            Modulus of elasticity to use for the rebar. Defaults to 29000 ksi"""
        self.size = size
        self.coated = coated
        self.unpack_for_templates = True

        if isclose(f_y.to("psi"), round(f_y.to("psi"))):
            self.f_y = round(f_y.to("psi").magnitude)*unit.psi
        else:
            self.f_y = f_y.to("psi")

        if isclose(E_s.to("psi"), round(E_s.to("psi"))):
            self.E_s = round(E_s.to("psi").magnitude)*unit.psi
        else:
            self.E_s = E_s.to("psi")

        dimensions = rebar_database.loc[size, :].to_dict()
        for attribute, value in dimensions.items():
            setattr(self, attribute, value)


class Steel:
    """Class to store data for steel materials"""
    def __init__(self, name: str):
        """Initialize a steel from the structuraltools steel database. Custom steel
        types are not currently supported.

        Parameters
        ==========

        name : str
            Name of the steel. Must match a name in the structuraltools steel
            database."""
        self.name = name
        self.unpack_for_templates = True
        properties = steel_database.loc[name, :].to_dict()
        for attribute, value in properties.items():
            setattr(self, attribute, value)
