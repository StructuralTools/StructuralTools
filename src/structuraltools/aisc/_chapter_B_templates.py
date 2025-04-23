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


table_B4_1b_10_lamb_p = Template("Math", r"\lambda_{pf} &= 0.38 \cdot \sqrt{\frac{E}{F_y}} = 0.38 \cdot \sqrt{\frac{$E}{$F_y}} &= $lamb_pf")

table_B4_1b_10_lamb_r = Template("Math", r"\lambda_{rf} &= \sqrt{\frac{E}{F_y}} = \sqrt{\frac{$E}{$F_y}} &= $lamb_rf")

table_B4_1b_15_lamb_p = Template("Math", r"\lambda_{pw} &= 3.76 \cdot \sqrt{\frac{E}{F_y}} = 3.76 \cdot \sqrt{\frac{$E}{$F_y}} &= $lamb_pw")

table_B4_1b_15_lamb_r = Template("Math", r"\lambda_{rw} &= 5.7 \cdot \sqrt{\frac{E}{F_y}} = 5.7 \cdot \sqrt{\frac{$E}{$F_y}} &= $lamb_rw")
