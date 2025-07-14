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

from structuraltools import aisc
from structuraltools.aisc import chapter_F
from structuraltools.unit import unit


def test_eq_F2_1():
    string, M_p = chapter_F.eq_F2_1(
        F_y=50*unit.ksi,
        Z_x=20*unit.inch**3,
        precision=4)
    assert isclose(M_p, 1000/12*unit.kipft)
    assert M_p.units == "kipft"
    assert string == r"M_p &= F_y \cdot Z_x = 50\ \mathrm{ksi} \cdot 20\ \mathrm{in}^{3} &= 83.33\ \mathrm{kipft}"

def test_eq_F2_2():
    string, M_ltb = chapter_F.eq_F2_2(
        C_b=1,
        M_p=83*unit.kipft,
        F_y=50*unit.ksi,
        S_x=15*unit.inch**3,
        L_b=5*unit.ft,
        L_p=3*unit.ft,
        L_r=10*unit.ft,
        precision=4)
    assert isclose(M_ltb, 71.78571429*unit.kipft, atol=1e-8*unit.kipft)
    assert M_ltb.units == "kipft"
    assert string == r"""M_{ltb} &= C_b \cdot \left(M_p - \left(M_p - 0.7 \cdot F_y \cdot S_x\right) \cdot \left(\frac{L_b - L_p}{L_r - L_p}\right)\right)
\\
&= 1 \cdot \left(83\ \mathrm{kipft} - \left(83\ \mathrm{kipft} - 0.7 \cdot 50\ \mathrm{ksi} \cdot 15\ \mathrm{in}^{3}\right) \cdot \left(\frac{5\ \mathrm{ft} - 3\ \mathrm{ft}}{10\ \mathrm{ft} - 3\ \mathrm{ft}}\right)\right)
\\
&= 71.79\ \mathrm{kipft}"""

def test_eq_F2_3():
    string, M_ltb = chapter_F.eq_F2_3(
        F_cr=17*unit.ksi,
        S_x=25.4*unit.inch**3,
        precision=4)
    assert isclose(M_ltb, 35.98333333*unit.kipft, atol=1e-8*unit.kipft)
    assert M_ltb.units == "kipft"
    assert string == r"M_{ltb} &= F_{cr} \cdot S_x = 17\ \mathrm{ksi} \cdot 25.4\ \mathrm{in}^{3} &= 35.98\ \mathrm{kipft}"

def test_eq_F2_4():
    string, F_cr = chapter_F.eq_F2_4(
        C_b=1,
        E=29000*unit.ksi,
        L_b=15*unit.ft,
        r_ts=1.04*unit.inch,
        J=0.293*unit.inch**4,
        c=1,
        S_x=25.4*unit.inch**3,
        h_o=11.9*unit.inch,
        precision=4)
    assert isclose(F_cr, 17.26466339*unit.ksi, atol=1e-8*unit.ksi)
    assert F_cr.units == "ksi"
    assert string == r"""F_{cr} &= \frac{C_b \cdot \pi^2 \cdot E}{\left(\frac{L_b}{r_{ts}}\right)^2} \cdot \sqrt{1 + 0.078 \cdot \frac{J \cdot c}{S_x \cdot h_o} \cdot \left(\frac{L_b}{r_{ts}}\right)^2}
\\
&= \frac{1 \cdot \pi^2 \cdot 2.9\times 10^{4}\ \mathrm{ksi}}{\left(\frac{15\ \mathrm{ft}}{1.04\ \mathrm{in}}\right)^2} \cdot \sqrt{1 + 0.078 \cdot \frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}} \cdot \left(\frac{15\ \mathrm{ft}}{1.04\ \mathrm{in}}\right)^2}
\\
&= 17.26\ \mathrm{ksi}"""

def test_eq_F2_5():
    string, L_p = chapter_F.eq_F2_5(
        r_y=0.848*unit.inch,
        E=29000*unit.ksi,
        F_y=50*unit.ksi,
        precision=4)
    assert isclose(L_p, 2.995306513*unit.ft, atol=1e-8*unit.ft)
    assert L_p.units == "ft"
    assert string == r"L_p &= 1.76 \cdot r_y \cdot \sqrt{\frac{E}{F_y}} = 1.76 \cdot 0.848\ \mathrm{in} \cdot \sqrt{\frac{2.9\times 10^{4}\ \mathrm{ksi}}{50\ \mathrm{ksi}}} &= 2.995\ \mathrm{ft}"

