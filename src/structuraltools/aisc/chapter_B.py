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

from numpy import sqrt

from structuraltools.unit import Stress
from structuraltools.utils import fill_template, Result


resources = importlib.resources.files("structuraltools.aisc.resources")
with open(resources.joinpath("chapter_B_templates_processed.json")) as file:
    templates = json.load(file)


def table_B4_1b_10_lamb_p(E: Stress, F_y: Stress, **string_options) -> Result[float]:
    """Calculate the case 10 compact/non-compact limiting width-to-thickness
    ratio from AISC 360-22 Table B4.1b

    Parameters
    ==========

    E : Stress
        Steel modulus of elasticity

    F_y : Stress
        Steel yield stress"""
    lamb_pf = 0.38*sqrt(E/F_y).to("dimensionless").magnitude
    return fill_template(lamb_pf, templates["table_B4_1b_10_lamb_p"], locals(), **string_options)

def table_B4_1b_10_lamb_r(E: Stress, F_y: Stress, **string_options) -> Result[float]:
    """Calculate the case 10 non-compact/slender limiting width-to-thickness
    ratio from AISC 360-22 Table B4.1b

    Parameters
    ==========

    E : Stress
        Steel modulus of elasticity

    F_y : Stress
        Steel yield stress"""
    lamb_rf = sqrt(E/F_y).to("dimensionless").magnitude
    return fill_template(lamb_rf, templates["table_B4_1b_10_lamb_r"], locals(), **string_options)

def table_B4_1b_15_lamb_p(E: Stress, F_y: Stress, **string_options) -> Result[float]:
    """Calculate the case 15 compact/non-compact limiting width-to-thickness
    ratio from AISC 360-22 Table B4.1b

    Parameters
    ==========

    E : Stress
        Steel modulus of elasticity

    F_y : Stress
        Steel yield stress"""
    lamb_pw = 3.76*sqrt(E/F_y).to("dimensionless").magnitude
    return fill_template(lamb_pw, templates["table_B4_1b_15_lamb_p"], locals(), **string_options)

def table_B4_1b_15_lamb_r(E: Stress, F_y: Stress, **string_options) -> Result[float]:
    """Calculate the case 15 non-compact/slender limiting width-to-thickness
    ratio from AISC 360-22 Table B4.1b

    Parameters
    ==========

    E : Stress
        Steel modulus of elasticity

    F_y : Stress
        Steel yield stress"""
    lamb_rw = 5.7*sqrt(E/F_y).to("dimensionless").magnitude
    return fill_template(lamb_rw, templates["table_B4_1b_15_lamb_r"], locals(), **string_options)
