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


def test_straight_bar_factors_1():
    concrete = materials.Concrete(6000*unit.psi, w_c=110*unit.pcf)
    rebar = materials.Rebar(8, coated=True)
    results = aci.development_length.straight_bar_factors(
        rebar=rebar,
        concrete=concrete,
        c_c=2*unit.inch,
        s=6*unit.inch,
        concrete_below=True,
        return_string=True)
    assert results[0:] == (0.75, 1, 1.5, 1, 1.3)

def test_straight_bar_factors_2():
    concrete = materials.Concrete(4000*unit.psi)
    rebar = materials.Rebar(4, f_y=80*unit.ksi, coated=True)
    results = aci.development_length.straight_bar_factors(
        rebar=rebar,
        concrete=concrete,
        c_c=3*unit.inch,
        s=3*unit.inch,
        return_string=True)
    assert results[0:] == (1, 1.15, 1.5, 1, 1)

def test_straight_bar_factors_3():
    concrete = materials.Concrete(4000*unit.psi)
    rebar = materials.Rebar(4, f_y=100*unit.ksi, coated=True)
    results = aci.development_length.straight_bar_factors(
        rebar=rebar,
        concrete=concrete,
        c_c=3*unit.inch,
        s=12*unit.inch,
        use_psi_s=True,
        return_string=True)
    assert results[0:] == (1, 1.3, 1.2, 0.8, 1)

def test_straight_bar_factors_4():
    concrete = materials.Concrete(4000*unit.psi)
    rebar = materials.Rebar(8)
    results = aci.development_length.straight_bar_factors(
        rebar=rebar,
        concrete=concrete,
        c_c=3*unit.inch,
        s=12*unit.inch,
        return_string=True)
    assert results[0:] == (1, 1, 1, 1, 1)

def test_straight_bar_min():
    concrete = materials.Concrete(4000*unit.psi)
    rebar = materials.Rebar(4)
    l_d = aci.development_length.straight_bar(
        rebar=rebar,
        concrete=concrete,
        c_c=3*unit.inch,
        s=12*unit.inch,
        return_string=True)
    assert isclose(l_d, 12*unit.inch)
    assert l_d.units == "inch"

def test_straight_bar_A_tr():
    concrete = materials.Concrete(4000*unit.psi)
    rebar = materials.Rebar(8)
    l_d = aci.development_length.straight_bar(
        rebar=rebar,
        concrete=concrete,
        c_c=3*unit.inch,
        s=12*unit.inch,
        n=4,
        A_tr=0.79*unit.inch**2,
        return_string=True)
    assert isclose(l_d, 17.11052041*unit.inch, atol=1e-8)
    assert l_d.units == "inch"

def test_straight_bar():
    concrete = materials.Concrete(4000*unit.psi, w_c=110*unit.pcf)
    rebar = materials.Rebar(8, f_y=80*unit.ksi, coated=True)
    l_d = aci.development_length.straight_bar(
        rebar=rebar,
        concrete=concrete,
        c_c=3*unit.inch,
        s=12*unit.inch,
        concrete_below=True,
        return_string=True)
    assert isclose(l_d, 64.83572711*unit.inch, atol=1e-8)
    assert l_d.units == "inch"

def test_standard_hook_factors_1():
    concrete = materials.Concrete(4000*unit.psi, w_c=110*unit.pcf)
    rebar = materials.Rebar(8, coated=True)
    results = aci.development_length.standard_hook_factors(
        rebar=rebar,
        concrete=concrete,
        c_c_side=3*unit.inch,
        s=4*unit.inch,
        A_th=1*unit.inch**2,
        in_column=True,
        return_string=True)
    assert isclose(results[-1], 0.8666666667, atol=1e-10)
    assert results[0:-1] == (0.75, 1.2, 1, 1)

def test_standard_hook_factors_2():
    concrete = materials.Concrete(6000*unit.psi)
    rebar = materials.Rebar(8)
    results = aci.development_length.standard_hook_factors(
        rebar=rebar,
        concrete=concrete,
        c_c_side=6*unit.inch,
        s=6*unit.inch,
        in_column=True,
        return_string=True)
    assert isclose(results[-1], 1)
    assert results[0:-1] == (1, 1, 1, 1)

def test_standard_hook_factors_3():
    concrete = materials.Concrete(6000*unit.psi)
    rebar = materials.Rebar(8)
    results = aci.development_length.standard_hook_factors(
        rebar=rebar,
        concrete=concrete,
        c_c_side=2*unit.inch,
        s=4*unit.inch,
        in_column=True,
        return_string=True)
    assert isclose(results[-1], 1)
    assert results[0:-1] == (1, 1, 1.6, 1.25)

def test_standard_hook_factors_4():
    concrete = materials.Concrete(6000*unit.psi)
    rebar = materials.Rebar(8)
    results = aci.development_length.standard_hook_factors(
        rebar=rebar,
        concrete=concrete,
        c_c_side=3*unit.inch,
        s=4*unit.inch,
        return_string=True)
    assert isclose(results[-1], 1)
    assert results[0:-1] == (1, 1, 1.6, 1.25)

def test_standard_hook_factors_5():
    concrete = materials.Concrete(6000*unit.psi)
    rebar = materials.Rebar(14)
    results = aci.development_length.standard_hook_factors(
        rebar=rebar,
        concrete=concrete,
        c_c_side=12*unit.inch,
        s=12*unit.inch,
        return_string=True)
    assert isclose(results[-1], 1)
    assert results[0:-1] == (1, 1, 1.6, 1.25)

def test_standard_hook_min():
    concrete = materials.Concrete(4000*unit.psi)
    rebar = materials.Rebar(4)
    l_dh = aci.development_length.standard_hook(
        rebar=rebar,
        concrete=concrete,
        c_c_side=3*unit.inch,
        s=12*unit.inch,
        return_string=True)
    assert isclose(l_dh, 6*unit.inch)
    assert l_dh.units == "inch"

def test_standard_hook_in_column():
    concrete = materials.Concrete(8000*unit.psi, w_c=110*unit.pcf)
    rebar = materials.Rebar(8, coated=True)
    l_dh = aci.development_length.standard_hook(
        rebar=rebar,
        concrete=concrete,
        c_c_side=3*unit.inch,
        s=4*unit.inch,
        n=4,
        in_column=True,
        return_string=True)
    assert isclose(l_dh, 31.22364012*unit.inch, atol=1e-8)
    assert l_dh.units == "inch"

def test_standard_hook():
    concrete = materials.Concrete(8000*unit.psi, w_c=110*unit.pcf)
    rebar = materials.Rebar(8, coated=True)
    l_dh = aci.development_length.standard_hook(
        rebar=rebar,
        concrete=concrete,
        c_c_side=3*unit.inch,
        s=4*unit.inch,
        n=4,
        return_string=True)
    assert isclose(l_dh, 39.02955015*unit.inch, atol=1e-8)
    assert l_dh.units == "inch"
