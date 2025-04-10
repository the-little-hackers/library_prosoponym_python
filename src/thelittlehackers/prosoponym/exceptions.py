# MIT License
#
# Copyright (C) 2024 The Little Hackers.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from typing import Sequence

from thelittlehackers.exceptions import TheLittleHackersBaseError

from thelittlehackers.prosoponym.constants import LexicalNameComponent
from thelittlehackers.prosoponym.constants import ProsoponymErrorCode


class IncompleteFullNameError(TheLittleHackersBaseError):
    """
    Raised when no lexical name order can be determined for formatting
    a person's full name.
    """
    def __init__(self):
        super().__init__(
            "The full name must include both the first and last names",
            ProsoponymErrorCode.INCOMPLETE_FULL_NAME
        )


class IndeterminateLexicalNameOrderError(TheLittleHackersBaseError):
    """
    Raised when no lexical name order can be determined for formatting a
    person's full name.
    """
    def __init__(self):
        super().__init__(
            "No lexical name order can be determined to format the person's full "
            "name.",
            ProsoponymErrorCode.INDETERMINATE_LEXICAL_NAME_ORDER
        )


class InvalidLexicalNameOrderError(TheLittleHackersBaseError):
    """
    Raised when a person's full name is not formatted according to the
    lexical order of their culture.
    """
    def __init__(self):
        super().__init__(
            "The full name does not follow the lexical order of the person's culture",
            ProsoponymErrorCode.INVALID_LEXICAL_NAME_ORDER
        )


class MissingNameComponentsError(TheLittleHackersBaseError):
    """
    Indicate that some components of a first or last name of a person are
    missing in the full name of this person.
    """
    def __init__(
            self,
            lexical_name_component: LexicalNameComponent,
            missing_components: Sequence[str]
    ):
        self.__lexical_name_component = lexical_name_component
        self.__missing_components = missing_components

    def __str__(self):
        lexical_name_component_label = (
            'first name' if self.__lexical_name_component == LexicalNameComponent.FIRST_NAME
            else 'last name'
        )
        missing_components = [
            format_first_name(component) if self.__lexical_name_component == LexicalNameComponent.FIRST_NAME
                else format_last_name(component)
            for component in self.__missing_components
        ]
        formatted_missing_components = [f'"{component}"' for component in missing_components]
        return f"Missing {lexical_name_component_label}: {', '.join(formatted_missing_components)}"

    @property
    def lexical_name_component(self) -> LexicalNameComponent:
        return self.__lexical_name_component

    @property
    def missing_components(self) -> list[str]:
        return self.__missing_components
