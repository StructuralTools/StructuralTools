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


def test_WideFlange_init():
    steel = materials.Steel("A992")
    wide_flange = aisc.WideFlange("W10X12", steel)
    assert wide_flange.W == 12*unit.plf


class TestWideFlange:
    def setup_method(self, method):
        self.steel = materials.Steel("A992")

    def test_moment_capacity_plastic(self):
        wide_flange = aisc.WideFlange("W12X22", self.steel)
        markdown, phi_b, M_n = wide_flange.moment_capacity(return_markdown=True)
        assert isclose(phi_b*M_n, 110*unit.kipft, atol=1*unit.kipft)
        assert markdown == r"""$$ \begin{aligned}
    M_p &= F_y \cdot Z_x
        = 50\ \mathrm{ksi} \cdot 29.3\ \mathrm{in}^{3}
        &= 122.083\ \mathrm{kipft}
    \\[10pt]
    \\[10pt]
    L_p &= 1.76 \cdot r_y \sqrt{\frac{E}{F_y}}
        = 1.76 \cdot 0.848\ \mathrm{in} \sqrt{\frac{29000\ \mathrm{ksi}}{50\ \mathrm{ksi}}}
        &= 35.944\ \mathrm{in}
    \\[10pt]
    \text{Since, } & \left(L_b \leq L_p \Leftarrow 0\ \mathrm{in} \leq 35.944\ \mathrm{in}\right):
        \\[10pt]
        M_{ltb} &= M_p
            = 122.083\ \mathrm{kipft}
            &= 122.083\ \mathrm{kipft}
    \\[10pt]
    \\[10pt]
    \lambda_{pf} &= 0.38 \cdot \sqrt{\frac{E}{F_y}}
        = 0.38 \cdot \sqrt{\frac{29000\ \mathrm{ksi}}{50\ \mathrm{ksi}}}
        &= 9.152
    \\[10pt]
    \text{Since, } & \left(\lambda_f < \lambda_{pf} \Leftarrow 4.74 < 9.152\right):
        \\[10pt]
        M_{flb} &= M_p
            = 122.083\ \mathrm{kipft}
            &= 122.083\ \mathrm{kipft}
    \\[10pt]
    \\[10pt]
    M_n &= \operatorname{min}\left(M_p,\ M_{ltb},\ M_{flb}\right)
        = \operatorname{min}\left(122.083\ \mathrm{kipft},\ 122.083\ \mathrm{kipft},\ 122.083\ \mathrm{kipft}\right)
        &= 122.083\ \mathrm{kipft}
\end{aligned} $$"""

    def test_moment_capacity_inelastic_ltb(self):
        wide_flange = aisc.WideFlange("W12X22", self.steel)
        markdown, phi_b, M_n = wide_flange.moment_capacity(L_b=7*unit.ft, return_markdown=True)
        assert isclose(phi_b*M_n, 81.7*unit.kipft, atol=1*unit.kipft)
        assert markdown == r"""$$ \begin{aligned}
    M_p &= F_y \cdot Z_x
        = 50\ \mathrm{ksi} \cdot 29.3\ \mathrm{in}^{3}
        &= 122.083\ \mathrm{kipft}
    \\[10pt]
    \\[10pt]
    L_p &= 1.76 \cdot r_y \sqrt{\frac{E}{F_y}}
        = 1.76 \cdot 0.848\ \mathrm{in} \sqrt{\frac{29000\ \mathrm{ksi}}{50\ \mathrm{ksi}}}
        &= 35.944\ \mathrm{in}
    \\[10pt]
    L_r &= \frac{1.95 \cdot r_{ts} \cdot E}{0.7 \cdot F_y} \cdot \sqrt{\frac{J \cdot c}{S_x \cdot h_o} + \sqrt{\left(\frac{J \cdot c}{S_x \cdot h_o}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot F_y}{E}\right)^2}}
        \\
        &= \frac{1.95 \cdot 1.04\ \mathrm{in} \cdot 29000\ \mathrm{ksi}}{0.7 \cdot 50\ \mathrm{ksi}} \cdot \sqrt{\frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}} + \sqrt{\left(\frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot 50\ \mathrm{ksi}}{29000\ \mathrm{ksi}}\right)^2}}
        \\
        &= 109.591\ \mathrm{in}
    \\[10pt]
    \text{Since, } & \left(L_p < L_b \leq L_r \Leftarrow 35.944\ \mathrm{in} < 7\ \mathrm{ft} \leq 109.591\ \mathrm{in}\right):
        \\[10pt]
        M_{ltb} &= C_b \cdot \left(M_p - \left(M_p - 0.7 \cdot F_y \cdot S_x\right) \cdot \frac{L_b - L_p}{L_r - L_p}\right)
            \\
            &= 1 \cdot \left(122.083\ \mathrm{kipft} - \left(122.083\ \mathrm{kipft} - 0.7 \cdot 50\ \mathrm{ksi} \cdot 25.4\ \mathrm{in}^{3}\right) \cdot \frac{7\ \mathrm{ft} - 35.944\ \mathrm{in}}{109.591\ \mathrm{in} - 35.944\ \mathrm{in}}\right)
            \\
            &= 90.763\ \mathrm{kipft}
    \\[10pt]
    \\[10pt]
    \lambda_{pf} &= 0.38 \cdot \sqrt{\frac{E}{F_y}}
        = 0.38 \cdot \sqrt{\frac{29000\ \mathrm{ksi}}{50\ \mathrm{ksi}}}
        &= 9.152
    \\[10pt]
    \text{Since, } & \left(\lambda_f < \lambda_{pf} \Leftarrow 4.74 < 9.152\right):
        \\[10pt]
        M_{flb} &= M_p
            = 122.083\ \mathrm{kipft}
            &= 122.083\ \mathrm{kipft}
    \\[10pt]
    \\[10pt]
    M_n &= \operatorname{min}\left(M_p,\ M_{ltb},\ M_{flb}\right)
        = \operatorname{min}\left(122.083\ \mathrm{kipft},\ 90.763\ \mathrm{kipft},\ 122.083\ \mathrm{kipft}\right)
        &= 90.763\ \mathrm{kipft}
\end{aligned} $$"""

    def test_moment_capacity_elastic_ltb(self):
        wide_flange = aisc.WideFlange("W12X22", self.steel)
        markdown, phi_b, M_n = wide_flange.moment_capacity(L_b=15*unit.ft, return_markdown=True)
        assert isclose(phi_b*M_n, 32.9*unit.kipft, atol=1*unit.kipft)
        assert markdown == r"""$$ \begin{aligned}
    M_p &= F_y \cdot Z_x
        = 50\ \mathrm{ksi} \cdot 29.3\ \mathrm{in}^{3}
        &= 122.083\ \mathrm{kipft}
    \\[10pt]
    \\[10pt]
    L_r &= \frac{1.95 \cdot r_{ts} \cdot E}{0.7 \cdot F_y} \cdot \sqrt{\frac{J \cdot c}{S_x \cdot h_o} + \sqrt{\left(\frac{J \cdot c}{S_x \cdot h_o}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot F_y}{E}\right)^2}}
        \\
        &= \frac{1.95 \cdot 1.04\ \mathrm{in} \cdot 29000\ \mathrm{ksi}}{0.7 \cdot 50\ \mathrm{ksi}} \cdot \sqrt{\frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}} + \sqrt{\left(\frac{0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}}\right)^2 + 6.76 \cdot \left(\frac{0.7 \cdot 50\ \mathrm{ksi}}{29000\ \mathrm{ksi}}\right)^2}}
        \\
        &= 109.591\ \mathrm{in}
    \\[10pt]
    \text{Since, } & \left(L_b > L_r \Leftarrow 15\ \mathrm{ft} > 109.591\ \mathrm{in}\right):
        \\[10pt]
        M_{ltb} &= \frac{S_x \cdot C_b \cdot \pi^2 \cdot E}{\left(\frac{L_b}{r_{ts}}\right)^2} \cdot \sqrt{1 + \frac{0.078 \cdot J \cdot c}{S_x \cdot h_o} \cdot \left(\frac{L_b}{r_{ts}}\right)^2}
            \\
            &= \frac{25.4\ \mathrm{in}^{3} \cdot 1 \cdot \pi^2 \cdot 29000\ \mathrm{ksi}}{\left(\frac{15\ \mathrm{ft}}{1.04\ \mathrm{in}}\right)^2} \cdot \sqrt{1 + \frac{0.078 \cdot 0.293\ \mathrm{in}^{4} \cdot 1}{25.4\ \mathrm{in}^{3} \cdot 11.9\ \mathrm{in}} \cdot \left(\frac{15\ \mathrm{ft}}{1.04\ \mathrm{in}}\right)^2}
            \\
            &= 36.544\ \mathrm{kipft}
    \\[10pt]
    \\[10pt]
    \lambda_{pf} &= 0.38 \cdot \sqrt{\frac{E}{F_y}}
        = 0.38 \cdot \sqrt{\frac{29000\ \mathrm{ksi}}{50\ \mathrm{ksi}}}
        &= 9.152
    \\[10pt]
    \text{Since, } & \left(\lambda_f < \lambda_{pf} \Leftarrow 4.74 < 9.152\right):
        \\[10pt]
        M_{flb} &= M_p
            = 122.083\ \mathrm{kipft}
            &= 122.083\ \mathrm{kipft}
    \\[10pt]
    \\[10pt]
    M_n &= \operatorname{min}\left(M_p,\ M_{ltb},\ M_{flb}\right)
        = \operatorname{min}\left(122.083\ \mathrm{kipft},\ 36.544\ \mathrm{kipft},\ 122.083\ \mathrm{kipft}\right)
        &= 36.544\ \mathrm{kipft}
\end{aligned} $$"""

    def test_moment_capacity_flange_local_buckling(self):
        wide_flange = aisc.WideFlange("W10X12", self.steel)
        markdown, phi_b, M_n = wide_flange.moment_capacity(return_markdown=True)
        assert isclose(phi_b*M_n, 46.9*unit.kipft, atol=1*unit.kipft)
        assert markdown == r"""$$ \begin{aligned}
    M_p &= F_y \cdot Z_x
        = 50\ \mathrm{ksi} \cdot 12.6\ \mathrm{in}^{3}
        &= 52.5\ \mathrm{kipft}
    \\[10pt]
    \\[10pt]
    L_p &= 1.76 \cdot r_y \sqrt{\frac{E}{F_y}}
        = 1.76 \cdot 0.785\ \mathrm{in} \sqrt{\frac{29000\ \mathrm{ksi}}{50\ \mathrm{ksi}}}
        &= 33.273\ \mathrm{in}
    \\[10pt]
    \text{Since, } & \left(L_b \leq L_p \Leftarrow 0\ \mathrm{in} \leq 33.273\ \mathrm{in}\right):
        \\[10pt]
        M_{ltb} &= M_p
            = 52.5\ \mathrm{kipft}
            &= 52.5\ \mathrm{kipft}
    \\[10pt]
    \\[10pt]
    \lambda_{pf} &= 0.38 \cdot \sqrt{\frac{E}{F_y}}
        = 0.38 \cdot \sqrt{\frac{29000\ \mathrm{ksi}}{50\ \mathrm{ksi}}}
        &= 9.152
    \\[10pt]
    \lambda_{rf} &= 1 \cdot \sqrt{\frac{E}{F_y}}
        = 1 \cdot \sqrt{\frac{29000\ \mathrm{ksi}}{50\ \mathrm{ksi}}}
        &= 24.083
    \\[10pt]
    \text{Since, } & \left(\lambda_{pf} \leq \lambda_f < \lambda_{rf} \Leftarrow 9.152 \leq 9.43 < 24.083\right):
        \\[10pt]
        M_{flb} &= M_p - \left(M_p - 0.7 \cdot F_y \cdot S_x\right) \cdot \frac{\lambda_f - \lambda_{pf}} {\lambda_{rf} - \lambda_{pf}}
            \\
            &= 52.5\ \mathrm{kipft} - \left(52.5\ \mathrm{kipft} - 0.7 \cdot 50\ \mathrm{ksi} \cdot 10.9\ \mathrm{in}^{3}\right) \cdot \frac{9.43 - 9.152}{24.083 - 9.152}
            \\
            &= 52.114\ \mathrm{kipft}
    \\[10pt]
    \\[10pt]
    M_n &= \operatorname{min}\left(M_p,\ M_{ltb},\ M_{flb}\right)
        = \operatorname{min}\left(52.5\ \mathrm{kipft},\ 52.5\ \mathrm{kipft},\ 52.114\ \mathrm{kipft}\right)
        &= 52.114\ \mathrm{kipft}
\end{aligned} $$"""