def test_eq_F2_6():
    string, L_r = chapter_F.eq_F2_6(
        r_ts=1.04*unit.inch,
        E=29000*unit.ksi,
        F_y=50*unit.ksi,
        J=0.293*unit.inch**4,
        c=1,
        S_x=25.4*unit.inch**3,
        h_o=11.9*unit.inch,
        precision=4)
    assert isclose(L_r, 9.132623412*unit.ft, atol=1e-9*unit.ft)
    assert L_r.units == "ft"
    assert string == r"""L_r &= 1.95 \cdot r_{ts} \cdot \frac{E}{0.7 \cdot F_y} \cdot \sqrt{\frac{J \cdot c}{S_x \cdot h_o} + \sqrt{\left(\frac{J \cdot c}{S_x \cdot h_o}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot F_y}{E}\right)^2}}
\\
&= 1.95 \cdot 1.04\ \mathrm{in} \frac{2.9\times 10^{4}\ \mathrm{ksi}}{0.7 \cdot 50\ \mathrm{ksi}} \cdot \sqrt{\frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}} + \sqrt{\left(\frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}}\right)^2 +6.76 \cdot \left(\frac{0.7 \cdot 50\ \mathrm{ksi}}{2.9\times 10^{4}\ \mathrm{ksi}}\right)^2}}
\\
&= 9.133\ \mathrm{ft}"""

def test_eq_F2_8b():
    string, c = chapter_F.eq_F2_8b(
        h_o=9.56*unit.inch,
        I_y=2.8*unit.inch**4,
        C_w=56.9*unit.inch**6,
        precision=4)
    assert isclose(c, 1.060353756, atol=1e-9)
    assert string == r"c &= \frac{h_o}{2} \cdot \sqrt{\frac{I_y}{C_w}} = \frac{9.56\ \mathrm{in}}{2} \cdot \sqrt{\frac{2.8\ \mathrm{in}^{4}}{56.9\ \mathrm{in}^{6}}} &= 1.06"

def test_sec_F2_1():
    shape = aisc.WideFlange("W12X22", "A992")
    string, M_p = chapter_F.sec_F2_1(shape, precision=4)
    assert isclose(M_p, 122.0833333*unit.kipft, atol=1e-7*unit.kipft)
    assert M_p.units == "kipft"
    assert string == r"""\begin{aligned}
    M_p &= F_y \cdot Z_x = 50\ \mathrm{ksi} \cdot 29.3\ \mathrm{in}^{3} &= 122.1\ \mathrm{kipft}
\end{aligned}"""

def test_sec_F2_2_plastic_WideFlange():
    shape = aisc.WideFlange("W12X22", "A992")
    _, M_p = chapter_F.sec_F2_1(shape)
    string, M_ltb = chapter_F.sec_F2_2(
        shape=shape,
        L_b=2*unit.ft,
        M_p=M_p,
        C_b=1,
        precision=4)
    assert isclose(M_ltb, 122.0833333*unit.kipft, atol=1e-7*unit.kipft)
    assert M_ltb.units == "kipft"
    assert string == r"""\begin{aligned}
    L_p &= 1.76 \cdot r_y \cdot \sqrt{\frac{E}{F_y}} = 1.76 \cdot 0.848\ \mathrm{in} \cdot \sqrt{\frac{2.9\times 10^{4}\ \mathrm{ksi}}{50\ \mathrm{ksi}}} &= 2.995\ \mathrm{ft}
    \\[10pt]
    \text{Since, } & \left(L_b \leq L_p \Leftarrow 2\ \mathrm{ft} \leq 2.995\ \mathrm{ft}\right):
        \\[10pt]
        M_{ltb} &= M_p = 122.1\ \mathrm{kipft} &= 122.1\ \mathrm{kipft}
\end{aligned}"""

