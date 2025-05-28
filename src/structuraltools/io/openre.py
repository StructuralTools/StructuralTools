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


from itertools import count as itercount
from typing import Optional
import xml.etree.ElementTree as ET

import pandas as pd

from structuraltools.unit import unit, Force, Length, LineLoad, Moment


class Model:
    """Class to read OpenRE files."""
    def __init__(self, filepath: str):
        """Read an OpenRE file

        Parameters
        ==========

        filepath : str
            Path to the file"""
        self.xml = ET.parse(filepath)

        # Get the units from the OpenRE file
        unit_codes = self.xml.getroot().get("Units").split("-")
        match unit_codes[0]:
            case "Kip":
                self.force_unit = unit.kip
            case "Lb":
                self.force_unit = unit.lb
            case _:
                raise NotImplementedError(f"{unit_codes} units are not currently supported")
        match unit_codes[1]:
            case "ft":
                self.length_unit = unit.ft
            case "in":
                self.length_unit = unit.inch
            case _:
                raise NotImplementedError(f"{unit_codes} units are not currently supported")

        # Sort and store the load conditions
        self.load_cases = {}
        self.design_combs = set()
        self.service_combs = set()
        for loading in self.xml.iterfind("Data/LoadConditions/*"):
            if loading.tag == "LoadCase":
                self.load_cases.update(
                    {loading.get("ID"): loading.get("Category")})
            else:
                if loading.get("Type") == "Design":
                    self.design_combs.add(loading.get("ID"))
                elif loading.get("Type") == "Service":
                    self.service_combs.add(loading.get("ID"))
                else:
                    raise ValueError(
                        f"Unsupported load combination type: {loading.get("Type")}")

        # Find the next nodal and member load IDs
        nodal = 0
        concentrated = 0
        distributed = 0
        for load in self.xml.iterfind("Data/Loads/*"):
            value = int(load.attrib["ID"])
            if load.tag == "Nodal" and value > nodal:
                nodal = value
            elif load.tag == "MemberConcentrated" and value > concentrated:
                concentrated = value
            elif load.tag == "MemberDistributed" and value > distributed:
                distributed = value
        self.nodal_ids = itercount(nodal+1)
        self.concentrated_ids = itercount(concentrated+1)
        self.distributed_ids = itercount(distributed+1)

    def add_distributed_load(
            self,
            member: int | str,
            load_case: str,
            direction: str,
            initial: LineLoad,
            final: Optional[LineLoad] = None,
            start: Length | str = "0%",
            end: Length | str = "100%",
            category: str = "Overall") -> None:
        """Add a member distributed load to the model

        Parameters
        ==========

        member : int or str
            ID number of the member to add the load to

        load_case : str
            ID of the load case to add the load to

        direction : str
            String indicating which axis the load acts along.
            One of: "X", "Y", or "Z"

        initial : LineLoad
            Load magnitude at the start of the load length

        final : LineLoad, Optional
            Load magnitude at the end of the load length.
            Optional for a uniform load.

        start : Length or str, Optional
            Where on the member to start the load length. May be a length
            quantity representing an absolute distance from the start of the
            member or a string representing a percentage along the member
            length. Defaults to "0%".

        end : Length or str, Optional
            Where on the member to end the load length. Similar to start.
            Defaults to "100%".

        category : str, Optional
            One of "Overall" or "OverProjection". Defaults to "Overall"."""
        lineload_unit = f"{self.force_unit:D}/{self.length_unit:D}"
        initial = str(initial.to(lineload_unit).magnitude)
        if final:
            final = str(final.to(lineload_unit).magnitude)
        else:
            final = initial

        if not isinstance(start, str):
            start = str(start.to(f"{self.length_unit:D}").magnitude)
        if not isinstance(end, str):
            end = str(end.to(f"{self.length_unit:D}").magnitude)

        load = ET.SubElement(self.xml.find("Data/Loads"), "MemberDistributed",
            {"ID": str(self.distributed_ids.__next__()), "LoadCaseID": load_case,
             "Direction": direction, "Category": category})
        ET.SubElement(load, "Member", {"ID": str(member)})
        value = ET.SubElement(load, "Value", {"Start": start, "End": end})
        ET.SubElement(value, "Initial").text = initial
        ET.SubElement(value, "Final").text = final

    def add_load_case(self, ID: str, name: str, category: str) -> None:
        """Add a load case to the model

        Parameters
        ==========

        ID : str
            Load case ID

        name : str
            Load case name

        category : str
            Load case category for creating load combinations.
            See the RAM Elements manual for the list of predefined categories"""
        self.load_cases.update({ID: category})
        ET.SubElement(self.xml.find("Data/LoadConditions"),
            "LoadCase", {"ID": ID, "Name": name, "Category": category})

    def add_nodal_load(
            self,
            node: int | str,
            load_case: str,
            FX: Optional[Force] = None,
            FY: Optional[Force] = None,
            FZ: Optional[Force] = None,
            MX: Optional[Moment] = None,
            MY: Optional[Moment] = None,
            MZ: Optional[Moment] = None) -> None:
        """Add a nodal load to the model

        Parameters
        ==========

        node : int or str
            ID number of the node to add the load to

        load_case : str
            ID of the load case to add the load to

        FX, FY, FZ : Force, Optional
            Forces along the x, y, and z axis respectively

        MX, MY, MZ : Moment, Optional
            Moments about the x, y, and z axis respectively"""
        load = ET.SubElement(self.xml.find("Data/Loads"), "Nodal",
            {"ID": str(self.nodal_ids.__next__()), "LoadCaseID": load_case})
        ET.SubElement(load, "Node", {"ID": str(node)})
        values = ET.SubElement(load, "Values")
        force_unit = f"{self.force_unit:D}"
        for axis, value in {"FX": FX, "FY": FY, "FZ": FZ}.items():
            if value:
                ET.SubElement(values, axis).text = str(value.to(force_unit).magnitude)
        torque_unit = f"{self.force_unit:D}*{self.length_unit:D}"
        for axis, value in {"MX": MX, "MY": MY, "MZ": MZ}.items():
            if value:
                ET.SubElement(values, axis).text = str(value.to(torque_unit).magnitude)

    def get_node_location(self, node: int | str) -> dict[str, Length]:
        """Return the location of the specified node

        Parameters
        ==========

        node : int or str
            ID number of the node"""
        node = self.xml.find(f"Data/Nodes/Node[@ID='{str(node)}']")
        return {axis: float(node.get(axis, 0))*self.length_unit for axis in ["X", "Y", "Z"]}

    def get_node_reactions(self, node: int | str, cases: str) -> pd.DataFrame:
        """Return the reaction forces for the specified node

        Parameters
        ==========

        node : int or str
            ID number of the node

        cases : str
            One of: "load_cases", "design_combs", or "service_combs"
            indicating which load cases/combinations to return the reactions for"""
        if cases == "load_cases":
            cases = self.load_cases.keys()
        else:
            cases = getattr(self, cases)

        reactions = pd.DataFrame(columns=["FX", "FY", "FZ", "MX", "MY", "MZ"])
        search = f"Output/NodeReactions/Reactions[@NodeID='{str(node)}']"
        for reaction in self.xml.iterfind(search):
            case_id = reaction.get("LoadCombinationID", reaction.get("LoadCaseID"))
            if case_id in cases:
                reactions.loc[case_id, :] = 0
                for direction in reaction:
                    reactions.at[case_id, direction.tag] = direction.text

        reactions.loc[:, "FX":"FZ"] = reactions.loc[:, "FX":"FZ"].map(
            lambda value: float(value)*self.force_unit)
        reactions.loc[:, "MX":"MZ"] = reactions.loc[:, "MX":"MZ"].map(
            lambda value: float(value)*self.force_unit*self.length_unit)
        return reactions

    def get_member_end_forces(
        self,
        member: int | str,
        node: int | str,
        cases: str) -> pd.DataFrame:
        """Return the member end reaction forces for the specified member at the
        specified node.

        Parameters
        ==========

        member : int or str
            ID number of the member

        node : int or str
            ID number of the node

        cases : str
            One of: "load_cases", "design_combinations", or "service_combinations"
            indicating which load cases/combinations to return the reactions for."""
        # Determine if the start or the end of the member was requested
        node = str(node)
        member = str(member)

        member_xml = self.xml.find(f"Data/Members/Member[@ID='{member}']")
        if member_xml.get("StartNodeID") == node:
            end_search = "Station[@X='0']/*"
        elif member_xml.get("EndNodeID") == node:
            end_search = "Station[@X!='0']/*"
        else:
            raise ValueError(f"Node {node} is not and end node for member {member}")

        if cases == "load_cases":
            cases = self.load_cases.keys()
        else:
            cases = getattr(self, cases)

        end_forces = pd.DataFrame(
            columns=["Axial", "V2", "V3", "Torsion", "M22", "M33"])
        search = f"Output/MemberEndForces/EndForce[@MemberID='{member}']"
        for end_force in self.xml.iterfind(search):
            case_id = end_force.get("LoadCombinationID", end_force.get("LoadCaseID"))
            if case_id in cases:
                end_forces.loc[case_id, :] = 0
                for force in end_force.iterfind(end_search):
                    end_forces.at[case_id, force.tag] = force.text

        end_forces.loc[:, "Axial":"V3"] = end_forces.loc[:, "Axial":"V3"].map(
            lambda value: float(value)*self.force_unit)
        end_forces.loc[:, "Torsion": "M33"] = end_forces.loc[:, "Torsion": "M33"].map(
            lambda value: float(value)*self.force_unit*self.length_unit)
        return end_forces

    def get_member_end_nodes(self, member: int | str) -> dict[str, str]:
        """Return a dictionary containing the IDs of the member start and
        end nodes

        Parameters
        ==========

        member : int or str
            ID of the member"""
        member = self.xml.find(f"Data/Members/Member[@ID='{str(member)}']").attrib
        return {"start": member["StartNodeID"], "end": member["EndNodeID"]}

    def write(self, filename: str, space: str = "    ") -> None:
        """Write the model to the specified file

        Parameters
        ==========

        filename : str
            File to write the model to

        space : str
            Space to use when formatting the xml"""
        ET.indent(self.xml, space)
        self.xml.write(filename)
