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


from structuraltools import MarkdownTemplate


calc_wind_server_inputs = MarkdownTemplate(r"""$header Ground Elevation Factor
$$$$ \begin{aligned}
    $K_e_str
\end{aligned} $$$$
<br/>
$header Roof Velocity Pressure
$$$$ \begin{aligned}
    $K_h_str
    \\[10pt]
    $q_h_str
\end{aligned} $$$$
<br/>
$header Gust Effect Factor
$$$$ \begin{aligned}
    \bar{z} &= \operatorname{max}\left(0.6 \cdot h,\ z_{min}\right) = \operatorname{max}\left(0.6 \cdot $h,\ $z_min\right) &= $bar_z
    \\[10pt]
    $I_bar_z_str
    \\[10pt]
    $L_bar_z_str
\end{aligned} $$$$

$header# X-Axis
$$$$ \begin{aligned}
    $Q_x_str
    \\[10pt]
    $G_x_str
\end{aligned} $$$$

$header# Y-Axis
$$$$ \begin{aligned}
    $Q_y_str
    \\[10pt]
    $G_y_str
\end{aligned} $$$$""")

calc_wind_server_inputs_with_parapet = MarkdownTemplate(r"""$header Ground Elevation Factor
$$$$ \begin{aligned}
    $K_e_str
\end{aligned} $$$$
<br/>
$header Roof Velocity Pressure
$$$$ \begin{aligned}
    $K_h_str
    \\[10pt]
    $q_h_str
\end{aligned} $$$$
<br/>
$header Parapet Velocity Pressure
$$$$ \begin{aligned}
    $K_p_str
    \\[10pt]
    $q_p_str
\end {aligned} $$$$
<br/>
$header Gust Effect Factor
$$$$ \begin{aligned}
    \bar{z} &= \operatorname{max}\left(0.6 \cdot h,\ z_{min}\right) = \operatorname{max}\left(0.6 \cdot $h,\ $z_min\right) &= $bar_z
    \\[10pt]
    $I_bar_z_str
    \\[10pt]
    $L_bar_z_str
\end{aligned} $$$$

$header# X-Axis
$$$$ \begin{aligned}
    $Q_x_str
    \\[10pt]
    $G_x_str
\end{aligned} $$$$

$header# Y-Axis
$$$$ \begin{aligned}
    $Q_y_str
    \\[10pt]
    $G_y_str
\end{aligned} $$$$""")