def test_sec_F2_2_inelastic_WideFlange():
    shape = aisc.WideFlange("W12X22", "A992")
    _, M_p = chapter_F.sec_F2_1(shape)
    string, M_ltb = chapter_F.sec_F2_2(
        shape=shape,
        L_b=7*unit.ft,
        M_p=M_p,
        C_b=1,
        precision=4)
    assert isclose(M_ltb, 90.7*unit.kipft, atol=1*unit.kipft)
    assert M_ltb.units == "kipft"
    assert string == r"""\begin{aligned}
    L_p &= 1.76 \cdot r_y \cdot \sqrt{\frac{E}{F_y}} = 1.76 \cdot 0.848\ \mathrm{in} \cdot \sqrt{\frac{2.9\times 10^{4}\ \mathrm{ksi}}{50\ \mathrm{ksi}}} &= 2.995\ \mathrm{ft}
    \\[10pt]
    L_r &= 1.95 \cdot r_{ts} \cdot \frac{E}{0.7 \cdot F_y} \cdot \sqrt{\frac{J \cdot c}{S_x \cdot h_o} + \sqrt{\left(\frac{J \cdot c}{S_x \cdot h_o}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot F_y}{E}\right)^2}}
\\
&= 1.95 \cdot 1.04\ \mathrm{in} \frac{2.9\times 10^{4}\ \mathrm{ksi}}{0.7 \cdot 50\ \mathrm{ksi}} \cdot \sqrt{\frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}} + \sqrt{\left(\frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}}\right)^2 +6.76 \cdot \left(\frac{0.7 \cdot 50\ \mathrm{ksi}}{2.9\times 10^{4}\ \mathrm{ksi}}\right)^2}}
\\
&= 9.133\ \mathrm{ft}
    \\[10pt]
    \text{Since, } & \left(L_p < L_b \leq L_r \Leftarrow 2.995\ \mathrm{ft} < 7\ \mathrm{ft} \leq 9.133\ \mathrm{ft}\right):
        \\[10pt]
        M_{ltb} &= C_b \cdot \left(M_p - \left(M_p - 0.7 \cdot F_y \cdot S_x\right) \cdot \left(\frac{L_b - L_p}{L_r - L_p}\right)\right)
\\
&= 1 \cdot \left(122.1\ \mathrm{kipft} - \left(122.1\ \mathrm{kipft} - 0.7 \cdot 50\ \mathrm{ksi} \cdot 25.4\ \mathrm{in}^{3}\right) \cdot \left(\frac{7\ \mathrm{ft} - 2.995\ \mathrm{ft}}{9.133\ \mathrm{ft} - 2.995\ \mathrm{ft}}\right)\right)
\\
&= 90.76\ \mathrm{kipft}
\end{aligned}"""

def test_sec_F2_2_elastic_WideFlange():
    shape = aisc.WideFlange("W12X22", "A992")
    _, M_p = chapter_F.sec_F2_1(shape)
    string, M_ltb = chapter_F.sec_F2_2(
        shape=shape,
        L_b=15*unit.ft,
        M_p=M_p,
        C_b=1,
        precision=4)
    assert isclose(M_ltb, 36.5*unit.kipft, atol=1*unit.kipft)
    assert M_ltb.units == "kipft"
    assert string == r"""\begin{aligned}
    L_r &= 1.95 \cdot r_{ts} \cdot \frac{E}{0.7 \cdot F_y} \cdot \sqrt{\frac{J \cdot c}{S_x \cdot h_o} + \sqrt{\left(\frac{J \cdot c}{S_x \cdot h_o}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot F_y}{E}\right)^2}}
\\
&= 1.95 \cdot 1.04\ \mathrm{in} \frac{2.9\times 10^{4}\ \mathrm{ksi}}{0.7 \cdot 50\ \mathrm{ksi}} \cdot \sqrt{\frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}} + \sqrt{\left(\frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}}\right)^2 +6.76 \cdot \left(\frac{0.7 \cdot 50\ \mathrm{ksi}}{2.9\times 10^{4}\ \mathrm{ksi}}\right)^2}}
\\
&= 9.133\ \mathrm{ft}
    \\[10pt]
    \text{Since, } & \left(L_b > L_r \Leftarrow 15\ \mathrm{ft} > 9.133\ \mathrm{ft}\right):
        \\[10pt]
        F_{cr} &= \frac{C_b \cdot \pi^2 \cdot E}{\left(\frac{L_b}{r_{ts}}\right)^2} \cdot \sqrt{1 + 0.078 \cdot \frac{J \cdot c}{S_x \cdot h_o} \cdot \left(\frac{L_b}{r_{ts}}\right)^2}
\\
&= \frac{1 \cdot \pi^2 \cdot 2.9\times 10^{4}\ \mathrm{ksi}}{\left(\frac{15\ \mathrm{ft}}{1.04\ \mathrm{in}}\right)^2} \cdot \sqrt{1 + 0.078 \cdot \frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}} \cdot \left(\frac{15\ \mathrm{ft}}{1.04\ \mathrm{in}}\right)^2}
\\
&= 17.26\ \mathrm{ksi}
        \\[10pt]
        M_{ltb} &= F_{cr} \cdot S_x = 17.26\ \mathrm{ksi} \cdot 25.4\ \mathrm{in}^{3} &= 36.54\ \mathrm{kipft}
\end{aligned}"""

