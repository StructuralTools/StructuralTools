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


from structuraltools.unit import Length
from structuraltools.utils import sqrt


class Rectangle:
    """Base class for rectangular sections"""

    def __init__(
        self,
        d: Length,
        b: Length):
        """Create a new rectangular section.

        Parameters
        ==========

        d : pint length quantity
            Section depth

        b : pint length quantity
            Section width"""
        if d >= b:
            self.d = d.to("inch")
            self.b = b.to("inch")
        else:
            self.d = b.to("inch")
            self.b = d.to("inch")

        self.A = (self.d*self.b).to("inch**2")
        self.S_x = (self.b*self.d**2/6).to("inch**3")
        self.I_x = (self.b*self.d**3/12).to("inch**4")
        self.r_x = (sqrt(self.I_x/self.A)).to("inch")
        self.S_y = (self.d*self.b**2/6).to("inch**3")
        self.I_y = (self.d*self.b**3/12).to("inch**4")
        self.r_y = (sqrt(self.I_y/self.A)).to("inch")
