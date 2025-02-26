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


from IPython.display import display, Latex
from numpy import sqrt

from structuraltools import resources, unit, utils
from structuraltools import _materials_latex as templates

class Concrete:
    """Class to store data for concrete materials and calculate basic material
       properties."""
    def __init__(self, f_prime_c, **kwargs):
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
               Poisson's ration of the concrete

           show : bool, optional
               Whether to display all calculations made

           dec : int, optional
               Number of decimal places to use in LaTeX representation
               of calculations"""
        self.f_prime_c = min(round(f_prime_c.to("psi").magnitude), 10000)*unit.psi
        self.w_c = round(kwargs.get("w_c", 150*unit.pcf).to("pcf").magnitude)*unit.pcf
        self.max_agg = kwargs.get("max_agg", 1*unit.inch).to("inch")
        self.v = kwargs.get("v", 0.2)
        dec = kwargs.get("decimal_points", 3)
        latex = {"w_c": self.w_c, "f_prime_c": self.f_prime_c}

        low = 100*unit.pcf
        high = 135*unit.pcf
        if self.w_c <= low:
            self.lamb = 0.75
            latex.update({
                "lamb": self.lamb,
                "lamb_str": templates.Concrete_lamb_low.substitute(
                    lamb=self.lamb, w_c=self.w_c, low=low)
            })
        elif self.w_c <= high:
            self.lamb = min(0.0075*(self.w_c/unit.pcf).to("dimensionless").magnitude, 1)
            latex.update({
                "lamb": round(self.lamb, dec),
                "lamb_str": templates.Concrete_lamb_mid.substitute(
                    lamb=round(self.lamb, dec), w_c=self.w_c, low=low, high=high)
            })
        else:
            self.lamb = 1
            latex.update({
                "lamb": self.lamb,
                "lamb_str": templates.Concrete_lamb_high.substitute(
                    lamb=self.lamb, w_c=self.w_c, high=high)
            })

        low = 4000*unit.psi
        high = 8000*unit.psi
        if self.f_prime_c <= low:
            self.beta_1 = 0.85
            latex.update({"beta_1_str": templates.Concrete_beta_1_low.substitute(
                beta_1=self.beta_1, f_prime_c=self.f_prime_c, low=low)})
        elif self.f_prime_c < high:
            beta_1 = 0.85-0.05*(self.f_prime_c-4000*unit.psi)/(1000*unit.psi)
            self.beta_1 = beta_1.to("dimensionless").magnitude
            latex.update({"beta_1_str": templates.Concrete_beta_1_mid.substitute(
                beta_1=round(self.beta_1, dec), f_prime_c=self.f_prime_c, low=low, high=high)})
        else:
            self.beta_1 = 0.65
            latex.update({"beta_1_str": templates.Concrete_beta_1_high.substitute(
                beta_1=self.beta_1, f_prime_c=self.f_prime_c, high=high)})

        self.E_c = (self.w_c/unit.pcf)**1.5*33*sqrt(self.f_prime_c*unit.psi)
        self.f_r = 7.5*self.lamb*sqrt(self.f_prime_c*unit.psi)
        latex.update({"E_c": round(self.E_c, dec), "f_r": round(self.f_r, dec)})

        self.latex = templates.Concrete.substitute(**latex)
        if kwargs.get("show"):
            display(Latex(self.latex))


class Rebar:
    """Class to store data for rebar"""
    def __init__(self, size: int, **kwargs):
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
        rebar_database = resources.joinpath("ACI_rebar_sizes.csv")
        self.size = size
        self.f_y = round(kwargs.get("f_y", 60000*unit.psi).to("psi").magnitude)*unit.psi
        self.coated = kwargs.get("coated", False)
        self.E_s = round(kwargs.get("E_s", 29e6*unit.psi).to("psi").magnitude)*unit.psi
        dimensions = utils.get_table_entry(rebar_database, str(self.size))
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
        steel_database = resources.joinpath("steel_materials.csv")
        self.name = name
        properties = utils.get_table_entry(steel_database, self.name)
        for attribute, value in properties.items():
            setattr(self, attribute, value)
