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


from typing import Optional

from pint import Quantity
from sympy import lambdify, Piecewise, Rational, symbols
from sympy.physics.continuum_mechanics.beam import Beam

from structuraltools import unit
from structuraltools import Length, MomentOfInertia, Stress


class ContinuumBeam:
    """Wrapper class for SymPy Beam to allow it to be used with Pint units.
    Select SymPy Beam methods are mirrored or passed through. Other SymPy Beam
    methods can be accessed through ContinuumBeam.beam."""
    def __init__(
        self,
        length: Length,
        elastic_modulus: Stress,
        second_moment: MomentOfInertia,
        length_unit: str = "inch",
        force_unit: str = "lb",):
        """Create a ContinuumBeam

        Parameters
        ==========

        length : Length
            Beam length

        elastic_modulus : Stress
            Modulus of elasticity of the beam

        second_moment : MomentOfInertia
            Second area moment of inertia of the beam

        length_unit : str, optional
            Length unit to use for calculations and when returning the results

        force_unit : str, optional
            Force unit to use for calculations and when returning the results"""
        self.length_unit = length_unit
        self.force_unit = force_unit
        self.loads = {}
        self.supports = {}

        self.moment_unit = f"{force_unit}*{length_unit}"
        self.beam_args = (
            Rational(length.to(length_unit).magnitude),
            Rational(elastic_modulus.to(f"{force_unit}/{length_unit}**2").magnitude),
            Rational(second_moment.to(f"{length_unit}**4").magnitude)
        )

    def apply_support(self, name: str, loc: Length, kind: str) -> None:
        """Add a support to the beam.

        Parameters
        ==========

        name : str
            Unique name of the support being added.

        loc : Length
            Location to add the support

        kind : str
            Kind of support to apply. One of: "pin", "roller", or "fixed"."""
        self.supports.update({
            name: (Rational(loc.to(self.length_unit).magnitude), kind)})

    def apply_load(
        self,
        name: str,
        value: Quantity,
        start: Length,
        order: int,
        end: Optional[Length] = None) -> None:
        """Apply a load to the beam.

        Parameters
        ==========

        name : str
            Unique name of the load being added

        value : Quantity
            Magnitude of the load being added

        start : Length
            The starting point of the applied load. For point moment and point
            forces this is the location the load is applied.

        order : int
            The order of the applied load
            - For point moments, order = -2
            - For point loads, order = -1
            - For constant distributed loads, order = 0
            - For ramp loads, order = 1
            - For Parabolic ramp loads, order = 2
            - ... so on

        end : Length, Optional
            End point of distributed loads. If not provided it is assumed that
            distributed loads end at the end of the beam."""
        if end is not None:
            end = Rational(end.to(self.length_unit).magnitude)
        self.loads.update({name: (
            Rational(value.to(self.moment_unit+f"/{self.length_unit}"*(2+order)).magnitude),
            Rational(start.to(self.length_unit).magnitude),
            order,
            end)})

    def remove_load(self, name: Optional[str]) -> None:
        """Remove the specified load from the beam

        Parameters
        ==========

        name : str, Optional
            Name of load to be removed. If no name is specified all loads are
            removed."""
        if name is not None:
            del self.loads[name]
        else:
            self.loads = {}

    def solve_beam(self) -> None:
        """Solve the beam and store the results"""
        self.beam = Beam(*self.beam_args)

        self.support_symbols = {}
        self.support_symbols_list = []
        for name, args in self.supports.items():
            syms = self.beam.apply_support(*args)
            self.support_symbols.update({name: syms})
            if isinstance(syms, tuple):
                self.support_symbols_list.extend(syms)
            else:
                self.support_symbols_list.append(syms)

        for load in self.loads.values():
            self.beam.apply_load(*load)

        self.beam.solve_for_reaction_loads(*self.support_symbols_list)

        # Store reactions
        self.reactions = {}
        for name, syms in self.support_symbols.items():
            if isinstance(syms, tuple):
                self.reactions.update({name: (
                    float(self.beam.reaction_loads[syms[0]])*unit(self.force_unit),
                    float(self.beam.reaction_loads[syms[1]])*unit(self.moment_unit))})
            else:
                self.reactions.update({name:
                    float(self.beam.reaction_loads[syms])*unit(self.force_unit)})

        # Store shear force, bending moment, and deflection functions
        x = symbols("x")
        self.shear_force = unit.wraps(self.force_unit, self.length_unit) \
            (lambdify([x], self.beam.shear_force().rewrite(Piecewise), "numpy"))
        self.bending_moment = unit.wraps(self.moment_unit, self.length_unit) \
            (lambdify([x], self.beam.bending_moment().rewrite(Piecewise), "numpy"))
        self.deflection = unit.wraps(self.length_unit, self.length_unit) \
            (lambdify([x], self.beam.deflection().rewrite(Piecewise), "numpy"))

    # Pass through draw and plotting functions
    def draw(self, pictorial: bool = True) -> None:
        """Pass through to SymPy Beam.draw().show()"""
        self.beam.draw(pictorial=pictorial).show()

    def plot_shear_force(self) -> None:
        """Pass through to SymPy Beam.plot_shear_force(). Graph is in
           the set length and force units."""
        self.beam.plot_shear_force()

    def plot_bending_moment(self) -> None:
        """Pass through to SymPy Beam.plot_bending_moment(). Graph is
           in the set length and force units."""
        self.beam.plot_bending_moment()

    def plot_deflection(self) -> None:
        """Pass through to SymPy Beam.plot_deflection(). Graph is in
           the set length and force units."""
        self.beam.plot_deflection()

    def plot_loading_results(self) -> None:
        """Pass through to SymPy Beam.plot_loading_results(). Graph is
           in the set length and force units."""
        self.beam.plot_loading_results()
