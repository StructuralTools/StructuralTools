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


def test_calc_K_z_low():
    K_z = asce.wind_loading.calc_K_z(10*unit.ft, 2460*unit.ft, 9.8)
    assert isclose(K_z, 0.8511539011, abs_tol=1e-10)

def test_calc_K_z_mid():
    K_z = asce.wind_loading.calc_K_z(100*unit.ft, 2460*unit.ft, 9.8)
    assert isclose(K_z, 1.253581964, abs_tol=1e-9)

def test_calc_K_z_high():
    K_z = asce.wind_loading.calc_K_z(3000*unit.ft, 2460*unit.ft, 9.8)
    assert K_z == 2.41

def test_calc_q_z():
    q_z = asce.wind_loading.calc_q_z(1.21, 1, 0.96, 110*unit.mph)
    assert isclose(q_z.to("psf").magnitude, 35.9817216, abs_tol=1e-7)

def test_calc_wind_server_inputs():
    inputs = asce.wind_loading.calc_wind_server_inputs(
        V=110*unit.mph,
        exposure="B",
        building_type="low-rise",
        roof_type="flat",
        roof_angle=0,
        L_x=211.5*unit.ft,
        L_y=78.5*unit.ft,
        h=51.25*unit.ft,
        z_e=520*unit.ft,
        h_p=53.25*unit.ft)
    assert isclose(inputs["K_e"], 0.981352065, abs_tol=1e-9)
    assert isclose(inputs["q_h"].to("psf").magnitude, 24.16680433, abs_tol=1e-8)
    assert isclose(inputs["q_p"].to("psf").magnitude, 24.41477673, abs_tol=1e-8)
    assert isclose(inputs["G_x"], 0.840652037, abs_tol=1e-9)
    assert isclose(inputs["G_y"], 0.8068246373, abs_tol=1e-10)

def test_CandCServer_init_gable():
    CandC = asce.wind_loading.CandCServer(
        building_type="low-rise",
        roof_type="gable",
        roof_angle=10,
        GC_pi=0.18,
        h_c = 10*unit.ft,
        h_e = 20*unit.ft)
    keys = ("1+", "1-", "2+", "2-", "3+", "3-", "4+", "4-", "4P+",
            "4P-", "5+", "5-", "5P+", "5P-", "C+", "C-")
    assert tuple(CandC.coefficients.keys()) == keys
    assert CandC.coefficients["1-"]["c1"] == -3.0155
    assert CandC.coefficients["4-"]["c1"] == -1.2766
    assert CandC.coefficients["C-"]["c1"] == -0.7

def test_CandCServer_init_open_monoslope():
    CandC = asce.wind_loading.CandCServer(
        building_type="open",
        roof_type="monoslope_clear",
        roof_angle=22.5,
        GC_pi=0.18)
    assert CandC.coefficients["1+"]["kind"] == "constants"
    assert isclose(CandC.coefficients["1+"]["c3"], 2.2)
    assert isclose(CandC.coefficients["1-"]["c3"], -2.2)
    assert isclose(CandC.coefficients["2+"]["c2"], 3.3)
    assert isclose(CandC.coefficients["2-"]["c2"], -3.35)
    assert isclose(CandC.coefficients["3+"]["c1"], 4.4)
    assert isclose(CandC.coefficients["3-"]["c1"], -4.4)

class TestCandCServerLowRise:
    def setup_method(self, method):
        self.CandC = asce.wind_loading.CandCServer(
            building_type="low-rise",
            roof_type="gable",
            roof_angle=0,
            a=10*unit.ft,
            G={"x": 0.85, "y": 0.85},
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
            G={"x": 0.85, "y": 0.85},
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
