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


from structuraltools import sections
from structuraltools.unit import unit
from structuraltools.utils import isclose


def test_Rectangle_init():
    plate = sections.Rectangle(4*unit.inch, 1*unit.inch)
    assert isclose(plate.A, 4*unit.inch**2)
    assert isclose(plate.S_x, 2.66666667*unit.inch**3, atol=1e-8*unit.inch**3)
    assert isclose(plate.I_x, 5.33333333*unit.inch**4, atol=1e-8*unit.inch**4)
    assert isclose(plate.r_x, 1.15470054*unit.inch, atol=1e-8*unit.inch)
    assert isclose(plate.S_y, 0.66666667*unit.inch**3, atol=1e-8*unit.inch**3)
    assert isclose(plate.I_y, 0.33333333*unit.inch**4, atol=1e-8*unit.inch**4)
    assert isclose(plate.r_y, 0.28867513*unit.inch, atol=1e-8*unit.inch)
