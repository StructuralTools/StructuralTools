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


from structuraltools import materials
from structuraltools.aci import chapter_25
from structuraltools.unit import unit
from structuraltools.utils import isclose


def test_eq_25_4_2_4a():
    l_prime_d = chapter_25.eq_25_4_2_4a(
        f_y=60*unit.ksi,
        psi_t=1,
        psi_e=1,
        psi_s=1,
        psi_g=1,
        lamb=1,
        f_prime_c=4000*unit.psi,
        c_b=3*unit.inch,
        K_tr=0.658*unit.inch,
        d_b=1*unit.inch,
        return_string=True)
    assert isclose(l_prime_d, 19.4508604*unit.inch, atol=1e-7*unit.inch)
    assert l_prime_d.string == r"""l'_d &= \left(\frac{3 \cdot f_y \cdot \operatorname{min}\left(\psi_t \cdot \psi_e ,\ 1.7\right) \cdot \psi_s \cdot \psi_g}{40 \cdot \lambda \cdot \sqrt{f'_c} \cdot \left(\frac{c_b + K_{tr}}{d_b}\right)}\right) \cdot d_b
    \\
    &= \left(\frac{3 \cdot 60\ \mathrm{ksi} \cdot \operatorname{min}\left(1 \cdot 1 ,\ 1.7\right) \cdot 1 \cdot 1}{40 \cdot 1 \cdot \sqrt{4000\ \mathrm{psi}} \cdot \left(\frac{3\ \mathrm{in} + 0.658\ \mathrm{in}}{1\ \mathrm{in}}\right)}\right) \cdot 1\ \mathrm{in}
    \\
    &= 19.451\ \mathrm{in}"""

def test_eq_25_4_2_4b():
    K_tr = chapter_25.eq_25_4_2_4b(
        A_tr=0.79*unit.inch**2,
        s=12*unit.inch,
        n=4,
        return_string=True)
    assert isclose(K_tr, 0.6583333333*unit.inch, atol=1e-10*unit.inch)
    assert K_tr.string == r"K_{tr} &= \frac{40 \cdot A_{tr}}{s \cdot n} = \frac{40 \cdot 0.79\ \mathrm{in}^{2}}{12\ \mathrm{in} \cdot 4} &= 0.658\ \mathrm{in}"

def test_table_25_4_2_5_lamb_light():
    lamb = chapter_25.table_25_4_2_5_lamb(110*unit.pcf, return_string=True)
    assert lamb == 0.75
    assert lamb.string == r"\text{Since, } & \left(w_c < 135\ \mathrm{pcf} \Leftarrow 110\ \mathrm{pcf} < 135\ \mathrm{pcf}\right): & \lambda &= 0.75"

def test_table_25_4_2_5_lamb_normal():
    lamb = chapter_25.table_25_4_2_5_lamb(145*unit.pcf, return_string=True)
    assert lamb == 1
    assert lamb.string == r"\text{Since, } & \left(w_c \geq 135\ \mathrm{pcf} \Leftarrow 145\ \mathrm{pcf} \geq 135\ \mathrm{pcf}\right): & \lambda &= 1"

def test_table_25_4_2_5_psi_g_low():
    psi_g = chapter_25.table_25_4_2_5_psi_g(60000*unit.psi, return_string=True)
    assert psi_g == 1
    assert psi_g.string == r"\text{Since, } & \left(f_y \leq 60\ \mathrm{ksi} \Leftarrow 60\ \mathrm{ksi} \leq 60\ \mathrm{ksi}\right): & \psi_g &= 1"

def test_table_25_4_2_5_psi_g_mid():
    psi_g = chapter_25.table_25_4_2_5_psi_g(80*unit.ksi, return_string=True)
    assert psi_g == 1.15
    assert psi_g.string == r"\text{Since, } & \left(60\ \mathrm{ksi} < f_y \leq 80\ \mathrm{ksi} \Leftarrow 60\ \mathrm{ksi} < 80\ \mathrm{ksi} \leq 80\ \mathrm{ksi}\right): & \psi_g &= 1.15"

def test_table_25_4_2_5_psi_g_high():
    psi_g = chapter_25.table_25_4_2_5_psi_g(100*unit.ksi, return_string=True)
    assert psi_g == 1.3
    assert psi_g.string == r"\text{Since, } & \left(f_y > 80\ \mathrm{ksi} \Leftarrow 100\ \mathrm{ksi} > 80\ \mathrm{ksi}\right): & \psi_g &= 1.3"

