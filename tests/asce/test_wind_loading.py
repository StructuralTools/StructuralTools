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

from structuraltools.asce import wind_loading
from structuraltools.unit import unit


def calc_K_zt():
    string, K_zt = wind_loading.calc_K_zt(
        feature="escarpment",
        H=500*unit.ft,
        L_h=1500*unit.ft,
        x=300*unit.ft,
        z=50*unit.ft,
        exposure="B",
        precision=4)
    assert isclose(K_zt, 1.484767957, atol=1e-9)
    assert string == r"""$$
\begin{aligned}
    L'_h &= \operatorname{max}\left(L_h,\ 2 \cdot H\right) = \operatorname{max}\left(1500\ \mathrm{ft},\ 2 \cdot 500\ \mathrm{ft}\right) &= 1500\ \mathrm{ft}
    \\[10pt]
    K_1 &= 0.75 \cdot \frac{H}{L'_h} = 0.75 \cdot \frac{500\ \mathrm{ft}}{1500\ \mathrm{ft}} &= 0.25
    \\[10pt]
    K_2 &= 1 - \frac{|x|}{\mu \cdot L'_h} = 1 - \frac{|300\ \mathrm{ft}|}{4 \cdot 1500\ \mathrm{ft}} &= 0.95
    \\[10pt]
    K_3 &= e^{- \frac{\gamma \cdot z}{L'_h}} = e^{- \frac{2.5 \cdot 50\ \mathrm{ft}}{1500\ \mathrm{ft}}} &= 0.92
    \\[10pt]
    K_{zt} &= \left(1 + K_1 \cdot K_2 \cdot K_3\right)^2 = \left(1 + 0.25 \cdot 0.95 \cdot 0.92\right)^2 &= 1.485
\end{aligned}
$$"""

