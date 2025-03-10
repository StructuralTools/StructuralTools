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


from math import isclose

from structuraltools import asce, unit


def test_calc_K_zt():
    K_zt = asce.wind_loading.calc_K_zt(
        feature="escarpment",
        H=500*unit.ft,
        L_h=1500*unit.ft,
        x=300*unit.ft,
        z=50*unit.ft,
        exposure="B")
    assert isclose(K_zt, 1.484767957, abs_tol=1e-9)

def test_calc_K_z_low():
    latex, K_z = asce.wind_loading._calc_K_z(10*unit.ft, 2460*unit.ft, 9.8, return_latex=True)
    assert isclose(K_z, 0.8511539011, abs_tol=1e-10)
    assert latex == r"""
    $$ \begin{aligned}
        K_z &= 2.41 \cdot \frac{\operatorname{max}\left(z, 15 \mathrm{ft}\right)}{z_g}^{\frac{2}{\alpha}} = 2.41 \cdot \frac{\operatorname{max}\left(10\ \mathrm{ft} , 15 \mathrm{ft}\right)}{2460\ \mathrm{ft}}^{\frac{2}{9.8}} &= 0.851
    \end{aligned} $$
"""

def test_calc_K_z_mid():
    latex, K_z = asce.wind_loading._calc_K_z(100*unit.ft, 2460*unit.ft, 9.8, return_latex=True)
    assert isclose(K_z, 1.253581964, abs_tol=1e-9)
    assert latex == r"""
    $$ \begin{aligned}
        K_z &= 2.41 \cdot \frac{\operatorname{max}\left(z, 15 \mathrm{ft}\right)}{z_g}^{\frac{2}{\alpha}} = 2.41 \cdot \frac{\operatorname{max}\left(100\ \mathrm{ft} , 15 \mathrm{ft}\right)}{2460\ \mathrm{ft}}^{\frac{2}{9.8}} &= 1.254
    \end{aligned} $$
"""

def test_calc_K_z_high():
    latex, K_z = asce.wind_loading._calc_K_z(3000*unit.ft, 2460*unit.ft, 9.8, return_latex=True)
    assert K_z == 2.41
    assert latex == r"""
    $$ \begin{aligned}
        & \text{Since, } \left(z > z_g \Leftarrow 3000\ \mathrm{ft} > 2460\ \mathrm{ft}\right): & K_z &= 2.41
    \end{aligned} $$
"""

