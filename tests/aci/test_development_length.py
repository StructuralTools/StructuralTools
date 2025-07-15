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

from structuraltools.aci import development_length, materials
from structuraltools.unit import unit


def test_straight_min():
    concrete = materials.Concrete(4000*unit.psi)
    rebar = materials.Rebar(4)
    string, l_d = development_length.straight(
        rebar=rebar,
        concrete=concrete,
        c_c=3*unit.inch,
        s=12*unit.inch,
        precision=4)
    assert isclose(l_d, 12*unit.inch)
    assert l_d.units == "inch"
    assert string == r"""$$\begin{aligned}
    \text{Since, } & \left(w_c \geq 135\ \mathrm{pcf} \Leftarrow 150\ \mathrm{pcf} \geq 135\ \mathrm{pcf}\right): & \lambda &= 1
    \\[10pt]
    \text{Since, } & \left(f_y \leq 60\ \mathrm{ksi} \Leftarrow 60\ \mathrm{ksi} \leq 60\ \mathrm{ksi}\right): & \psi_g &= 1
    \\[10pt]
    \text{Since, } & \left(\mathrm{coated} = \mathrm{False}\right): & \psi_e &= 1
    \\[10pt]
    \text{Since, } & \left(\psi_s \text{ not applied}\right): & \psi_s &= 1
    \\[10pt]
    \text{Since, } & \left(\text{Concrete below} \leq 12\ \mathrm{in}\right): & \psi_t &= 1
\end{aligned}$$
$$\begin{aligned}
    K_{tr} &= \frac{40 \cdot A_{tr}}{s \cdot n} = \frac{40 \cdot 0\ \mathrm{in}^{2}}{12\ \mathrm{in} \cdot 1} &= 0\ \mathrm{in}
    \\[10pt]
    c_b &= \operatorname{min}\left(c_c + \frac{d_b}{2},\ \frac{s}{2}\right) = \operatorname{min}\left(3\ \mathrm{in} + \frac{0.5\ \mathrm{in}}{2},\ \frac{12\ \mathrm{in}}{2}\right) &= 3.25\ \mathrm{in}
    \\[10pt]
    l'_d &= \left(\frac{3 \cdot f_y \cdot \operatorname{min}\left(\psi_t \cdot \psi_e,\ 1.7\right) \cdot \psi_s \cdot \psi_g}{40 \cdot \lambda \cdot \sqrt{f'_c} \cdot \left(\frac{c_b + K_{tr}}{d_b}\right)}\right) \cdot d_b = \left(\frac{3 \cdot 6\times 10^{4}\ \mathrm{psi} \cdot \operatorname{min}\left(1 \cdot 1,\ 1.7\right) \cdot 1 \cdot 1}{40 \cdot 1 \cdot \sqrt{4000\ \mathrm{psi}} \cdot \left(\frac{3.25\ \mathrm{in} + 0\ \mathrm{in}}{0.5\ \mathrm{in}}\right)}\right) \cdot 0.5\ \mathrm{in} &= 5.473\ \mathrm{in}
    \\[10pt]
    l_d &= \operatorname{max}\left(l'_d,\ 12\ \mathrm{in}\right) = \operatorname{max}\left(5.473\ \mathrm{in},\ 12\ \mathrm{in}\right) &= 12\ \mathrm{in}
\end{aligned}$$"""

