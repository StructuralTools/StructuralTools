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


from structuraltools import LatexTemplate, MathTemplate


fig_26_8_1 = LatexTemplate(r"""\begin{aligned}
    L_h &= \operatorname{max}\left(L_h,\ 2 \cdot H\right) = \operatorname{max}\left($L_h,\ 2 \cdot $H\right) &= $L_h_bounded
    \\[10pt]
    K_1 &= $K_1_factor \cdot \frac{H}{L_h} = $K_1_factor \cdot \frac{$H}{$L_h_bounded} &= $K_1
    \\[10pt]
    K_2 &= 1 - \frac{|x|}{\mu \cdot L_h} = 1 - \frac{|$x|}{$mu \cdot $L_h_bounded} &= $K_2
    \\[10pt]
    K_3 &= e^{- \frac{\gamma \cdot z}{L_h}} = e^{- \frac{$gamma \cdot $z}{$L_h_bounded}} &= $K_3
    \\[10pt]
    K_{zt} &= \left(1 + K_1 \cdot K_2 \cdot K_3\right)^2 = \left(1 + $K_1 \cdot $K_2 \cdot $K_3\right)^2 &= $K_zt
\end{aligned}""")

table_26_9_1 = MathTemplate(r"K_e &= e^{-0.0000362 \cdot z_e} = e^{-0.0000362 \cdot $z_e} &= $K_e")

table_26_10_1 = MathTemplate(r"K_{$elevation} &= 2.41 \cdot \left(\frac{\operatorname{min}\left(\operatorname{max}\left(15\ \mathrm{ft},\ $elevation\right),\ z_g\right)}{z_g}\right)^{\frac{2}{\alpha}} = 2.41 \cdot \left(\frac{\operatorname{min}\left(\operatorname{max}\left(15\ \mathrm{ft},\ $z\right),\ $z_g\right)}{$z_g}\right)^{\frac{2}{$alpha}} &= $K_z")

eq_26_10_1 = MathTemplate(r"q_{$elevation} &= 0.00256 \cdot K_{$elevation} \cdot K_{zt} \cdot K_e \cdot V^2 = 0.00256 \cdot $K_z \cdot $K_zt \cdot K_e \cdot \left($V\right)^2 &= $q_z")

eq_26_11_6 = MathTemplate(r"G_{$axis} &= 0.925 \cdot \left(\frac{1 + 1.7 \cdot g_Q \cdot I_\bar{z} \cdot Q_{$axis}}{1 + 1.7 \cdot g_v \cdot I_\bar{z}}\right) = 0.925 \cdot \left(\frac{1 + 1.7 \cdot $g_Q \cdot $I_bar_z \cdot $Q}{1 + 1.7 \cdot $g_v \cdot $I_bar_z}\right) &= $G")

eq_26_11_7 = MathTemplate(r"I_\bar{z} &= c \cdot \left(\frac{33}{\bar{z}}\right)^\frac{1}{6} = $c \cdot \left(\frac{33}{$bar_z}\right)^\frac{1}{6} &= $I_bar_z")

eq_26_11_8 = MathTemplate(r"Q_{$axis_1} &= \sqrt{\frac{1}{1 + 0.63 \cdot \left(\frac{L_{$axis_2} + h}{L_\bar{z}}\right)^{0.63}}} = \sqrt{\frac{1}{1 + 0.63 \cdot \left(\frac{$L + $h}{$L_bar_z}\right)^{0.63}}} &= $Q")

eq_26_11_9 = MathTemplate(r"L_\bar{z} &= l \cdot \left(\frac{\bar{z}}{33}\right)^{\bar{\epsilon}} = $L \cdot \left(\frac{$bar_z}{33}\right)^{$bar_epsilon} &= $L_bar_z")
