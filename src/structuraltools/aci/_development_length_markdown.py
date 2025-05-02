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


straight_lamb_low = Template("Math", r"& \text{Since, } \left(w_c < $normal_weight \Leftarrow $w_c < $normal_weight\right): & \lambda &= $lamb")

straight_lamb_high = Template("Math", r"& \text{Since, } \left(w_c \geq $normal_weight \Leftarrow $w_c \geq $normal_weight\right): & \lambda &= $lamb")

straight_psi_g_low = Template("Math", r"& \text{Since, } \left(f_y \leq $psi_g_low_limit \Leftarrow $f_y \leq $psi_g_low_limit\right): & \psi_g &= $psi_g")

straight_psi_g_mid = Template("Math", r"& \text{Since, } \left($psi_g_low_limit < f_y \leq $psi_g_high_limit \Leftarrow $psi_g_low_limit < $f_y \leq $psi_g_high_limit\right): & \psi_g &= $psi_g")

straight_psi_g_high = Template("Math", r"& \text{Since, } \left(f_y > $psi_g_high_limit \Leftarrow $f_y > $psi_g_high_limit\right): & \psi_g &= $psi_g")

straight_psi_e_c_c = Template("Math", r"& \text{Since, } \left(\mathrm{coated} = \mathrm{True}\right) \text{ and } \left(c_c < 3 \cdot d_b \Leftarrow $c_c < $d_b3\right): & \psi_e &= $psi_e")

straight_psi_e_s = Template("Math", r"& \text{Since, } \left(\mathrm{coated} = \mathrm{True}\right) \text{ and } \left(s < 7 \cdot d_b \Leftarrow $s < $d_b7\right): & \psi_e &= $psi_e")

straight_psi_e_true = Template("Math", r"& \text{Since, } \left(\mathrm{coated} = \mathrm{True}\right): & \psi_e &= $psi_e")

straight_psi_e_false = Template("Math", r"& \text{Since, } \left(\mathrm{coated} = \mathrm{False}\right): & \psi_e &= $psi_e")

straight_psi_s_big = Template("Math", r"& \text{Since, } \left(\text{Rebar size} \geq 7\right): & \psi_s &= $psi_s")

straight_psi_s_small = Template("Math", r"& \text{Since, } \left(\psi_s \text{ not applied}\right): & \psi_s &= $psi_s")

straight_psi_s_used = Template("Math", r"& \text{Since, } \left(\text{Rebar size} \leq 6\right): & \psi_s &= $psi_s")

straight_psi_t_true = Template("Math", r"& \text{Since, } \left(\text{Concrete below} > $limit\right): & \psi_t &= $psi_t")

straight_psi_t_false = Template("Math", r"& \text{Since, } \left(\text{Concrete below} \leq $limit\right): & \psi_t &= $psi_t")

straight_bar_factors = Template("Latex", r"""\begin{aligned}
    $lamb_template
    \\[10pt]
    $psi_g_template
    \\[10pt]
    $psi_e_template
    \\[10pt]
    $psi_s_template
    \\[10pt]
    $psi_t_template
\end{aligned}""")

straight_bar = Template("Markdown", r"""$factors_markdown
$$$$ \begin{aligned}
    \\[10pt]
    K_{tr} &= \frac{40 \cdot A_{tr}}{s \cdot n}
        = \frac{40 \cdot $A_tr}{$s \cdot $n}
        &= $K_tr
    \\[10pt]
    c_b &= \operatorname{min}\left(c_c + \frac{d_b}{2} ,\ \frac{s}{2}\right)
        = \operatorname{min}\left($c_c + \frac{$d_b}{2} ,\ \frac{$s}{2}\right)
        &= $c_b
    \\[10pt]
    l'_d &= \left(\frac{3 \cdot f_y \cdot \operatorname{min}\left(\psi_t \cdot \psi_e ,\ 1.7\right) \cdot \psi_s \cdot \psi_g}{40 \cdot \lambda \cdot \sqrt{f'_c \cdot \mathrm{psi}} \cdot \left(\frac{c_b + K_{tr}}{d_b}\right)}\right) \cdot d_b
        \\
        &= \left(\frac{3 \cdot $f_y \cdot \operatorname{min}\left($psi_t \cdot $psi_e ,\ 1.7\right) \cdot $psi_s \cdot $psi_g}{40 \cdot $lamb \cdot \sqrt{$f_prime_c \cdot \mathrm{psi}} \cdot \left(\frac{$c_b + $K_tr}{$d_b}\right)}\right) \cdot $d_b
        \\
        &= $l_prime_d
    \\[10pt]
    l_d &= \operatorname{max}\left(l'_d ,\ $l_d_limit\right)
        = \operatorname{max}\left($l_prime_d ,\ $l_d_limit\right)
        &= $l_d
\end{aligned} $$$$""")

