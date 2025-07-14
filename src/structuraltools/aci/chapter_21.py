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


import importlib.resources
import json

from structuraltools.aci import materials
from structuraltools.utils import fill_template, Result


resources = importlib.resources.files("structuraltools.aci.resources")
with open(resources.joinpath("chapter_21_templates_processed.json")) as file:
    templates = json.load(file)


def table_21_2_2(rebar: materials.Rebar, epsilon_t: float, **string_options
                 ) ->  Result[float]:
    """ACI 318-19 Table 21.2.2

    Parameters
    ==========

    rebar : structuraltools.aci.materials.Rebar
        Rebar with the highest tensile stress in the cross-section

    epsilon_t : float
        Net tensile strain in the extreme layer of longitudinal tension
        reinforcement at nominal strength, excluding strains due to effective
        prestress, creep, shrinkage, and temperature."""
    epsilon_ty = (rebar.f_y/rebar.E_s).to("dimensionless").magnitude
    epsilon_ty003 = epsilon_ty+0.003
    if epsilon_t <= epsilon_ty:
        phi = 0.65
        template = templates["table_21_2_2_compression"]
    elif  epsilon_t < epsilon_ty003:
        phi = 0.65+0.25*(epsilon_t-epsilon_ty)/0.003
        template = templates["table_21_2_2_transition"]
    else:
        phi = 0.9
        template = templates["table_21_2_2_tension"]
    return fill_template(phi, template, locals(), **string_options)
