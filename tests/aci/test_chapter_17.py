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

from structuraltools.aci import chapter_17
from structuraltools.unit import unit


def test_eq_17_6_1_2():
    string, N_sa = chapter_17.eq_17_6_1_2(
        A_seN=0.5*unit.inch**2,
        f_uta=100*unit.ksi,
        f_ya=60*unit.ksi,
        precision=4)
    assert isclose(N_sa, 50000*unit.lb)
    assert N_sa.units == "lb"
    assert string == r"N_{sa} &= A_{se,N} \cdot \operatorname{min}\left(f_{uta},\ 1.9 \cdot f_{ya},\ 125\ \mathrm{ksi}\right) = 0.5\ \mathrm{in}^{2} \cdot \operatorname{min}\left(100\ \mathrm{ksi},\ 1.9 \cdot 60\ \mathrm{ksi},\ 125\ \mathrm{ksi}\right) &= 5\times 10^{4}\ \mathrm{lb}"