def test_straight_A_tr():
    concrete = materials.Concrete(4000*unit.psi)
    rebar = materials.Rebar(8)
    string, l_d = development_length.straight(
        rebar=rebar,
        concrete=concrete,
        c_c=3*unit.inch,
        s=12*unit.inch,
        n=4,
        A_tr=0.79*unit.inch**2,
        precision=4)
    assert isclose(l_d, 17.11052041*unit.inch, atol=1e-8)
    assert l_d.units == "inch"
    assert string == r"""$$\begin{aligned}
    \text{Since, } & \left(w_c \geq 135\ \mathrm{pcf} \Leftarrow 150\ \mathrm{pcf} \geq 135\ \mathrm{pcf}\right): & \lambda &= 1
    \\[10pt]
    \text{Since, } & \left(f_y \leq 60\ \mathrm{ksi} \Leftarrow 60\ \mathrm{ksi} \leq 60\ \mathrm{ksi}\right): & \psi_g &= 1
    \\[10pt]
    \text{Since, } & \left(\mathrm{coated} = \mathrm{False}\right): & \psi_e &= 1
    \\[10pt]
    \text{Since, } & \left(\text{Rebar size} \geq 7\right): & \psi_s &= 1
    \\[10pt]
    \text{Since, } & \left(\text{Concrete below} \leq 12\ \mathrm{in}\right): & \psi_t &= 1
\end{aligned}$$
$$\begin{aligned}
    K_{tr} &= \frac{40 \cdot A_{tr}}{s \cdot n} = \frac{40 \cdot 0.79\ \mathrm{in}^{2}}{12\ \mathrm{in} \cdot 4} &= 0.6583\ \mathrm{in}
    \\[10pt]
    c_b &= \operatorname{min}\left(c_c + \frac{d_b}{2},\ \frac{s}{2}\right) = \operatorname{min}\left(3\ \mathrm{in} + \frac{1\ \mathrm{in}}{2},\ \frac{12\ \mathrm{in}}{2}\right) &= 3.5\ \mathrm{in}
    \\[10pt]
    l'_d &= \left(\frac{3 \cdot f_y \cdot \operatorname{min}\left(\psi_t \cdot \psi_e,\ 1.7\right) \cdot \psi_s \cdot \psi_g}{40 \cdot \lambda \cdot \sqrt{f'_c} \cdot \left(\frac{c_b + K_{tr}}{d_b}\right)}\right) \cdot d_b = \left(\frac{3 \cdot 6\times 10^{4}\ \mathrm{psi} \cdot \operatorname{min}\left(1 \cdot 1,\ 1.7\right) \cdot 1 \cdot 1}{40 \cdot 1 \cdot \sqrt{4000\ \mathrm{psi}} \cdot \left(\frac{3.5\ \mathrm{in} + 0.6583\ \mathrm{in}}{1\ \mathrm{in}}\right)}\right) \cdot 1\ \mathrm{in} &= 17.11\ \mathrm{in}
    \\[10pt]
    l_d &= \operatorname{max}\left(l'_d,\ 12\ \mathrm{in}\right) = \operatorname{max}\left(17.11\ \mathrm{in},\ 12\ \mathrm{in}\right) &= 17.11\ \mathrm{in}
\end{aligned}$$"""

def test_straight():
    concrete = materials.Concrete(4000*unit.psi, w_c=110*unit.pcf)
    rebar = materials.Rebar(8, f_y=80*unit.ksi, coated=True)
    string, l_d = development_length.straight(
        rebar=rebar,
        concrete=concrete,
        c_c=3*unit.inch,
        s=12*unit.inch,
        concrete_below=True,
        precision=4)
    assert isclose(l_d, 64.83572711*unit.inch, atol=1e-8)
    assert l_d.units == "inch"
    assert string == r"""$$\begin{aligned}
    \text{Since, } & \left(w_c < 135\ \mathrm{pcf} \Leftarrow 110\ \mathrm{pcf} < 135\ \mathrm{pcf}\right): & \lambda &= 0.75
    \\[10pt]
    \text{Since, } & \left(60\ \mathrm{ksi} < f_y \leq 80\ \mathrm{ksi} \Leftarrow 60\ \mathrm{ksi} < 80\ \mathrm{ksi} \leq 80\ \mathrm{ksi}\right): & \psi_g &= 1.15
    \\[10pt]
    \text{Since, } & \left(\mathrm{coated} = \mathrm{True}\right): & \psi_e &= 1.2
    \\[10pt]
    \text{Since, } & \left(\text{Rebar size} \geq 7\right): & \psi_s &= 1
    \\[10pt]
    \text{Since, } & \left(\text{Concrete below} > 12\ \mathrm{in}\right): & \psi_t &= 1.3
\end{aligned}$$
$$\begin{aligned}
    K_{tr} &= \frac{40 \cdot A_{tr}}{s \cdot n} = \frac{40 \cdot 0\ \mathrm{in}^{2}}{12\ \mathrm{in} \cdot 1} &= 0\ \mathrm{in}
    \\[10pt]
    c_b &= \operatorname{min}\left(c_c + \frac{d_b}{2},\ \frac{s}{2}\right) = \operatorname{min}\left(3\ \mathrm{in} + \frac{1\ \mathrm{in}}{2},\ \frac{12\ \mathrm{in}}{2}\right) &= 3.5\ \mathrm{in}
    \\[10pt]
    l'_d &= \left(\frac{3 \cdot f_y \cdot \operatorname{min}\left(\psi_t \cdot \psi_e,\ 1.7\right) \cdot \psi_s \cdot \psi_g}{40 \cdot \lambda \cdot \sqrt{f'_c} \cdot \left(\frac{c_b + K_{tr}}{d_b}\right)}\right) \cdot d_b = \left(\frac{3 \cdot 8\times 10^{4}\ \mathrm{psi} \cdot \operatorname{min}\left(1.3 \cdot 1.2,\ 1.7\right) \cdot 1 \cdot 1.15}{40 \cdot 0.75 \cdot \sqrt{4000\ \mathrm{psi}} \cdot \left(\frac{3.5\ \mathrm{in} + 0\ \mathrm{in}}{1\ \mathrm{in}}\right)}\right) \cdot 1\ \mathrm{in} &= 64.84\ \mathrm{in}
    \\[10pt]
    l_d &= \operatorname{max}\left(l'_d,\ 12\ \mathrm{in}\right) = \operatorname{max}\left(64.84\ \mathrm{in},\ 12\ \mathrm{in}\right) &= 64.84\ \mathrm{in}
\end{aligned}$$"""

