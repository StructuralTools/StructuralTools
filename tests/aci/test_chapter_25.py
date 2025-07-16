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

from structuraltools.aci import chapter_25, materials
from structuraltools.unit import unit


def test_eq_25_4_2_4a():
    string, l_prime_d = chapter_25.eq_25_4_2_4a(
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
        precision=4)
    assert isclose(l_prime_d, 19.4508604*unit.inch, atol=1e-7*unit.inch)
    assert string == r"l'_d &= \left(\frac{3 \cdot f_y \cdot \operatorname{min}\left(\psi_t \cdot \psi_e,\ 1.7\right) \cdot \psi_s \cdot \psi_g}{40 \cdot \lambda \cdot \sqrt{f'_c} \cdot \left(\frac{c_b + K_{tr}}{d_b}\right)}\right) \cdot d_b = \left(\frac{3 \cdot 60\ \mathrm{ksi} \cdot \operatorname{min}\left(1 \cdot 1,\ 1.7\right) \cdot 1 \cdot 1}{40 \cdot 1 \cdot \sqrt{4000\ \mathrm{psi}} \cdot \left(\frac{3\ \mathrm{in} + 0.658\ \mathrm{in}}{1\ \mathrm{in}}\right)}\right) \cdot 1\ \mathrm{in} &= 19.45\ \mathrm{in}"

def test_eq_25_4_2_4b():
    string, K_tr = chapter_25.eq_25_4_2_4b(
        A_tr=0.79*unit.inch**2,
        s=12*unit.inch,
        n=4,
        precision=4)
    assert isclose(K_tr, 0.6583333333*unit.inch, atol=1e-10*unit.inch)
    assert string == r"K_{tr} &= \frac{40 \cdot A_{tr}}{s \cdot n} = \frac{40 \cdot 0.79\ \mathrm{in}^{2}}{12\ \mathrm{in} \cdot 4} &= 0.6583\ \mathrm{in}"

def test_table_25_4_2_5_lamb_light():
    string, lamb = chapter_25.table_25_4_2_5_lamb(110*unit.pcf, precision=4)
    assert lamb == 0.75
    assert string == r"\text{Since, } & \left(w_c < 135\ \mathrm{pcf} \Leftarrow 110\ \mathrm{pcf} < 135\ \mathrm{pcf}\right): & \lambda &= 0.75"

def test_table_25_4_2_5_lamb_normal():
    string, lamb = chapter_25.table_25_4_2_5_lamb(145*unit.pcf, precision=4)
    assert lamb == 1
    assert string == r"\text{Since, } & \left(w_c \geq 135\ \mathrm{pcf} \Leftarrow 145\ \mathrm{pcf} \geq 135\ \mathrm{pcf}\right): & \lambda &= 1"

def test_table_25_4_2_5_psi_g_low():
    string, psi_g = chapter_25.table_25_4_2_5_psi_g(60000*unit.psi, precision=4)
    assert psi_g == 1
    assert string == r"\text{Since, } & \left(f_y \leq 60\ \mathrm{ksi} \Leftarrow 60\ \mathrm{ksi} \leq 60\ \mathrm{ksi}\right): & \psi_g &= 1"

def test_table_25_4_2_5_psi_g_mid():
    string, psi_g = chapter_25.table_25_4_2_5_psi_g(80*unit.ksi, precision=4)
    assert psi_g == 1.15
    assert string == r"\text{Since, } & \left(60\ \mathrm{ksi} < f_y \leq 80\ \mathrm{ksi} \Leftarrow 60\ \mathrm{ksi} < 80\ \mathrm{ksi} \leq 80\ \mathrm{ksi}\right): & \psi_g &= 1.15"

def test_table_25_4_2_5_psi_g_high():
    string, psi_g = chapter_25.table_25_4_2_5_psi_g(100*unit.ksi, precision=4)
    assert psi_g == 1.3
    assert string == r"\text{Since, } & \left(f_y > 80\ \mathrm{ksi} \Leftarrow 100\ \mathrm{ksi} > 80\ \mathrm{ksi}\right): & \psi_g &= 1.3"

