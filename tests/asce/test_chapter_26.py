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

from structuraltools import unit

from structuraltools.asce import chapter_26


def test_fig_26_8_1():
    string, K_zt = chapter_26.fig_26_8_1(
        feature="escarpment",
        H=500*unit.ft,
        L_h=1500*unit.ft,
        x=300*unit.ft,
        z=50*unit.ft,
        exposure="B",
        return_string=True)
    assert isclose(K_zt, 1.484767957, atol=1e-9)
    assert string == r"""\begin{aligned}
    L_h &= \operatorname{max}\left(L_h,\ 2 \cdot H\right) = \operatorname{max}\left(1500\ \mathrm{ft},\ 2 \cdot 500\ \mathrm{ft}\right) &= 1500\ \mathrm{ft}
    \\[10pt]
    K_1 &= 0.75 \cdot \frac{H}{L_h} = 0.75 \cdot \frac{500\ \mathrm{ft}}{1500\ \mathrm{ft}} &= 0.25
    \\[10pt]
    K_2 &= 1 - \frac{|x|}{\mu \cdot L_h} = 1 - \frac{|300\ \mathrm{ft}|}{4 \cdot 1500\ \mathrm{ft}} &= 0.95
    \\[10pt]
    K_3 &= e^{- \frac{\gamma \cdot z}{L_h}} = e^{- \frac{2.5 \cdot 50\ \mathrm{ft}}{1500\ \mathrm{ft}}} &= 0.92
    \\[10pt]
    K_{zt} &= \left(1 + K_1 \cdot K_2 \cdot K_3\right)^2 = \left(1 + 0.25 \cdot 0.95 \cdot 0.92\right)^2 &= 1.485
\end{aligned}"""

def test_table_26_9_1():
    string, K_e = chapter_26.table_26_9_1(500*unit.ft, return_string=True)
    assert isclose(K_e, 0.9820628212, atol=1e-10)
    assert string == r"K_e &= e^{-0.0000362 \cdot z_e} = e^{-0.0000362 \cdot 500\ \mathrm{ft}} &= 0.982"

def test_table_26_10_1_low():
    string, K_z = chapter_26.table_26_10_1(
        z=10*unit.ft,
        z_g=chapter_26.table_26_11_1.at["C", "z_g"],
        alpha=chapter_26.table_26_11_1.at["C", "alpha"],
        return_string=True)
    assert isclose(K_z, 0.8511539011, atol=1e-10)
    assert string == r"K_{z} &= 2.41 \cdot \left(\frac{\operatorname{min}\left(\operatorname{max}\left(15\ \mathrm{ft},\ z\right),\ z_g\right)}{z_g}\right)^{\frac{2}{\alpha}} = 2.41 \cdot \left(\frac{\operatorname{min}\left(\operatorname{max}\left(15\ \mathrm{ft},\ 10\ \mathrm{ft}\right),\ 2460\ \mathrm{ft}\right)}{2460\ \mathrm{ft}}\right)^{\frac{2}{9.8}} &= 0.851"

def test_table_26_10_1_mid():
    string, K_h = chapter_26.table_26_10_1(
        z=100*unit.ft,
        z_g=chapter_26.table_26_11_1.at["C", "z_g"],
        alpha=chapter_26.table_26_11_1.at["C", "alpha"],
        elevation="h",
        return_string=True)
    assert isclose(K_h, 1.253581964, atol=1e-9)
    assert string == r"K_{h} &= 2.41 \cdot \left(\frac{\operatorname{min}\left(\operatorname{max}\left(15\ \mathrm{ft},\ h\right),\ z_g\right)}{z_g}\right)^{\frac{2}{\alpha}} = 2.41 \cdot \left(\frac{\operatorname{min}\left(\operatorname{max}\left(15\ \mathrm{ft},\ 100\ \mathrm{ft}\right),\ 2460\ \mathrm{ft}\right)}{2460\ \mathrm{ft}}\right)^{\frac{2}{9.8}} &= 1.254"