def test_calc_wind_server_inputs():
    string, inputs = wind_loading.calc_wind_server_inputs(
        V=110*unit.mph,
        exposure="B",
        building_type="low-rise",
        roof_type="flat",
        roof_angle=0,
        ridge_axis="x",
        L_x=211.5*unit.ft,
        L_y=78.5*unit.ft,
        h=51.25*unit.ft,
        z_e=520*unit.ft,
        h_p=53.25*unit.ft,
        precision=4)
    assert isclose(inputs["K_e"], 0.981352065, atol=1e-9)
    assert isclose(inputs["q_h"], 24.16680433*unit.psf, atol=1e-8*unit.psf)
    assert isclose(inputs["q_p"], 24.41477673*unit.psf, atol=1e-8*unit.psf)
    assert isclose(inputs["G_x"], 0.840652037, atol=1e-9)
    assert isclose(inputs["G_y"], 0.8068246373, atol=1e-10)
    assert isclose(inputs["a"], 7.85*unit.ft)
    assert string == r"""#### Ground Elevation Factor
$$
\begin{aligned}
    K_e &= e^{-0.0000362 \cdot z_e} = e^{-0.0000362 \cdot 520\ \mathrm{ft}} &= 0.9814
\end{aligned}
$$

#### Roof Velocity Pressure
$$
\begin{aligned}
    K_{h} &= 2.41 \cdot \left(\frac{\operatorname{min} \left(\operatorname{max}\left(15\ \mathrm{ft},\ h\right),\ z_g\right)}{z_g}\right)^{\frac{2}{\alpha}} = 2.41 \cdot \left(\frac{\operatorname{min}\left(\operatorname{max}\left(15\ \mathrm{ft},\ 51.25\ \mathrm{ft}\right),\ 3280\ \mathrm{ft}\right)}{3280\ \mathrm{ft}}\right)^{\frac{2}{7.5}} &= 0.795
    \\[10pt]
    q_{h} &= 0.00256 \cdot K_{h} \cdot K_{zt} \cdot K_e \cdot V^2 = 0.00256 \cdot 0.795 \cdot 1 \cdot 0.9814 \cdot \left(110\ \mathrm{mph}\right)^2 &= 24.17\ \mathrm{psf}
\end{aligned}
$$

#### Parapet Velocity Pressure
$$
\begin{aligned}
    K_{p} &= 2.41 \cdot \left(\frac{\operatorname{min} \left(\operatorname{max}\left(15\ \mathrm{ft},\ p\right),\ z_g\right)}{z_g}\right)^{\frac{2}{\alpha}} = 2.41 \cdot \left(\frac{\operatorname{min}\left(\operatorname{max}\left(15\ \mathrm{ft},\ 53.25\ \mathrm{ft}\right),\ 3280\ \mathrm{ft}\right)}{3280\ \mathrm{ft}}\right)^{\frac{2}{7.5}} &= 0.8032
    \\[10pt]
    q_{p} &= 0.00256 \cdot K_{p} \cdot K_{zt} \cdot K_e \cdot V^2 = 0.00256 \cdot 0.8032 \cdot 1 \cdot 0.9814 \cdot \left(110\ \mathrm{mph}\right)^2 &= 24.41\ \mathrm{psf}
\end{aligned}
$$

#### Gust Effect Factor
$$
\begin{aligned}
    \bar{z} &= \operatorname{max}\left(0.6 \cdot h,\ z_{min}\right) = \operatorname{max}\left(0.6 \cdot 51.25\ \mathrm{ft},\ 30\ \mathrm{ft}\right) &= 30.75\ \mathrm{ft}
    \\[10pt]
    I_\bar{z} &= c \cdot \left(\frac{33}{\bar{z}}\right)^\frac{1}{6} = 0.3 \cdot \left(\frac{33}{30.75\ \mathrm{ft}}\right)^\frac{1}{6} &= 0.3036
    \\[10pt]
    L_\bar{z} &= l \cdot \left(\frac{\bar{z}}{33}\right)^\bar{\epsilon} = 320\ \mathrm{ft} \cdot \left(\frac{30.75\ \mathrm{ft}}{33}\right)^{0.3333} &= 312.6\ \mathrm{ft}
    \\[10pt]
    Q_{x} &= \sqrt{\frac{1}{1 + 0.63 \cdot \left(\frac{L_{y} + h}{L_\bar{z}}\right)^{0.63}}} = \sqrt{\frac{1}{1 + 0.63 \cdot \left(\frac{78.5\ \mathrm{ft} + 51.25\ \mathrm{ft}}{312.6\ \mathrm{ft}}\right)^{0.63}}} &= 0.8568
    \\[10pt]
    G_{x} &= 0.925 \cdot \left(\frac{1 + 1.7 \cdot g_Q \cdot I_\bar{z} \cdot Q_{x}}{1 + 1.7 \cdot g_v \cdot I_\bar{z}}\right) = 0.925 \cdot \left(\frac{1 + 1.7 \cdot 3.4 \cdot 0.3036 \cdot 0.8568}{1 + 1.7 \cdot 3.4 \cdot 0.3036}\right) &= 0.8407
    \\[10pt]
    Q_{y} &= \sqrt{\frac{1}{1 + 0.63 \cdot \left(\frac{L_{x} + h}{L_\bar{z}}\right)^{0.63}}} = \sqrt{\frac{1}{1 + 0.63 \cdot \left(\frac{211.5\ \mathrm{ft} + 51.25\ \mathrm{ft}}{312.6\ \mathrm{ft}}\right)^{0.63}}} &= 0.7994
    \\[10pt]
    G_{y} &= 0.925 \cdot \left(\frac{1 + 1.7 \cdot g_Q \cdot I_\bar{z} \cdot Q_{y}}{1 + 1.7 \cdot g_v \cdot I_\bar{z}}\right) = 0.925 \cdot \left(\frac{1 + 1.7 \cdot 3.4 \cdot 0.3036 \cdot 0.7994}{1 + 1.7 \cdot 3.4 \cdot 0.3036}\right) &= 0.8068
\end{aligned}
$$"""

def test_MainWindServer_init_gable():
    MWFRS = wind_loading.MainWindServer(
        building_type="low-rise",
        roof_type="gable",
        roof_angle=15,
        ridge_axis="x",
        L_x=211.5*unit.ft,
        L_y=78.5*unit.ft,
        h=51.25*unit.ft,
        GC_pi=0.18)
    assert MWFRS.coefs["x"]["parapet"]["windward"]["c1"] == 1.5
    assert isclose(MWFRS.coefs["x"]["wall"]["leeward"]["c1"], -0.2652866242, atol=1e-10)
    assert MWFRS.coefs["x"]["roof"]["d<=h"]["c1"] == -0.9
    assert MWFRS.coefs["y"]["parapet"]["leeward"]["c1"] == -1
    assert MWFRS.coefs["y"]["wall"]["side"]["c1"] == -0.7
    assert isclose(MWFRS.coefs["y"]["roof"]["windward"]["c1"], -0.7917197452, atol=1e-10)

