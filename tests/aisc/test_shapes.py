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
from structuraltools.unit import unit


def test_Plate_init():
    plate = aisc.Plate(4*unit.inch, 1*unit.inch, "A36")
    assert isclose(plate.A, 4*unit.inch**2)
    assert isclose(plate.S_x, 2.66666667*unit.inch**3, atol=1e-8*unit.inch**3)
    assert isclose(plate.I_x, 5.33333333*unit.inch**4, atol=1e-8*unit.inch**4)
    assert isclose(plate.r_x, 1.15470054*unit.inch, atol=1e-8*unit.inch)
    assert isclose(plate.Z_x, 4*unit.inch**3)
    assert isclose(plate.S_y, 0.66666667*unit.inch**3, atol=1e-8*unit.inch**3)
    assert isclose(plate.I_y, 0.33333333*unit.inch**4, atol=1e-8*unit.inch**4)
    assert isclose(plate.r_y, 0.28867513*unit.inch, atol=1e-8*unit.inch)
    assert isclose(plate.Z_y, 1*unit.inch**3)
    assert plate.F_y == 36*unit.ksi


class TestPlate:
    def setup_method(self, method):
        self.plate = aisc.Plate(12*unit.inch, 1*unit.inch, "A36")

    def test_compression_capacity_inelastic(self):
        string, phiP_n = self.plate.compression_capacity(3*unit.ft, "y", precision=4)
        assert isclose(phiP_n[1], 190.50898212391965*unit.kip)
        assert string == r"""$$
\begin{aligned}
    F_e &= \frac{\pi^2 \cdot E}{\left(\frac{L_{c_{y}}}{r_{y}}\right)^2} = \frac{\pi^2 \cdot 2.9\times 10^{4}\ \mathrm{ksi}}{\left(\frac{3\ \mathrm{ft}}{0.2887\ \mathrm{in}}\right)^2} &= 18.4\ \mathrm{ksi}
    \\[10pt]
    \text{Since, } & \left(\frac{F_y}{F_e} \leq 2.25 \Leftarrow \frac{36\ \mathrm{ksi}}{18.4\ \mathrm{ksi}} \leq 2.25\right):
    \\[10pt]
    F_n &= \left(0.658^{\frac{F_y}{F_e}}\right) \cdot F_y = \left(0.658^{\frac{36\ \mathrm{ksi}}{18.4\ \mathrm{ksi}}}\right) \cdot 36\ \mathrm{ksi} &=  15.88\ \mathrm{ksi}
    \\[10pt]
    P_n &= F_n \cdot A_g = 15.88\ \mathrm{ksi} \cdot 12\ \mathrm{in}^{2} &= 190.5\ \mathrm{kip}
\end{aligned}
$$"""

    def test_compression_capacity_elastic(self):
        string, phiP_n = self.plate.compression_capacity(4*unit.ft, "y", precision=4)
        assert isclose(phiP_n[1], 108.94689615143473*unit.kip)
        assert string == r"""$$
\begin{aligned}
    F_e &= \frac{\pi^2 \cdot E}{\left(\frac{L_{c_{y}}}{r_{y}}\right)^2} = \frac{\pi^2 \cdot 2.9\times 10^{4}\ \mathrm{ksi}}{\left(\frac{4\ \mathrm{ft}}{0.2887\ \mathrm{in}}\right)^2} &= 10.35\ \mathrm{ksi}
    \\[10pt]
    \text{Since, } & \left(\frac{F_y}{F_e} > 2.25 \Leftarrow \frac{36\ \mathrm{ksi}}{10.35\ \mathrm{ksi}} > 2.25\right):
    \\[10pt]
    F_n &= 0.877 \cdot F_e = 0.877 \cdot 10.35\ \mathrm{ksi} &= 9.079\ \mathrm{ksi}
    \\[10pt]
    P_n &= F_n \cdot A_g = 9.079\ \mathrm{ksi} \cdot 12\ \mathrm{in}^{2} &= 108.9\ \mathrm{kip}
\end{aligned}
$$"""

    def test_moment_capacity_plastic(self):
        string, phiM_n = self.plate.moment_capacity(precision=4)
        assert isclose(phiM_n[1], 108*unit.kipft)
        assert string == r"""#### Plastic Moment Capacity
$$
\begin{aligned}
    M_p &= \operatorname{min}\left(F_y \cdot Z_x,\ 1.5 \cdot F_y \cdot S_x\right) = \operatorname{min}\left(36\ \mathrm{ksi} \cdot 36\ \mathrm{in}^{3},\ 1.5 \cdot 36\ \mathrm{ksi} \cdot 24\ \mathrm{in}^{3}\right) &= 108\ \mathrm{kipft}
\end{aligned}
$$

#### Lateral-Torsional Buckling Moment Capacity
$$
\begin{aligned}
    \text{Since, } & \left(\frac{L_b \cdot d}{t^2} \leq \frac{0.08 \cdot E}{F_y} \Leftarrow \frac{0\ \mathrm{ft} \cdot 12\ \mathrm{in}}{\left(1\ \mathrm{in}\right)^2} \leq \frac{0.08 \cdot 2.9\times 10^{4}\ \mathrm{ksi}}{36\ \mathrm{ksi}}\right):
        \\[10pt]
        M_{ltb} &= M_p = 108\ \mathrm{kipft} &= 108\ \mathrm{kipft}
\end{aligned}
$$

#### Nominal Moment Capacity
$$
\begin{aligned}
    M_n &= \operatorname{min}\left(M_p,\ M_{ltb}\right) = \operatorname{min}\left(108\ \mathrm{kipft},\ 108\ \mathrm{kipft}\right) &= 108\ \mathrm{kipft}
\end{aligned}
$$"""

    def test_moment_capacity_LTB_short(self):
        string, phiM_n = self.plate.moment_capacity(
            L_b=100*unit.inch,
            precision=4)
        assert isclose(phiM_n[1], 80.05208276*unit.kipft, atol=1e-8)
        assert string == r"""#### Plastic Moment Capacity
$$
\begin{aligned}
    M_p &= \operatorname{min}\left(F_y \cdot Z_x,\ 1.5 \cdot F_y \cdot S_x\right) = \operatorname{min}\left(36\ \mathrm{ksi} \cdot 36\ \mathrm{in}^{3},\ 1.5 \cdot 36\ \mathrm{ksi} \cdot 24\ \mathrm{in}^{3}\right) &= 108\ \mathrm{kipft}
\end{aligned}
$$

#### Lateral-Torsional Buckling Moment Capacity
$$
\begin{aligned}
    \text{Since, } & \left(\frac{0.08 \cdot E}{F_y} < \frac{L_b \cdot d}{t^2} \leq \frac{1.9 \cdot E}{F_y} \Leftarrow \frac{0.08 \cdot 2.9\times 10^{4}\ \mathrm{ksi}}{36\ \mathrm{ksi}} < \frac{100\ \mathrm{in} \cdot 12\ \mathrm{in}}{\left(1\ \mathrm{in}\right)^2} \leq \frac{1.9 \cdot 2.9\times 10^{4}\ \mathrm{ksi}}{36\ \mathrm{ksi}}\right):
        \\[10pt]
        M_{ltb} &= C_b \cdot \left(1.52 - 0.274 \cdot \left(\frac{L_b \cdot d}{t^2}\right) \cdot \frac{F_y}{E}\right) \cdot F_y \cdot S_x
\\
&= 1 \cdot \left(1.52 - 0.274 \cdot \left(\frac{100\ \mathrm{in} \cdot 12\ \mathrm{in}}{\left(1\ \mathrm{in}\right)^2}\right) \cdot \frac{36\ \mathrm{ksi}}{2.9\times 10^{4}\ \mathrm{ksi}}\right) \cdot 36\ \mathrm{ksi} \cdot 24\ \mathrm{in}^{3}
\\
&= 80.05\ \mathrm{kipft}
\end{aligned}
$$

#### Nominal Moment Capacity
$$
\begin{aligned}
    M_n &= \operatorname{min}\left(M_p,\ M_{ltb}\right) = \operatorname{min}\left(108\ \mathrm{kipft},\ 80.05\ \mathrm{kipft}\right) &= 80.05\ \mathrm{kipft}
\end{aligned}
$$"""

    def test_moment_capacity_LTB_long(self):
        string, phiM_n = self.plate.moment_capacity(
            L_b=130*unit.inch,
            precision=4)
        assert isclose(phiM_n[1], 70.64102564*unit.kipft, atol=1e-8)
        assert string == r"""#### Plastic Moment Capacity
$$
\begin{aligned}
    M_p &= \operatorname{min}\left(F_y \cdot Z_x,\ 1.5 \cdot F_y \cdot S_x\right) = \operatorname{min}\left(36\ \mathrm{ksi} \cdot 36\ \mathrm{in}^{3},\ 1.5 \cdot 36\ \mathrm{ksi} \cdot 24\ \mathrm{in}^{3}\right) &= 108\ \mathrm{kipft}
\end{aligned}
$$

#### Lateral-Torsional Buckling Moment Capacity
$$
\begin{aligned}
    \text{Since, } & \left(\frac{L_b \cdot d}{t^2} > \frac{1.9 \cdot E}{F_y} \Leftarrow \frac{130\ \mathrm{in} \cdot 12\ \mathrm{in}}{\left(1\ \mathrm{in}\right)^2} > \frac{1.9 \cdot 2.9\times 10^{4}\ \mathrm{ksi}}{36\ \mathrm{ksi}}\right):
        \\[10pt]
        F_{cr} &= \frac{1.9 \cdot E \cdot C_b}{\frac{L_b \cdot d}{t^2}} = \frac{1.9 \cdot 2.9\times 10^{4}\ \mathrm{ksi} \cdot 1}{\frac{130\ \mathrm{in} \cdot 12\ \mathrm{in}}{\left(1\ \mathrm{in}\right)^2}} &= 35.32\ \mathrm{ksi}
        \\[10pt]
        M_{ltb} &= F_{cr} \cdot S_x = 35.32\ \mathrm{ksi} \cdot 24\ \mathrm{in}^{3} &= 70.64\ \mathrm{kipft}
\end{aligned}
$$

#### Nominal Moment Capacity
$$
\begin{aligned}
    M_n &= \operatorname{min}\left(M_p,\ M_{ltb}\right) = \operatorname{min}\left(108\ \mathrm{kipft},\ 70.64\ \mathrm{kipft}\right) &= 70.64\ \mathrm{kipft}
\end{aligned}
$$"""

    def test_moment_capacity_minor(self):
        string, phiM_n = self.plate.moment_capacity(axis="y", precision=4)
        assert isclose(phiM_n[1], 9*unit.kipft)
        assert string == r"""#### Nominal Moment Capacity
$$
\begin{aligned}
    M_n &= \operatorname{min}\left(F_y \cdot Z_y,\ 1.5 \cdot F_y \cdot S_y\right) = \operatorname{min}\left(36\ \mathrm{ksi} \cdot 3\ \mathrm{in}^{3},\ 1.5 \cdot 36\ \mathrm{ksi} \cdot 2\ \mathrm{in}^{3}\right) &= 9\ \mathrm{kipft}
\end{aligned}
$$"""


