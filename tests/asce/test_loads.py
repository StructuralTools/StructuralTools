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


from numpy import array, isclose

from structuraltools.asce.loads import (LoadCase, LoadCaseFactor, LoadCollector,
    LoadComb, LoadCombResult, reduce_combs)
from structuraltools.unit import unit
from structuraltools.utils import read_data_table


def test_reduce_combs():
    reactions = reduce_combs(read_data_table("tests/asce/test_reactions.csv"))
    expected_reactions = read_data_table("tests/asce/reduced_test_reactions.csv")
    assert all(reactions.eq(expected_reactions))

def test_reduce_combs_already_reduced():
    reactions = read_data_table("tests/asce/reduced_test_reactions.csv")
    reduced_reactions = reduce_combs(reactions)
    assert all(reduced_reactions.eq(reactions))


class TestLoadComb:
    def setup_method(self, method):
        self.load_comb = LoadComb("test_comb", D=1, L=2, S=3)
        self.loads = {"D": {"upD": 1, "D": 2}, "L": {"L": 3}}
        self.case_combs = [
            [LoadCase("D", "upD"), LoadCase("L", "L")],
            [LoadCase("D", "D"), LoadCase("L", "L")]
        ]

    def test_eval_loads(self):
        combs = self.load_comb.eval_loads(self.loads, self.case_combs)
        assert set(combs) == {
            LoadCombResult(
                name="test_comb",
                time_factor=1,
                factors=(LoadCaseFactor("D", "upD", 1), LoadCaseFactor("L", "L", 2)),
                result=7
            ),
            LoadCombResult(
                name="test_comb",
                time_factor=1,
                factors=(LoadCaseFactor("D", "D", 1), LoadCaseFactor("L", "L", 2)),
                result=8
            )
        }