def test_sec_F2():
    shape = aisc.WideFlange("W12X22", "A992")
    string, M_n = chapter_F.sec_F2(
        shape=shape,
        L_b=7*unit.ft,
        C_b=1,
        precision=4)
    assert isclose(M_n, 90.7*unit.kipft, atol=0.1*unit.kipft)
    assert M_n.units == "kipft"
    assert string == r"""#### Plastic Moment Capacity
$$\begin{aligned}
    M_p &= F_y \cdot Z_x = 50\ \mathrm{ksi} \cdot 29.3\ \mathrm{in}^{3} &= 122.1\ \mathrm{kipft}
\end{aligned}$$
<br/>
#### Lateral-Torsional Buckling Moment Capacity
$$\begin{aligned}
    L_p &= 1.76 \cdot r_y \cdot \sqrt{\frac{E}{F_y}} = 1.76 \cdot 0.848\ \mathrm{in} \cdot \sqrt{\frac{2.9\times 10^{4}\ \mathrm{ksi}}{50\ \mathrm{ksi}}} &= 2.995\ \mathrm{ft}
    \\[10pt]
    L_r &= 1.95 \cdot r_{ts} \cdot \frac{E}{0.7 \cdot F_y} \cdot \sqrt{\frac{J \cdot c}{S_x \cdot h_o} + \sqrt{\left(\frac{J \cdot c}{S_x \cdot h_o}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot F_y}{E}\right)^2}}
\\
&= 1.95 \cdot 1.04\ \mathrm{in} \frac{2.9\times 10^{4}\ \mathrm{ksi}}{0.7 \cdot 50\ \mathrm{ksi}} \cdot \sqrt{\frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}} + \sqrt{\left(\frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}}\right)^2 +6.76 \cdot \left(\frac{0.7 \cdot 50\ \mathrm{ksi}}{2.9\times 10^{4}\ \mathrm{ksi}}\right)^2}}
\\
&= 9.133\ \mathrm{ft}
    \\[10pt]
    \text{Since, } & \left(L_p < L_b \leq L_r \Leftarrow 2.995\ \mathrm{ft} < 7\ \mathrm{ft} \leq 9.133\ \mathrm{ft}\right):
        \\[10pt]
        M_{ltb} &= C_b \cdot \left(M_p - \left(M_p - 0.7 \cdot F_y \cdot S_x\right) \cdot \left(\frac{L_b - L_p}{L_r - L_p}\right)\right)
\\
&= 1 \cdot \left(122.1\ \mathrm{kipft} - \left(122.1\ \mathrm{kipft} - 0.7 \cdot 50\ \mathrm{ksi} \cdot 25.4\ \mathrm{in}^{3}\right) \cdot \left(\frac{7\ \mathrm{ft} - 2.995\ \mathrm{ft}}{9.133\ \mathrm{ft} - 2.995\ \mathrm{ft}}\right)\right)
\\
&= 90.76\ \mathrm{kipft}
\end{aligned}$$
<br/>
#### Nominal Moment Capacity
$$\begin{aligned}
    M_n &= \operatorname{min}\left(M_p,\ M_{ltb}\right) = \operatorname{min}\left(122.1\ \mathrm{kipft},\ 90.76\ \mathrm{kipft}\right) &= 90.76\ \mathrm{kipft}
\end{aligned}$$"""

def test_eq_F3_1():
    string, M_flb = chapter_F.eq_F3_1(
        M_p=122*unit.kipft,
        F_y=50*unit.ksi,
        S_x=25.4*unit.inch**3,
        lamb_f=15,
        lamb_pf=9,
        lamb_rf=24,
        precision=4)
    assert isclose(M_flb, 102.8333333*unit.kipft, atol=1e-7*unit.kipft)
    assert M_flb.units == "kipft"
    assert string == r"""M_{flb} &= M_p - \left(MT_p - 0.7 \cdot F_y \cdot S_x\right) \cdot \left(\frac{\lambda_f - \lambda_{pf}}{\lambda_{rf} - \lambda_{pf}}\right)
\\
&= 122\ \mathrm{kipft} - \left(122\ \mathrm{kipft} -0.7 \cdot 50\ \mathrm{ksi} \cdot 25.4\ \mathrm{in}^{3}\right) \cdot \left(\frac{15 - 9}{24 - 9}\right)
\\
&= 102.8\ \mathrm{kipft}"""

def test_eq_F3_2():
    string, M_flb = chapter_F.eq_F3_2(
        E=29000*unit.ksi,
        k_c=0.5,
        S_x=25*unit.inch**3,
        lamb_f=30,
        precision=4)
    assert isclose(M_flb, 30.20833333*unit.kipft, atol=1e-8*unit.kipft)
    assert M_flb.units == "kipft"
    assert string == r"M_{flb} &= \frac{0.9 \cdot E \cdot k_c \cdot S_x}{\lambda_f^2} = \frac{0.9 \cdot 2.9\times 10^{4}\ \mathrm{ksi} \cdot 0.5 \cdot 25\ \mathrm{in}^{3}}{30^2} &= 30.21\ \mathrm{kipft}"

def test_eq_F3_2a_low():
    string, k_c = chapter_F.eq_F3_2a(lamb_w=250, precision=4)
    assert k_c == 0.35
    assert string == r"k_c &= \operatorname{min}\left(\operatorname{max}\left(0.35,\ \frac{4}{\sqrt{\lambda_w}}\right),\ 0.76\right) = \operatorname{min}\left(\operatorname{max}\left(0.35,\ \frac{4}{\sqrt{250}}\right),\ 0.76\right) &= 0.35"

