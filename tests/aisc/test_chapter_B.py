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


from structuraltools.aisc import chapter_B
from structuraltools.unit import unit
from structuraltools.utils import isclose


def test_table_B4_1b_10_lamb_p():
    lamb_pf = chapter_B.table_B4_1b_10_lamb_p(
        E=29000*unit.ksi,
        F_y=50*unit.ksi,
        return_string=True)
    assert isclose(lamb_pf, 9.15161188, atol=1e-8)
    assert lamb_pf.string == r"\lambda_{pf} &= 0.38 \cdot \sqrt{\frac{E}{F_y}} = 0.38 \cdot \sqrt{\frac{29000\ \mathrm{ksi}}{50\ \mathrm{ksi}}} &= 9.152"

def test_table_B4_1b_10_lamb_r():
    lamb_rf = chapter_B.table_B4_1b_10_lamb_r(
        E=29000*unit.ksi,
        F_y=50*unit.ksi,
        return_string=True)
    assert isclose(lamb_rf, 24.08318916, atol=1e-8)
    assert lamb_rf.string == r"\lambda_{rf} &= \sqrt{\frac{E}{F_y}} = \sqrt{\frac{29000\ \mathrm{ksi}}{50\ \mathrm{ksi}}} &= 24.083"

def test_table_B4_1b_15_lamb_p():
    lamb_pw = chapter_B.table_B4_1b_15_lamb_p(
        E=29000*unit.ksi,
        F_y=50*unit.ksi,
        return_string=True)
    assert isclose(lamb_pw, 90.55279123, atol=1e-8)
    assert lamb_pw.string == r"\lambda_{pw} &= 3.76 \cdot \sqrt{\frac{E}{F_y}} = 3.76 \cdot \sqrt{\frac{29000\ \mathrm{ksi}}{50\ \mathrm{ksi}}} &= 90.553"

def test_table_B4_1b_15_lamb_r():
    lamb_rw = chapter_B.table_B4_1b_15_lamb_r(
        E=29000*unit.ksi,
        F_y=50*unit.ksi,
        return_string=True)
    assert isclose(lamb_rw, 137.2741782, atol=1e-7)
    assert lamb_rw.string == r"\lambda_{rw} &= 5.7 \cdot \sqrt{\frac{E}{F_y}} = 5.7 \cdot \sqrt{\frac{29000\ \mathrm{ksi}}{50\ \mathrm{ksi}}} &= 137.274"