hook_lamb_low = Template("Math", r"& \text{Since, } \left(w_c < $normal_weight \Leftarrow $w_c < $normal_weight\right): & \lambda &= $lamb")

hook_lamb_high = Template("Math", r"& \text{Since, } \left(w_c \geq $normal_weight \Leftarrow $w_c \geq $normal_weight\right): & \lambda &= $lamb")

hook_psi_e = Template("Math", r"& \text{Since, } \left(\mathrm{coated} = \mathrm{$coated}\right): & \psi_e &= $psi_e")

hook_psi_r_large = Template("Math", r"& \text{Since, } \left(\text{Rebar size} > 11 \Leftarrow $size > 11\right): & \psi_r &= $psi_r")

hook_psi_r_s = Template("Math", r"& \text{Since, } \left(s \geq 6 \cdot d_b \Leftarrow $s \geq $d_b6\right): & \psi_r &= $psi_r")

hook_psi_r_A_th = Template("Math", r"& \text{Since, } \left(A_{th} \geq 0.4 \cdot A_{hs} \Leftarrow $A_th \geq $A_hs04\right): & \psi_r &= $psi_r")

hook_psi_r_small = Template("Math", r"& \text{Since, } \left(A_{th} < 0.4 \cdot A_{hs} \Leftarrow $A_th < $A_hs04\right) \text{ and } \left(s < 6 \cdot d_b \Leftarrow $s < $d_b6\right): & \psi_r &= $psi_r")

hook_psi_o_large = Template("Math", r"& \text{Since, } \left(\text{Rebar size} > 11 \Leftarrow $size > 11\right): & \psi_o &= $psi_o")

hook_psi_o_d_b = Template("Math", r"& \text{Since, } \left(c_{c_{side}} \geq 6 \cdot d_b \Leftarrow $c_c_side \geq $d_b6\right): & \psi_o &= $psi_o")

hook_psi_o_column = Template("Math", r"& \text{Since, } \left(\text{In column} = \mathrm{True}\right) \text{ and } \left(c_{c_{side}} \geq $min_c_c_side \Leftarrow $c_c_side \geq $min_c_c_side\right): & \psi_o &= $psi_o")

hook_psi_o_column_small = Template("Math", r"& \text{Since, } \left(c_{c_{side}} < $min_c_c_side \Leftarrow $c_c_side < $min_c_c_side\right): & \psi_o &= $psi_o")

hook_psi_o_small = Template("Math", r"& \text{Since, } \left(c_{c_{side}} < 6 \cdot d_b \Leftarrow $c_c_side < $d_b6\right): & \psi_o &= $psi_o")

hook_psi_c = Template("Math", r"\psi_c &= \operatorname{min}\left(\frac{f'_c}{15000\ \mathrm{psi}} + 0.6 ,\ 1\right) = \operatorname{min}\left(\frac{$f_prime_c}{15000\ \mathrm{psi}} + 0.6 ,\ 1\right) &= $psi_c")

standard_hook_factors = Template("Latex", r"""\begin{aligned}
    $lamb_template
    \\[10pt]
    $psi_e_template
    \\[10pt]
    $psi_r_template
    \\[10pt]
    $psi_o_template
\end{aligned}
\begin{aligned}
    $psi_c_template
\end{aligned}""")

standard_hook = Template("Markdown", r"""$factors_markdown
$$$$ \begin{aligned}
    l'_{dh} &= \left(\frac{f_y \cdot \psi_e \cdot \psi_r \cdot \psi_o \cdot \psi_c}{55 \cdot \lambda \cdot \sqrt{f'_c \cdot \mathrm{pli}}}\right) \cdot d_b^{1.5}
    \\
    &= \left(\frac{$f_y \cdot $psi_e \cdot $psi_r \cdot $psi_o \cdot $psi_c}{55 \cdot $lamb \cdot \sqrt{$f_prime_c \cdot \mathrm{pli}}}\right) \cdot $d_b^{1.5}
    \\
    &= $l_prime_dh
    \\[10pt]
    l_{dh} &= \operatorname{max}\left(l'_{dh} ,\ 8 \cdot d_b ,\ $l_dh_limit\right) = \operatorname{max}\left($l_prime_dh, $d_b8, $l_dh_limit\right) &= $l_dh
    \\[10pt]
\end{aligned} $$$$""")
