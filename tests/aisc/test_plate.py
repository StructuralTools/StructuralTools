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


from math import isclose

from structuraltools import aisc, materials, unit

def test_Plate_init():
    steel = materials.Steel("A36")
    plate = aisc.Plate(4*unit.inch, 1*unit.inch, steel)
    assert isclose(plate.A.magnitude, 4)
    assert plate.A.units == "inch ** 2"
    assert isclose(plate.W.magnitude, 13.61111111, abs_tol=1e-8)
    assert plate.W.units == "plf"
    assert isclose(plate.Sx.magnitude, 2.66666667, abs_tol=1e-8)
    assert plate.Sx.units == "inch ** 3"
    assert isclose(plate.Zx.magnitude, 4)
    assert plate.Zx.units == "inch ** 3"
    assert isclose(plate.Ix.magnitude, 5.33333333, abs_tol=1e-8)
    assert plate.Ix.units == "inch ** 4"
    assert isclose(plate.rx.magnitude, 1.15470054, abs_tol=1e-8)
    assert plate.rx.units == "inch"
    assert isclose(plate.Sy.magnitude, 0.66666667, abs_tol=1e-8)
    assert plate.Sy.units == "inch ** 3"
    assert isclose(plate.Zy.magnitude, 1)
    assert plate.Zy.units == "inch ** 3"
    assert isclose(plate.Iy.magnitude, 0.33333333, abs_tol=1e-8)
    assert plate.Iy.units == "inch ** 4"
    assert isclose(plate.ry.magnitude, 0.28867513, abs_tol=1e-8)
    assert plate.ry.units == "inch"


