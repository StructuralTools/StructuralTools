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

from structuraltools.unit import Stress
from structuraltools.utils import Result


resources = importlib.resources.files("structuraltools.aisc.resources")

# Read chapter B templates into the templates dictionary


def table_B4_1b_10_lamb_p(E: Stress, F_y: Stress, **display_options) -> Result[float]:
    """Calculate the case 10 compact/non-compact limiting width-to-thickness
    ratio from AISC 360-22 Table B4.1b

    Parameters
    ==========

    E : Stress
        Steel modulus of elasticity

    F_y : Stress
        Steel yield stress"""
    lamb_pf = 0.38*sqrt(E/F_y).to("dimensionless").magnitude
    return templates.table_B4_1b_10_lamb_p.fill(locals(), lamb_pf, **display_options)

def table_B4_1b_10_lamb_r(E: Stress, F_y: Stress, **display_options) -> Result[float]:
    """Calculate the case 10 non-compact/slender limiting width-to-thickness
    ratio from AISC 360-22 Table B4.1b

    Parameters
    ==========

    E : Stress
        Steel modulus of elasticity

    F_y : Stress
        Steel yield stress"""
    lamb_rf = sqrt(E/F_y).to("dimensionless").magnitude
    return templates.table_B4_1b_10_lamb_r.fill(locals(), lamb_rf, **display_options)

def table_B4_1b_15_lamb_p(E: Stress, F_y: Stress, **display_options) -> Result[float]:
    """Calculate the case 15 compact/non-compact limiting width-to-thickness
    ratio from AISC 360-22 Table B4.1b

    Parameters
    ==========

    E : Stress
        Steel modulus of elasticity

    F_y : Stress
        Steel yield stress"""
    lamb_pw = 3.76*sqrt(E/F_y).to("dimensionless").magnitude
    return templates.table_B4_1b_15_lamb_p.fill(locals(), lamb_pw, **display_options)

def table_B4_1b_15_lamb_r(E: Stress, F_y: Stress, **display_options) -> Result[float]:
    """Calculate the case 15 non-compact/slender limiting width-to-thickness
    ratio from AISC 360-22 Table B4.1b

    Parameters
    ==========

    E : Stress
        Steel modulus of elasticity

    F_y : Stress
        Steel yield stress"""
    lamb_rw = 5.7*sqrt(E/F_y).to("dimensionless").magnitude
    return templates.table_B4_1b_15_lamb_r.fill(locals(), lamb_rw, **display_options)
