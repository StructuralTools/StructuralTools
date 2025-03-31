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

from structuraltools import aisc, materials, unit

def test_Plate_init():
    steel = materials.Steel("A36")
    plate = aisc.Plate(4*unit.inch, 1*unit.inch, steel)
    assert isclose(plate.A, 4*unit.inch**2)
    assert isclose(plate.W, 13.61111111*unit.plf, atol=1e-8)
    assert isclose(plate.S_x, 2.66666667*unit.inch**3, atol=1e-8)
    assert isclose(plate.Z_x, 4*unit.inch**3)
    assert isclose(plate.I_x, 5.33333333*unit.inch**4, atol=1e-8)
    assert isclose(plate.r_x, 1.15470054*unit.inch, atol=1e-8)
    assert isclose(plate.S_y, 0.66666667*unit.inch**3, atol=1e-8)
    assert isclose(plate.Z_y, 1*unit.inch**3)
    assert isclose(plate.I_y, 0.33333333*unit.inch**4, atol=1e-8)
    assert isclose(plate.r_y, 0.28867513*unit.inch, atol=1e-8)


class TestPlate:
    def setup_method(self, method):
        self.steel = materials.Steel("A36")
        self.plate = aisc.Plate(12*unit.inch, 1*unit.inch, self.steel)

    def test_compression_capacity_inelastic(self):
        phi, P_n = self.plate.compression_capacity(L_x=3*unit.ft, L_y=3*unit.ft)
        assert isclose(P_n, 190.50898212391965*unit.kip)

    def test_compression_capacity_elastic(self):
        phi, P_n = self.plate.compression_capacity(L_x=4*unit.ft, L_y=4*unit.ft)
        assert isclose(P_n, 108.94689615143473*unit.kip)

    def test_moment_capacity_major_plastic(self):
        markdown, phi, M_n = self.plate.moment_capacity(return_markdown=True)
        assert isclose(M_n, 108*unit.kipft)
        assert markdown == r"""$$ \begin{aligned}
    M_p &= \operatorname{min}\left(F_y \cdot Z_x ,\ 1.5 \cdot F_y \cdot S_x\right)
        = \operatorname{min}\left(36\ \mathrm{ksi} \cdot 36.0\ \mathrm{in}^{3} ,\ 1.5 \cdot 36\ \mathrm{ksi} \cdot 24.0\ \mathrm{in}^{3}\right)
        &= 108.0\ \mathrm{kipft}
    \\[10pt]
    \end{aligned} $$ $$ \begin{aligned}
    & \text{Since, } \left(\frac{L_d \cdot d}{t^2} \leq \frac{0.08 \cdot E}{F_y} \Leftarrow 0.0 \leq 64.444\right): & M_n &= M_p
\end{aligned} $$ $$ \begin{aligned}
\end{aligned} $$"""

    def test_moment_capacity_major_LTB_short(self):
        markdown, phi, M_n = self.plate.moment_capacity(
            L_b=100*unit.inch,
            return_markdown=True)
        assert isclose(M_n, 80.05208276*unit.kipft, atol=1e-8)
        assert markdown == r"""$$ \begin{aligned}
    M_p &= \operatorname{min}\left(F_y \cdot Z_x ,\ 1.5 \cdot F_y \cdot S_x\right)
        = \operatorname{min}\left(36\ \mathrm{ksi} \cdot 36.0\ \mathrm{in}^{3} ,\ 1.5 \cdot 36\ \mathrm{ksi} \cdot 24.0\ \mathrm{in}^{3}\right)
        &= 108.0\ \mathrm{kipft}
    \\[10pt]
    & \text{Since, } \left(\frac{0.08 \cdot E}{F_y} < \frac{L_b \cdot d}{t^2} \leq \frac{1.9 \cdot E}{F_y} \Leftarrow 64.444 < 1200.0 \leq 1530.556\right):
    \\[10pt]
    & \qquad M_n = \operatorname{min}\left(C_b \cdot \left(1.52 - 0.274 \cdot \frac{L_b \cdot d \cdot F_y}{t^2 \cdot E}\right) \cdot F_y \cdot S_x ,\ M_p\right)
        \\
        & \qquad = \operatorname{min}\left(1 \cdot \left(1.52 - 0.274 \cdot \frac{100\ \mathrm{in} \cdot 12\ \mathrm{in} \cdot 36\ \mathrm{ksi}}{1\ \mathrm{in}^2 \cdot 29000\ \mathrm{ksi}}\right) \cdot 36\ \mathrm{ksi} \cdot 24.0\ \mathrm{in}^{3} ,\ 108.0\ \mathrm{kipft}\right)
        \\
        & \qquad = 80.052\ \mathrm{kipft}
\end{aligned} $$"""

    def test_moment_capacity_major_LTB_long(self):
        markdown, phi, M_n = self.plate.moment_capacity(
            L_b=130*unit.inch,
            return_markdown=True)
        assert isclose(M_n, 70.64102564*unit.kipft, atol=1e-8)
        assert markdown == r"""$$ \begin{aligned}
    M_p &= \operatorname{min}\left(F_y \cdot Z_x ,\ 1.5 \cdot F_y \cdot S_x\right)
        = \operatorname{min}\left(36\ \mathrm{ksi} \cdot 36.0\ \mathrm{in}^{3} ,\ 1.5 \cdot 36\ \mathrm{ksi} \cdot 24.0\ \mathrm{in}^{3}\right)
        &= 108.0\ \mathrm{kipft}
    \\[10pt]
    & \text{Since, } \left(\frac{L_d \cdot d}{t^2} > \frac{1.9 \cdot E}{F_y} \Leftarrow 1560.0 > 1530.556\right):
    \\[10pt]
    & \qquad M_n = \operatorname{min}\left(\frac{1.9 \cdot E \cdot C_b \cdot t^2 \cdot S_x}{L_b \cdot d} ,\ M_p\right)
        \\
        & \qquad = \operatorname{min}\left(\frac{1.9 \cdot 29000\ \mathrm{ksi} \cdot 1 \cdot 1\ \mathrm{in}^2 \cdot 24.0\ \mathrm{in}^{3}}{130\ \mathrm{in} \cdot 12\ \mathrm{in}} ,\ M_p\right)
        \\
        & \qquad = 70.641\ \mathrm{kipft}
\end{aligned} $$"""


