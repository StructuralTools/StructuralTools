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


from copy import copy
import importlib.resources
import json

from structuraltools.utils import round_to


resources = importlib.resources.files("structuraltools.awc.resources")
with open(resources.joinpath("chapter_2_data.json")) as file:
    chapter_2_data = json.load(file)


def sec_2_3_3(temperature: float, wet_service: bool) -> dict[str: float]:
    """Determine the temperature factor according to
    Section 2.3.3 of the 2024 NDS

    Parameters
    ==========

    temperature : float
        Service temperature

    wet_service : bool
        Boolean indicating if the wet service factor should be applied"""
    temperature = str(min(max(100, round_to(temperature, 25)), 150))
    print(temperature)
    wet_service = "wet" if wet_service else "dry"
    C_t = copy(chapter_2_data["C_t"][wet_service][temperature])
    return C_t