def test_table_25_4_2_5_psi_e_c_c():
    string, psi_e = chapter_25.table_25_4_2_5_psi_e(
        coated=True,
        d_b=1*unit.inch,
        c_c=2.5*unit.inch,
        s=8*unit.inch,
        precision=4)
    assert psi_e == 1.5
    assert string == r"\text{Since, } & \left(\mathrm{coated} = \mathrm{True}\right) \text{ and } \left(c_c < 3 \cdot d_b \Leftarrow 2.5\ \mathrm{in} < 3\ \mathrm{in}\right): & \psi_e &= 1.5"

def test_table_25_4_2_5_psi_e_s():
    string, psi_e = chapter_25.table_25_4_2_5_psi_e(
        coated=True,
        d_b=1*unit.inch,
        c_c=4*unit.inch,
        s=6*unit.inch,
        precision=4)
    assert psi_e == 1.5
    assert string == r"\text{Since, } & \left(\mathrm{coated} = \mathrm{True}\right) \text{ and } \left(s < 7 \cdot d_b \Leftarrow 6\ \mathrm{in} < 7\ \mathrm{in}\right): & \psi_e &= 1.5"

def test_table_25_4_2_5_psi_e_true():
    string, psi_e = chapter_25.table_25_4_2_5_psi_e(
        coated=True,
        d_b=1*unit.inch,
        c_c=4*unit.inch,
        s=8*unit.inch,
        precision=4)
    assert psi_e == 1.2
    assert string == r"\text{Since, } & \left(\mathrm{coated} = \mathrm{True}\right): & \psi_e &= 1.2"

def test_table_25_4_2_5_psi_e_false():
    string, psi_e = chapter_25.table_25_4_2_5_psi_e(
        coated=False,
        d_b=1*unit.inch,
        c_c=4*unit.inch,
        s=6*unit.inch,
        precision=4)
    assert psi_e == 1
    assert string == r"\text{Since, } & \left(\mathrm{coated} = \mathrm{False}\right): & \psi_e &= 1"

def test_table_25_4_2_5_psi_s_big():
    string, psi_s = chapter_25.table_25_4_2_5_psi_s(True, 8, precision=4)
    assert psi_s == 1
    assert string == r"\text{Since, } & \left(\text{Rebar size} \geq 7\right): & \psi_s &= 1"

def test_table_25_4_2_5_psi_s_used():
    string, psi_s = chapter_25.table_25_4_2_5_psi_s(True, 6, precision=4)
    assert psi_s == 0.8
    assert string == r"\text{Since, } & \left(\text{Rebar size} \leq 6\right): & \psi_s &= 0.8"

def test_table_25_4_2_5_psi_s_small():
    string, psi_s = chapter_25.table_25_4_2_5_psi_s(False, 6, precision=4)
    assert psi_s == 1
    assert string == r"\text{Since, } & \left(\psi_s \text{ not applied}\right): & \psi_s &= 1"

def test_table_25_4_2_5_psi_t_true():
    string, psi_t = chapter_25.table_25_4_2_5_psi_t(True, precision=4)
    assert psi_t == 1.3
    assert string == r"\text{Since, } & \left(\text{Concrete below} > 12\ \mathrm{in}\right): & \psi_t &= 1.3"

def test_table_25_4_2_5_psi_t_false():
    string, psi_t = chapter_25.table_25_4_2_5_psi_t(False, precision=4)
    assert psi_t == 1
    assert string == r"\text{Since, } & \left(\text{Concrete below} \leq 12\ \mathrm{in}\right): & \psi_t &= 1"

