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


from xml.etree import ElementTree

import pandas as pd

from structuraltools import unit


class Model:
    """Class to read OpenRE files."""
    def __init__(self, filepath: str):
        """Read an OpenRE file

        Parameters
        ==========

        filepath : str
            Path to the file"""
        self.model_tree = ElementTree.parse(filepath)
        self.model = self.model_tree.getroot()
        self.nodes = self.model[0][0]
        self.members = self.model[0][2]
        self.node_reactions = self.model[2][2]
        self.member_end_forces = self.model[2][1]

        # Get the units from the OpenRE file
        unit_codes = self.model.attrib["Units"].split("-")
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
        self.design_combinations = set()
        self.service_combinations = set()
        for load_condition in self.model[0][4]:
            if load_condition.get("Type") == "Design":
                self.design_combinations.add(load_condition.get("ID"))
            elif load_condition.get("Type") == "Service":
                self.service_combinations.add(load_condition.get("ID"))
            else:
                self.load_cases.update(
                    {load_condition.get("ID"): load_condition.get("Category")})

    def get_node_reactions(self, node: int, cases: str) -> pd.DataFrame:
        """Return the reaction forces for the specified node

        Parameters
        ==========

        node : int
            ID number of the node

        cases : str
            One of: "load_cases", "design_combinations", or "service_combinations"
            indicating which load cases/combinations to return the reactions for"""
        node = str(node)
        if cases == "load_cases":
            cases = self.load_cases.keys()
        else:
            cases = getattr(self, cases)
        reactions = pd.DataFrame(columns=["FX", "FY", "FZ", "MX", "MY", "MZ"])
        for entry in self.node_reactions:
            node_id = entry.get("NodeID")
            case_id = entry.get("LoadCombinationID", entry.get("LoadCaseID"))
            if node_id == node and case_id in cases:
                reactions.loc[case_id, :] = 0
                for reaction in entry:
                    reactions.at[case_id, reaction.tag] = float(reaction.text)
        reactions.loc[:, "FX":"FZ"] = reactions.loc[:, "FX":"FZ"].map(
            lambda value: value*self.force_unit)
        reactions.loc[:, "MX":"MZ"] = reactions.loc[:, "MX":"MZ"].map(
            lambda value: value*self.force_unit*self.length_unit)
        return reactions

    def get_member_end_forces(
        self,
        member: int,
        node: int,
        cases: str) -> pd.DataFrame:
        """Return the member end reaction forces for the specified member at the
        specified node.

        Parameters
        ==========

        member : int
            ID number of the member

        node : int
            ID number of the node

        cases : str
            One of: "load_cases", "design_combinations", or "service_combinations"
            indicating which load cases/combinations to return the reactions for."""
        # Determine if the start or the end of the member was requested
        node = str(node)
        try:
            member_xml = self.members[member-1]
            member = str(member)
            assert member_xml.get("ID") == member
        except AssertionError:
            for member_xml in self.members:
                if member_xml.get("ID") == member:
                    break

        if member_xml.get("StartNodeID") == node:
            get_0 = True
        elif member_xml.get("EndNodeID") == node:
            get_0 = False
        else:
            raise ValueError(f"Node {node} is not and end node for member {member}")

        if cases == "load_cases":
            cases = self.load_cases.keys()
        else:
            cases = getattr(self, cases)
        end_forces = pd.DataFrame(
            columns=["Axial", "V2", "V3", "Torsion", "M22", "M33"])
        for entry in self.member_end_forces:
            member_id = entry.get("MemberID")
            case_id = entry.get("LoadCombinationID", entry.get("LoadCaseID"))
            if member_id == member and case_id in cases:
                end_forces.loc[case_id, :] = 0
                for end in entry:
                    if end.get("X") == "0" and get_0:
                        for force in end:
                            end_forces.at[case_id, force.tag] = float(force.text)
                    elif end.get("X") != "0" and not get_0:
                        for force in end:
                            end_forces.at[case_id, force.tag] = float(force.text)
        end_forces.loc[:, "Axial":"V3"] = end_forces.loc[:, "Axial":"V3"].map(
            lambda value: value*self.force_unit)
        end_forces.loc[:, "Torsion": "M33"] = end_forces.loc[:, "Torsion": "M33"].map(
            lambda value: value*self.force_unit*self.length_unit)
        return end_forces