def test_table_26_10_1_high():
    string, K_h = chapter_26.table_26_10_1(
        z=3000*unit.ft,
        z_g=chapter_26.table_26_11_1.at["C", "z_g"],
        alpha=chapter_26.table_26_11_1.at["C", "alpha"],
        elevation="h",
        return_string=True)
    assert K_h == 2.41
    assert string == r"K_{h} &= 2.41 \cdot \left(\frac{\operatorname{min}\left(\operatorname{max}\left(15\ \mathrm{ft},\ h\right),\ z_g\right)}{z_g}\right)^{\frac{2}{\alpha}} = 2.41 \cdot \left(\frac{\operatorname{min}\left(\operatorname{max}\left(15\ \mathrm{ft},\ 3000\ \mathrm{ft}\right),\ 2460\ \mathrm{ft}\right)}{2460\ \mathrm{ft}}\right)^{\frac{2}{9.8}} &= 2.41"

def test_eq_26_10_1():
    string, q_h = chapter_26.eq_26_10_1(
        K_z=1.21,
        K_zt=1,
        K_e=0.96,
        V=110*unit.mph,
        elevation="h",
        return_string=True)
    assert isclose(q_h, 35.9817216*unit.psf, atol=1e-7*unit.psf)
    assert string == r"q_{h} &= 0.00256 \cdot K_{h} \cdot K_{zt} \cdot K_e \cdot V^2 = 0.00256 \cdot 1.21 \cdot 1 \cdot K_e \cdot 110\ \mathrm{mph}^2 &= 35.982\ \mathrm{psf}"

def test_eq_26_11_6():
    string, G_x = chapter_26.eq_26_11_6(
        I_bar_z=0.285,
        Q=0.868,
        axis="x",
        return_string=True)
    assert isclose(G_x, 0.8490224644, atol=1e-10)
    assert string == r"G_{x} &= 0.925 \cdot \left(\frac{1 + 1.7 \cdot g_Q \cdot I_\bar{z} \cdot Q_{x}}{1 + 1.7 \cdot g_v \cdot I_\bar{z}}\right) = 0.925 \cdot \left(\frac{1 + 1.7 \cdot 3.4 \cdot 0.285 \cdot 0.868}{1 + 1.7 \cdot 3.4 \cdot 0.285}\right) &= 0.849"

def test_eq_26_11_7():
    string, I_bar_z = chapter_26.eq_26_11_7(0.3, 45*unit.ft, return_string=True)
    assert isclose(I_bar_z, 0.2848862525, atol=1e-10)
    assert string == r"I_\bar{z} &= c \cdot \left(\frac{33}{\bar{z}}\right)^\frac{1}{6} = 0.3 \cdot \left(\frac{33}{45\ \mathrm{ft}}\right)^\frac{1}{6} &= 0.285"

def test_eq_26_11_8():
    string, Q_x = chapter_26.eq_26_11_8(
        L=50*unit.ft,
        h=75*unit.ft,
        L_bar_z=355*unit.ft,
        axis_1="x",
        axis_2="y",
        return_string=True)
    assert isclose(Q_x, 0.8682859277, atol=1e-10)
    assert string == r"Q_{x} &= \sqrt{\frac{1}{1 + 0.63 \cdot \left(\frac{L_{y} + h}{L_\bar{z}}\right)^{0.63}}} = \sqrt{\frac{1}{1 + 0.63 \cdot \left(\frac{50\ \mathrm{ft} + 75\ \mathrm{ft}}{355\ \mathrm{ft}}\right)^{0.63}}} &= 0.868"

def test_eq_26_11_9():
    string, L_bar_z = chapter_26.eq_26_11_9(
        L=320*unit.ft,
        bar_z=45*unit.ft,
        bar_epsilon=1/3,
        return_string=True)
    assert isclose(L_bar_z, 354.8538349*unit.ft, atol=1e-7*unit.ft)
    assert string == r"L_\bar{z} &= l \cdot \left(\frac{\bar{z}}{33}\right)^{\bar{\epsilon}} = 320\ \mathrm{ft} \cdot \left(\frac{45\ \mathrm{ft}}{33}\right)^{0.333} &= 354.854\ \mathrm{ft}"