def test_eq_F3_2a_calculated():
    string, k_c = chapter_F.eq_F3_2a(lamb_w=100, precision=4)
    assert isclose(k_c, 0.4)
    assert string == r"k_c &= \operatorname{min}\left(\operatorname{max}\left(0.35,\ \frac{4}{\sqrt{\lambda_w}}\right),\ 0.76\right) = \operatorname{min}\left(\operatorname{max}\left(0.35,\ \frac{4}{\sqrt{100}}\right),\ 0.76\right) &= 0.4"

def test_eq_F3_2a_high():
    string, k_c = chapter_F.eq_F3_2a(lamb_w=20, precision=4)
    assert k_c == 0.76
    assert string == r"k_c &= \operatorname{min}\left(\operatorname{max}\left(0.35,\ \frac{4}{\sqrt{\lambda_w}}\right),\ 0.76\right) = \operatorname{min}\left(\operatorname{max}\left(0.35,\ \frac{4}{\sqrt{20}}\right),\ 0.76\right) &= 0.76"

def test_sec_F3_2_noncompact():
    shape = aisc.WideFlange("W10X12", "A992")
    string, M_flb = chapter_F.sec_F3_2(shape, 52.5*unit.kipft, precision=4)
    assert isclose(M_flb, 52.11390857*unit.kipft, atol=1e-8*unit.kipft)
    assert string == r"""\begin{aligned}
    \lambda_{p_f} &= 0.38 \cdot \sqrt{\frac{E}{F_y}} = 0.38 \cdot \sqrt{\frac{2.9\times 10^{4}\ \mathrm{ksi}}{50\ \mathrm{ksi}}} &= 9.152
    \\[10pt]
    \lambda_{r_f} &= \sqrt{\frac{E}{F_y}} = \sqrt{\frac{2.9\times 10^{4}\ \mathrm{ksi}}{50\ \mathrm{ksi}}} &= 24.08
    \\[10pt]
    \text{Since, } & \left(\lambda_{pf} \leq \lambda_f < \lambda_{rf} \Leftarrow 9.152 \leq 9.43 < 24.08\right):
        \\[10pt]
        M_{flb} &= M_p - \left(MT_p - 0.7 \cdot F_y \cdot S_x\right) \cdot \left(\frac{\lambda_f - \lambda_{pf}}{\lambda_{rf} - \lambda_{pf}}\right)
\\
&= 52.5\ \mathrm{kipft} - \left(52.5\ \mathrm{kipft} -0.7 \cdot 50\ \mathrm{ksi} \cdot 10.9\ \mathrm{in}^{3}\right) \cdot \left(\frac{9.43 - 9.152}{24.08 - 9.152}\right)
\\
&= 52.11\ \mathrm{kipft}
\end{aligned}"""

def test_sec_F3_2_slender():
    """This test fakes a slender flange, and doesn't actually calculate the
    moment capacity of an actual steel section. Ideally this is updated to use a
    custom section."""
    shape = aisc.WideFlange("W10X12", "A992")
    shape.lamb_f = 26.4
    string, M_flb = chapter_F.sec_F3_2(shape, 52.5*unit.kipft, precision=4)
    assert isclose(M_flb, 19.93172738*unit.kipft, atol=1e-8*unit.kipft)
    assert string == r"""\begin{aligned}
    \lambda_{r_f} &= \sqrt{\frac{E}{F_y}} = \sqrt{\frac{2.9\times 10^{4}\ \mathrm{ksi}}{50\ \mathrm{ksi}}} &= 24.08
    \\[10pt]
    \text{Since, } & \left(\lambda_f \geq \lambda_{rf} \Leftarrow 26.4 \geq 24.08\right):
        \\[10pt]
        k_c &= \operatorname{min}\left(\operatorname{max}\left(0.35,\ \frac{4}{\sqrt{\lambda_w}}\right),\ 0.76\right) = \operatorname{min}\left(\operatorname{max}\left(0.35,\ \frac{4}{\sqrt{46.6}}\right),\ 0.76\right) &= 0.586
        \\[10pt]
        M_{flb} &= \frac{0.9 \cdot E \cdot k_c \cdot S_x}{\lambda_f^2} = \frac{0.9 \cdot 2.9\times 10^{4}\ \mathrm{ksi} \cdot 0.586 \cdot 10.9\ \mathrm{in}^{3}}{26.4^2} &= 19.93\ \mathrm{kipft}
\end{aligned}"""

