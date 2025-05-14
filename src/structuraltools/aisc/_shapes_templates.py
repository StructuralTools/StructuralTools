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


Plate_moment_capacity_x = Template("Markdown", r"""$M_n_string""")

Plate_moment_capacity_y = Template("Markdown", r"""$header Nominal Moment Capacity
$$$$ \begin{aligned}
    M_n &= \operatorname{min}\left(F_y \cdot Z_y,\ 1.5 \cdot F_y \cdot S_y\right) = \operatorname{min}\left($F_y \cdot $Z_y,\ 1.5 \cdot $F_y \cdot $S_y\right) &= $M_n
\end{aligned} $$$$""")

WideFlange_moment_capacity = Template("Markdown", r"""$M_n_string""")