def test_table_25_4_2_5_test_1():
    concrete = materials.Concrete(6000*unit.psi, w_c=110*unit.pcf)
    rebar = materials.Rebar(8, coated=True)
    string, results = chapter_25.table_25_4_2_5(
        rebar=rebar,
        concrete=concrete,
        c_c=2*unit.inch,
        s=6*unit.inch,
        use_psi_s=False,
        concrete_below=True,
        precision=4)
    assert results == {"lamb": 0.75, "psi_g": 1, "psi_e": 1.5, "psi_s": 1, "psi_t": 1.3}
    assert string == r"""$$
\begin{aligned}
    \text{Since, } & \left(w_c < 135\ \mathrm{pcf} \Leftarrow 110\ \mathrm{pcf} < 135\ \mathrm{pcf}\right): & \lambda &= 0.75
    \\[10pt]
    \text{Since, } & \left(f_y \leq 60\ \mathrm{ksi} \Leftarrow 60\ \mathrm{ksi} \leq 60\ \mathrm{ksi}\right): & \psi_g &= 1
    \\[10pt]
    \text{Since, } & \left(\mathrm{coated} = \mathrm{True}\right) \text{ and } \left(c_c < 3 \cdot d_b \Leftarrow 2\ \mathrm{in} < 3\ \mathrm{in}\right): & \psi_e &= 1.5
    \\[10pt]
    \text{Since, } & \left(\text{Rebar size} \geq 7\right): & \psi_s &= 1
    \\[10pt]
    \text{Since, } & \left(\text{Concrete below} > 12\ \mathrm{in}\right): & \psi_t &= 1.3
\end{aligned}
$$"""

def test_table_25_4_2_5_test_2():
    concrete = materials.Concrete(4000*unit.psi)
    rebar = materials.Rebar(4, f_y=80*unit.ksi, coated=True)
    string, results = chapter_25.table_25_4_2_5(
        rebar=rebar,
        concrete=concrete,
        c_c=3*unit.inch,
        s=3*unit.inch,
        use_psi_s=False,
        concrete_below=False,
        precision=4)
    assert results == {"lamb": 1, "psi_g": 1.15, "psi_e": 1.5, "psi_s": 1, "psi_t": 1}
    assert string == r"""$$
\begin{aligned}
    \text{Since, } & \left(w_c \geq 135\ \mathrm{pcf} \Leftarrow 150\ \mathrm{pcf} \geq 135\ \mathrm{pcf}\right): & \lambda &= 1
    \\[10pt]
    \text{Since, } & \left(60\ \mathrm{ksi} < f_y \leq 80\ \mathrm{ksi} \Leftarrow 60\ \mathrm{ksi} < 80\ \mathrm{ksi} \leq 80\ \mathrm{ksi}\right): & \psi_g &= 1.15
    \\[10pt]
    \text{Since, } & \left(\mathrm{coated} = \mathrm{True}\right) \text{ and } \left(s < 7 \cdot d_b \Leftarrow 3\ \mathrm{in} < 3.5\ \mathrm{in}\right): & \psi_e &= 1.5
    \\[10pt]
    \text{Since, } & \left(\psi_s \text{ not applied}\right): & \psi_s &= 1
    \\[10pt]
    \text{Since, } & \left(\text{Concrete below} \leq 12\ \mathrm{in}\right): & \psi_t &= 1
\end{aligned}
$$"""

def test_table_25_4_2_5_test_3():
    concrete = materials.Concrete(4000*unit.psi)
    rebar = materials.Rebar(4, f_y=100*unit.ksi, coated=True)
    string, results = chapter_25.table_25_4_2_5(
        rebar=rebar,
        concrete=concrete,
        c_c=3*unit.inch,
        s=12*unit.inch,
        use_psi_s=True,
        concrete_below=False,
        precision=4)
    assert results == {"lamb": 1, "psi_g": 1.3, "psi_e": 1.2, "psi_s": 0.8, "psi_t": 1}
    assert string == r"""$$
\begin{aligned}
    \text{Since, } & \left(w_c \geq 135\ \mathrm{pcf} \Leftarrow 150\ \mathrm{pcf} \geq 135\ \mathrm{pcf}\right): & \lambda &= 1
    \\[10pt]
    \text{Since, } & \left(f_y > 80\ \mathrm{ksi} \Leftarrow 100\ \mathrm{ksi} > 80\ \mathrm{ksi}\right): & \psi_g &= 1.3
    \\[10pt]
    \text{Since, } & \left(\mathrm{coated} = \mathrm{True}\right): & \psi_e &= 1.2
    \\[10pt]
    \text{Since, } & \left(\text{Rebar size} \leq 6\right): & \psi_s &= 0.8
    \\[10pt]
    \text{Since, } & \left(\text{Concrete below} \leq 12\ \mathrm{in}\right): & \psi_t &= 1
\end{aligned}
$$"""