def test_sec_F3():
    shape = aisc.WideFlange("W10X12", "A992")
    string, M_n = chapter_F.sec_F3(shape, 0*unit.ft, 1, precision=4)
    assert isclose(M_n, 52.11390857*unit.kipft, atol=1e-8*unit.kipft)
    assert string == r"""#### Plastic Moment
$$\begin{aligned}
    M_p &= F_y \cdot Z_x = 50\ \mathrm{ksi} \cdot 12.6\ \mathrm{in}^{3} &= 52.5\ \mathrm{kipft}
\end{aligned}$$
<br/>
#### Lateral-Torsional Buckling Moment Capacity
$$\begin{aligned}
    L_p &= 1.76 \cdot r_y \cdot \sqrt{\frac{E}{F_y}} = 1.76 \cdot 0.785\ \mathrm{in} \cdot \sqrt{\frac{2.9\times 10^{4}\ \mathrm{ksi}}{50\ \mathrm{ksi}}} &= 2.773\ \mathrm{ft}
    \\[10pt]
    \text{Since, } & \left(L_b \leq L_p \Leftarrow 0\ \mathrm{ft} \leq 2.773\ \mathrm{ft}\right):
        \\[10pt]
        M_{ltb} &= M_p = 52.5\ \mathrm{kipft} &= 52.5\ \mathrm{kipft}
\end{aligned}$$
<br/>
#### Compression Flange Local Buckling Moment Capacity
$$\begin{aligned}
    \lambda_{p_f} &= 0.38 \cdot \sqrt{\frac{E}{F_y}} = 0.38 \cdot \sqrt{\frac{2.9\times 10^{4}\ \mathrm{ksi}}{50\ \mathrm{ksi}}} &= 9.152
    \\[10pt]
    \lambda_{r_f} &= \sqrt{\frac{E}{F_y}} = \sqrt{\frac{2.9\times 10^{4}\ \mathrm{ksi}}{50\ \mathrm{ksi}}} &= 24.08
    \\[10pt]
    \text{Since, } & \left(\lambda_{pf} \leq \lambda_f < \lambda_{rf} \Leftarrow 9.152 \leq 9.43 < 24.08\right):
        \\[10pt]
        M_{flb} &= M_p - \left(MT_p - 0.7 \cdot F_y \cdot S_x\right) \cdot \left(\frac{\lambda_f - \lambda_{pf}}{\lambda_{rf} - \lambda_{pf}}\right)
\\
&= 52.5\ \mathrm{kipft} - \left(52.5\ \mathrm{kipft} -0.7 \cdot 50\ \mathrm{ksi} \cdot 10.9\ \mathrm{in}^{3}\right) \cdot \left(\frac{9.43 - 9.152}{24.08 - 9.152}\right)
\\
&= 52.11\ \mathrm{kipft}
\end{aligned}$$
<br/>
#### Nominal Moment Capacity
$$\begin{aligned}
    M_n &= \operatorname{min}\left(M_{ltb},\ M_{flb}\right) = \operatorname{min}\left(52.5\ \mathrm{kipft},\ 52.11\ \mathrm{kipft}\right) &= 52.11\ \mathrm{kipft}
\end{aligned}$$"""

def test_eq_F11_1():
    string, M_p = chapter_F.eq_F11_1(
        F_y=50*unit.ksi,
        Z_x=12*unit.inch**3,
        S_x=8*unit.inch**3,
        precision=4)
    assert isclose(M_p, 50*unit.kipft)
    assert string == r"M_p &= \operatorname{min}\left(F_y \cdot Z_x,\ 1.5 \cdot F_y \cdot S_x\right) = \operatorname{min}\left(50\ \mathrm{ksi} \cdot 12\ \mathrm{in}^{3},\ 1.5 \cdot 50\ \mathrm{ksi} \cdot 8\ \mathrm{in}^{3}\right) &= 50\ \mathrm{kipft}"

def test_eq_F11_3():
    string, M_ltb = chapter_F.eq_F11_3(
        C_b=1,
        L_b=12*unit.inch,
        d=6*unit.inch,
        t=1*unit.inch,
        F_y=50*unit.ksi,
        E=29000*unit.ksi,
        S_x=6*unit.inch**3,
        precision=4)
    assert isclose(M_ltb, 37.14965517*unit.kipft, atol=1e-8*unit.kipft)
    assert string == r"""M_{ltb} &= C_b \cdot \left(1.52 - 0.274 \cdot \left(\frac{L_b \cdot d}{t^2}\right) \cdot \frac{F_y}{E}\right) \cdot F_y \cdot S_x
\\
&= 1 \cdot \left(1.52 - 0.274 \cdot \left(\frac{12\ \mathrm{in} \cdot 6\ \mathrm{in}}{\left(1\ \mathrm{in}\right)^2}\right) \cdot \frac{50\ \mathrm{ksi}}{2.9\times 10^{4}\ \mathrm{ksi}}\right) \cdot 50\ \mathrm{ksi} \cdot 6\ \mathrm{in}^{3}
\\
&= 37.15\ \mathrm{kipft}"""