def test_table_25_4_2_5_psi_e_c_c():
    psi_e = chapter_25.table_25_4_2_5_psi_e(
        coated=True,
        d_b=1*unit.inch,
        c_c=2.5*unit.inch,
        s=8*unit.inch,
        return_string=True)
    assert psi_e == 1.5
    assert psi_e.string == r"\text{Since, } & \left(\mathrm{coated} = \mathrm{True}\right) \text{ and } \left(c_c < 3 \cdot d_b \Leftarrow 2.5\ \mathrm{in} < 3\ \mathrm{in}\right): & \psi_e &= 1.5"

def test_table_25_4_2_5_psi_e_s():
    psi_e = chapter_25.table_25_4_2_5_psi_e(
        coated=True,
        d_b=1*unit.inch,
        c_c=4*unit.inch,
        s=6*unit.inch,
        return_string=True)
    assert psi_e == 1.5
    assert psi_e.string == r"\text{Since, } & \left(\mathrm{coated} = \mathrm{True}\right) \text{ and } \left(s < 7 \cdot d_b \Leftarrow 6\ \mathrm{in} < 7\ \mathrm{in}\right): & \psi_e &= 1.5"

def test_table_25_4_2_5_psi_e_true():
    psi_e = chapter_25.table_25_4_2_5_psi_e(
        coated=True,
        d_b=1*unit.inch,
        c_c=4*unit.inch,
        s=8*unit.inch,
        return_string=True)
    assert psi_e == 1.2
    assert psi_e.string == r"\text{Since, } & \left(\mathrm{coated} = \mathrm{True}\right): & \psi_e &= 1.2"

def test_table_25_4_2_5_psi_e_false():
    psi_e = chapter_25.table_25_4_2_5_psi_e(
        coated=False,
        d_b=1*unit.inch,
        c_c=4*unit.inch,
        s=6*unit.inch,
        return_string=True)
    assert psi_e == 1
    assert psi_e.string == r"\text{Since, } & \left(\mathrm{coated} = \mathrm{False}\right): & \psi_e &= 1"

def test_table_25_4_2_5_psi_s_big():
    psi_s = chapter_25.table_25_4_2_5_psi_s(True, 8, return_string=True)
    assert psi_s == 1
    assert psi_s.string == r"\text{Since, } & \left(\text{Rebar size} \geq 7\right): & \psi_s &= 1"

def test_table_25_4_2_5_psi_s_used():
    psi_s = chapter_25.table_25_4_2_5_psi_s(True, 6, return_string=True)
    assert psi_s == 0.8
    assert psi_s.string == r"\text{Since, } & \left(\text{Rebar size} \leq 6\right): & \psi_s &= 0.8"

def test_table_25_4_2_5_psi_s_small():
    psi_s = chapter_25.table_25_4_2_5_psi_s(False, 6, return_string=True)
    assert psi_s == 1
    assert psi_s.string == r"\text{Since, } & \left(\psi_s \text{ not applied}\right): & \psi_s &= 1"

def test_table_25_4_2_5_psi_t_true():
    psi_t = chapter_25.table_25_4_2_5_psi_t(True, return_string=True)
    assert psi_t == 1.3
    assert psi_t.string == r"\text{Since, } & \left(\text{Concrete below} > 12\ \mathrm{in}\right): & \psi_t &= 1.3"

def test_table_25_4_2_5_psi_t_false():
    psi_t = chapter_25.table_25_4_2_5_psi_t(False, return_string=True)
    assert psi_t == 1
    assert psi_t.string == r"\text{Since, } & \left(\text{Concrete below} \leq 12\ \mathrm{in}\right): & \psi_t &= 1"

def test_table_25_4_2_5_test_1():
    concrete = materials.Concrete(6000*unit.psi, w_c=110*unit.pcf)
    rebar = materials.Rebar(8, coated=True)
    results = chapter_25.table_25_4_2_5(
        rebar=rebar,
        concrete=concrete,
        c_c=2*unit.inch,
        s=6*unit.inch,
        use_psi_s=False,
        concrete_below=True,
        return_string=True)
    assert results == (0.75, 1, 1.5, 1, 1.3)
    assert results.string == r"""\begin{aligned}
    \text{Since, } & \left(w_c < 135\ \mathrm{pcf} \Leftarrow 110\ \mathrm{pcf} < 135\ \mathrm{pcf}\right): & \lambda &= 0.75
    \\[10pt]
    \text{Since, } & \left(f_y \leq 60\ \mathrm{ksi} \Leftarrow 60\ \mathrm{ksi} \leq 60\ \mathrm{ksi}\right): & \psi_g &= 1
    \\[10pt]
    \text{Since, } & \left(\mathrm{coated} = \mathrm{True}\right) \text{ and } \left(c_c < 3 \cdot d_b \Leftarrow 2\ \mathrm{in} < 3.0\ \mathrm{in}\right): & \psi_e &= 1.5
    \\[10pt]
    \text{Since, } & \left(\text{Rebar size} \geq 7\right): & \psi_s &= 1
    \\[10pt]
    \text{Since, } & \left(\text{Concrete below} > 12\ \mathrm{in}\right): & \psi_t &= 1.3
\end{aligned}"""