def test_MainWindServer_minimum_pressure():
    MWFRS = wind_loading.MainWindServer(
        V=110*unit.mph,
        building_type="low-rise",
        roof_angle=15,
        ridge_axis="x",
        L_x=30*unit.ft,
        L_y=30*unit.ft,
        h=30*unit.ft,
        K_d=0.85,
        GC_pi=0.18,
        q_h=21.34887631*unit.psf,
        G_x=0.85,
        G_y=0.85)
    pressure = MWFRS.get_load("x", "wall", "side")
    assert pressure[0] == -16*unit.psf
    assert pressure[1] == -16*unit.psf

class TestMainWindServer:
    def setup_method(self, method):
        self.MWFRS = wind_loading.MainWindServer(
            V=150*unit.mph,
            building_type="low-rise",
            roof_angle=15,
            ridge_axis="x",
            L_x=30*unit.ft,
            L_y=30*unit.ft,
            h=30*unit.ft,
            K_d=0.85,
            K_zt=1,
            GC_pi=0.18,
            z_g=3280*unit.ft,
            alpha=7.5,
            K_e=1,
            q_h=39.69832372*unit.psf,
            q_p=40.72022963*unit.psf,
            G_x=0.85,
            G_y=0.85)

    def test_get_load_windward_wall(self):
        pressure = self.MWFRS.get_load("x", "wall", 25*unit.ft)
        assert isclose(pressure[0], 27.93056453*unit.psf, atol=1e-8*unit.psf)
        assert isclose(pressure[1], 27.93056453*unit.psf, atol=1e-8*unit.psf)

    def test_get_load_leeward_wall(self):
        pressure = self.MWFRS.get_load("y", "wall", "leeward")
        assert isclose(pressure[0], -20.41486297*unit.psf, atol=1e-8*unit.psf)
        assert isclose(pressure[1], -20.41486297*unit.psf, atol=1e-8*unit.psf)

    def test_get_load_windward_parapet(self):
        pressure = self.MWFRS.get_load("x", "parapet", "windward")
        assert isclose(pressure[0], 51.91829278*unit.psf, atol=1e-8*unit.psf)
        assert isclose(pressure[1], 51.91829278*unit.psf, atol=1e-8*unit.psf)

    def test_get_load_flat_roof(self):
        pressure = self.MWFRS.get_load("x", "roof", 25*unit.ft)
        assert isclose(pressure[0], -26.15127075*unit.psf, atol=1e-8*unit.psf)
        assert isclose(pressure[1], -11.23661053*unit.psf, atol=1e-8*unit.psf)

    def test_get_load_gable_roof(self):
        pressure = self.MWFRS.get_load("y", "roof", "windward")
        assert isclose(pressure[0], -34.75588242*unit.psf, atol=1e-8*unit.psf)
        assert isclose(pressure[1], -11.23661053*unit.psf, atol=1e-8*unit.psf)

def test_CandCServer_init_gable():
    CandC = wind_loading.CandCServer(
        building_type="low-rise",
        roof_type="gable",
        roof_angle=10,
        GC_pi=0.18,
        h_c = 10*unit.ft,
        h_e = 20*unit.ft)
    keys = {"1+", "1-", "2+", "2-", "3+", "3-", "4+", "4-", "4P+",
            "4P-", "5+", "5-", "5P+", "5P-", "C+", "C-"}
    assert set(CandC.coefs.keys()) == keys
    assert CandC.coefs["1-"]["c1"] == -3.0155
    assert CandC.coefs["4-"]["c1"] == -1.2766
    assert CandC.coefs["C-"]["c1"] == -0.7

def test_CandCServer_init_open_monoslope():
    CandC = wind_loading.CandCServer(
        building_type="open",
        roof_type="monoslope_clear",
        roof_angle=22.5,
        GC_pi=0.18)
    assert CandC.coefs["1+"]["kind"] == "constants"
    assert isclose(CandC.coefs["1+"]["c3"], 2.2)
    assert isclose(CandC.coefs["1-"]["c3"], -2.2)
    assert isclose(CandC.coefs["2+"]["c2"], 3.3)
    assert isclose(CandC.coefs["2-"]["c2"], -3.35)
    assert isclose(CandC.coefs["3+"]["c1"], 4.4)
    assert isclose(CandC.coefs["3-"]["c1"], -4.4)

