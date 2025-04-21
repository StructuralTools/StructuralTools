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


import copy
import json
from typing import Optional

from numpy import log10, sign

from structuraltools import resources, unit, utils
from structuraltools import Area, Length, Pressure, Velocity

from structuraltools.asce import chapter_26
from structuraltools.asce import _wind_loading_templates as templates



def calc_wind_server_inputs(
    V: Velocity,
    exposure: str,
    building_type: str,
    L_x: Length,
    L_y: Length,
    h: Length,
    roof_type: str = "flat",
    roof_angle: float = 0,
    ridge_axis: Optional[str] = None,
    K_d: float = 0.85,
    K_zt: float = 1,
    z_e: Length = 0*unit.ft,
    GC_pi: float = 0.18,
    h_p: Optional[Length] = None,
    h_e: Optional[Length] = None,
    h_c: Optional[Length] = None,
    **display_options) -> dict[str, any] | tuple[str, dict[str, any]]:
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

    V : Velocity
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

    L_x : Length
        Maximum length of the building along the x-axis.

    L_y : Length
        Maximum length of the building along the y-axis

    h : Length
        Mean roof height

    roof_angle : float, optional
        Roof angle theta in degrees. Use 0 for flat roofs.

    ridge_axis : str, optional
        String indicating the roof ridge direction. One of "x" or "y".

    K_d : float, optional
        Wind directionality factor from ASCE 7-22 Table 26.6-1. Defaults to
        0.85 for buildings, and should be set explicitly for other kinds of
        structures.

    K_zt : float, optional
        Topographic factor from ASCE 7-22 Figure 26.8-1. By default this is
        assumed to be 1, but it should be set explicitly if the structure is
        in the upper one-half of a hill or ridge or near the crest of an
        escarpment.

    z_e : Length, optional
        Ground elevation above sea level. Defaults to 0, which can
        conservatively be used in all cases.

    GC_pi : float, optional
        Internal pressure coefficient from ASCE 7-22 Table 26.13-1. By default
        this is set to 0.18 for an enclosed building, and it should be set
        explicity for other building types

    h_p : Length, optional
        Parapet height. Should be set if wind loads on parapets are needed.

    h_e : Length, optional
        Eave height. Should be set if wind loads on canopies are needed.
        Note: This can also be set when initializing a CandCServer if multiple
        eave heights are needed.

    h_c : Length, optional
        Canopy height. Should be set if wind loads on canopies are needed.
        Note: This can also be set when initializing a CandCServer if multiple
        canopy heights are needed."""
    options = copy.copy(display_options)
    options.update({"display": False, "return_string": True})

    values = chapter_26.table_26_11_1.loc[exposure, :].to_dict()

    # Calculate K_e according to ASCE 7-22 Table 26.9-1 footnotes 1 and 2
    K_e_str, K_e = chapter_26.table_26_9_1(z_e, **options)

    # Calculate velocity pressure at the roof height and the parapet height,
    # if applicable, according to ASCE 7-22 Table 26.10-1 footnote 1 and
    # ASCE 7-22 Equation 26.10-1
    K_h_str, K_h = chapter_26.table_26_10_1(h, values["z_g"], values["alpha"],
        "h", **options)
    q_h_str, q_h = chapter_26.eq_26_10_1(K_h, K_zt, K_e, V, "h", **options)
    if h_p:
        K_p_str, K_p = chapter_26.table_26_10_1(h_p, values["z_g"],
            values["alpha"], "p", **options)
        q_p_str, q_p = chapter_26.eq_26_10_1(K_p, K_zt, K_e, V, "p", **options)
        template = templates.calc_wind_server_inputs_with_parapet
    else:
        template = templates.calc_wind_server_inputs
        q_p = None


    # Calculate the gust effect factor for the x and y directions according to
    # ASCE 7-22 Section 26.11.4
    z_min = values["z_min"]
    bar_z = max(0.6*h, z_min).to("ft")
    I_bar_z_str, I_bar_z = chapter_26.eq_26_11_7(values["c"], bar_z, **options)
    L_bar_z_str, L_bar_z = chapter_26.eq_26_11_9(values["l"], bar_z,
        values["bar_epsilon"], **options)

    Q_x_str, Q_x = chapter_26.eq_26_11_8(L_y, h, L_bar_z, "x", "y", **options)
    G_x_str, G_x = chapter_26.eq_26_11_6(I_bar_z, Q_x, "x", **options)

    Q_y_str, Q_y = chapter_26.eq_26_11_8(L_x, h, L_bar_z, "y", "x", **options)
    G_y_str, G_y = chapter_26.eq_26_11_6(I_bar_z, Q_y, "y", **options)


    # Calculate length a for C&C wind loads
    a = max(min(0.1*L_x, 0.1*L_y, 0.4*h), 0.04*min(L_x, L_y), 3*unit.ft).to("ft")

    # Assemble and return the values dictionary
    return_values = {
        "V": V,
        "building_type": building_type,
        "roof_type": roof_type,
        "roof_angle": roof_angle,
        "ridge_axis": ridge_axis,
        "L_x": L_x,
        "L_y": L_y,
        "h": h,
        "K_d": K_d,
        "K_zt": K_zt,
        "GC_pi": GC_pi,
        "h_e": h_e,
        "h_c": h_c,
        "z_g": values["z_g"],
        "alpha": values["alpha"],
        "K_e": K_e,
        "q_h": q_h,
        "q_p": q_p,
        "G_x": G_x,
        "G_y": G_y,
        "a": a
    }
    return utils.fill_template(template, locals(), return_values, **display_options)


class MainWindServer:
    """Class for calculating MWFRS wind pressures per ASCE 7-22 Chapter 27"""
    def __init__(self, filepath: str = "", **kwargs):
        """Create a new MainWindServer. Values can be loaded from a file or
        passed manually, but all values should be specified. Values that are
        passed manually will override values provided by the file.

        Parameters
        ==========

        file : str, optional
            Path to json file to load variables from

        building_type : str
            Type of building for MWFRS calculations.
            One of: "low-rise" or "mid-rise"

        roof_angle : float
            Roof angle ($\\theta$) in degrees. Use 0 for flat roofs.

        ridge_axis : str or None
            String indicating the roof ridge direction. One of: "x" or "y".

        L_x : Length
            Maximum length of the building along the x-axis.

        L_y : Length
            Maximum length of the building along the y-axis

        h : Length
            Mean roof height

        G_x : float
            Gust effect factor for wind along the x-axis

        G_y : float
            Gust effect factor for wind along the y-axis

        GC_pi : float
            Internal pressure coefficient

        K_d : float
            Wind directionality factor

        K_zt : float
            Topographic factor from ASCE 7-22 Figure 26.8-1

        K_e : float
            Ground elevation factor from ASCE 7-22 Table 26.9-1

        V : Velocity
            Basic wind speed from the ASCE 7 Hazard tool

        z_g : Length
            z_g from ASCE 7-22 Table 26.11-1

        alpha : float
            alpha from ASCE 7-22 Table 26.11-1

        q_h : Pressure
            Velocity pressure factor at roof height

        q_p : Pressure or None, optional
            Velocity pressure factor at parapet height"""
        # Merge file arguments and keyword arguments to set attributes
        if filepath:
            with open(filepath, "r") as file:
                raw = json.load(file)
            file_vals = {key: utils.convert_to_unit(value) for key, value in raw.items()}
        else:
            file_vals = {}

        attributes = ("building_type", "roof_type", "roof_angle", "ridge_axis",
                     "L_x", "L_y", "h", "G_x", "G_y", "GC_pi", "K_d", "K_zt",
                     "K_e", "V", "z_g", "alpha", "q_h", "q_p")
        for attribute in attributes:
            setattr(self, attribute, kwargs.get(attribute, file_vals.get(attribute)))
        self.G = {"x": self.G_x, "y": self.G_y}
        self.GC_pi = abs(self.GC_pi)

        # Generate C_p lookup dictionary
        with open(resources.joinpath("ASCE_MainWindCoefficients.json")) as file:
            type_coefs = json.load(file)[self.building_type]

        if self.building_type in ("low-rise", "mid-rise"):
            # Get parapet coefficients
            self.coefs = {
                "x": {"parapet": type_coefs["parapet"]},
                "y": {"parapet": type_coefs["parapet"]}
            }
            # Get wall coefficients
            for axis, L, B in (("x", self.L_x, self.L_y), ("y", self.L_y, self.L_x)):
                x_3 = (L/B).to("dimensionless").magnitude
                if x_3 <= 1:
                    self.coefs[axis].update({"wall": type_coefs["wall"]["L/B=1"]})
                elif x_3 <= 2:
                    self.coefs[axis].update({"wall": utils.linterp_dicts(
                        1, type_coefs["wall"]["L/B=1"],
                        2, type_coefs["wall"]["L/B=2"],
                        x_3)})
                elif x_3 <= 4:
                    self.coefs[axis].update({"wall": utils.linterp_dicts(
                        2, type_coefs["wall"]["L/B=2"],
                        4, type_coefs["wall"]["L/B=4"],
                        x_3)})
                else:
                    self.coefs[axis].update({"wall": type_coefs["wall"]["L/B=4"]})
            # Get roof coefficients
            for axis, L in (("x", self.L_x), ("y", self.L_y)):
                x_3 = (self.h/L).to("dimensionless").magnitude
                if self.ridge_axis == axis or self.roof_angle < 10:
                    # Use table for flat roof or wind parallel to ridge
                    if x_3 <= 0.5:
                        self.coefs[axis].update({
                            "roof": type_coefs["roof_parallel"]["h/L=0.5"]})
                    elif x_3 <= 1:
                        self.coefs[axis].update({"roof": utils.linterp_dicts(
                            0.5, type_coefs["roof_parallel"]["h/L=0.5"],
                            1, type_coefs["roof_parallel"]["h/L=1"],
                            x_3)})
                    else:
                        self.coefs[axis].update({
                            "roof": type_coefs["roof_parallel"]["h/L=1"]})
                elif self.ridge_axis is not None:
                    # Use table for wind normal to ridge
                    roof_angles = (10, 15, 20, 25, 30, 35, 45, 60, 80)
                    angle_index = sum(self.roof_angle > x for x in roof_angles)
                    angles = (roof_angles[angle_index-1], roof_angles[angle_index])
                    dicts = {}
                    for ratio in ("h/L=0.25", "h/L=0.5", "h/L=1"):
                        dicts.update({ratio: utils.linterp_dicts(
                            angles[0], type_coefs["roof_normal"][ratio][str(angles[0])],
                            angles[1], type_coefs["roof_normal"][ratio][str(angles[1])],
                            self.roof_angle)})
                    # Get final roof dictionary
                    if x_3 <= 0.25:
                        self.coefs[axis].update({"roof": dicts["h/L=0.25"]})
                    elif x_3 <= 0.5:
                        self.coefs[axis].update({"roof": utils.linterp_dicts(
                            0.25, dicts["h/L=0.25"], 0.5, dicts["h/L=0.5"], x_3)})
                    elif x_3 <= 1:
                        self.coefs[axis].update({"roof": utils.linterp_dicts(
                            0.5, dicts["h/L=0.5"], 1, dicts["h/L=1"], x_3)})
                    else:
                        self.coefs[axis].update({"roof": dicts["h/L=1"]})
                else:
                    raise ValueError("ridge_axis not set")
        elif self.building_type == "open":
            raise NotImplementedError("open buildings have not yet been implemented")
        else:
            raise ValueError(f"Unsupported building type: {self.building_type}")

    def get_load(
        self,
        axis: str,
        element: str,
        location: str | Length) -> Pressure:
        """Get the wind pressures for the specified axis, element, and location.
        Note: q_i is always taken as q_h so calculations for partially enclosed
        buildings may be conservative.

        Parameters
        ==========

        axis : str
            Wind direction. One of: "x" or "y"

        element : str
            Element to get the wind pressure on.
            One of: "wall", "parapet", or "roof"

        location : str or Length
            Location of the element to get the wind pressure on.
                - "leeward" or "side" for leeward or side walls respectively
                - Height above ground level for windward walls
                - "windward" or "leeward" for parapets
                - "windward" or "leeward" for wind normal to gable, hip,
                monoslope, or mansard roofs
                - Distance from windward edge for flat roofs or wind parallel 
                to gable, hip, monoslope, or mansard roofs"""
        if not isinstance(location, str):
            d = location
            if element == "roof":
                if d <= self.h/2:
                    location = "d<=h/2"
                elif d <= self.h:
                    location = "d<=h"
                elif d <= 2*self.h:
                    location = "d<=2h"
                else:
                    location = "d>2h"
            elif element == "wall":
                location = "windward"

        coefs = self.coefs[axis][element][location]
        p_min = unit(coefs["p_min"])
        match coefs.get("q_z", "q_h"):
            case "q_h":
                q_z = self.q_h
            case "q_z":
                K_z = chapter_26.table_26_10_1(d, self.z_g, self.alpha)
                q_z = chapter_26.eq_26_10_1(K_z, self.K_zt, self.K_e, self.V)
            case "q_p":
                q_z = self.q_p

        pressures = []
        for C_p in (coefs["c1"], coefs["c2"]):
            if element == "parapet":
                p = q_z*self.K_d*C_p
            else:
                p = q_z*self.K_d*self.G[axis]*C_p+self.q_h*self.K_d*self.GC_pi*sign(C_p)
            pressures.append(max(abs(p), p_min)*sign(p))
        return pressures


class CandCServer:
    """Class for calculating C&C wind pressures per ASCE 7-22 Chapter 30"""
    def __init__(self, filepath: str = "", **kwargs):
        """Create a new CandCServer. Values can be loaded from a file or passed
        manually, but all values should be specified. Values that are passed
        manually will override values provided by the file.

        Parameters
        ==========

        file : str, optional
            Path to json file to load variables from

        building_type : str
            Type of building for CandC calculations.
            One of: "low-rise" or "open"

        roof_type : str
            Type of roof for CandC calculations. Should be one of "gable",
            "hip", or "canopy" for low-rise buildings and one of
            "monoslope_clear" or "monoslope_obstructed" for open buildings.

        roof_angle : float
            Roof angle ($\\theta$) in degrees

        a : Length
            Length of wind zone dimension a

        G_x : float
            Gust effect factor for wind along the x-axis

        G_y : float
            Gust effect factor for wind along the y-axis

        GC_pi : float
            Internal pressure coefficient

        K_d : float
            Wind directionality factor

        q_h : Pressure
            Velocity pressure factor at roof height

        h_c : Length or None, optional
            Canopy height

        h_e : Length or None, optional
            Eve height for canopy calculations

        q_p : Pressure or None, optional
            Velocity pressure factor at parapet height"""
        # Merge file arguments and keyword arguments to set attributes
        if filepath:
            with open(filepath, "r") as file:
                raw = json.load(file)
            file_vals = {key: utils.convert_to_unit(value) for key, value in raw.items()}
        else:
            file_vals = {}

        attributes = ("building_type", "roof_type", "roof_angle", "a", "G_x",
                     "G_y", "GC_pi", "h_c", "h_e", "K_d", "q_h", "q_p")
        for attribute in attributes:
            setattr(self, attribute, kwargs.get(attribute, file_vals.get(attribute)))
        self.G = {"x": self.G_x, "y": self.G_y}
        self.GC_pi = abs(self.GC_pi)

        # Generate C_p lookup dictionary
        with open(resources.joinpath("ASCE_CandCCoefficients.json")) as coefficients_file:
            type_coefs = json.load(coefficients_file)[self.building_type]

        match self.building_type:
            case "low-rise":
                # Get wall coefficients
                self.coefs = type_coefs["walls"]
                # Get roof coefficients
                if self.roof_angle <= 7:
                    self.coefs.update(type_coefs["flat"])
                elif self.roof_angle <= 20:
                    self.coefs.update(type_coefs["low_"+self.roof_type])
                elif self.roof_angle <= 27:
                    self.coefs.update(type_coefs["mid_"+self.roof_type])
                elif self.roof_angle <= 45:
                    self.coefs.update(type_coefs["high_"+self.roof_type])
                else:
                    raise ValueError("Roof slope greater than 45 degrees")
                # Get canopy coefficients
                if self.h_c and self.h_e:
                    if self.h_c/self.h_e <= 0.5:
                        self.coefs.update(type_coefs["low_canopy"])
                    elif self.h_c/self.h_e < 0.9:
                        self.coefs.update(type_coefs["mid_canopy"])
                    elif self.h_c/self.h_e <= 1:
                        self.coefs.update(type_coefs["high_canopy"])
                    else:
                        raise ValueError("Canopy is higher than mean eave height")
            case "mid-rise":
                raise NotImplementedError("mid-rise buildings have not yet been implemented")
            case "open":
                # Get roof coefficients
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
                self.coefs = utils.linterp_dicts(
                    slopes[0],
                    type_coefs[self.roof_type+"_"+str(slopes[0])],
                    slopes[1],
                    type_coefs[self.roof_type+"_"+str(slopes[1])],
                    self.roof_angle)
            case _:
                raise ValueError(f"Unsupported building type: {self.building_type}")

    def get_load(
        self,
        zone: str,
        area: Area,
        G_method: str = "max",
        q_z: Optional[Pressure] = None,
        GC_pi: Optional[float] = None,
        p_min: Optional[Pressure] = None) -> Pressure:
        """Get the wind pressure for the specified zone and area

        Parameters
        ==========

        zone : str
            C&C wind zone to calculate wind pressure for. Allowable options
            depend on the building and roof type.

        area : Area
            Tributary area to calculate wind pressure for

        G_method : str, optional
            String indicating which G value to use for the calculation.
            Should be one of "x", "y", or "max".

        q_z : Pressure
            Velocity pressure factor at height z

        GC_pi : float
            Internal pressure coefficient

        p_min : Pressure, optional
            Minimum magnitude for CandC wind pressure. Default value is
            16 psf unless the zone requests a different value. Manually
            setting this value overrides the zone requesting a value."""
        coefs = self.coefs[zone]

        if GC_pi is not None:
            GC_pi = abs(GC_pi)
        else:
            GC_pi = coefs.get("GC_pi", self.GC_pi)

        if p_min is not None:
            p_min = abs(p_min)
        else:
            p_min = unit(coefs.get("p_min", "16 psf"))

        if not q_z and coefs.get("use_q_p"):
            q_z = self.q_p
        elif not q_z:
            q_z = self.q_h

        match coefs.get("kind"):
            case "single_log":
                area = area.to("ft**2").magnitude
                GC_p = coefs["c1"]+coefs["c2"]*log10(
                    min(max(area, coefs["low_limit"]), coefs["high_limit"]))
                p = q_z*self.K_d*(GC_p+GC_pi*sign(GC_p))
            case "double_log":
                area = area.to("ft**2").magnitude
                if area <= coefs["break_point"]:
                    GC_p = coefs["e1c1"]+coefs["e1c2"]*log10(max(area, coefs["low_limit"]))
                else:
                    GC_p = coefs["e2c1"]+coefs["e2c2"]*log10(min(area, coefs["high_limit"]))
                p = q_z*self.K_d*(GC_p+GC_pi*sign(GC_p))
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
                raise ValueError(f"Unsupported kind: {coefs.get("kind")}")
        return max(abs(p), abs(p_min))*sign(p)
