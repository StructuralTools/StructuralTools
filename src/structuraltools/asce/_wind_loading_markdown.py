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


from string import Template


calc_K_zt = Template(r"""$$$$ \begin{aligned}
    L_h &= \operatorname{max}\left(L_h,\ 2 \cdot H\right)
        = \operatorname{max}\left($L_h,\ 2 \cdot $H\right)
        &= $L_h_bounded
    \\[10pt]
    K_1 &= $K_1_factor \cdot \frac{H}{L_h}
        = $K_1_factor \cdot \frac{$H}{$L_h_bounded}
        &= $K_1
    \\[10pt]
    K_2 &= 1 - \frac{|x|}{\mu \cdot L_h}
        = 1 - \frac{|$x|}{$mu \cdot $L_h_bounded}
        &= $K_2
    \\[10pt]
    K_3 &= e^{- \frac{\gamma \cdot z}{L_h}}
        = e^{- \frac{$gamma \cdot $z}{$L_h_bounded}}
        &= $K_3
    \\[10pt]
    K_{zt} &= \left(1 + K_1 \cdot K_2 \cdot K_3\right)^2
        = \left(1 + $K_1 \cdot $K_2 \cdot $K_3\right)^2
        &= $K_zt
\end{aligned} $$$$""")

calc_K_z = Template(r"""$$$$ \begin{aligned}
    K_$subscript &= 2.41 \cdot \left(\frac{\operatorname{max}\left(\operatorname{min}\left(z,\ z_g\right),\ 15\ \mathrm{ft}\right)}{z_g}\right)^{\frac{2}{\alpha}}
        = 2.41 \cdot \left(\frac{\operatorname{max}\left(\operatorname{min}\left($z,\ $z_g\right),\ 15\ \mathrm{ft}\right)}{$z_g}\right)^{\frac{2}{$alpha}}
        &= $K_z
\end{aligned} $$$$""")

calc_q_z = Template(r"""$$$$ \begin{aligned}
    q_$subscript &= 0.00256 \cdot K_$subscript \cdot K_{zt} \cdot K_e \cdot V^2
        = 0.00256 \cdot $K_z \cdot $K_zt \cdot $K_e \cdot $V^2
        &= $q_z
\end{aligned} $$$$""")

calc_wind_server_inputs = Template(r"""$$$$ \begin{aligned}
    K_e &= e^{-0.0000362 \cdot Z_e}
        = e{-0.0000362 \cdot $Z_e}
        &= $K_e
    \\[10pt]
    $K_h_markdown
    \\[10pt]
    $q_h_markdown
    \\[10pt]
    $K_p_markdown
    \\[10pt]
    $q_p_markdown
    \\[10pt]
    \bar{z} &= \operatorname{max}\left(0.6 \cdot h,\ z_{min}\right)
        = \operatorname{max}\left(0.6 \cdot $h,\ $z_min\right)
        &= $z_bar
    \\[10pt]
    L_\bar{z} &= l \cdot \left(\frac{\bar{z}}{33}\right)^\bar{\epsilon}
        = $l \cdot \left(\frac{$z_bar}{33}\right)^$epsilon_bar
        &= $L_z
    \\[10pt]
    I_\bar{z} &= c \cdot \left(\frac{33}{\bar{z}}\right)^\frac{1}{6}
        = $c \cdot \left(\frac{33}{$z_bar}\right)^\frac{1}{6}
        &= $I_z
    \\[10pt]
    Q_x &= \sqrt{\frac{1}{1 + 0.63 \cdot \left(\frac{L_y + h}{L_\bar{z}}\right)^0.63}}
        = \sqrt{\frac{1}{1 + 0.63 \cdot \left(\frac{$L_y + $h}{$L_z}\right)^0.63}}
        &= $Q_x
    \\[10pt]
    G_x &=  0.925 \cdot \left(\frac{1 + 1.7 \cdot g_Q \cdot I_\bar{z} \cdot Q_x}{1 + 1.7 \cdot g_v \cdot I_\bar{z}}\right)
        = 0.925 \cdot \left(\frac{1 + 1.7 \cdot $g_Q \cdot $I_z \cdot $Q_x}{1 + 1.7 \cdot $g_v \cdot $I_z}\right)
        &= $G_x
    \\[10pt]
    Q_y &= \sqrt{\frac{1}{1 + 0.63 \cdot \left(\frac{L_x + h}{L_\bar{z}}\right)^0.63}}
        = \sqrt{\frac{1}{1 + 0.63 \cdot \left(\frac{$L_x + $h}{$L_z}\right)^0.63}}
        &= $Q_y
    \\[10pt]
    G_y &=  0.925 \cdot \left(\frac{1 + 1.7 \cdot g_Q \cdot I_\bar{z} \cdot Q_y}{1 + 1.7 \cdot g_v \cdot I_\bar{z}}\right)
        = 0.925 \cdot \left(\frac{1 + 1.7 \cdot $g_Q \cdot $I_z \cdot $Q_y}{1 + 1.7 \cdot $g_v \cdot $I_z}\right)
        &= $G_y
    \\[10pt]
    a &= \operatorname{max}\left(\operatorname{min}\left(0.1 \cdot L_x,\ 0.1 \cdot L_y,\ 0.4 \cdot h\right),\ 0.04 \cdot \operatorname{min}\left(L_x,\ L_y\right),\ 3\ \mathrm{ft}\right)
        \\
        &= \operatorname{max}\left(\operatorname{min}\left(0.1 \cdot $L_x,\ 0.1 \cdot $L_y,\ 0.4 \cdot $h\right),\ 0.04 \cdot \operatorname{min}\left($L_x,\ $L_y\right),\ 3\ \mathrm{ft}\right)
        \\
        &= $a
\end{aligned} $$$$""")