def test_WideFlange_init():
    wide_flange = aisc.WideFlange("W10X12", "A36")
    assert wide_flange.W == 12*unit.plf
    assert wide_flange.F_y == 36*unit.ksi


class TestWideFlange:
    def test_moment_capacity_plastic(self):
        wide_flange = aisc.WideFlange("W12X22")
        string, phiM_n = wide_flange.moment_capacity(precision=4)
        assert isclose(phiM_n[0]*phiM_n[1], 110*unit.kipft, atol=1*unit.kipft)
        assert string == r"""#### Plastic Moment Capacity
$$
\begin{aligned}
    M_p &= F_y \cdot Z_x = 50\ \mathrm{ksi} \cdot 29.3\ \mathrm{in}^{3} &= 122.1\ \mathrm{kipft}
\end{aligned}
$$

#### Lateral-Torsional Buckling Moment Capacity
$$
\begin{aligned}
    L_p &= 1.76 \cdot r_y \cdot \sqrt{\frac{E}{F_y}} = 1.76 \cdot 0.848\ \mathrm{in} \cdot \sqrt{\frac{2.9\times 10^{4}\ \mathrm{ksi}}{50\ \mathrm{ksi}}} &= 2.995\ \mathrm{ft}
    \\[10pt]
    \text{Since, } & \left(L_b \leq L_p \Leftarrow 0\ \mathrm{ft} \leq 2.995\ \mathrm{ft}\right):
        \\[10pt]
        M_{ltb} &= M_p = 122.1\ \mathrm{kipft} &= 122.1\ \mathrm{kipft}
\end{aligned}
$$

#### Nominal Moment Capacity
$$
\begin{aligned}
    M_n &= \operatorname{min}\left(M_p,\ M_{ltb}\right) = \operatorname{min}\left(122.1\ \mathrm{kipft},\ 122.1\ \mathrm{kipft}\right) &= 122.1\ \mathrm{kipft}
\end{aligned}
$$"""

    def test_moment_capacity_inelastic_ltb(self):
        wide_flange = aisc.WideFlange("W12X22")
        string, phiM_n = wide_flange.moment_capacity(L_b=7*unit.ft, precision=4)
        assert isclose(phiM_n[0]*phiM_n[1], 81.7*unit.kipft, atol=1*unit.kipft)
        assert string == r"""#### Plastic Moment Capacity
$$
\begin{aligned}
    M_p &= F_y \cdot Z_x = 50\ \mathrm{ksi} \cdot 29.3\ \mathrm{in}^{3} &= 122.1\ \mathrm{kipft}
\end{aligned}
$$

#### Lateral-Torsional Buckling Moment Capacity
$$
\begin{aligned}
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
\end{aligned}
$$

#### Nominal Moment Capacity
$$
\begin{aligned}
    M_n &= \operatorname{min}\left(M_p,\ M_{ltb}\right) = \operatorname{min}\left(122.1\ \mathrm{kipft},\ 90.76\ \mathrm{kipft}\right) &= 90.76\ \mathrm{kipft}
\end{aligned}
$$"""

    def test_moment_capacity_elastic_ltb(self):
        wide_flange = aisc.WideFlange("W12X22")
        string, phiM_n = wide_flange.moment_capacity(L_b=15*unit.ft, precision=4)
        assert isclose(phiM_n[0]*phiM_n[1], 32.9*unit.kipft, atol=1*unit.kipft)
        assert string == r"""#### Plastic Moment Capacity
$$
\begin{aligned}
    M_p &= F_y \cdot Z_x = 50\ \mathrm{ksi} \cdot 29.3\ \mathrm{in}^{3} &= 122.1\ \mathrm{kipft}
\end{aligned}
$$

#### Lateral-Torsional Buckling Moment Capacity
$$
\begin{aligned}
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
\end{aligned}
$$

#### Nominal Moment Capacity
$$
\begin{aligned}
    M_n &= \operatorname{min}\left(M_p,\ M_{ltb}\right) = \operatorname{min}\left(122.1\ \mathrm{kipft},\ 36.54\ \mathrm{kipft}\right) &= 36.54\ \mathrm{kipft}
\end{aligned}
$$"""

    def test_moment_capacity_flange_local_buckling(self):
        wide_flange = aisc.WideFlange("W10X12")
        string, phiM_n = wide_flange.moment_capacity(precision=4)
        assert isclose(phiM_n[0]*phiM_n[1], 46.9*unit.kipft, atol=1*unit.kipft)
        assert string == r"""#### Plastic Moment
$$
\begin{aligned}
    M_p &= F_y \cdot Z_x = 50\ \mathrm{ksi} \cdot 12.6\ \mathrm{in}^{3} &= 52.5\ \mathrm{kipft}
\end{aligned}
$$

#### Lateral-Torsional Buckling Moment Capacity
$$
\begin{aligned}
    L_p &= 1.76 \cdot r_y \cdot \sqrt{\frac{E}{F_y}} = 1.76 \cdot 0.785\ \mathrm{in} \cdot \sqrt{\frac{2.9\times 10^{4}\ \mathrm{ksi}}{50\ \mathrm{ksi}}} &= 2.773\ \mathrm{ft}
    \\[10pt]
    \text{Since, } & \left(L_b \leq L_p \Leftarrow 0\ \mathrm{ft} \leq 2.773\ \mathrm{ft}\right):
        \\[10pt]
        M_{ltb} &= M_p = 52.5\ \mathrm{kipft} &= 52.5\ \mathrm{kipft}
\end{aligned}
$$

#### Compression Flange Local Buckling Moment Capacity
$$
\begin{aligned}
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
\end{aligned}
$$

#### Nominal Moment Capacity
$$
\begin{aligned}
    M_n &= \operatorname{min}\left(M_{ltb},\ M_{flb}\right) = \operatorname{min}\left(52.5\ \mathrm{kipft},\ 52.11\ \mathrm{kipft}\right) &= 52.11\ \mathrm{kipft}
\end{aligned}
$$"""
