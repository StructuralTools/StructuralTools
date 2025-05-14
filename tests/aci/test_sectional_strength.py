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


from structuraltools import aci, materials
from structuraltools.unit import unit
from structuraltools.utils import isclose


def test_calc_phi_compression_controlled():
    rebar = materials.Rebar(4)
    phi = aci.sectional_strength.calc_phi(rebar, 0.002, return_string=True)
    assert phi == 0.65

def test_calc_phi_transition():
    rebar = materials.Rebar(4)
    phi = aci.sectional_strength.calc_phi(rebar, 0.003, return_string=True)
    assert isclose(phi, 0.7275862083, atol=1e-8)

def test_calc_phi_tension_controlled():
    rebar = materials.Rebar(4)
    phi = aci.sectional_strength.calc_phi(rebar, 0.006, return_string=True)
    assert phi == 0.9

def test_moment_capacity():
    concrete = materials.Concrete(4*unit.ksi)
    rebar = materials.Rebar(4)
    phi, M_n = aci.sectional_strength.moment_capacity(
        b=8*unit.inch,
        d=12*unit.inch,
        concrete=concrete,
        rebar=rebar,
        n=3,
        return_string=True)
    assert isclose(phi*M_n, 30.61323529*unit.kipft, atol=1e-8)
