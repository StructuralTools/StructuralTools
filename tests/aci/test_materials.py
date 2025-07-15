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


from numpy import isclose

from structuraltools.aci import materials
from structuraltools.unit import unit


def test_Concrete_init_ultra_lightweight():
    concrete = materials.Concrete(4*unit.ksi, w_c=90*unit.pcf)
    assert concrete.f_prime_c == 4000*unit.psi
    assert concrete.f_prime_c.units == "psi"
    assert isclose(concrete.E_c, 1782000*unit.psi)
    assert concrete.E_c.units == "psi"
    assert concrete.lamb == 0.75
    assert concrete.beta_1 == 0.85
    assert isclose(concrete.f_r, 355.7562368*unit.psi, atol=1e-7)
    assert concrete.f_r.units == "psi"

def test_Concrete_init_lightweight():
    concrete = materials.Concrete(5*unit.ksi, w_c=110*unit.pcf)
    assert isclose(concrete.E_c, 2692080.051*unit.psi, atol=1e-3)
    assert concrete.E_c.units == "psi"
    assert isclose(concrete.lamb, 0.825)
    assert isclose(concrete.beta_1, 0.8)
    assert isclose(concrete.f_r, 437.5223209*unit.psi, atol=1e-7)
    assert concrete.f_r.units == "psi"

def test_Concrete_init_normalweight():
    concrete = materials.Concrete(8*unit.ksi)
    assert isclose(concrete.E_c, 5422453.319*unit.psi, atol=0.001)
    assert concrete.E_c.units == "psi"
    assert concrete.lamb == 1
    assert concrete.beta_1 == 0.65
    assert concrete.f_r.units == "psi"
    assert isclose(concrete.f_r, 670.8203932*unit.psi, atol=1e-7)

def test_Rebar_init():
    rebar = materials.Rebar(4, f_y=60*unit.ksi)
    assert rebar.size == 4
    assert isclose(rebar.f_y, 60000*unit.psi)
    assert rebar.f_y.units == "psi"
    assert rebar.A_b.magnitude == 0.2
    assert rebar.A_b.units == "inch ** 2"
    assert rebar.w.magnitude == 0.668
    assert rebar.w.units == "plf"
    assert rebar.d_b.magnitude == 0.5
    assert rebar.d_b.units == "inch"
    assert rebar.D.magnitude == 3
    assert rebar.D.units == "inch"
    assert rebar.G.magnitude == 8
    assert rebar.G.units == "inch"
    assert rebar.J.magnitude == 4
    assert rebar.J.units == "inch"
