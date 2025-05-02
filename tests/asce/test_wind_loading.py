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


from structuraltools import asce
from structuraltools.unit import unit
from structuraltools.utils import isclose


def test_calc_wind_server_inputs():
    inputs = asce.wind_loading.calc_wind_server_inputs(
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
        return_string=True)
    assert isclose(inputs["K_e"], 0.981352065, atol=1e-9)
    assert isclose(inputs["q_h"], 24.16680433*unit.psf, atol=1e-8*unit.psf)
    assert isclose(inputs["q_p"], 24.41477673*unit.psf, atol=1e-8*unit.psf)
    assert isclose(inputs["G_x"], 0.840652037, atol=1e-9)
    assert isclose(inputs["G_y"], 0.8068246373, atol=1e-10)
    assert isclose(inputs["a"], 7.85*unit.ft)
    assert inputs.string == r"""#### Ground Elevation Factor
$$ \begin{aligned}
    K_e &= e^{-0.0000362 \cdot z_e} = e^{-0.0000362 \cdot 520\ \mathrm{ft}} &= 0.981
\end{aligned} $$
<br/>
#### Roof Velocity Pressure
$$ \begin{aligned}
    K_{h} &= 2.41 \cdot \left(\frac{\operatorname{min}\left(\operatorname{max}\left(15\ \mathrm{ft},\ h\right),\ z_g\right)}{z_g}\right)^{\frac{2}{\alpha}} = 2.41 \cdot \left(\frac{\operatorname{min}\left(\operatorname{max}\left(15\ \mathrm{ft},\ 51.25\ \mathrm{ft}\right),\ 3280\ \mathrm{ft}\right)}{3280\ \mathrm{ft}}\right)^{\frac{2}{7.5}} &= 0.795
    \\[10pt]
    q_{h} &= 0.00256 \cdot K_{h} \cdot K_{zt} \cdot K_e \cdot V^2 = 0.00256 \cdot 0.795 \cdot 1 \cdot 0.981 \cdot \left(110\ \mathrm{mph}\right)^2 &= 24.167\ \mathrm{psf}
\end{aligned} $$
<br/>
#### Parapet Velocity Pressure
$$ \begin{aligned}
    K_{p} &= 2.41 \cdot \left(\frac{\operatorname{min}\left(\operatorname{max}\left(15\ \mathrm{ft},\ p\right),\ z_g\right)}{z_g}\right)^{\frac{2}{\alpha}} = 2.41 \cdot \left(\frac{\operatorname{min}\left(\operatorname{max}\left(15\ \mathrm{ft},\ 53.25\ \mathrm{ft}\right),\ 3280\ \mathrm{ft}\right)}{3280\ \mathrm{ft}}\right)^{\frac{2}{7.5}} &= 0.803
    \\[10pt]
    q_{p} &= 0.00256 \cdot K_{p} \cdot K_{zt} \cdot K_e \cdot V^2 = 0.00256 \cdot 0.803 \cdot 1 \cdot 0.981 \cdot \left(110\ \mathrm{mph}\right)^2 &= 24.415\ \mathrm{psf}
\end {aligned} $$
<br/>
#### Gust Effect Factor
$$ \begin{aligned}
    \bar{z} &= \operatorname{max}\left(0.6 \cdot h,\ z_{min}\right) = \operatorname{max}\left(0.6 \cdot 51.25\ \mathrm{ft},\ 30\ \mathrm{ft}\right) &= 30.75\ \mathrm{ft}
    \\[10pt]
    I_\bar{z} &= c \cdot \left(\frac{33}{\bar{z}}\right)^\frac{1}{6} = 0.3 \cdot \left(\frac{33}{30.75\ \mathrm{ft}}\right)^\frac{1}{6} &= 0.304
    \\[10pt]
    L_\bar{z} &= l \cdot \left(\frac{\bar{z}}{33}\right)^{\bar{\epsilon}} = 320\ \mathrm{ft} \cdot \left(\frac{30.75\ \mathrm{ft}}{33}\right)^{0.333} &= 312.555\ \mathrm{ft}
\end{aligned} $$

##### X-Axis
$$ \begin{aligned}
    Q_{x} &= \sqrt{\frac{1}{1 + 0.63 \cdot \left(\frac{L_{y} + h}{L_\bar{z}}\right)^{0.63}}} = \sqrt{\frac{1}{1 + 0.63 \cdot \left(\frac{78.5\ \mathrm{ft} + 51.25\ \mathrm{ft}}{312.555\ \mathrm{ft}}\right)^{0.63}}} &= 0.857
    \\[10pt]
    G_{x} &= 0.925 \cdot \left(\frac{1 + 1.7 \cdot g_Q \cdot I_\bar{z} \cdot Q_{x}}{1 + 1.7 \cdot g_v \cdot I_\bar{z}}\right) = 0.925 \cdot \left(\frac{1 + 1.7 \cdot 3.4 \cdot 0.304 \cdot 0.857}{1 + 1.7 \cdot 3.4 \cdot 0.304}\right) &= 0.841
\end{aligned} $$

##### Y-Axis
$$ \begin{aligned}
    Q_{y} &= \sqrt{\frac{1}{1 + 0.63 \cdot \left(\frac{L_{x} + h}{L_\bar{z}}\right)^{0.63}}} = \sqrt{\frac{1}{1 + 0.63 \cdot \left(\frac{211.5\ \mathrm{ft} + 51.25\ \mathrm{ft}}{312.555\ \mathrm{ft}}\right)^{0.63}}} &= 0.799
    \\[10pt]
    G_{y} &= 0.925 \cdot \left(\frac{1 + 1.7 \cdot g_Q \cdot I_\bar{z} \cdot Q_{y}}{1 + 1.7 \cdot g_v \cdot I_\bar{z}}\right) = 0.925 \cdot \left(\frac{1 + 1.7 \cdot 3.4 \cdot 0.304 \cdot 0.799}{1 + 1.7 \cdot 3.4 \cdot 0.304}\right) &= 0.807
\end{aligned} $$"""

def test_MainWindServer_init_gable():
    MWFRS = asce.wind_loading.MainWindServer(
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
    MWFRS = asce.wind_loading.MainWindServer(
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
        self.MWFRS = asce.wind_loading.MainWindServer(
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
    CandC = asce.wind_loading.CandCServer(
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
    CandC = asce.wind_loading.CandCServer(
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
        self.CandC = asce.wind_loading.CandCServer(
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
        self.CandC = asce.wind_loading.CandCServer(
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