def test_table_25_4_2_5_test_4():
    concrete = materials.Concrete(4000*unit.psi)
    rebar = materials.Rebar(8)
    string, results = chapter_25.table_25_4_2_5(
        rebar=rebar,
        concrete=concrete,
        c_c=3*unit.inch,
        s=12*unit.inch,
        use_psi_s=False,
        concrete_below=False,
        precision=4)
    assert results == {"lamb": 1, "psi_g": 1, "psi_e": 1, "psi_s": 1, "psi_t": 1}
    assert string == r"""$$
\begin{aligned}
    \text{Since, } & \left(w_c \geq 135\ \mathrm{pcf} \Leftarrow 150\ \mathrm{pcf} \geq 135\ \mathrm{pcf}\right): & \lambda &= 1
    \\[10pt]
    \text{Since, } & \left(f_y \leq 60\ \mathrm{ksi} \Leftarrow 60\ \mathrm{ksi} \leq 60\ \mathrm{ksi}\right): & \psi_g &= 1
    \\[10pt]
    \text{Since, } & \left(\mathrm{coated} = \mathrm{False}\right): & \psi_e &= 1
    \\[10pt]
    \text{Since, } & \left(\text{Rebar size} \geq 7\right): & \psi_s &= 1
    \\[10pt]
    \text{Since, } & \left(\text{Concrete below} \leq 12\ \mathrm{in}\right): & \psi_t &= 1
\end{aligned}
$$"""

def test_eq_25_4_3_1a():
    string, l_prime_dh = chapter_25.eq_25_4_3_1a(
        f_y=60*unit.ksi,
        psi_e=1,
        psi_r=1,
        psi_o=1,
        psi_c=1,
        lamb=1,
        f_prime_c=6000*unit.psi,
        d_b=1*unit.inch,
        precision=4)
    assert isclose(l_prime_dh, 14.0835758*unit.inch, atol=1e-7*unit.inch)
    assert string == r"l'_{dh} &= \left(\frac{f_y \cdot \psi_e \cdot \psi_r \cdot \psi_o \cdot \psi_c}{55 \cdot \lambda \cdot \sqrt{f'_c}}\right) \cdot d_b^{1.5} = \left(\frac{60\ \mathrm{ksi} \cdot 1 \cdot 1 \cdot 1 \cdot 1}{55 \cdot 1 \cdot \sqrt{6000\ \mathrm{psi}}}\right) \cdot \left(1\ \mathrm{in}\right)^{1.5} &= 14.08\ \mathrm{in}"

def test_table_25_4_3_2_lamb_light():
    string, lamb = chapter_25.table_25_4_3_2_lamb(110*unit.pcf, precision=4)
    assert lamb == 0.75
    assert string == r"& \text{Since, } \left(w_c < 135\ \mathrm{pcf} \Leftarrow 110\ \mathrm{pcf} < 135\ \mathrm{pcf}\right): & \lambda &= 0.75"

def test_table_25_4_3_2_lamb_normal():
    string, lamb = chapter_25.table_25_4_3_2_lamb(145*unit.pcf, precision=4)
    assert lamb == 1
    assert string == r"& \text{Since, } \left(w_c \geq 135\ \mathrm{pcf} \Leftarrow 145\ \mathrm{pcf} \geq 135\ \mathrm{pcf}\right): & \lambda &= 1"

