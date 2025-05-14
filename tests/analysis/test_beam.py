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


from structuraltools import analysis
from structuraltools.unit import unit
from structuraltools.utils import isclose


def test_ContinuumBeam_init():
    beam = analysis.beam.ContinuumBeam(
        length=120.5*unit.inch,
        elastic_modulus=29000*unit.ksi,
        second_moment=1*unit.inch**4)
    assert isclose(beam.beam_args[0], 120.5)
    assert isclose(beam.beam_args[1], 29e6)
    assert isclose(beam.beam_args[2], 1)


class TestContinuumBeam:
    def setup_method(self, method):
        self.l = 120*unit.inch
        self.E = 29000*unit.ksi
        self.I = 1*unit.inch**4
        self.beam = analysis.beam.ContinuumBeam(self.l, self.E, self.I)

    def test_apply_support(self):
        self.beam.apply_support("start", 0*unit.inch, "pin")
        assert isclose(self.beam.supports["start"][0], 0)
        assert self.beam.supports["start"][1] == "pin"

    def test_apply_load(self):
        self.beam.apply_load(
            name="test",
            value=50*unit.plf,
            start=0*unit.inch,
            order=0)
        assert isclose(self.beam.loads["test"][0], 50/12)
        assert isclose(self.beam.loads["test"][1], 0)
        assert self.beam.loads["test"][2] == 0
        assert self.beam.loads["test"][3] is None

    def test_solve_beam_simply_supported_uniform_load(self):
        w = 20*unit.pli
        self.beam.apply_support("start", 0*unit.inch, "pin")
        self.beam.apply_support("end", self.l, "roller")
        self.beam.apply_load("uniform", w, 0*unit.inch, 0)
        self.beam.solve_beam()
        assert isclose(self.beam.reactions["start"], -w*self.l/2, atol=1e-10*unit.lb)
        assert isclose(self.beam.reactions["end"], -w*self.l/2, atol=1e-10*unit.lb)
        assert isclose(self.beam.shear_force(0*unit.inch), w*self.l/2)
        assert isclose(self.beam.bending_moment(self.l/2), w*self.l**2/8)
        assert isclose(self.beam.deflection(self.l/2), 5*w*self.l**4/(384*self.E*self.I))

    def test_solve_beam_cantilever_ramp_load(self):
        W = 1*unit.psi*self.l**2/2
        self.beam.apply_support("end", self.l, "fixed")
        self.beam.apply_load("ramp", 1*unit.psi, 0*unit.inch, 1)
        self.beam.solve_beam()
        assert isclose(self.beam.reactions["end"][0], -W)
        assert isclose(self.beam.reactions["end"][1], -W*self.l/3)
        assert isclose(self.beam.shear_force(self.l-1e-10*unit.inch), -W)
        assert isclose(self.beam.bending_moment(self.l-1e-10*unit.inch), -W*self.l/3)
        assert isclose(self.beam.deflection(0*unit.inch), W*self.l**3/(15*self.E*self.I))