class TestPlate:
    def setup_method(self, method):
        self.steel = materials.Steel("A36")
        self.plate = aisc.Plate(12*unit.inch, 1*unit.inch, self.steel)

    def test_moment_capacity_major_plastic(self):
        latex, phi, M_n = self.plate.moment_capacity(return_latex=True)
        assert isclose(M_n.to("kipft").magnitude, 108)
        assert M_n.units == "kipft"
        assert latex == r"""
    $$ \begin{aligned}
        M_p &= \operatorname{min}\left(F_y \cdot Z_x ,\ 1.5 \cdot F_y \cdot S_x\right) = \operatorname{min}\left(36\ \mathrm{ksi} \cdot 36.0\ \mathrm{in}^{3} ,\ 1.5 \cdot 36\ \mathrm{ksi} \cdot 24.0\ \mathrm{in}^{3}\right) &= 108.0\ \mathrm{kipft}
        \\[10pt]
        
    \end{aligned} $$
    $$ \begin{aligned}
        & \text{Since, } \left(\frac{L_d \cdot d}{t^2} \leq \frac{0.08 \cdot E}{F_y} \Leftarrow 0.0 \leq 64.444\right): & M_n &= M_p
    \end{aligned} $$
    $$ \begin{aligned}

        \\[10pt]
    \end{aligned} $$
"""

    def test_moment_capacity_major_LTB_short(self):
        latex, phi, M_n = self.plate.moment_capacity(
            L_b=100*unit.inch,
            return_latex=True)
        assert isclose(M_n.to("kipft").magnitude, 80.05208276, abs_tol=1e-8)
        assert M_n.units == "kipft"
        assert latex == r"""
    $$ \begin{aligned}
        M_p &= \operatorname{min}\left(F_y \cdot Z_x ,\ 1.5 \cdot F_y \cdot S_x\right) = \operatorname{min}\left(36\ \mathrm{ksi} \cdot 36.0\ \mathrm{in}^{3} ,\ 1.5 \cdot 36\ \mathrm{ksi} \cdot 24.0\ \mathrm{in}^{3}\right) &= 108.0\ \mathrm{kipft}
        \\[10pt]
        
    & \text{Since, } \left(\frac{0.08 \cdot E}{F_y} < \frac{L_b \cdot d}{t^2} \leq \frac{1.9 \cdot E}{F_y} \Leftarrow 64.444 < 1200.0 \leq 1530.556\right):
        \\[10pt]
        & \qquad M_n = \operatorname{min}\left(C_b \cdot \left(1.52 - 0.274 \cdot \frac{L_b \cdot d \cdot F_y}{t^2 \cdot E}\right) \cdot F_y \cdot S_x ,\ M_p\right)
        \\
        & \qquad = \operatorname{min}\left(1 \cdot \left(1.52 - 0.274 \cdot \frac{100\ \mathrm{in} \cdot 12\ \mathrm{in} \cdot 36\ \mathrm{ksi}}{1\ \mathrm{in}^2 \cdot 29000\ \mathrm{ksi}}\right) \cdot 36\ \mathrm{ksi} \cdot 24.0\ \mathrm{in}^{3} ,\ 108.0\ \mathrm{kipft}\right)
        \\
        & \qquad = 80.052\ \mathrm{kipft}

        \\[10pt]
    \end{aligned} $$
"""

    def test_moment_capacity_major_LTB_long(self):
        latex, phi, M_n = self.plate.moment_capacity(
            L_b=130*unit.inch,
            return_latex=True)
        assert isclose(M_n.to("kipft").magnitude, 70.64102564, abs_tol=1e-8)
        assert M_n.units == "kipft"
        assert latex == r"""
    $$ \begin{aligned}
        M_p &= \operatorname{min}\left(F_y \cdot Z_x ,\ 1.5 \cdot F_y \cdot S_x\right) = \operatorname{min}\left(36\ \mathrm{ksi} \cdot 36.0\ \mathrm{in}^{3} ,\ 1.5 \cdot 36\ \mathrm{ksi} \cdot 24.0\ \mathrm{in}^{3}\right) &= 108.0\ \mathrm{kipft}
        \\[10pt]
        
    & \text{Since, } \left(\frac{L_d \cdot d}{t^2} > \frac{1.9 \cdot E}{F_y} \Leftarrow 1560.0 > 1530.556\right):
        \\
        & \qquad M_n = \operatorname{min}\left(\frac{1.9 \cdot E \cdot C_b \cdot t^2 \cdot S_x}{L_b \cdot d} ,\ M_p\right)
        \\
        & \qquad = \operatorname{min}\left(\frac{1.9 \cdot 29000\ \mathrm{ksi} \cdot 1 \cdot 1\ \mathrm{in}^2 \cdot 24.0\ \mathrm{in}^{3}}{130\ \mathrm{in} \cdot 12\ \mathrm{in}} ,\ M_p\right)
        \\
        & \qquad = 70.641\ \mathrm{kipft}

        \\[10pt]
    \end{aligned} $$
"""