def test_calc_q_z():
    latex, q_z = asce.wind_loading._calc_q_z(1.21, 1, 0.96, 110*unit.mph, return_latex=True)
    assert isclose(q_z.to("psf").magnitude, 35.9817216, abs_tol=1e-7)
    assert latex == r"q_z &= 0.00256 \cdot K_z \cdot K_{zt} \cdot K_e \cdot V^2 = 0.00256 \cdot 1.21 \cdot 1 \cdot 0.96 \cdot 110\ \mathrm{mph}^2 &= 35.982\ \mathrm{psf}"

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
        Z_e=520*unit.ft,
        h_p=53.25*unit.ft)
    assert isclose(inputs["K_e"], 0.981352065, abs_tol=1e-9)
    assert isclose(inputs["q_h"].to("psf").magnitude, 24.16680433, abs_tol=1e-8)
    assert isclose(inputs["q_p"].to("psf").magnitude, 24.41477673, abs_tol=1e-8)
    assert isclose(inputs["G_x"], 0.840652037, abs_tol=1e-9)
    assert isclose(inputs["G_y"], 0.8068246373, abs_tol=1e-10)

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
    assert isclose(MWFRS.coefs["x"]["wall"]["leeward"]["c1"], -0.2652866242, abs_tol=1e-10)
    assert MWFRS.coefs["x"]["roof"]["d<=h"]["c1"] == -0.9
    assert MWFRS.coefs["y"]["parapet"]["leeward"]["c1"] == -1
    assert MWFRS.coefs["y"]["wall"]["side"]["c1"] == -0.7
    assert isclose(MWFRS.coefs["y"]["roof"]["windward"]["c1"], -0.7917197452, abs_tol=1e-10)

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
        assert isclose(pressure[0].to("psf").magnitude, 27.93056453, abs_tol=1e-8)
        assert isclose(pressure[1].to("psf").magnitude, 27.93056453, abs_tol=1e-8)

    def test_get_load_leeward_wall(self):
        pressure = self.MWFRS.get_load("y", "wall", "leeward")
        assert isclose(pressure[0].to("psf").magnitude, -20.41486297, abs_tol=1e-8)
        assert isclose(pressure[1].to("psf").magnitude, -20.41486297, abs_tol=1e-8)

    def test_get_load_windward_parapet(self):
        pressure = self.MWFRS.get_load("x", "parapet", "windward")
        assert isclose(pressure[0].to("psf").magnitude, 51.91829278, abs_tol=1e-8)
        assert isclose(pressure[1].to("psf").magnitude, 51.91829278, abs_tol=1e-8)

    def test_get_load_flat_roof(self):
        pressure = self.MWFRS.get_load("x", "roof", 25*unit.ft)
        assert isclose(pressure[0].to("psf").magnitude, -26.15127075, abs_tol=1e-8)
        assert isclose(pressure[1].to("psf").magnitude, -11.23661053, abs_tol=1e-8)

    def test_get_load_gable_roof(self):
        pressure = self.MWFRS.get_load("y", "roof", "windward")
        assert isclose(pressure[0].to("psf").magnitude, -34.75588242, abs_tol=1e-8)
        assert isclose(pressure[1].to("psf").magnitude, -11.23661053, abs_tol=1e-8)

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
        assert isclose(pressure.to("psf").magnitude, 27.8834, abs_tol=1e-4)

    def test_get_load_single_log_pressure_mid_range(self):
        pressure = self.CandC.get_load("4+", 50*unit.ft**2)
        assert isclose(pressure.to("psf").magnitude, 24.96655763, abs_tol=1e-8)

    def test_get_load_single_log_pressure_upper_bound(self):
        pressure = self.CandC.get_load("4+", 750*unit.ft**2)
        assert isclose(pressure.to("psf").magnitude, 20.79349963, abs_tol=1e-8)

    def test_get_load_single_log_pressure_negative_pressure(self):
        pressure = self.CandC.get_load("4-", 50*unit.ft**2)
        assert isclose(pressure.to("psf").magnitude, -27.32955763, abs_tol=1e-8)

    def test_get_load_single_log_pressure_minimum_pressure(self):
        pressure = self.CandC.get_load("1_prime+", 500*unit.ft**2)
        assert isclose(pressure.to("psf").magnitude, 16)

    def test_get_load_single_log_pressure_negative_minimum_pressure(self):
        pressure = self.CandC.get_load("1_prime-", 1000*unit.ft**2)
        assert isclose(pressure.to("psf").magnitude, -16)

    def test_get_load_double_log_pressure_lower_bound(self):
        pressure = self.CandC.get_load("1V-", 9*unit.ft**2)
        assert isclose(pressure.to("psf").magnitude, -44.4244, abs_tol=1e-4)

    def test_get_load_double_log_pressure_lower_range(self):
        pressure = self.CandC.get_load("1V-", 20*unit.ft**2)
        assert isclose(pressure.to("psf").magnitude, -43.71306611, abs_tol=1e-8)

    def test_get_load_double_log_pressure_break_point(self):
        pressure = self.CandC.get_load("1V-", 100*unit.ft**2)
        assert isclose(pressure.to("psf").magnitude, -42.0614, abs_tol=1e-4)

    def test_get_load_double_log_pressure_upper_range(self):
        pressure = self.CandC.get_load("1V-", 200*unit.ft**2)
        assert isclose(pressure.to("psf").magnitude, -35.95530998, abs_tol=1e-8)

    def test_get_load_double_log_pressure_upper_bound(self):
        pressure = self.CandC.get_load("1V-", 750*unit.ft**2)
        assert isclose(pressure.to("psf").magnitude, -27.8834, abs_tol=1e-4)

    def test_get_load_composite_pressure(self):
        pressure = self.CandC.get_load("4P+", 50*unit.ft**2)
        assert isclose(pressure.to("psf").magnitude, 67.02889315, abs_tol=1e-8)

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
        assert isclose(pressure.to("psf").magnitude, 48.2052)

    def test_get_load_constants_pressure_medium_area(self):
        pressure = self.CandC.get_load("3+", 200*unit.ft**2)
        assert isclose(pressure.to("psf").magnitude, 36.1539)

    def test_get_load_constants_pressure_large_area(self):
        pressure = self.CandC.get_load("3+", 500*unit.ft**2)
        assert isclose(pressure.to("psf").magnitude, 24.1026)
