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

from numpy import e, log10, sqrt

from structuraltools import resources, unit, utils


def calc_K_z(z, z_g, alpha: float) -> float:
    """Calculate the velocity pressure exposure coefficient (K_z) per
    ASCE 7-22 Table 26.10-1 footnote 1

    Parameters
    ==========

    z : pint length quantity
        Elevation to calculate the K_z at

    z_g : pint length quantity
        Elevation of maximum K_z

    alpha : float
        Terrain exposure constant alpha from ASCE 7-22 Table 26.11-1"""
    if 0 <= z and z <= z_g:
        K_z = 2.41*(max(z.to("ft"), 15*unit.ft)/z_g.to("ft")).magnitude**(2/alpha)
    elif z <= 3280*unit.ft:
        K_z = 2.41
    else:
        raise ValueError("z is outside of the bounds supported by ASCE 7-22")
    return K_z

def calc_q_z(K_z: float, K_zt: float, K_e: float, V):
    """Calculate the velocity pressure (q_z) per ASCE 7-22 Equation 26.10-1

    Parameters
    ==========

    K_z : float
        Velocity pressure exposure coefficient from ASCE 7-22 Table 26.10-1

    K_zt : float
        Topographic factor from ASCE 7-22 Figure 26.8-1

    K_e : float
        Ground elevation factor from ASCE 7-22 Table 26.9-1

    V : pint velocity quantity
        Basic wind speed from the ASCE 7 Hazard tool"""
    q_z = 0.00256*K_z*K_zt*K_e*((V.to("mph").magnitude)**2)*unit.psf
    return q_z

def calc_wind_server_inputs(
    V,
    exposure: str,
    building_type: str,
    roof_type: str,
    roof_angle: float,
    L_x,
    L_y,
    h,
    **kwargs):
    """Performs calculations from ASCE 7-22 Chapter 26 and returns a dictionary
    of results that can be used as input for a MainWindServer or a CandCServer.

    The gust effect factor is calculated for two orthogonal axis according to
    the procedure in ASCE 7-22 Section 26.11.4 for rigid buildings. A rigid
    building has a fundamental natural frequency greater than or equal to 1 Hz.
    It is the user's responsibility to ensure that a rigid analysis is
    appropriate; low-rise buildings may be considered rigid according to
    ASCE 7-22 Section 26.11.2.

    Parameters
    ==========

    V : pint velocity quantity
        Basic wind speed from the ASCE 7 Hazard tool

    exposure : str
        Exposure catagory from ASCE 7-22 section 26.7.3.
        Should be one of "B", "C", or "D".

    building_type : str
        String indicating the building type.
        Currently "low-rise" and "open" are supported

    roof_type : str
        String indicating the roof type. Currently "flat", "gable", and "hip"
        are supported for low-rise buildings and "monoslope_clear" and
        "monoslope_obstructed" are supported for open buildings.

    roof_angle : float
        Roof angle theta. Use 0 for flat roofs.

    L_x : pint length quantity
        Maximum length of the building along the x-axis.

    L_y : pint length quantity
        Maximum length of the building along the y-axis

    h : pint length quantity
        Mean roof height

    K_d : float, optional
        Wind directionality factor from ASCE 7-22 Table 26.6-1. Defaults to
        0.85 for buildings, and should be set explicitly for other kinds of
        structures.

    K_zt : float, optional
        Topographic factor from ASCE 7-22 Figure 26.8-1. By default this is
        assumed to be 1, but it should be set explicitly if the structure is
        in the upper one-half of a hill or ridge or near the crest of an
        escarpment.

    z_e : pint length quantity, optional
        Ground elevation above sea level. Defaults to 0, which can
        conservatively be used in all cases.

    GC_pi : float, optional
        Internal pressure coefficient from ASCE 7-22 Table 26.13-1. By default
        this is set to 0.18 for an enclosed building, and it should be set
        explicity for other building types

    h_p : pint length quantity, optional
        Parapet height. Should be set if wind loads on parapets are needed.

    h_e : pint length quantity, optional
        Eave height. Should be set if wind loads on canopies are needed.
        Note: This can also be set when initializing a CandCServer if multiple
        eave heights are needed.

    h_c : pint length quantity, optional
        Canopy height. Should be set if wind loads on canopies are needed.
        Note: This can also be set when initializing a CandCServer if multiple
        canopy heights are needed."""
    exposure_constants = utils.get_table_entry(
        resources.joinpath("ASCE_Table_26-11-1.csv"),
        exposure)

    # Calculate K_e according to ASCE 7-22 Table 26.9-1 footnotes 1 and 2
    K_e = e**(-0.0000362*(kwargs.pop("z_e", 0*unit.ft).to("ft").magnitude))

    # Calculate velocity pressure at the roof height and the parapet height,
    # if applicable, according to ASCE 7-22 Table 26.10-1 footnote 1 and
    # ASCE 7-22 Equation 26.10-1
    K_h = calc_K_z(h, exposure_constants["z_g"], exposure_constants["alpha"])
    q_h = calc_q_z(K_h, kwargs.get("K_zt", 1), K_e, V)
    if (h_p := kwargs.pop("h_p", None)):
        K_p = calc_K_z(h_p, exposure_constants["z_g"], exposure_constants["alpha"])
        q_p = calc_q_z(K_p, kwargs.get("K_zt", 1), K_e, V)

    # Calculate the gust effect factor for the x and y directions according to
    # ASCE 7-22 Section 26.11.4
    z_bar = max(0.6*h, exposure_constants["z_min"]).to("ft")
    L_z = exposure_constants["l"]*(z_bar/(33*unit.ft))**exposure_constants["epsilon_bar"]  # (26.11-9)
    I_z = exposure_constants["c"]*(33/z_bar.magnitude)**(1/6)  # (26.11-7)

    Q_x = sqrt(1/(1+0.63*((L_y+h).to("ft")/L_z)**0.63)).magnitude  # (26.11-8)
    G_x = 0.925*((1+1.7*3.4*I_z*Q_x)/(1+1.7*3.4*I_z))  # (26.11-6)

    Q_y = sqrt(1/(1+0.63*((L_x+h).to("ft")/L_z)**0.63)).magnitude  # (26.11-8)
    G_y = 0.925*((1+1.7*3.4*I_z*Q_y)/(1+1.7*3.4*I_z))  # (26.11-6)

    # Calculate length a for C&C wind loads
    a = max(min(0.1*L_x, 0.1*L_y, 0.4*h), 0.04*min(L_x, L_y), 3*unit.ft)

    # Assemble and return the values dictionary
    values = {
        "V": V.to("mph"),
        "building_type": building_type,
        "roof_type": roof_type,
        "roof_angle": roof_angle,
        "K_d": kwargs.get("K_d", 0.85),
        "K_zt": kwargs.get("K_zt", 1),
        "GC_pi": kwargs.get("GC_pi", 0.18),
        "h_e": kwargs.get("h_e"),
        "h_c": kwargs.get("h_c"),
        "z_g": exposure_constants["z_g"],
        "alpha": exposure_constants["alpha"],
        "K_e": K_e,
        "q_h": q_h,
        "q_p": q_p,
        "G_x": G_x,
        "G_y": G_y,
        "a": a
    }
    return values


class CandCServer:
    """Class for calculating C&C wind pressures per ASCE 7-22 Chapter 30"""
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
        self.G = kwargs.get("G", {file_values.get("G_x"), file_values.get("G_y")})
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
