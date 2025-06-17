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
        # Expand the provided load combinations
        full_keys = map(lambda x: tuple(product({x[0]}, x[1].keys())), self.loads.items())
        to_merge = product(product(*full_keys), combs)

        def merge_factors(keys: tuple[str, str], factors: dict[str, float]
                          ) -> tuple[tuple[tuple[str, str], float], ...]:
            return tuple((key, x) for key in keys if (x := factors.get(key[0])))
        combs = set(filter(None, starmap(merge_factors, to_merge)))

        # Analyze each load combination and store extreme values
        extremes = {}
        self.combs = {}
        for comb in combs:
            result = sum(map(lambda x: self.loads[x[0][0]][x[0][1]]*x[1], comb))
            self.combs.update({comb: result})
            if isinstance(getattr(result, "magnitude", result), Iterable):
                extremes.update({"max_envelope":
                    maximum(extremes.get("max_envelope", result), result)})
                extremes.update({"min_envelope":
                    minimum(extremes.get("min_envelope", result), result)})
                max_value = max(result)
                min_value = min(result)
            else:
                max_value = result
                min_value = result
            if max_value >= extremes.get("max_value", max_value):
                extremes.update({"max_value": max_value, "max_comb": comb})
            if min_value <= extremes.get("min_value", min_value):
                extremes.update({"min_value": min_value, "min_comb": comb})

        # Calculate absolute max values
        if extremes.get("max_envelope") is not None:
            extremes.update({"abs_max_envelope": maximum(
                abs(extremes["max_envelope"]), abs(extremes["min_envelope"]))})
        if abs(extremes["max_value"]) >= abs(extremes["min_value"]):
            extremes.update({
                "abs_max_value": abs(extremes["max_value"]),
                "abs_max_comb": extremes["max_comb"]
            })
        else:
            extremes.update({
                "abs_max_value": abs(extremes["min_value"]),
                "abs_max_comb": extremes["min_comb"]
            })

        # Store results as attributes
        for attr, value in extremes.items():
            setattr(self, attr, value)
