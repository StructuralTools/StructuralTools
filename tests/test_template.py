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


from structuraltools import unit

from structuraltools.template import Result, Template


def test_Template():
    template = Template("Markdown", "$header $test_string $length $length_str")
    test_string = "Hello World!"
    length = Result("length", 3.66667*unit.ft)
    options = {"return_string": True, "decimal_points": 2, "header_level": 2}
    result = template.fill(locals(), length, **options)
    assert result == length
    assert result.string == r"## Hello World! 3.67\ \mathrm{ft} length"