class TestLoadCollector:
    def setup_method(self, method):
        self.combs = [
            LoadComb("1", D=1.4),
            LoadComb("2", D=1.2, L=1.6, W=0.5),
            LoadComb("3", L_r=1.6)
        ]
        self.collector = LoadCollector()

    def test_add_load_single(self):
        self.collector.add_load("D", "D", 1)
        self.collector.add_load("D", "D", 2)
        self.collector.add_load("W", "W+", 3)
        self.collector.add_load("W", "W-", 4)
        assert self.collector.loads == {"D": {"D": 3}, "W": {"W+": 3, "W-": 4}}

    def test_add_load_multiple_cases(self):
        self.collector.add_load("D", {"D", "upD"}, 1)
        self.collector.add_load("D", {"D", "upD"}, 2)
        self.collector.add_load("D", "upD", 3)
        self.collector.add_load("D", "D", 4)
        assert set(self.collector.loads.keys()) == {"D"}
        assert set(self.collector.loads["D"].keys()) == {"D", "upD"}
        assert self.collector.loads["D"]["D"] == 7
        assert self.collector.loads["D"]["upD"] == 6

    def test_add_load_multiple_kinds(self):
        self.collector.add_load({"S", "Sdrift"}, "S", 1)
        self.collector.add_load({"S", "Sdrift"}, "S", 2)
        self.collector.add_load("S", "S", 3)
        self.collector.add_load("Sdrift", "S", 4)
        assert set(self.collector.loads.keys()) == {"S", "Sdrift"}
        assert set(self.collector.loads["S"].keys()) == {"S"}
        assert set(self.collector.loads["Sdrift"].keys()) == {"S"}
        assert self.collector.loads["S"]["S"] == 6
        assert self.collector.loads["Sdrift"]["S"] == 7

    def test_add_load_multiple_kinds_and_cases(self):
        self.collector.add_load(["D", "L"], ["D", "L"], 1)
        self.collector.add_load(["D", "L"], ["D", "L"], 2)
        assert self.collector.loads == {"D": {"D": 3, "L": 3}, "L": {"D": 3, "L": 3}}

    def test_eval_combs_floats(self):
        self.collector.add_load("D", "D1", 1)
        self.collector.add_load("D", "D2", 2)
        self.collector.add_load("L", "L1", 1)
        self.collector.add_load("L", "L2", 2)
        factored_load = self.collector.eval_combs(self.combs)
        assert len(factored_load["combs"]) == 6
        assert isclose(factored_load["max_value"], 5.6)
        assert factored_load["max_comb"].factors == (
            LoadCaseFactor("D", "D2", 1.2),
            LoadCaseFactor("L", "L2", 1.6))
        assert isclose(factored_load["min_value"], 1.4)
        assert factored_load["min_comb"].factors == (LoadCaseFactor("D", "D1", 1.4),)
        assert isclose(factored_load["abs_max_value"], 5.6)
        assert factored_load["abs_max_comb"].factors == (
            LoadCaseFactor("D", "D2", 1.2),
            LoadCaseFactor("L", "L2", 1.6))

    def test_eval_combs_quantities(self):
        self.collector.add_load("D", "D1", -1*unit.lb)
        self.collector.add_load("D", "D2", 2*unit.lb)
        self.collector.add_load("L", "L1", -1*unit.lb)
        self.collector.add_load("L", "L2", 2*unit.lb)
        factored_load = self.collector.eval_combs(self.combs)
        assert len(factored_load["combs"]) == 6
        assert isclose(factored_load["max_value"], 5.6*unit.lb)
        assert factored_load["max_comb"].factors == (
            LoadCaseFactor("D", "D2", 1.2),
            LoadCaseFactor("L", "L2", 1.6))
        assert isclose(factored_load["min_value"], -2.8*unit.lb)
        assert factored_load["min_comb"].factors == (
            LoadCaseFactor("D", "D1", 1.2),
            LoadCaseFactor("L", "L1", 1.6))
        assert isclose(factored_load["abs_max_value"], 5.6*unit.lb)
        assert factored_load["abs_max_comb"].factors == (
            LoadCaseFactor("D", "D2", 1.2),
            LoadCaseFactor("L", "L2", 1.6))

    def test_eval_combs_arrays(self):
        self.collector.add_load("D", "D1", array([1, 4, 5]))
        self.collector.add_load("D", "D2", array([-2, 3, 6]))
        self.collector.add_load("L", "L1", array([1, 4, 5]))
        self.collector.add_load("L", "L2", array([-2, 3, 6]))
        factored_load = self.collector.eval_combs(self.combs)
        assert len(factored_load["combs"]) == 6
        assert isclose(factored_load["max_value"], 16.8)
        assert factored_load["max_comb"].factors == (
            LoadCaseFactor("D", "D2", 1.2),
            LoadCaseFactor("L", "L2", 1.6))
        assert all(isclose(factored_load["max_envelope"], [2.8, 11.2, 16.8]))
        assert isclose(factored_load["min_value"], -5.6)
        assert factored_load["min_comb"].factors == (
            LoadCaseFactor("D", "D2", 1.2),
            LoadCaseFactor("L", "L2", 1.6))
        assert all(isclose(factored_load["min_envelope"], [-5.6, 4.2, 7]))
        assert isclose(factored_load["abs_max_value"], 16.8)
        assert factored_load["abs_max_comb"].factors == (
            LoadCaseFactor("D", "D2", 1.2),
            LoadCaseFactor("L", "L2", 1.6))
        assert all(isclose(factored_load["abs_max_envelope"], [5.6, 11.2, 16.8]))

    def test_eval_combs_quantity_arrays(self):
        self.collector.add_load("D", "D1", [1, 4, 5]*unit.lb)
        self.collector.add_load("D", "D2", [2, 3, 6]*unit.lb)
        self.collector.add_load("L", "L1", [1, 4, 5]*unit.lb)
        self.collector.add_load("L", "L2", [2, 3, 6]*unit.lb)
        factored_load = self.collector.eval_combs(self.combs)
        assert len(factored_load["combs"]) == 6
        assert isclose(factored_load["max_value"], 16.8*unit.lb)
        assert factored_load["max_comb"].factors == (
            LoadCaseFactor("D", "D2", 1.2),
            LoadCaseFactor("L", "L2", 1.6))
        assert all(isclose(factored_load["max_envelope"], [5.6, 11.2, 16.8]*unit.lb))
        assert isclose(factored_load["min_value"], 1.4*unit.lb)
        assert factored_load["min_comb"].factors == (LoadCaseFactor("D", "D1", 1.4),)
        assert all(isclose(factored_load["min_envelope"], [1.4, 4.2, 7]*unit.lb))
        assert isclose(factored_load["abs_max_value"], 16.8*unit.lb)
        assert factored_load["abs_max_comb"].factors == (
            LoadCaseFactor("D", "D2", 1.2),
            LoadCaseFactor("L", "L2", 1.6))
        assert all(isclose(factored_load["abs_max_envelope"], [5.6, 11.2, 16.8]*unit.lb))
