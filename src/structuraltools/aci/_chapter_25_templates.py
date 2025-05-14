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


eq_25_4_2_4a = Template("Math", r"""l'_d &= \left(\frac{3 \cdot f_y \cdot \operatorname{min}\left(\psi_t \cdot \psi_e ,\ 1.7\right) \cdot \psi_s \cdot \psi_g}{40 \cdot \lambda \cdot \sqrt{f'_c} \cdot \left(\frac{c_b + K_{tr}}{d_b}\right)}\right) \cdot d_b
    \\
    &= \left(\frac{3 \cdot $f_y \cdot \operatorname{min}\left($psi_t \cdot $psi_e ,\ 1.7\right) \cdot $psi_s \cdot $psi_g}{40 \cdot $lamb \cdot \sqrt{$f_prime_c} \cdot \left(\frac{$c_b + $K_tr}{$d_b}\right)}\right) \cdot $d_b
    \\
    &= $l_prime_d""")

eq_25_4_2_4b = Template("Math", r"K_{tr} &= \frac{40 \cdot A_{tr}}{s \cdot n} = \frac{40 \cdot $A_tr}{$s \cdot $n} &= $K_tr")

table_25_4_2_5_lamb_light = Template("Math", r"\text{Since, } & \left(w_c < $normal_weight \Leftarrow $w_c < $normal_weight\right): & \lambda &= $lamb")

table_25_4_2_5_lamb_normal = Template("Math", r"\text{Since, } & \left(w_c \geq $normal_weight \Leftarrow $w_c \geq $normal_weight\right): & \lambda &= $lamb")

table_25_4_2_5_psi_g_low = Template("Math", r"\text{Since, } & \left(f_y \leq $low_limit \Leftarrow $f_y \leq $low_limit\right): & \psi_g &= $psi_g")

table_25_4_2_5_psi_g_mid = Template("Math", r"\text{Since, } & \left($low_limit < f_y \leq $high_limit \Leftarrow $low_limit < $f_y \leq $high_limit\right): & \psi_g &= $psi_g")

table_25_4_2_5_psi_g_high = Template("Math", r"\text{Since, } & \left(f_y > $high_limit \Leftarrow $f_y > $high_limit\right): & \psi_g &= $psi_g")

table_25_4_2_5_psi_e_c_c = Template("Math", r"\text{Since, } & \left(\mathrm{coated} = \mathrm{True}\right) \text{ and } \left(c_c < 3 \cdot d_b \Leftarrow $c_c < $d_b3\right): & \psi_e &= $psi_e")

table_25_4_2_5_psi_e_s = Template("Math", r"\text{Since, } & \left(\mathrm{coated} = \mathrm{True}\right) \text{ and } \left(s < 7 \cdot d_b \Leftarrow $s < $d_b7\right): & \psi_e &= $psi_e")

table_25_4_2_5_psi_e_true = Template("Math", r"\text{Since, } & \left(\mathrm{coated} = \mathrm{True}\right): & \psi_e &= $psi_e")

table_25_4_2_5_psi_e_false = Template("Math", r"\text{Since, } & \left(\mathrm{coated} = \mathrm{False}\right): & \psi_e &= $psi_e")

table_25_4_2_5_psi_s_big = Template("Math", r"\text{Since, } & \left(\text{Rebar size} \geq 7\right): & \psi_s &= $psi_s")

table_25_4_2_5_psi_s_small = Template("Math", r"\text{Since, } & \left(\psi_s \text{ not applied}\right): & \psi_s &= $psi_s")

table_25_4_2_5_psi_s_used = Template("Math", r"\text{Since, } & \left(\text{Rebar size} \leq 6\right): & \psi_s &= $psi_s")

table_25_4_2_5_psi_t_true = Template("Math", r"\text{Since, } & \left(\text{Concrete below} > $limit\right): & \psi_t &= $psi_t")

table_25_4_2_5_psi_t_false = Template("Math", r"\text{Since, } & \left(\text{Concrete below} \leq $limit\right): & \psi_t &= $psi_t")

table_25_4_2_5 = Template("Latex", r"""\begin{aligned}
    $lamb_string
    \\[10pt]
    $psi_g_string
    \\[10pt]
    $psi_e_string
    \\[10pt]
    $psi_s_string
    \\[10pt]
    $psi_t_string
\end{aligned}""")