def test_table_25_4_3_2_psi_e_true():
    string, psi_e = chapter_25.table_25_4_3_2_psi_e(True, precision=4)
    assert psi_e == 1.2
    assert string == r"& \text{Since, } \left(\mathrm{coated} = \mathrm{True}\right): & \psi_e &= 1.2"

def test_table_25_4_3_2_psi_e_false():
    string, psi_e = chapter_25.table_25_4_3_2_psi_e(False, precision=4)
    assert psi_e == 1
    assert string == r"& \text{Since, } \left(\mathrm{coated} = \mathrm{False}\right): & \psi_e &= 1"

def test_table_25_4_3_2_psi_r_large():
    string, psi_r = chapter_25.table_25_4_3_2_psi_r(
        d_b=1.693*unit.inch,
        A_hs=2.25*unit.inch**2,
        size=14,
        s=12*unit.inch,
        A_th=0*unit.inch**2,
        precision=4)
    assert psi_r == 1.6
    assert string == r"& \text{Since, } \left(\text{Rebar size} > 11 \Leftarrow 14 > 11\right): & \psi_r &= 1.6"

def test_table_25_4_3_2_psi_r_s():
    string, psi_r = chapter_25.table_25_4_3_2_psi_r(
        d_b=1*unit.inch,
        A_hs=0.79*unit.inch**2,
        size=8,
        s=12*unit.inch,
        A_th=0*unit.inch**2,
        precision=4)
    assert psi_r == 1
    assert string == r"& \text{Since, } \left(s \geq 6 \cdot d_b \Leftarrow 12\ \mathrm{in} \geq 6\ \mathrm{in}\right): & \psi_r &= 1"

def test_table_25_4_3_2_psi_r_A_th():
    string, psi_r = chapter_25.table_25_4_3_2_psi_r(
        d_b=1*unit.inch,
        A_hs=0.79*unit.inch**2,
        size=8,
        s=4*unit.inch,
        A_th=1*unit.inch**2,
        precision=4)
    assert psi_r == 1
    assert string == r"& \text{Since, } \left(A_{th} \geq 0.4 \cdot A_{hs} \Leftarrow 1\ \mathrm{in}^{2} \geq 0.316\ \mathrm{in}^{2}\right): & \psi_r &= 1"

def test_table_25_4_3_2_psi_r_small():
    string, psi_r = chapter_25.table_25_4_3_2_psi_r(
        d_b=1*unit.inch,
        A_hs=0.79*unit.inch**2,
        size=8,
        s=4*unit.inch,
        A_th=0*unit.inch**2,
        precision=4)
    assert psi_r == 1.6
    assert string == r"& \text{Since, } \left(A_{th} < 0.4 \cdot A_{hs} \Leftarrow 0\ \mathrm{in}^{2} < 0.316\ \mathrm{in}^{2}\right) \text{ and } \left(s < 6 \cdot d_b \Leftarrow 4\ \mathrm{in} < 6\ \mathrm{in}\right): & \psi_r &= 1.6"

def test_table_25_4_3_2_psi_o_large():
    string, psi_o = chapter_25.table_25_4_3_2_psi_o(
        d_b=1.693*unit.inch,
        size=14,
        c_c_side=3*unit.inch,
        in_column=False,
        precision=4)
    assert psi_o == 1.25
    assert string == r"& \text{Since, } \left(\text{Rebar size} > 11 \Leftarrow 14 > 11\right): & \psi_o &= 1.25"

def test_table_25_4_3_2_psi_o_d_b():
    string, psi_o = chapter_25.table_25_4_3_2_psi_o(
        d_b=1*unit.inch,
        size=8,
        c_c_side=12*unit.inch,
        in_column=False,
        precision=4)
    assert psi_o == 1
    assert string == r"& \text{Since, } \left(c_{c_{side}} \geq 6 \cdot d_b \Leftarrow 12\ \mathrm{in} \geq 6\ \mathrm{in}\right): & \psi_o &= 1"

