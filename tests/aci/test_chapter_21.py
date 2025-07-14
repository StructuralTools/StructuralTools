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

from structuraltools.aci import chapter_21, materials
from structuraltools.unit import unit


def test_calc_phi_compression_controlled():
    rebar = materials.Rebar(4)
    string, phi = chapter_21.table_21_2_2(rebar, 0.002, precision=4)
    assert phi == 0.65
    assert string == r"""\begin{aligned}
    & \text{Since, } \left(\epsilon_t \leq \epsilon_{ty} \Leftarrow 0.002 \leq 0.002069\right): & \phi &= 0.65
\end{aligned}"""

def test_calc_phi_transition():
    rebar = materials.Rebar(4)
    string, phi = chapter_21.table_21_2_2(rebar, 0.003, precision=4)
    assert isclose(phi, 0.7275862083, atol=1e-8)
    assert string == r"""\begin{aligned}
    & \text{Since, } \left(\epsilon_{ty} < \epsilon_t < \epsilon_{ty} + 0.003 \Leftarrow 0.002069 < 0.003 < 0.005069\right):
        \\[10pt]
        & \qquad \phi = 0.65 + 0.25 \cdot \frac{\epsilon_t - \epsilon_{ty}}{0.003} = 0.65 + 0.25 \cdot \frac{0.003 - 0.002069}{0.003} &= 0.7276
\end{aligned}"""

def test_calc_phi_tension_controlled():
    rebar = materials.Rebar(4)
    string, phi = chapter_21.table_21_2_2(rebar, 0.006, precision=4)
    assert phi == 0.9
    assert string == r"""\begin{aligned}
    & \text{Since, } \left(\epsilon_t \geq \epsilon_{ty} +0.003 \Leftarrow 0.006 \geq 0.005069\right): & \phi &= 0.9
\end{aligned}"""
