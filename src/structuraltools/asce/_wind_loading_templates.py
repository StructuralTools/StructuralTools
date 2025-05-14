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


from structuraltools.template import Template


calc_wind_server_inputs = Template("Markdown", r"""$header Ground Elevation Factor
$$$$ \begin{aligned}
    $K_e_string
\end{aligned} $$$$
<br/>
$header Roof Velocity Pressure
$$$$ \begin{aligned}
    $K_h_string
    \\[10pt]
    $q_h_string
\end{aligned} $$$$
<br/>
$header Gust Effect Factor
$$$$ \begin{aligned}
    \bar{z} &= \operatorname{max}\left(0.6 \cdot h,\ z_{min}\right) = \operatorname{max}\left(0.6 \cdot $h,\ $z_min\right) &= $bar_z
    \\[10pt]
    $I_bar_z_string
    \\[10pt]
    $L_bar_z_string
\end{aligned} $$$$

$header# X-Axis
$$$$ \begin{aligned}
    $Q_x_string
    \\[10pt]
    $G_x_string
\end{aligned} $$$$

$header# Y-Axis
$$$$ \begin{aligned}
    $Q_y_string
    \\[10pt]
    $G_y_string
\end{aligned} $$$$""")

calc_wind_server_inputs_with_parapet = Template("Markdown", r"""$header Ground Elevation Factor
$$$$ \begin{aligned}
    $K_e_string
\end{aligned} $$$$
<br/>
$header Roof Velocity Pressure
$$$$ \begin{aligned}
    $K_h_string
    \\[10pt]
    $q_h_string
\end{aligned} $$$$
<br/>
$header Parapet Velocity Pressure
$$$$ \begin{aligned}
    $K_p_string
    \\[10pt]
    $q_p_string
\end {aligned} $$$$
<br/>
$header Gust Effect Factor
$$$$ \begin{aligned}
    \bar{z} &= \operatorname{max}\left(0.6 \cdot h,\ z_{min}\right) = \operatorname{max}\left(0.6 \cdot $h,\ $z_min\right) &= $bar_z
    \\[10pt]
    $I_bar_z_string
    \\[10pt]
    $L_bar_z_string
\end{aligned} $$$$

$header# X-Axis
$$$$ \begin{aligned}
    $Q_x_string
    \\[10pt]
    $G_x_string
\end{aligned} $$$$

$header# Y-Axis
$$$$ \begin{aligned}
    $Q_y_string
    \\[10pt]
    $G_y_string
\end{aligned} $$$$""")