def test_hook_min():
    concrete = materials.Concrete(4000*unit.psi)
    rebar = materials.Rebar(4)
    string, l_dh = development_length.hook(
        rebar=rebar,
        concrete=concrete,
        c_c_side=3*unit.inch,
        s=12*unit.inch,
        precision=4)
    assert isclose(l_dh, 6*unit.inch)
    assert l_dh.units == "inch"
    assert string == r"""$$\begin{aligned}
    & \text{Since, } \left(w_c \geq 135\ \mathrm{pcf} \Leftarrow 150\ \mathrm{pcf} \geq 135\ \mathrm{pcf}\right): & \lambda &= 1
    \\[10pt]
    & \text{Since, } \left(\mathrm{coated} = \mathrm{False}\right): & \psi_e &= 1
    \\[10pt]
    & \text{Since, } \left(s \geq 6 \cdot d_b \Leftarrow 12\ \mathrm{in} \geq 3\ \mathrm{in}\right): & \psi_r &= 1
    \\[10pt]
    & \text{Since, } \left(c_{c_{side}} \geq 6 \cdot d_b \Leftarrow 3\ \mathrm{in} \geq 3\ \mathrm{in}\right): & \psi_o &= 1
\end{aligned}$$
$$\begin{aligned}
    \psi_c &= \operatorname{min}\left(\frac{f'_c}{15000\ \mathrm{psi}} + 0.6,\ 1\right) = \operatorname{min}\left(\frac{4000\ \mathrm{psi}}{15000\ \mathrm{psi}} + 0.6,\ 1\right) &= 0.8667
\end{aligned}$$
$$\begin{aligned}
    l'_{dh} &= \left(\frac{f_y \cdot \psi_e \cdot \psi_r \cdot \psi_o \cdot \psi_c}{55 \cdot \lambda \cdot \sqrt{f'_c}}\right) \cdot d_b^{1.5} = \left(\frac{6\times 10^{4}\ \mathrm{psi} \cdot 1 \cdot 1 \cdot 1 \cdot 0.8667}{55 \cdot 1 \cdot \sqrt{4000\ \mathrm{psi}}}\right) \cdot \left(0.5\ \mathrm{in}\right)^{1.5} &= 5.285\ \mathrm{in}
    \\[10pt]
    l_{dh} &= \operatorname{max}\left(l'_{dh},\ 8 \cdot d_b,\ 6\ \mathrm{in}\right) = \operatorname{max}\left(5.285\ \mathrm{in},\ 8 \cdot 0.5\ \mathrm{in},\ 6\ \mathrm{in}\right) &= 6\ \mathrm{in}
\end{aligned}$$"""

