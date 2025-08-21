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


from structuraltools.awc import chapter_2


def test_sec_2_3_3():
    C_t = chapter_2.sec_2_3_3(temperature=125, wet_service=True)
    assert C_t == {"F_b": 0.7, "F_t": 0.9, "F_v": 0.7, "F_c": 0.7,
                   "F_c_perp": 0.7, "E": 0.9, "E_min": 0.9}