class TestPlateMinor:
    def setup_method(self, method):
        self.steel = materials.Steel("A36")
        self.plate = aisc.Plate(1*unit.inch, 12*unit.inch, self.steel)

    def test_moment_capacity_minor_plastic(self):
        markdown, phi, M_n = self.plate.moment_capacity_minor(return_markdown=True)
        assert isclose(M_n, 108*unit.kipft)
        assert markdown == r"""$$ \begin{aligned}
    M_p &= \operatorname{min}\left(F_y \cdot Z_y ,\ 1.5 \cdot F_y \cdot S_y\right)
        = \operatorname{min}\left(36\ \mathrm{ksi} \cdot 36.0\ \mathrm{in}^{3} ,\ 1.5 \cdot 36\ \mathrm{ksi} \cdot 24.0\ \mathrm{in}^{3}\right)
        &= 108.0\ \mathrm{kipft}
    \\[10pt]
    \end{aligned} $$ $$ \begin{aligned}
    & \text{Since, } \left(\frac{L_d \cdot t}{d^2} \leq \frac{0.08 \cdot E}{F_y} \Leftarrow 0.0 \leq 64.444\right): & M_n &= M_p
\end{aligned} $$ $$ \begin{aligned}
\end{aligned} $$"""

    def test_moment_capacity_minor_LTB_short(self):
        markdown, phi, M_n = self.plate.moment_capacity_minor(
            L_b=100*unit.inch,
            return_markdown=True)
        assert isclose(M_n, 80.05208276*unit.kipft, atol=1e-8)
        assert markdown == r"""$$ \begin{aligned}
    M_p &= \operatorname{min}\left(F_y \cdot Z_y ,\ 1.5 \cdot F_y \cdot S_y\right)
        = \operatorname{min}\left(36\ \mathrm{ksi} \cdot 36.0\ \mathrm{in}^{3} ,\ 1.5 \cdot 36\ \mathrm{ksi} \cdot 24.0\ \mathrm{in}^{3}\right)
        &= 108.0\ \mathrm{kipft}
    \\[10pt]
    & \text{Since, } \left(\frac{0.08 \cdot E}{F_y} < \frac{L_b \cdot t}{d^2} \leq \frac{1.9 \cdot E}{F_y} \Leftarrow 64.444 < 1200.0 \leq 1530.556\right):
    \\[10pt]
    & \qquad M_n = \operatorname{min}\left(C_b \cdot \left(1.52 - 0.274 \cdot \frac{L_b \cdot t \cdot F_y}{d^2 \cdot E}\right) \cdot F_y \cdot S_y ,\ M_p\right)
        \\
        & \qquad = \operatorname{min}\left(1 \cdot \left(1.52 - 0.274 \cdot \frac{100\ \mathrm{in} \cdot 12\ \mathrm{in} \cdot 36\ \mathrm{ksi}}{1\ \mathrm{in}^2 \cdot 29000\ \mathrm{ksi}}\right) \cdot 36\ \mathrm{ksi} \cdot 24.0\ \mathrm{in}^{3} ,\ 108.0\ \mathrm{kipft}\right)
        \\
        & \qquad = 80.052\ \mathrm{kipft}
\end{aligned} $$"""

    def test_moment_capacity_minor_LTB_long(self):
        markdown, phi, M_n = self.plate.moment_capacity_minor(
            L_b=130*unit.inch,
            return_markdown=True)
        assert isclose(M_n, 70.64102564*unit.kipft, atol=1e-8)
        assert markdown == r"""$$ \begin{aligned}
    M_p &= \operatorname{min}\left(F_y \cdot Z_y ,\ 1.5 \cdot F_y \cdot S_y\right)
        = \operatorname{min}\left(36\ \mathrm{ksi} \cdot 36.0\ \mathrm{in}^{3} ,\ 1.5 \cdot 36\ \mathrm{ksi} \cdot 24.0\ \mathrm{in}^{3}\right)
        &= 108.0\ \mathrm{kipft}
    \\[10pt]
    & \text{Since, } \left(\frac{L_d \cdot t}{d^2} > \frac{1.9 \cdot E}{F_y} \Leftarrow 1560.0 > 1530.556\right):
    \\[10pt]
    & \qquad M_n = \operatorname{min}\left(\frac{1.9 \cdot E \cdot C_b \cdot d^2 \cdot S_y}{L_b \cdot t} ,\ M_p\right)
        \\
        & \qquad = \operatorname{min}\left(\frac{1.9 \cdot 29000\ \mathrm{ksi} \cdot 1 \cdot 1\ \mathrm{in}^2 \cdot 24.0\ \mathrm{in}^{3}}{130\ \mathrm{in} \cdot 12\ \mathrm{in}} ,\ M_p\right)
        \\
        & \qquad = 70.641\ \mathrm{kipft}
\end{aligned} $$"""
