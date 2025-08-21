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


from collections.abc import Iterable
from itertools import product, starmap
from typing import NamedTuple

from numpy import maximum, minimum, sign
import pandas as pd

from structuraltools.unit import Numeric, NumericArray


pd.options.mode.copy_on_write = True


def _does_not_control(testing: pd.Series, other: pd.Series) -> bool:
    """Check if all testing load combination might be the controlling load
    combination if the other load combination is also checked

    Parameters
    ==========

    testing : pd.Series
        Load combination that is currently being checked

    other : pd.Series
        Load combination that is beign checked against"""
    less_equal = all(testing.abs() <= other.abs())
    same_signs = all(sign(testing) == sign(other))
    return less_equal and same_signs

def reduce_combs(combs: pd.DataFrame) -> pd.DataFrame:
    """Reduces the provided set of load combinations to only the set of load
    combinations that may control the design

    Parameters
    ==========

    combs : pd.DataFrame
        Set of load combinations to reduce"""
    reduced_combs = pd.DataFrame(columns=combs.columns)
    for current_name in tuple(combs.index):
        current = combs.loc[current_name, :]
        combs = combs.drop(current_name)
        add_to_reduced = True
        for _, other in reduced_combs.iterrows():
            if _does_not_control(current, other):
                add_to_reduced = False
                break
        if add_to_reduced:
            for _, other in combs.iterrows():
                if _does_not_control(current, other):
                    add_to_reduced = False
                    break
        if add_to_reduced:
            reduced_combs.loc[current_name, :] = current
    return reduced_combs


class LoadCase(NamedTuple):
    kind: str
    case: str


class LoadCombResult(NamedTuple):
    name: str
    time_factor: float
    factors: dict[LoadCase, float]
    result: Numeric | NumericArray


class LoadComb:
    """Class to represent a single load combination"""
    def __init__(self, name: str, time_factor: float, **factors):
        """Create a new load combination

        Parameters
        ==========

        name : str
            Load combination name

        time_factor : float
            Time effect factor for load duration sensitive materials

        factors : float
            Load factors to use with each load kind"""
        self.name = name
        self.time_factor = time_factor
        self.factors = factors

    def eval_loads(
            self,
            loads: dict[str, dict[str, Numeric | NumericArray]],
            case_combs: list[list[LoadCase]]
            ) -> dict[str, LoadCombResult]:
        """Use the load combination to evaluate the provided loads

        Parameters
        ==========

        loads : dict[str, dict[str, Numeric | NumericArray]]
            Dictionary of load kinds and associated load cases provided by a
            LoadCollector

        case_combs : list[list[LoadCase]]
            Product expansion of the loads dictionary keys provided by the
            LoadCollector"""
        comb_results = []
        for case_comb in case_combs:
            factors = {}
            results = []
            for case in case_comb:
                factor = self.factors.get(case.kind)
                if factor:
                    factors.update({case: factor})
                    results.append(loads[case.kind][case.case]*factor)
            result = sum(results)
            comb_results.append(LoadCombResult(self.name, self.time_factor, factors, result))
        return comb_results


class LoadCollector:
    """Class to store unfactored results from load cases and factor the results
    based on a list of load cases."""
    def __init__(self):
        """Create an empty LoadCollector."""
        self.loads = {}

    def add_load(
        self,
        kind: str | Iterable[str],
        case: str | Iterable[str],
        value: Numeric | NumericArray) -> None:
        """Adds loads to the internal load dictionary and updates the cases
        dictionary.

        Parameters
        ==========

        kind : str or Iterable[str]
            Identifier for top level load organization. Load factors are applied
            at this level, so any load cases contained in this kind will use the
            load factor assigned to the kind. It is expected that this level
            will be used to organize loads by dead, live, wind, etc. If kind is
            an iterable it is zipped with case if case is also an iterable; if
            case is not an iterable the product of kind and case is taken.

        case : str or Iterable[str]
            String identifier for second level load organization. All load cases
            use the factor assigned to their load kind, so load cases can be
            used to apply separate instances of a kind of load. It is expected
            that this level will be used to distinguish between dead load and
            uplift dead load, positive and negative wind loads, etc. If case is
            an iterable and kind is not an iterable the product of kind and case
            is taken.

        value : Numeric or NumericArray
            Value to add to the load case. This can take a number of different
            types, but the type must be consistent across all values add to the
            LoadCollector."""
        if isinstance(kind, str) and isinstance(case, str):
            self.loads.update({kind: self.loads.get(kind, {})})
            self.loads[kind].update({case: self.loads[kind].get(case, 0)+value})
        else:
            if isinstance(kind, str):
                kind_case = product({kind}, case)
            elif isinstance(case, str):
                kind_case = product(kind, {case})
            else:
                kind_case = zip(kind, case)
            for kind, case in kind_case:
                self.add_load(kind, case, value)

    def eval_combs(self, combs: Iterable[dict[str, float]]) -> None:
        """Calculates the maximum and minimum factored values and envelopes for
           the specified list of load combinitions and stores the associated
           load combinations. Note: Envelopes are only calculated for
           array-like values.

           Parameters
           ==========

           combs : iterable
               Iterable of load combinations. Each load combination should
               be a dictionary with keys that match the load kinds"""
        # Generate an exhaustive list of list of LoadCase from the load
        # dictionary that includes all relevant combinations of load cases.
        load_kinds = []
        for kind, cases in self.loads.items():
            load_cases = []
            for case in cases.keys():
                load_cases.append(LoadCase(kind, case))
            load_kinds.append(load_cases)
        case_combs = list(product(*load_kinds))

        # The supplied load cases have a method to evaluate themselves for all
        # of the case combinations provided and return all of the raw results
        # as a list of LoadCombResult.
        factored_load = {"combs": []}
        for comb in combs:
            factored_load.update({
                "combs": factored_load["combs"]+comb.eval_loads(self.loads, case_combs)
            })

        # Check if the loads in the load collector are array like
        try:
            _ = factored_load["combs"][0]
            array_like = True
        except TypeError:
            array_like = False

        # Envelope the load combination results
        for comb in factored_load["combs"]:
            if array_like:
                factored_load.update({"max_envelope": maximum(
                    factored_load.get("max_envelope", comb.result), comb.result)})
                factored_load.update({"min_envelope", minimum(
                    factored_load.get("min_envelope", comb.result), comb.result)})
                max_value = max(comb.result)
                min_value = min(comb.result)
            else:
                max_value = comb.result
                min_value = comb.result
            if max_value >= factored_load.get("max_comb", comb).result:
                factored_load.update({"max_value": max_value, "max_comb": comb})
            if min_value <= factored_load.get("min_comb", comb).result:
                factored_load.update({"min_value": min_value, "min_comb": comb})

        if abs(factored_load["max_value"]) >= abs(factored_load["min_value"]):
            factored_load.update({
                "abs_max_value": abs(factored_load["max_value"]),
                "abs_max_comb": factored_load["max_comb"]
            })
        else:
            factored_load.update({
                "abs_max_value": abs(factored_load["min_value"]),
                "abs_max_comb": factored_load["min_comb"]
            })

        if array_like:
            factored_load.update({"abs_max_envelope": maximum(
                abs(factored_load["max_envelope"]), abs(factored_load["min_envelope"]))})
        else:
            factored_load.update({
                "max_envelope": [factored_load["max_value"]],
                "min_envelope": [factored_load["min_value"]],
                "abs_max_envelope": [factored_load["abs_max_value"]]
            })

        return factored_load