class TestPlateMinor:
    def setup_method(self, method):
        self.steel = materials.Steel("A36")
        self.plate = aisc.Plate(1*unit.inch, 12*unit.inch, self.steel)

    def test_moment_capacity_minor_plastic(self):
        latex, phi, M_n = self.plate.moment_capacity_minor(return_latex=True)
        assert isclose(M_n.to("kipft").magnitude, 108)
        assert M_n.units == "kipft"
        assert latex == r"""
    $$ \begin{aligned}
        M_p &= \operatorname{min}\left(F_y \cdot Z_y ,\ 1.5 \cdot F_y \cdot S_y\right) = \operatorname{min}\left(36\ \mathrm{ksi} \cdot 36.0\ \mathrm{in}^{3} ,\ 1.5 \cdot 36\ \mathrm{ksi} \cdot 24.0\ \mathrm{in}^{3}\right) &= 108.0\ \mathrm{kipft}
        \\[10pt]
        
    \end{aligned} $$
    $$ \begin{aligned}
        & \text{Since, } \left(\frac{L_d \cdot t}{d^2} \leq \frac{0.08 \cdot E}{F_y} \Leftarrow 0.0 \leq 64.444\right): & M_n &= M_p
    \end{aligned} $$
    $$ \begin{aligned}

        \\[10pt]
    \end{aligned} $$
"""

    def test_moment_capacity_minor_LTB_short(self):
        latex, phi, M_n = self.plate.moment_capacity_minor(
            L_b=100*unit.inch,
            return_latex=True)
        assert isclose(M_n.to("kipft").magnitude, 80.05208276, abs_tol=1e-8)
        assert M_n.units == "kipft"
        assert latex == r"""
    $$ \begin{aligned}
        M_p &= \operatorname{min}\left(F_y \cdot Z_y ,\ 1.5 \cdot F_y \cdot S_y\right) = \operatorname{min}\left(36\ \mathrm{ksi} \cdot 36.0\ \mathrm{in}^{3} ,\ 1.5 \cdot 36\ \mathrm{ksi} \cdot 24.0\ \mathrm{in}^{3}\right) &= 108.0\ \mathrm{kipft}
        \\[10pt]
        
    & \text{Since, } \left(\frac{0.08 \cdot E}{F_y} < \frac{L_b \cdot t}{d^2} \leq \frac{1.9 \cdot E}{F_y} \Leftarrow 64.444 < 1200.0 \leq 1530.556\right):
        \\[10pt]
        & \qquad M_n = \operatorname{min}\left(C_b \cdot \left(1.52 - 0.274 \cdot \frac{L_b \cdot t \cdot F_y}{d^2 \cdot E}\right) \cdot F_y \cdot S_y ,\ M_p\right)
        \\
        & \qquad = \operatorname{min}\left(1 \cdot \left(1.52 - 0.274 \cdot \frac{100\ \mathrm{in} \cdot 12\ \mathrm{in} \cdot 36\ \mathrm{ksi}}{1\ \mathrm{in}^2 \cdot 29000\ \mathrm{ksi}}\right) \cdot 36\ \mathrm{ksi} \cdot 24.0\ \mathrm{in}^{3} ,\ 108.0\ \mathrm{kipft}\right)
        \\
        & \qquad = 80.052\ \mathrm{kipft}

        \\[10pt]
    \end{aligned} $$
"""

    def test_moment_capacity_minor_LTB_long(self):
        latex, phi, M_n = self.plate.moment_capacity_minor(
            L_b=130*unit.inch,
            return_latex=True)
        assert isclose(M_n.to("kipft").magnitude, 70.64102564, abs_tol=1e-8)
        assert M_n.units == "kipft"
        assert latex == r"""
    $$ \begin{aligned}
        M_p &= \operatorname{min}\left(F_y \cdot Z_y ,\ 1.5 \cdot F_y \cdot S_y\right) = \operatorname{min}\left(36\ \mathrm{ksi} \cdot 36.0\ \mathrm{in}^{3} ,\ 1.5 \cdot 36\ \mathrm{ksi} \cdot 24.0\ \mathrm{in}^{3}\right) &= 108.0\ \mathrm{kipft}
        \\[10pt]
        
    & \text{Since, } \left(\frac{L_d \cdot t}{d^2} > \frac{1.9 \cdot E}{F_y} \Leftarrow 1560.0 > 1530.556\right):
        \\
        & \qquad M_n = \operatorname{min}\left(\frac{1.9 \cdot E \cdot C_b \cdot d^2 \cdot S_y}{L_b \cdot t} ,\ M_p\right)
        \\
        & \qquad = \operatorname{min}\left(\frac{1.9 \cdot 29000\ \mathrm{ksi} \cdot 1 \cdot 1\ \mathrm{in}^2 \cdot 24.0\ \mathrm{in}^{3}}{130\ \mathrm{in} \cdot 12\ \mathrm{in}} ,\ M_p\right)
        \\
        & \qquad = 70.641\ \mathrm{kipft}

        \\[10pt]
    \end{aligned} $$
"""
