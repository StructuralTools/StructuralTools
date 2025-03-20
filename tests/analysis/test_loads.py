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

from structuraltools import analysis, unit, utils


def test_reduce_combs():
    reactions = utils.read_data_table("tests/analysis/test_reactions.csv")
    reactions = analysis.loads.reduce_combs(reactions)
    expected_reactions = utils.read_data_table("tests/analysis/reduced_test_reactions.csv")
    assert all(reactions.eq(expected_reactions))

def test_reduce_combs_already_reduced():
    reactions = utils.read_data_table("tests/analysis/reduced_test_reactions.csv")
    reduced_reactions = analysis.loads.reduce_combs(reactions)
    assert all(reduced_reactions.eq(reactions))


class TestLoadCollector:
    def setup_method(self, method):
        self.combs = [{"D": 1.4}, {"D": 1.2, "L": 1.6, "W": 0.5}, {"L_r": 1.6}]
        self.collector = analysis.loads.LoadCollector()

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
        assert self.collector.loads == {"D": {"D": 3}, "L": {"L": 3}}

    def test_eval_combs_floats(self):
        self.collector.add_load(("D", "L"), ("D1", "L1"), 1)
        self.collector.add_load(("D", "L"), ("D2", "L2"), 2)
        self.collector.eval_combs(self.combs)
        combs = {
            ((("D", "D1"), 1.4),): 1.4,
            ((("D", "D2"), 1.4),): 2.8,
            ((("D", "D1"), 1.2), (("L", "L1"), 1.6)): 2.8,
            ((("D", "D1"), 1.2), (("L", "L2"), 1.6)): 4.4,
            ((("D", "D2"), 1.2), (("L", "L1"), 1.6)): 4,
            ((("D", "D2"), 1.2), (("L", "L2"), 1.6)): 5.6
        }
        assert all([isclose(self.collector.combs[key], value) for key, value in combs.items()])
        assert set(self.collector.combs.keys()) == set(combs.keys())
        assert isclose(self.collector.max_value, 5.6)
        assert self.collector.max_comb == ((("D", "D2"), 1.2), (("L", "L2"), 1.6))
        assert isclose(self.collector.min_value, 1.4)
        assert self.collector.min_comb == ((("D", "D1"), 1.4),)

    def test_eval_combs_quantities(self):
        self.collector.add_load(("D", "L"), ("D1", "L1"), -1*unit.lb)
        self.collector.add_load(("D", "L"), ("D2", "L2"), 2*unit.lb)
        self.collector.eval_combs(self.combs)
        assert isclose(self.collector.max_value, 5.6*unit.lb)
        assert self.collector.max_comb == ((("D", "D2"), 1.2), (("L", "L2"), 1.6))
        assert isclose(self.collector.min_value, -2.8*unit.lb)
        assert self.collector.min_comb == ((("D", "D1"), 1.2), (("L", "L1"), 1.6))
        assert isclose(self.collector.abs_max_value, 5.6*unit.lb)
        assert self.collector.abs_max_comb == ((("D", "D2"), 1.2), (("L", "L2"), 1.6))

    def test_eval_combs_arrays(self):
        self.collector.add_load(("D", "L"), ("D1", "L1"), array([1, 4, 5]))
        self.collector.add_load(("D", "L"), ("D2", "L2"), array([-2, 3, 6]))
        self.collector.eval_combs(self.combs)
        assert isclose(self.collector.max_value, 16.8)
        assert self.collector.max_comb == ((("D", "D2"), 1.2), (("L", "L2"), 1.6))
        assert all(isclose(self.collector.max_envelope, [2.8, 11.2, 16.8]))
        assert isclose(self.collector.min_value, -5.6)
        assert self.collector.min_comb == ((("D", "D2"), 1.2), (("L", "L2"), 1.6))
        assert all(isclose(self.collector.min_envelope, [-5.6, 4.2, 7]))
        assert isclose(self.collector.abs_max_value, 16.8)
        assert self.collector.abs_max_comb == ((("D", "D2"), 1.2), (("L", "L2"), 1.6))
        assert all(isclose(self.collector.abs_max_envelope, [5.6, 11.2, 16.8]))

    def test_eval_combs_quantity_arrays(self):
        self.collector.add_load(("D", "L"), ("D1", "L1"), [1, 4, 5]*unit.lb)
        self.collector.add_load(("D", "L"), ("D2", "L2"), [2, 3, 6]*unit.lb)
        self.collector.eval_combs(self.combs)
        assert isclose(self.collector.max_value, 16.8*unit.lb)
        assert self.collector.max_comb == ((("D", "D2"), 1.2), (("L", "L2"), 1.6))
        assert all(isclose(self.collector.max_envelope, [5.6, 11.2, 16.8]*unit.lb))
        assert isclose(self.collector.min_value, 1.4*unit.lb)
        assert self.collector.min_comb == ((("D", "D1"), 1.4),)
        assert all(isclose(self.collector.min_envelope, [1.4, 4.2, 7]*unit.lb))

    def test_eval_combs_twice(self):
        self.collector.add_load(("D", "L"), ("D1", "L1"), 1)
        self.collector.add_load(("D", "L"), ("D2", "L2"), 2)
        self.collector.eval_combs(self.combs)
        self.collector.eval_combs([{"D": 1.4}])
        combs = {
            ((("D", "D1"), 1.4),): 1.4,
            ((("D", "D2"), 1.4),): 2.8
        }
        assert all([isclose(self.collector.combs[key], value) for key, value in combs.items()])
        assert set(self.collector.combs.keys()) == set(combs.keys())
        assert isclose(self.collector.max_value, 2.8)
        assert self.collector.max_comb == ((("D", "D2"), 1.4),)
        assert isclose(self.collector.min_value, 1.4)
        assert self.collector.min_comb == ((("D", "D1"), 1.4),)
