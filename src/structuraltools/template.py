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


from string import Template as PyTemplate

from IPython.display import display, Latex, Markdown
from numpy import ceil, floor, trunc
from pint import Quantity

from structuraltools import decimal_points, header_level


class ResultIterator:
    def __init__(self, result, reverse: bool = False):
        self.string = result.string
        if reverse:
            self.iterator = iter(reversed(result.value))
        else:
            self.iterator = iter(result.value)

    def __iter__(self):
        return self

    def __reversed__(self):
        self.iterator = iter(reversed(list(self.iterator)))
        return self

    def __next__(self):
        return Result(self.string, self.iterator.__next__())


class Result[value_type]:
    """Class to allow the string representation of a calculation to be returned
    with the calculated result while still allowing the calculated result to be
    used more or less as its own type. This works by passing most of the dunder
    functions through to Result.value. The string can be accessed with
    Result.string."""
    def __init__(self, string: str, *value: value_type):
        """Create a new Result

        Parameters
        ==========

        string : str
            String to store in self.string

        value : any
            Value(s) the result represents. If multiple values are provided
            they are packed into a tuple."""
        self.string = string
        if len(value) == 1:
            self.value = value[0]
        else:
            self.value = value

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)

    def __format__(self, format_spec):
        return format(self.value)

    def __lt__(self, other):
        if isinstance(other, Result):
            return self.value < other.value
        else:
            return self.value < other

    def __le__(self, other):
        if isinstance(other, Result):
            return self.value <= other.value
        else:
            return self.value <= other

    def __eq__(self, other):
        if isinstance(other, Result):
            return self.value == other.value
        else:
            return self.value == other

    def __ne__(self, other):
        if isinstance(other, Result):
            return self.value != other.value
        else:
            return self.value != other

    def __gt__(self, other):
        if isinstance(other, Result):
            return self.value > other.value
        else:
            return self.value > other

    def __ge__(self, other):
        if isinstance(other, Result):
            return self.value >= other.value
        else:
            return self.value >= other

    def __bool__(self):
        return bool(self.value)

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, value):
        self.value[key] = value

    def __delitem__(self, key):
        del self.value[key]

    def __iter__(self):
        return ResultIterator(self)

    def __reversed__(self):
        return ResultIterator(self, True)

    def __contains__(self, item):
        return item in self.value

    def __add__(self, other):
        return self.value+other

    def __sub__(self, other):
        return self.value-other

    def __mul__(self, other):
        return self.value*other

    def __matmul__(self, other):
        return self.value@other

    def __truediv__(self, other):
        return self.value/other

    def __floordiv__(self, other):
        return self.value//other

    def __mod__(self, other):
        return self.value%other

    def __divmod__(self, other):
        return divmod(self.value, other)

    def __pow__(self, exp, mod=None):
        return pow(self.value, exp, mod)

    def __lshift__(self, other):
        return self.value<<other

    def __rshift__(self, other):
        return self.value>>other

    def __and__(self, other):
        return self.value&other

    def __xor__(self, other):
        return self.value^other

    def __or__(self, other):
        return self.value|other

    def __radd__(self, other):
        return other+self.value

    def __rsub__(self, other):
        return other-self.value

    def __rmul__(self, other):
        return other*self.value

    def __rmatmul__(self, other):
        return other@self.value

    def __rtruediv__(self, other):
        return other/self.value

    def __rfloordiv__(self, other):
        return other//self.value

    def __rmod__(self, other):
        return other%self.value

    def __rdivmod__(self, other):
        return divmod(other, self.value)

    def __rpow__(self, base, mod):
        return pow(base, self.value, mod)

    def __rlshift__(self, other):
        return other<<self.value

    def __rrshift__(self, other):
        return other>>self.value

    def __rand__(self, other):
        return other&self.value

    def __rxor__(self, other):
        return other^self.value

    def __ror__(self, other):
        return other|self.value

    def __iadd__(self, other):
        self.value += other
        return self

    def __isub__(self, other):
        self.value -= other
        return self

    def __imul__(self, other):
        self.value *= other
        return self

    def __imatmul__(self, other):
        self.value @= other
        return self

    def __itruediv__(self, other):
        self.value /= other
        return self

    def __ifloordiv__(self, other):
        self.value //= other
        return self

    def __imod__(self, other):
        self.value %= other
        return self

    def __ipow__(self, other):
        self.value **= other
        return self

    def __ilshift__(self, other):
        self.value <<= other
        return self

    def __irshift__(self, other):
        self.value >>= other
        return self

    def __iand__(self, other):
        self.value &= other
        return self

    def __ixor__(self, other):
        self.value ^= other
        return self

    def __ior__(self, other):
        self.value |= other
        return self

    def __neg__(self):
        return -self.value

    def __pos__(self):
        return +self.value

    def __abs__(self):
        return abs(self.value)

    def __invert__(self):
        return ~self.value

    def __complex__(self):
        return complex(self.value)

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __index__(self):
        return self.value.__index__()

    def __round__(self, *args):
        return round(self.value, *args)

    def __trunc__(self):
        return trunc(self.value)

    def __floor__(self):
        return floor(self.value)

    def __ceil__(self):
        return ceil(self.value)

    def to(self, unit_str):
        return self.value.to(unit_str)


class Template:
    """Template class with additional functionality to make it easy to handle
    the string representation of functions"""
    def __init__(self, kind: str, string: str):
        """Create a new result template with either a template string or with a
        string and value(s).

        Parameters
        ==========

        template_str : str
            String to use for the template

        string : str
            String to use as the filled template.

        value : any
            Value(s) to present as."""
        self.kind = kind
        self.string = string

    def display(self, string):
        """Display the provided string with the display settings based on
        self.kind

        Parameters
        ==========

        string : str
            String to display"""
        if self.kind == "Math":
            display(Latex(rf"\begin{{aligned}} {string} \end{{aligned}}"))
        elif self.kind == "Markdown":
            display(Markdown(string))
        else:
            display(Latex(string))

    def fill(
            self,
            variables: dict,
            *return_value,
            display: bool = False,
            return_string: bool = False,
            decimal_points: int = decimal_points,
            header_level: int = header_level) -> Result:
        """Pass provided values through and display or fill the representation
        string if desired. This is designed to be used in the return statement
        of a function.

        Parameters
        ==========

        variables : dict
            Values to fill out the template with

        return_value : any
            Values to return. If return_string is specified the string will be
            prepended to return_values and the result returned.

        display : bool
            Whether or not to display the filled template

        fill : bool
            Whether or not to return the filled template

        decimal_points : int
            How many decimal points to round to when writing values into the template

        header_level : int
            Header level to use when filling in markdown templates"""
        if not (display or return_string):
            return Result("", *return_value)

        _ = variables.pop("self", None)
        rounded_variables = {"header": "#"*header_level}
        for key, value in variables.items():
            if isinstance(value, Result):
                rounded_variables.update({key+"_str": value.string})
                value = value.value
            if isinstance(value, Quantity | float):
                rounded_variables.update({key: round(value, decimal_points)})
            else:
                rounded_variables.update({key: value})

        string = PyTemplate(self.string).substitute(**rounded_variables)
        if display:
            self.display(string)
        return Result(string, *return_value)