def test_eq_F11_4():
    string, M_ltb = chapter_F.eq_F11_4(38*unit.ksi, 24*unit.inch**3, precision=4)
    assert isclose(M_ltb, 76*unit.kipft)
    assert string == r"M_{ltb} &= F_{cr} \cdot S_x = 38\ \mathrm{ksi} \cdot 24\ \mathrm{in}^{3} &= 76\ \mathrm{kipft}"

def test_eq_F11_5():
    string, F_cr = chapter_F.eq_F11_5(
        E=29000*unit.ksi,
        C_b=1,
        L_b=120*unit.inch,
        d=12*unit.inch,
        t=1*unit.inch,
        precision=4)
    assert isclose(F_cr, 38.26388889*unit.ksi, atol=1e-8*unit.ksi)
    assert string == r"F_{cr} &= \frac{1.9 \cdot E \cdot C_b}{\frac{L_b \cdot d}{t^2}} = \frac{1.9 \cdot 2.9\times 10^{4}\ \mathrm{ksi} \cdot 1}{\frac{120\ \mathrm{in} \cdot 12\ \mathrm{in}}{\left(1\ \mathrm{in}\right)^2}} &= 38.26\ \mathrm{ksi}"

def test_sec_F11_1_rect():
    shape = aisc.Plate(4*unit.inch, 1*unit.inch, "A36")
    string, M_p = chapter_F.sec_F11_1(shape, precision=4)
    assert isclose(M_p, 12*unit.kipft)
    assert string == r"""\begin{aligned}
    M_p &= \operatorname{min}\left(F_y \cdot Z_x,\ 1.5 \cdot F_y \cdot S_x\right) = \operatorname{min}\left(36\ \mathrm{ksi} \cdot 4\ \mathrm{in}^{3},\ 1.5 \cdot 36\ \mathrm{ksi} \cdot 2.667\ \mathrm{in}^{3}\right) &= 12\ \mathrm{kipft}
\end{aligned}"""

def test_sec_F11_2_plastic():
    shape = aisc.Plate(4*unit.inch, 1*unit.inch, "A36")
    _, M_p = chapter_F.sec_F11_1(shape)
    string, M_ltb = chapter_F.sec_F11_2(
        shape=shape,
        L_b=12*unit.inch,
        M_p=M_p,
        C_b=1,
        precision=4)
    assert isclose(M_ltb, 12*unit.kipft)
    assert string == r"""\begin{aligned}
    \text{Since, } & \left(\frac{L_b \cdot d}{t^2} \leq \frac{0.08 \cdot E}{F_y} \Leftarrow \frac{12\ \mathrm{in} \cdot 4\ \mathrm{in}}{\left(1\ \mathrm{in}\right)^2} \leq \frac{0.08 \cdot 2.9\times 10^{4}\ \mathrm{ksi}}{36\ \mathrm{ksi}}\right):
        \\[10pt]
        M_{ltb} &= M_p = 12\ \mathrm{kipft} &= 12\ \mathrm{kipft}
\end{aligned}"""

def test_sec_F11_2_inelastic():
    shape = aisc.Plate(4*unit.inch, 1*unit.inch, "A36")
    _, M_p = chapter_F.sec_F11_1(shape)
    string, M_ltb = chapter_F.sec_F11_2(
        shape=shape,
        L_b=24*unit.inch,
        M_p=M_p,
        C_b=1,
        precision=4)
    assert isclose(M_ltb, 11.89877407*unit.kipft, atol=1e-8*unit.kipft)
    assert string == r"""\begin{aligned}
    \text{Since, } & \left(\frac{0.08 \cdot E}{F_y} < \frac{L_b \cdot d}{t^2} \leq \frac{1.9 \cdot E}{F_y} \Leftarrow \frac{0.08 \cdot 2.9\times 10^{4}\ \mathrm{ksi}}{36\ \mathrm{ksi}} < \frac{24\ \mathrm{in} \cdot 4\ \mathrm{in}}{\left(1\ \mathrm{in}\right)^2} \leq \frac{1.9 \cdot 2.9\times 10^{4}\ \mathrm{ksi}}{36\ \mathrm{ksi}}\right):
        \\[10pt]
        M_{ltb} &= C_b \cdot \left(1.52 - 0.274 \cdot \left(\frac{L_b \cdot d}{t^2}\right) \cdot \frac{F_y}{E}\right) \cdot F_y \cdot S_x
\\
&= 1 \cdot \left(1.52 - 0.274 \cdot \left(\frac{24\ \mathrm{in} \cdot 4\ \mathrm{in}}{\left(1\ \mathrm{in}\right)^2}\right) \cdot \frac{36\ \mathrm{ksi}}{2.9\times 10^{4}\ \mathrm{ksi}}\right) \cdot 36\ \mathrm{ksi} \cdot 2.667\ \mathrm{in}^{3}
\\
&= 11.9\ \mathrm{kipft}
\end{aligned}"""