def test_hook_in_column():
    concrete = materials.Concrete(8000*unit.psi, w_c=110*unit.pcf)
    rebar = materials.Rebar(8, coated=True)
    string, l_dh = development_length.hook(
        rebar=rebar,
        concrete=concrete,
        c_c_side=3*unit.inch,
        s=4*unit.inch,
        n=4,
        in_column=True,
        precision=4)
    assert isclose(l_dh, 31.22364012*unit.inch, atol=1e-8)
    assert l_dh.units == "inch"
    assert string == r"""$$\begin{aligned}
    & \text{Since, } \left(w_c < 135\ \mathrm{pcf} \Leftarrow 110\ \mathrm{pcf} < 135\ \mathrm{pcf}\right): & \lambda &= 0.75
    \\[10pt]
    & \text{Since, } \left(\mathrm{coated} = \mathrm{True}\right): & \psi_e &= 1.2
    \\[10pt]
    & \text{Since, } \left(A_{th} < 0.4 \cdot A_{hs} \Leftarrow 0\ \mathrm{in}^{2} < 1.264\ \mathrm{in}^{2}\right) \text{ and } \left(s < 6 \cdot d_b \Leftarrow 4\ \mathrm{in} < 6\ \mathrm{in}\right): & \psi_r &= 1.6
    \\[10pt]
    & \text{Since, } \left(\text{In column} = \mathrm{True}\right) \text{ and } \left(c_{c_{side}} \geq 2.5\ \mathrm{in} \Leftarrow 3\ \mathrm{in} \geq 2.5\ \mathrm{in}\right): & \psi_o &= 1
\end{aligned}$$
$$\begin{aligned}
    \psi_c &= \operatorname{min}\left(\frac{f'_c}{15000\ \mathrm{psi}} + 0.6,\ 1\right) = \operatorname{min}\left(\frac{8000\ \mathrm{psi}}{15000\ \mathrm{psi}} + 0.6,\ 1\right) &= 1
\end{aligned}$$
$$\begin{aligned}
    l'_{dh} &= \left(\frac{f_y \cdot \psi_e \cdot \psi_r \cdot \psi_o \cdot \psi_c}{55 \cdot \lambda \cdot \sqrt{f'_c}}\right) \cdot d_b^{1.5} = \left(\frac{6\times 10^{4}\ \mathrm{psi} \cdot 1.2 \cdot 1.6 \cdot 1 \cdot 1}{55 \cdot 0.75 \cdot \sqrt{8000\ \mathrm{psi}}}\right) \cdot \left(1\ \mathrm{in}\right)^{1.5} &= 31.22\ \mathrm{in}
    \\[10pt]
    l_{dh} &= \operatorname{max}\left(l'_{dh},\ 8 \cdot d_b,\ 6\ \mathrm{in}\right) = \operatorname{max}\left(31.22\ \mathrm{in},\ 8 \cdot 1\ \mathrm{in},\ 6\ \mathrm{in}\right) &= 31.22\ \mathrm{in}
\end{aligned}$$"""

def test_hook():
    concrete = materials.Concrete(8000*unit.psi, w_c=110*unit.pcf)
    rebar = materials.Rebar(8, coated=True)
    string, l_dh = development_length.hook(
        rebar=rebar,
        concrete=concrete,
        c_c_side=3*unit.inch,
        s=4*unit.inch,
        n=4,
        precision=4)
    assert isclose(l_dh, 39.02955015*unit.inch, atol=1e-8)
    assert l_dh.units == "inch"
    assert string == r"""$$\begin{aligned}
    & \text{Since, } \left(w_c < 135\ \mathrm{pcf} \Leftarrow 110\ \mathrm{pcf} < 135\ \mathrm{pcf}\right): & \lambda &= 0.75
    \\[10pt]
    & \text{Since, } \left(\mathrm{coated} = \mathrm{True}\right): & \psi_e &= 1.2
    \\[10pt]
    & \text{Since, } \left(A_{th} < 0.4 \cdot A_{hs} \Leftarrow 0\ \mathrm{in}^{2} < 1.264\ \mathrm{in}^{2}\right) \text{ and } \left(s < 6 \cdot d_b \Leftarrow 4\ \mathrm{in} < 6\ \mathrm{in}\right): & \psi_r &= 1.6
    \\[10pt]
    & \text{Since, } \left(c_{c_{side}} < 6 \cdot d_b \Leftarrow 3\ \mathrm{in} < 6\ \mathrm{in}\right): & \psi_o &= 1.25
\end{aligned}$$
$$\begin{aligned}
    \psi_c &= \operatorname{min}\left(\frac{f'_c}{15000\ \mathrm{psi}} + 0.6,\ 1\right) = \operatorname{min}\left(\frac{8000\ \mathrm{psi}}{15000\ \mathrm{psi}} + 0.6,\ 1\right) &= 1
\end{aligned}$$
$$\begin{aligned}
    l'_{dh} &= \left(\frac{f_y \cdot \psi_e \cdot \psi_r \cdot \psi_o \cdot \psi_c}{55 \cdot \lambda \cdot \sqrt{f'_c}}\right) \cdot d_b^{1.5} = \left(\frac{6\times 10^{4}\ \mathrm{psi} \cdot 1.2 \cdot 1.6 \cdot 1.25 \cdot 1}{55 \cdot 0.75 \cdot \sqrt{8000\ \mathrm{psi}}}\right) \cdot \left(1\ \mathrm{in}\right)^{1.5} &= 39.03\ \mathrm{in}
    \\[10pt]
    l_{dh} &= \operatorname{max}\left(l'_{dh},\ 8 \cdot d_b,\ 6\ \mathrm{in}\right) = \operatorname{max}\left(39.03\ \mathrm{in},\ 8 \cdot 1\ \mathrm{in},\ 6\ \mathrm{in}\right) &= 39.03\ \mathrm{in}
\end{aligned}$$"""
