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
        self.model = ElementTree.parse(filepath)

        # Get the units from the OpenRE file
        unit_codes = self.model.getroot().get("Units").split("-")
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
        for loading in self.model.iterfind("Data/LoadConditions/*"):
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
                        f"Unsupported load combination type: {load_condition.get("Type")}")

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
        for entry in self.model.iterfind(search):
            case_id = entry.get("LoadCombinationID", entry.get("LoadCaseID"))
            if case_id in cases:
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

        member_xml = self.model.find(f"Data/Members/Member[@ID='{member}']")
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
        for entry in self.model.iterfind(search):
            case_id = entry.get("LoadCombinationID", entry.get("LoadCaseID"))
            if case_id in cases:
                end_forces.loc[case_id, :] = 0
                for force in entry.iterfind(end_search):
                    end_forces.at[case_id, force.tag] = float(force.text)

        end_forces.loc[:, "Axial":"V3"] = end_forces.loc[:, "Axial":"V3"].map(
            lambda value: value*self.force_unit)
        end_forces.loc[:, "Torsion": "M33"] = end_forces.loc[:, "Torsion": "M33"].map(
            lambda value: value*self.force_unit*self.length_unit)
        return end_forces