def test_table_25_4_2_5_test_2():
    concrete = materials.Concrete(4000*unit.psi)
    rebar = materials.Rebar(4, f_y=80*unit.ksi, coated=True)
    results = chapter_25.table_25_4_2_5(
        rebar=rebar,
        concrete=concrete,
        c_c=3*unit.inch,
        s=3*unit.inch,
        use_psi_s=False,
        concrete_below=False,
        return_string=True)
    assert results == (1, 1.15, 1.5, 1, 1)
    assert results.string == r"""\begin{aligned}
    \text{Since, } & \left(w_c \geq 135\ \mathrm{pcf} \Leftarrow 150\ \mathrm{pcf} \geq 135\ \mathrm{pcf}\right): & \lambda &= 1
    \\[10pt]
    \text{Since, } & \left(60\ \mathrm{ksi} < f_y \leq 80\ \mathrm{ksi} \Leftarrow 60\ \mathrm{ksi} < 80\ \mathrm{ksi} \leq 80\ \mathrm{ksi}\right): & \psi_g &= 1.15
    \\[10pt]
    \text{Since, } & \left(\mathrm{coated} = \mathrm{True}\right) \text{ and } \left(s < 7 \cdot d_b \Leftarrow 3\ \mathrm{in} < 3.5\ \mathrm{in}\right): & \psi_e &= 1.5
    \\[10pt]
    \text{Since, } & \left(\psi_s \text{ not applied}\right): & \psi_s &= 1
    \\[10pt]
    \text{Since, } & \left(\text{Concrete below} \leq 12\ \mathrm{in}\right): & \psi_t &= 1
\end{aligned}"""

def test_table_25_4_2_5_test_3():
    concrete = materials.Concrete(4000*unit.psi)
    rebar = materials.Rebar(4, f_y=100*unit.ksi, coated=True)
    results = chapter_25.table_25_4_2_5(
        rebar=rebar,
        concrete=concrete,
        c_c=3*unit.inch,
        s=12*unit.inch,
        use_psi_s=True,
        concrete_below=False,
        return_string=True)
    assert results == (1, 1.3, 1.2, 0.8, 1)
    assert results.string == r"""\begin{aligned}
    \text{Since, } & \left(w_c \geq 135\ \mathrm{pcf} \Leftarrow 150\ \mathrm{pcf} \geq 135\ \mathrm{pcf}\right): & \lambda &= 1
    \\[10pt]
    \text{Since, } & \left(f_y > 80\ \mathrm{ksi} \Leftarrow 100\ \mathrm{ksi} > 80\ \mathrm{ksi}\right): & \psi_g &= 1.3
    \\[10pt]
    \text{Since, } & \left(\mathrm{coated} = \mathrm{True}\right): & \psi_e &= 1.2
    \\[10pt]
    \text{Since, } & \left(\text{Rebar size} \leq 6\right): & \psi_s &= 0.8
    \\[10pt]
    \text{Since, } & \left(\text{Concrete below} \leq 12\ \mathrm{in}\right): & \psi_t &= 1
\end{aligned}"""

def test_table_25_4_2_5_test_4():
    concrete = materials.Concrete(4000*unit.psi)
    rebar = materials.Rebar(8)
    results = chapter_25.table_25_4_2_5(
        rebar=rebar,
        concrete=concrete,
        c_c=3*unit.inch,
        s=12*unit.inch,
        use_psi_s=False,
        concrete_below=False,
        return_string=True)
    assert results == (1, 1, 1, 1, 1)
    assert results.string == r"""\begin{aligned}
    \text{Since, } & \left(w_c \geq 135\ \mathrm{pcf} \Leftarrow 150\ \mathrm{pcf} \geq 135\ \mathrm{pcf}\right): & \lambda &= 1
    \\[10pt]
    \text{Since, } & \left(f_y \leq 60\ \mathrm{ksi} \Leftarrow 60\ \mathrm{ksi} \leq 60\ \mathrm{ksi}\right): & \psi_g &= 1
    \\[10pt]
    \text{Since, } & \left(\mathrm{coated} = \mathrm{False}\right): & \psi_e &= 1
    \\[10pt]
    \text{Since, } & \left(\text{Rebar size} \geq 7\right): & \psi_s &= 1
    \\[10pt]
    \text{Since, } & \left(\text{Concrete below} \leq 12\ \mathrm{in}\right): & \psi_t &= 1
\end{aligned}"""
