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


import json

from numpy import log10

from structuraltools import resources, unit, utils


class CandCServer:
    """Class for calculating C&C wind pressures"""
    def __init__(self, filepath: str = "", **kwargs):
        """Create a new CandCServer. Values can be loaded from a file or passed
        manually, but all values should be specified. Values that are passed
        manually will override values provided by the file.

        Parameters
        ==========

        file : str, optional
            Path to file to load variables from

        building_type : string, optional
            Type of building for CandC calculations.
            One of: "low-rise" or "open"

        roof_type : string, optional
            Type of roof for CandC calculations. Should be one of "gable",
            "hip", or "canopy" for low-rise buildings and one of
            "monoslope_clear" or "monoslope_obstructed" for open buildings.

        roof_angle : float, optional
            Roof angle ($\\theta$) in degrees

        a : pint length quantity, optional
            Length of wind zone dimension a

        G : dict, optional
            dict of {"x": float, "y": float} containing the gust effect
            factors for the x and y directions

        GC_pi : float, optional
            Internal pressure coefficient

        h_c : pint length quantity, optional
            Canopy height

        h_e : pint length quantity, optional
            Eve height for canopy calculations

        K_d : float, optional
            Wind directionality factor

        q_h : pint pressure quantity, optional
            Velocity pressure factor at roof height

        q_p : pint pressure quantity, optional
            Velocity pressure factor at parapet height"""
        if filepath:
            with open(filepath, "r") as json_file:
                file_values = json.load(json_file)["CandCServer_values"]
            for key, value in file_values.items():
                file_values.update({key: utils.convert_to_unit(value)})
        else:
            file_values = {}

        self.building_type = kwargs.get("building_type", file_values.get("building_type"))
        self.roof_type = kwargs.get("roof_type", file_values.get("roof_type"))
        self.roof_angle = kwargs.get("roof_angle", file_values.get("roof_angle"))
        self.a = kwargs.get("a", file_values.get("a"))
        self.G = kwargs.get("G", file_values.get("G"))
        self.GC_pi = abs(kwargs.get("GC_pi", file_values.get("GC_pi")))
        self.h_c = kwargs.get("h_c", file_values.get("h_c"))
        self.h_e = kwargs.get("h_e", file_values.get("h_e"))
        self.K_d = kwargs.get("K_d", file_values.get("K_d"))
        self.q_h = kwargs.get("q_h", file_values.get("q_h"))
        self.q_p = kwargs.get("q_p", file_values.get("q_p"))

        with open(resources.joinpath("CandCCoefficients.json")) as coefficients_file:
            type_coefficients = json.load(coefficients_file)[self.building_type]

        if self.building_type == "low-rise":
            # Get roof coefficients
            if self.roof_angle <= 7:
                self.coefficients = type_coefficients["flat"]
            elif self.roof_angle <= 20:
                self.coefficients = type_coefficients["low_"+self.roof_type]
            elif self.roof_angle <= 27:
                self.coefficients = type_coefficients["mid_"+self.roof_type]
            elif self.roof_angle <= 45:
                self.coefficients = type_coefficients["high_"+self.roof_type]
            else:
                raise ValueError("Roof slope greater than 45 degrees")

            # Get wall coefficients
            self.coefficients.update(type_coefficients["walls"])

            # Get canopy coefficients
            if self.h_c and self.h_e:
                if self.h_c/self.h_e <= 0.5:
                    self.coefficients.update(type_coefficients["low_canopy"])
                elif self.h_c/self.h_e < 0.9:
                    self.coefficients.update(type_coefficients["mid_canopy"])
                elif self.h_c/self.h_e <= 1:
                    self.coefficients.update(type_coefficients["high_canopy"])
                else:
                    raise ValueError("Canopy is higher than mean eave height")

        elif self.building_type == "open":
            if self.roof_angle <= 7.5:
                slopes = (0, 7.5)
            elif self.roof_angle <= 15:
                slopes = (7.5, 15)
            elif self.roof_angle <= 30:
                slopes = (15, 30)
            elif self.roof_angle <= 45:
                slopes = (30, 45)
            else:
                raise ValueError("Roof slope is greater than 45 degrees")

            # Open roofs use interpolation between provided roof slope values
            # The interpolation is performed here for all roof zones and areas
            values = (
                type_coefficients[self.roof_type+"_"+str(slopes[0])],
                type_coefficients[self.roof_type+"_"+str(slopes[1])]
            )
            self.coefficients = {}
            for zone in values[0].keys():
                self.coefficients.update({zone: {}})
                for key in values[0][zone].keys():
                    if isinstance(values[0][zone][key], int | float):
                        self.coefficients[zone].update({
                            key: utils.linterp(
                                slopes[0],
                                values[0][zone][key],
                                slopes[1],
                                values[1][zone][key],
                                self.roof_angle)
                            })
                    else:
                        self.coefficients[zone].update({key: values[0][zone][key]})


    def get_load(self, zone: str, area, **kwargs):
        """Get the wind pressure for the specified zone and area

        Parameters
        ==========

        zone : str
            C&C wind zone to calculate wind pressure for. Allowable options
            depend on the building and roof type.

        area : pint area quantity
            Tributary area to calculate wind pressure for

        q_z : pint pressure quantity
            Velocity pressure factor at height z

        GC_pi : float
            Internal pressure coefficient

        p_min : pint pressure quantity, optional
            Minimum magnitude for CandC wind pressure. Default value is
            16 psf unless the zone requests a different value. Manually
            setting this value overrides the zone requesting a value.

        G_method : str, optional
            String indicating which G value to use for the calculation.
            Should be one of "x", "y", or "max"."""
        coefs = self.coefficients[zone]
        GC_pi = kwargs.get("GC_pi", coefs.get("GC_pi", self.GC_pi))
        p_min = kwargs.get("p_min", unit(coefs.get("p_min", "16 psf")))
        G_method = kwargs.get("G_method", "max")
        if kwargs.get("q_z"):
            q_z = kwargs["q_z"]
        elif coefs.get("use_q_p", False):
            q_z = self.q_p
        else:
            q_z = self.q_h

        match coefs.get("kind"):
            case "single_log":
                area = area.to("ft**2").magnitude
                GC_p = coefs["c1"]+coefs["c2"]*log10(
                    min(max(area, coefs["low_limit"]), coefs["high_limit"]))
                p = q_z*self.K_d*(GC_p+GC_pi*GC_p/abs(GC_p))
            case "double_log":
                area = area.to("ft**2").magnitude
                if area <= coefs["break_point"]:
                    GC_p = coefs["e1c1"]+coefs["e1c2"]*log10(max(area, coefs["low_limit"]))
                else:
                    GC_p = coefs["e2c1"]+coefs["e2c2"]*log10(min(area, coefs["high_limit"]))
                p = q_z*self.K_d*(GC_p+GC_pi*GC_p/abs(GC_p))
            case "constants":
                if area <= self.a**2:
                    C_n = coefs["c1"]
                elif area <= 4*self.a**2:
                    C_n = coefs["c2"]
                else:
                    C_n = coefs["c3"]
                G = self.G.get(G_method, max(self.G.values()))
                p = q_z*self.K_d*G*C_n
            case "composite":
                p_positive = self.get_load(
                    coefs["positive_zone"],
                    area,
                    q_z=q_z,
                    GC_pi=GC_pi,
                    p_min=0*unit.psf)
                p_negative = self.get_load(
                    coefs["negative_zone"],
                    area,
                    q_z=q_z,
                    GC_pi=GC_pi,
                    p_min=0*unit.psf)
                p = p_positive-p_negative
            case _:
                raise ValueError("Unsupported kind")
        return max(abs(p), abs(p_min))*p/abs(p)
