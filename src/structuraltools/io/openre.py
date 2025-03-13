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
        self.node_reactions = self.model[2][2]

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

    def get_node_reactions(self, node: str) -> pd.DataFrame:
        """Return the reaction forces for the specified node

        Parameters
        ==========

        node : str
            ID number of the node"""
        reactions = pd.DataFrame(columns=("FX", "FY", "FZ", "MX", "MY", "MZ"))
        for entry in self.node_reactions:
            node_id, case_id = entry.attrib.values()
            if node_id == node:
                reactions.loc[case_id, :] = 0
                for reaction in entry:
                    reactions.at[case_id, reaction.tag] = float(reaction.text)
        reactions.loc[:, "FX":"FZ"] = reactions.loc[:, "FX":"FZ"].map(
            lambda value: value*self.force_unit)
        reactions.loc[:, "MX":"MZ"] = reactions.loc[:, "MX":"MZ"].map(
            lambda value: value*self.force_unit*self.length_unit)
        return reactions