def test_table_25_4_3_2_psi_o_column():
    string, psi_o = chapter_25.table_25_4_3_2_psi_o(
        d_b=1*unit.inch,
        size=8,
        c_c_side=4*unit.inch,
        in_column=True,
        precision=4)
    assert psi_o == 1
    assert string == r"& \text{Since, } \left(\text{In column} = \mathrm{True}\right) \text{ and } \left(c_{c_{side}} \geq 2.5\ \mathrm{in} \Leftarrow 4\ \mathrm{in} \geq 2.5\ \mathrm{in}\right): & \psi_o &= 1"

def test_table_25_4_3_2_psi_o_column_small():
    string, psi_o = chapter_25.table_25_4_3_2_psi_o(
        d_b=1*unit.inch,
        size=8,
        c_c_side=2*unit.inch,
        in_column=True,
        precision=4)
    assert psi_o == 1.25
    assert string == r"& \text{Since, } \left(c_{c_{side}} < 2.5\ \mathrm{in} \Leftarrow 2\ \mathrm{in} < 2.5\ \mathrm{in}\right): & \psi_o &= 1.25"

def test_table_25_4_3_2_psi_o_small():
    string, psi_o = chapter_25.table_25_4_3_2_psi_o(
        d_b=1*unit.inch,
        size=8,
        c_c_side=4*unit.inch,
        in_column=False,
        precision=4)
    assert psi_o == 1.25
    assert string == r"& \text{Since, } \left(c_{c_{side}} < 6 \cdot d_b \Leftarrow 4\ \mathrm{in} < 6\ \mathrm{in}\right): & \psi_o &= 1.25"

def test_table_25_4_3_2_psi_c():
    string, psi_c = chapter_25.table_25_4_3_2_psi_c(4000*unit.psi, precision=4)
    assert isclose(psi_c, 0.8666666667, atol=1e-10)
    assert string == r"\psi_c &= \operatorname{min}\left(\frac{f'_c}{15000\ \mathrm{psi}} + 0.6,\ 1\right) = \operatorname{min}\left(\frac{4000\ \mathrm{psi}}{15000\ \mathrm{psi}} + 0.6,\ 1\right) &= 0.8667"

def test_table_25_4_3_2_test_1():
    concrete = materials.Concrete(4000*unit.psi, w_c=110*unit.pcf)
    rebar = materials.Rebar(8, coated=True)
    string, results = chapter_25.table_25_4_3_2(
        rebar=rebar,
        concrete=concrete,
        c_c_side=3*unit.inch,
        s=4*unit.inch,
        n=1,
        A_th=1*unit.inch**2,
        in_column=True,
        precision=4)
    assert isclose(results.pop("psi_c"), 0.8666666667, atol=1e-10)
    assert results == {"lamb": 0.75, "psi_e": 1.2, "psi_r": 1, "psi_o": 1}
    assert string == r"""$$
\begin{aligned}
    & \text{Since, } \left(w_c < 135\ \mathrm{pcf} \Leftarrow 110\ \mathrm{pcf} < 135\ \mathrm{pcf}\right): & \lambda &= 0.75
    \\[10pt]
    & \text{Since, } \left(\mathrm{coated} = \mathrm{True}\right): & \psi_e &= 1.2
    \\[10pt]
    & \text{Since, } \left(A_{th} \geq 0.4 \cdot A_{hs} \Leftarrow 1\ \mathrm{in}^{2} \geq 0.316\ \mathrm{in}^{2}\right): & \psi_r &= 1
    \\[10pt]
    & \text{Since, } \left(\text{In column} = \mathrm{True}\right) \text{ and } \left(c_{c_{side}} \geq 2.5\ \mathrm{in} \Leftarrow 3\ \mathrm{in} \geq 2.5\ \mathrm{in}\right): & \psi_o &= 1
\end{aligned}
$$
$$
\begin{aligned}
    \psi_c &= \operatorname{min}\left(\frac{f'_c}{15000\ \mathrm{psi}} + 0.6,\ 1\right) = \operatorname{min}\left(\frac{4000\ \mathrm{psi}}{15000\ \mathrm{psi}} + 0.6,\ 1\right) &= 0.8667
\end{aligned}
$$"""