class TestCandCServerLowRise:
    def setup_method(self, method):
        self.CandC = wind_loading.CandCServer(
            building_type="low-rise",
            roof_type="gable",
            roof_angle=0,
            a=10*unit.ft,
            G_x=0.85,
            G_y=0.85,
            GC_pi=0.18,
            h_c = 10*unit.ft,
            h_e = 20*unit.ft,
            K_d=0.85,
            q_h=27.8*unit.psf,
            q_p=28.1*unit.psf)

    def test_get_load_single_log_pressure_lower_bound(self):
        pressure = self.CandC.get_load("4+", 9*unit.ft**2)
        assert isclose(pressure, 27.8834*unit.psf, atol=1e-4*unit.psf)

    def test_get_load_single_log_pressure_mid_range(self):
        pressure = self.CandC.get_load("4+", 50*unit.ft**2)
        assert isclose(pressure, 24.96655763*unit.psf, atol=1e-8*unit.psf)

    def test_get_load_single_log_pressure_upper_bound(self):
        pressure = self.CandC.get_load("4+", 750*unit.ft**2)
        assert isclose(pressure, 20.79349963*unit.psf, atol=1e-8*unit.psf)

    def test_get_load_single_log_pressure_negative_pressure(self):
        pressure = self.CandC.get_load("4-", 50*unit.ft**2)
        assert isclose(pressure, -27.32955763*unit.psf, atol=1e-8*unit.psf)

    def test_get_load_single_log_pressure_minimum_pressure(self):
        pressure = self.CandC.get_load("1_prime+", 500*unit.ft**2)
        assert isclose(pressure.to("psf").magnitude, 16)

    def test_get_load_single_log_pressure_negative_minimum_pressure(self):
        pressure = self.CandC.get_load("1_prime-", 1000*unit.ft**2)
        assert isclose(pressure.to("psf").magnitude, -16)

    def test_get_load_double_log_pressure_lower_bound(self):
        pressure = self.CandC.get_load("1V-", 9*unit.ft**2)
        assert isclose(pressure, -44.4244*unit.psf, atol=1e-4*unit.psf)

    def test_get_load_double_log_pressure_lower_range(self):
        pressure = self.CandC.get_load("1V-", 20*unit.ft**2)
        assert isclose(pressure, -43.71306611*unit.psf, atol=1e-8*unit.psf)

    def test_get_load_double_log_pressure_break_point(self):
        pressure = self.CandC.get_load("1V-", 100*unit.ft**2)
        assert isclose(pressure, -42.0614*unit.psf, atol=1e-4*unit.psf)

    def test_get_load_double_log_pressure_upper_range(self):
        pressure = self.CandC.get_load("1V-", 200*unit.ft**2)
        assert isclose(pressure, -35.95530998*unit.psf, atol=1e-8*unit.psf)

    def test_get_load_double_log_pressure_upper_bound(self):
        pressure = self.CandC.get_load("1V-", 750*unit.ft**2)
        assert isclose(pressure, -27.8834*unit.psf, atol=1e-4*unit.psf)

    def test_get_load_composite_pressure(self):
        pressure = self.CandC.get_load("4P+", 50*unit.ft**2)
        assert isclose(pressure, 67.02889315*unit.psf, atol=1e-8*unit.psf)

    def test_get_load_composite_pressure_minimum_pressure(self):
        pressure = self.CandC.get_load("4P+", 600*unit.ft**2, q_z=14*unit.psf)
        assert isclose(pressure.to("psf").magnitude, 32)


class TestCandCServerOpen:
    def setup_method(self, method):
        self.CandC = wind_loading.CandCServer(
            building_type="open",
            roof_type="monoslope_clear",
            roof_angle=0,
            a=10*unit.ft,
            G_x=0.85,
            G_y=0.85,
            GC_pi=0.18,
            K_d=0.85,
            q_h=27.8*unit.psf,
            q_p=28.1*unit.psf)

    def test_get_load_constants_pressure_small_area(self):
        pressure = self.CandC.get_load("3+", 10*unit.ft**2)
        assert isclose(pressure, 48.2052*unit.psf)

    def test_get_load_constants_pressure_medium_area(self):
        pressure = self.CandC.get_load("3+", 200*unit.ft**2)
        assert isclose(pressure, 36.1539*unit.psf)

    def test_get_load_constants_pressure_large_area(self):
        pressure = self.CandC.get_load("3+", 500*unit.ft**2)
        assert isclose(pressure, 24.1026*unit.psf)
