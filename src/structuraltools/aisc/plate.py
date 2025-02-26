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

from structuraltools import unit
from structuraltools.aisc import _plate_latex as templates

class Plate:
    """Class for calculating steel plate strength. For consistency with the
       other shapes the x-axis intersects the width of the plate (b) and
       represents the strong axis for bending."""
    def __init__(self, d, t, material):
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

        self.A = (self.d*self.t).to("inch**2")
        self.W = (self.A*material.w_s).to("plf")
        self.Sx = (self.t*self.d**2/6).to("inch**3")
        self.Zx = (self.t*self.d**2/4).to("inch**3")
        self.Ix = (self.t*self.d**3/12).to("inch**4")
        self.rx = (sqrt(self.Ix/self.A)).to("inch")
        self.Sy = (self.d*self.t**2/6).to("inch**3")
        self.Zy = (self.d*self.t**2/4).to("inch**3")
        self.Iy = (self.d*self.t**3/12).to("inch**4")
        self.ry = (sqrt(self.Iy/self.A)).to("inch")

    def moment_capacity(self, L_b=0*unit.inch, C_b: int = 1, **kwargs):
        """Calculate the major axis moment capacity according to
           AISC 360-22 Section F11

           Parameters
           ==========

           L_b : pint length quantity, optional
               Unbraced length for lateral-torsional buckling

           C_b : float
               Lateral-torsional buckling modification factor. Defaults to 1.

           show : bool, optional
               Boolean indicating if the calculations shold be shown in
               Jupyter output

           return_latex : bool, optional
               Boolean indicating if the latex string should be returned

           decimal_points : int, optional
               How many decimal places to use when displaying calculations in
               Jupyter output. Defaults to 3"""
        dec = kwargs.get("decimal_points", 3)
        phi_b = 0.9
        latex = {
            "C_b": round(C_b, dec),
            "d" : round(self.d, dec),
            "E": self.material.E,
            "F_y": self.material.F_y,
            "L_b": round(L_b, dec),
            "S_x": round(self.Sx, dec),
            "t": round(self.t, dec),
            "Z_x": round(self.Zx, dec)
        }

        short = 0.08*self.material.E/self.material.F_y
        long = 1.9*self.material.E/self.material.F_y
        length = L_b*self.d/self.t**2
        M_p = min(self.material.F_y*self.Zx, 1.5*self.material.F_y*self.Sx).to("kipft")
        latex.update({
            "short": round(short, dec),
            "long": round(long, dec),
            "length": round(length, dec),
            "M_p": round(M_p, dec)
        })

        if length <= short:
            M_n = M_p
            latex.update({"M_n_str": templates.moment_plastic.substitute(
                M_n=round(M_n, dec), **latex)})
        elif length <= long:
            M_n = min(C_b*(1.52-0.274*(L_b*self.d*self.material.F_y)/
                (self.t**2*self.material.E))*self.material.F_y*self.Sx, M_p).to("kipft")
            latex.update({"M_n_str": templates.moment_ltb_short.substitute(
                M_n=round(M_n, dec), **latex)})
        else:
            M_n = min((1.9*self.material.E*C_b*self.t**2*self.Sx)/(L_b*self.d), M_p).to("kipft")
            latex.update({"M_n_str": templates.moment_ltb_long.substitute(
                M_n=round(M_n, dec), **latex)})

        if kwargs.get("show") or kwargs.get("return_latex"):
            latex = templates.moment_capacity.substitute(**latex)
            if kwargs.get("show"):
                display(Latex(latex))
            if kwargs.get("return_latex"):
                return latex, phi_b, M_n
        return phi_b, M_n

    def moment_capacity_minor(self, L_b=0*unit.inch, C_b: int = 1, **kwargs):
        """Calculate the minor axis moment capacity according to
           AISC 360-22 Section F11

           Parameters
           ==========

           L_b : pint length quantity, optional
               Unbraced length for lateral-torsional buckling

           C_b : float
               Lateral-torsional buckling modification factor. Defaults to 1.

           show : bool, optional
               Boolean indicating if the calculations shold be shown in
               Jupyter output

           return_latex : bool, optional
               Boolean indicating if the latex string should be returned

           decimal_points : int, optional
               How many decimal places to use when displaying calculations in
               Jupyter output. Defaults to 3"""
        dec = kwargs.get("decimal_points", 3)
        phi_b = 0.9
        latex = {
            "C_b": round(C_b, dec),
            "d" : round(self.d, dec),
            "E": self.material.E,
            "F_y": self.material.F_y,
            "L_b": round(L_b, dec),
            "S_y": round(self.Sy, dec),
            "t": round(self.t, dec),
            "Z_y": round(self.Zy, dec)
        }

        short = 0.08*self.material.E/self.material.F_y
        long = 1.9*self.material.E/self.material.F_y
        length = L_b*self.t/self.d**2
        M_p = min(self.material.F_y*self.Zy, 1.5*self.material.F_y*self.Sy).to("kipft")
        latex.update({
            "short": round(short, dec),
            "long": round(long, dec),
            "length": round(length, dec),
            "M_p": round(M_p, dec)
        })

        if length <= short:
            M_n = M_p
            latex.update({"M_n_str": templates.moment_minor_plastic.substitute(
                M_n=round(M_n, dec), **latex)})
        elif length <= long:
            M_n = min(C_b*(1.52-0.274*(L_b*self.t*self.material.F_y)/
                (self.d**2*self.material.E))*self.material.F_y*self.Sy, M_p).to("kipft")
            latex.update({"M_n_str": templates.moment_minor_ltb_short.substitute(
                M_n=round(M_n, dec), **latex)})
        else:
            M_n = min((1.9*self.material.E*C_b*self.d**2*self.Sy)/(L_b*self.t), M_p).to("kipft")
            latex.update({"M_n_str": templates.moment_minor_ltb_long.substitute(
                M_n=round(M_n, dec), **latex)})

        if kwargs.get("show") or kwargs.get("return_latex"):
            latex = templates.moment_capacity_minor.substitute(**latex)
            if kwargs.get("show"):
                display(Latex(latex))
            if kwargs.get("return_latex"):
                return latex, phi_b, M_n
        return phi_b, M_n