def test_table_25_4_3_2_test_2():
    concrete = materials.Concrete(6000*unit.psi)
    rebar = materials.Rebar(8)
    string, results = chapter_25.table_25_4_3_2(
        rebar=rebar,
        concrete=concrete,
        c_c_side=6*unit.inch,
        s=6*unit.inch,
        n=1,
        A_th=0*unit.inch**2,
        in_column=False,
        precision=4)
    assert isclose(results.pop("psi_c"), 1)
    assert results == {"lamb": 1, "psi_e": 1, "psi_r": 1, "psi_o": 1}
    assert string == r"""$$
\begin{aligned}
    & \text{Since, } \left(w_c \geq 135\ \mathrm{pcf} \Leftarrow 150\ \mathrm{pcf} \geq 135\ \mathrm{pcf}\right): & \lambda &= 1
    \\[10pt]
    & \text{Since, } \left(\mathrm{coated} = \mathrm{False}\right): & \psi_e &= 1
    \\[10pt]
    & \text{Since, } \left(s \geq 6 \cdot d_b \Leftarrow 6\ \mathrm{in} \geq 6\ \mathrm{in}\right): & \psi_r &= 1
    \\[10pt]
    & \text{Since, } \left(c_{c_{side}} \geq 6 \cdot d_b \Leftarrow 6\ \mathrm{in} \geq 6\ \mathrm{in}\right): & \psi_o &= 1
\end{aligned}
$$
$$
\begin{aligned}
    \psi_c &= \operatorname{min}\left(\frac{f'_c}{15000\ \mathrm{psi}} + 0.6,\ 1\right) = \operatorname{min}\left(\frac{6000\ \mathrm{psi}}{15000\ \mathrm{psi}} + 0.6,\ 1\right) &= 1
\end{aligned}
$$"""

def test_table_25_4_3_2_test_3():
    concrete = materials.Concrete(6000*unit.psi)
    rebar = materials.Rebar(8)
    string, results = chapter_25.table_25_4_3_2(
        rebar=rebar,
        concrete=concrete,
        c_c_side=2*unit.inch,
        s=4*unit.inch,
        n=1,
        A_th=0*unit.inch**2,
        in_column=True,
        precision=4)
    assert isclose(results.pop("psi_c"), 1)
    assert results == {"lamb": 1, "psi_e": 1, "psi_r": 1.6, "psi_o": 1.25}
    assert string == r"""$$
\begin{aligned}
    & \text{Since, } \left(w_c \geq 135\ \mathrm{pcf} \Leftarrow 150\ \mathrm{pcf} \geq 135\ \mathrm{pcf}\right): & \lambda &= 1
    \\[10pt]
    & \text{Since, } \left(\mathrm{coated} = \mathrm{False}\right): & \psi_e &= 1
    \\[10pt]
    & \text{Since, } \left(A_{th} < 0.4 \cdot A_{hs} \Leftarrow 0\ \mathrm{in}^{2} < 0.316\ \mathrm{in}^{2}\right) \text{ and } \left(s < 6 \cdot d_b \Leftarrow 4\ \mathrm{in} < 6\ \mathrm{in}\right): & \psi_r &= 1.6
    \\[10pt]
    & \text{Since, } \left(c_{c_{side}} < 2.5\ \mathrm{in} \Leftarrow 2\ \mathrm{in} < 2.5\ \mathrm{in}\right): & \psi_o &= 1.25
\end{aligned}
$$
$$
\begin{aligned}
    \psi_c &= \operatorname{min}\left(\frac{f'_c}{15000\ \mathrm{psi}} + 0.6,\ 1\right) = \operatorname{min}\left(\frac{6000\ \mathrm{psi}}{15000\ \mathrm{psi}} + 0.6,\ 1\right) &= 1
\end{aligned}
$$"""