def test_sec_F11_2_elastic():
    shape = aisc.Plate(12*unit.inch, 1*unit.inch, "A36")
    _, M_p = chapter_F.sec_F11_1(shape)
    string, M_ltb = chapter_F.sec_F11_2(
        shape=shape,
        L_b=130*unit.inch,
        M_p=M_p,
        C_b=1,
        precision=4)
    assert isclose(M_ltb, 70.64102564*unit.kipft, atol=1e-8*unit.kipft)
    assert string == r"""\begin{aligned}
    \text{Since, } & \left(\frac{L_b \cdot d}{t^2} > \frac{1.9 \cdot E}{F_y} \Leftarrow \frac{130\ \mathrm{in} \cdot 12\ \mathrm{in}}{\left(1\ \mathrm{in}\right)^2} > \frac{1.9 \cdot 2.9\times 10^{4}\ \mathrm{ksi}}{36\ \mathrm{ksi}}\right):
        \\[10pt]
        F_{cr} &= \frac{1.9 \cdot E \cdot C_b}{\frac{L_b \cdot d}{t^2}} = \frac{1.9 \cdot 2.9\times 10^{4}\ \mathrm{ksi} \cdot 1}{\frac{130\ \mathrm{in} \cdot 12\ \mathrm{in}}{\left(1\ \mathrm{in}\right)^2}} &= 35.32\ \mathrm{ksi}
        \\[10pt]
        M_{ltb} &= F_{cr} \cdot S_x = 35.32\ \mathrm{ksi} \cdot 24\ \mathrm{in}^{3} &= 70.64\ \mathrm{kipft}
\end{aligned}"""

def test_sec_F11():
    shape = aisc.Plate(4*unit.inch, 1*unit.inch, "A36")
    string, M_n = chapter_F.sec_F11(
        shape=shape,
        L_b=24*unit.inch,
        C_b=1,
        precision=4)
    assert isclose(M_n, 11.89877407*unit.kipft, atol=1e-8*unit.kipft)
    assert string == r"""#### Plastic Moment Capacity
$$\begin{aligned}
    M_p &= \operatorname{min}\left(F_y \cdot Z_x,\ 1.5 \cdot F_y \cdot S_x\right) = \operatorname{min}\left(36\ \mathrm{ksi} \cdot 4\ \mathrm{in}^{3},\ 1.5 \cdot 36\ \mathrm{ksi} \cdot 2.667\ \mathrm{in}^{3}\right) &= 12\ \mathrm{kipft}
\end{aligned}$$
<br/>
#### Lateral-Torsional Buckling Moment Capacity
$$\begin{aligned}
    \text{Since, } & \left(\frac{0.08 \cdot E}{F_y} < \frac{L_b \cdot d}{t^2} \leq \frac{1.9 \cdot E}{F_y} \Leftarrow \frac{0.08 \cdot 2.9\times 10^{4}\ \mathrm{ksi}}{36\ \mathrm{ksi}} < \frac{24\ \mathrm{in} \cdot 4\ \mathrm{in}}{\left(1\ \mathrm{in}\right)^2} \leq \frac{1.9 \cdot 2.9\times 10^{4}\ \mathrm{ksi}}{36\ \mathrm{ksi}}\right):
        \\[10pt]
        M_{ltb} &= C_b \cdot \left(1.52 - 0.274 \cdot \left(\frac{L_b \cdot d}{t^2}\right) \cdot \frac{F_y}{E}\right) \cdot F_y \cdot S_x
\\
&= 1 \cdot \left(1.52 - 0.274 \cdot \left(\frac{24\ \mathrm{in} \cdot 4\ \mathrm{in}}{\left(1\ \mathrm{in}\right)^2}\right) \cdot \frac{36\ \mathrm{ksi}}{2.9\times 10^{4}\ \mathrm{ksi}}\right) \cdot 36\ \mathrm{ksi} \cdot 2.667\ \mathrm{in}^{3}
\\
&= 11.9\ \mathrm{kipft}
\end{aligned}$$
<br/>
#### Nominal Moment Capacity
$$\begin{aligned}
    M_n &= \operatorname{min}\left(M_p,\ M_{ltb}\right) = \operatorname{min}\left(12\ \mathrm{kipft},\ 11.9\ \mathrm{kipft}\right) &= 11.9\ \mathrm{kipft}
\end{aligned}$$"""