def test_table_25_4_3_2_test_4():
    concrete = materials.Concrete(6000*unit.psi)
    rebar = materials.Rebar(8)
    string, results = chapter_25.table_25_4_3_2(
        rebar=rebar,
        concrete=concrete,
        c_c_side=3*unit.inch,
        s=4*unit.inch,
        n=1,
        A_th=0*unit.inch**2,
        in_column=False,
        precision=4)
    assert isclose(results.pop("psi_c"), 1)
    assert results == {"lamb": 1, "psi_e": 1, "psi_r": 1.6, "psi_o": 1.25}
    assert string == r"""$$
\begin{aligned}
    & \text{Since, } \left(w_c \geq 135\ \mathrm{pcf} \Leftarrow 150\ \mathrm{pcf} \geq 135\ \mathrm{pcf}\right): & \lambda &= 1
    \\[10pt]
    & \text{Since, } \left(\mathrm{coated} = \mathrm{False}\right): & \psi_e &= 1
    \\[10pt]
    & \text{Since, } \left(A_{th} < 0.4 \cdot A_{hs} \Leftarrow 0\ \mathrm{in}^{2} < 0.316\ \mathrm{in}^{2}\right) \text{ and } \left(s < 6 \cdot d_b \Leftarrow 4\ \mathrm{in} < 6\ \mathrm{in}\right): & \psi_r &= 1.6
    \\[10pt]
    & \text{Since, } \left(c_{c_{side}} < 6 \cdot d_b \Leftarrow 3\ \mathrm{in} < 6\ \mathrm{in}\right): & \psi_o &= 1.25
\end{aligned}
$$
$$
\begin{aligned}
    \psi_c &= \operatorname{min}\left(\frac{f'_c}{15000\ \mathrm{psi}} + 0.6,\ 1\right) = \operatorname{min}\left(\frac{6000\ \mathrm{psi}}{15000\ \mathrm{psi}} + 0.6,\ 1\right) &= 1
\end{aligned}
$$"""

def test_table_25_4_3_2_test_5():
    concrete = materials.Concrete(6000*unit.psi)
    rebar = materials.Rebar(14)
    string, results = chapter_25.table_25_4_3_2(
        rebar=rebar,
        concrete=concrete,
        c_c_side=12*unit.inch,
        s=12*unit.inch,
        n=1,
        A_th=0*unit.inch**2,
        in_column=False,
        precision=4)
    assert isclose(results.pop("psi_c"), 1)
    assert results == {"lamb": 1, "psi_e": 1, "psi_r": 1.6, "psi_o": 1.25}
    assert string == r"""$$
\begin{aligned}
    & \text{Since, } \left(w_c \geq 135\ \mathrm{pcf} \Leftarrow 150\ \mathrm{pcf} \geq 135\ \mathrm{pcf}\right): & \lambda &= 1
    \\[10pt]
    & \text{Since, } \left(\mathrm{coated} = \mathrm{False}\right): & \psi_e &= 1
    \\[10pt]
    & \text{Since, } \left(\text{Rebar size} > 11 \Leftarrow 14 > 11\right): & \psi_r &= 1.6
    \\[10pt]
    & \text{Since, } \left(\text{Rebar size} > 11 \Leftarrow 14 > 11\right): & \psi_o &= 1.25
\end{aligned}
$$
$$
\begin{aligned}
    \psi_c &= \operatorname{min}\left(\frac{f'_c}{15000\ \mathrm{psi}} + 0.6,\ 1\right) = \operatorname{min}\left(\frac{6000\ \mathrm{psi}}{15000\ \mathrm{psi}} + 0.6,\ 1\right) &= 1
\end{aligned}
$$"""
