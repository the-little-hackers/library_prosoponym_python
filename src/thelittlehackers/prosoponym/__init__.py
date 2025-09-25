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

import re
from pkgutil import extend_path
from typing import Sequence

import unidecode
from thelittlehackers.model.country import Country

from thelittlehackers.prosoponym.constants import COUNTRY_LEXICAL_NAME_ORDERS
from thelittlehackers.prosoponym.constants import LexicalNameComponent
from thelittlehackers.prosoponym.constants import LexicalNameOrder
from thelittlehackers.prosoponym.exceptions import IncompleteFullNameError
from thelittlehackers.prosoponym.exceptions import InvalidLexicalNameOrderError
from thelittlehackers.prosoponym.exceptions import MissingNameComponentsError
from thelittlehackers.prosoponym.exceptions import IndeterminateLexicalNameOrderError


__path__ = extend_path(__path__, __name__)


def __lowercase_name_components(name_components: Sequence[str]) -> Sequence[str]:
    """
    Convert all words in the given sequence to lowercase.


    :param name_components: A sequence of words.


    :return: A sequence where each word is converted to lowercase,
        preserving the original order.

    """
    return list(map(str.lower, name_components))  # type: ignore


def __normalized_name_components(name_components: Sequence[str]) -> Sequence[str]:
    """
    Normalize name components by converting letters to their unaccented
    Latin equivalents and transforming them to lowercase.


    :param name_components: A list of words representing name components.


    :return: A list of words where each word is converted to lowercase and
        stripped of diacritical marks, preserving the original order.
    """
    return [
        unidecode.unidecode(component.lower())
        for component in name_components
    ]


def __update_lexical_name_components(
        full_name_word_lexical_name_map: dict[int, LexicalNameComponent | None],
        full_name_components: Sequence[str],
        lexical_name_component: LexicalNameComponent,
        part_name_components: Sequence[str],
        lexical_name_order: LexicalNameOrder
) -> Sequence[str]:
    """
    Update the lexical name mapping of words in a full name.

    This function assigns the given lexical name component (e.g., first
    name or last name) to matching words in the full name, according to
    the specified lexical order.  Words that cannot be found are returned
    as missing components.


    :param full_name_word_lexical_name_map: A dictionary mapping word
        indices in the full name to their lexical name component (either
        first name or last name).

    :param full_name_components: The list of words in the full name.

    :param lexical_name_component: The lexical classification (first name
        or last name) for the words in ``part_name_components``.

    :param part_name_components: The list of words representing either the
        first name or last name within the full name.

    :param lexical_name_order: The order in which the full name is
        structured (e.g., Eastern or Western name order).


    :return: A list of words from ``part_name_components`` that were not
        found in ``full_name_components``.
    """
    part_name_components_found = {
        i: False
        for i in range(len(part_name_components))
    }

    # Try to find the components of the part name in the full name (strong
    # match).
    part_name_components_range = range(len(part_name_components))
    if (
        (
            lexical_name_component == LexicalNameComponent.FIRST_NAME
            and lexical_name_order == LexicalNameOrder.EASTERN_ORDER
        ) or (
            lexical_name_component == LexicalNameComponent.LAST_NAME
             and lexical_name_order == LexicalNameOrder.WESTERN_ORDER
        )
    ):
        part_name_components_range = reversed(part_name_components_range)

    for i in part_name_components_range:
        component = part_name_components[i]
        for j in range(len(full_name_components)):
            if component == full_name_components[j] and not full_name_word_lexical_name_map[j]:
                full_name_word_lexical_name_map[j] = lexical_name_component
                part_name_components_found[i] = True

    missing_part_name_components = [
        part_name_components[i]
        for i in range(len(part_name_components))
        if not part_name_components_found[i]
    ]

    return missing_part_name_components


def __describe_full_name_components(
        full_name_components: Sequence[str],
        first_name_components: Sequence[str],
        last_name_components: Sequence[str],
        lexical_name_order: LexicalNameOrder,
        strict: bool = True
) -> dict[int, LexicalNameComponent]:
    """
    Identify the lexical role (first name or last name) of each word in a
    person's full name.


    :note: The comparison between words in the full name, first name, and
        last name is case-insensitive.


    :param full_name_components: A list of words forming the person's full
        name, including first, last, and any middle names, ordered
        according to the lexical conventions of their culture.

    :param first_name_components: A list of words that make up the
        person's first name.

    :param last_name_components: A list of words that make up the person's
        last name (surname).

    :param lexical_name_order: The lexical order in which the person's
        full name is written.

    :param strict: If ``True``, words in the first and last name must
        exactly match their counterparts in the full name, including
        accents.  If ``False``, all words are normalized by removing
        accents before comparison.


    :return: A dictionary mapping each word's index in the full name to
        its lexical role.  The value is either `LexicalNameComponent.FIRST_NAME`
        or `LexicalNameComponent.LAST_NAME`.  If a word does not match
        either, it is assumed to be a middle name and is assigned ``None``.


    :raise MissingNameComponentsException: If any word from the first or
        last name is missing from the full name.
    """
    full_name_lowercase_components = __lowercase_name_components(full_name_components)
    first_name_lowercase_components = __lowercase_name_components(first_name_components)
    last_name_lowercase_components = __lowercase_name_components(last_name_components)

    full_name_normalized_components = __normalized_name_components(full_name_lowercase_components)
    first_name_normalized_components = __normalized_name_components(first_name_lowercase_components)
    last_name_normalized_components = __normalized_name_components(last_name_lowercase_components)

    full_name_word_lexical_name_map: dict[int, LexicalNameComponent | None] = {
        i: None
        for i in range(len(full_name_components))
    }

    # Try to determine the last name components of the full name.
    missing_part_name_components = __update_lexical_name_components(
        full_name_word_lexical_name_map,
        full_name_lowercase_components if strict else full_name_normalized_components,
        LexicalNameComponent.LAST_NAME,
        last_name_lowercase_components if strict else last_name_normalized_components,
        lexical_name_order
    )

    if missing_part_name_components:
        raise MissingNameComponentsError(LexicalNameComponent.LAST_NAME, missing_part_name_components)

    # Try to determine the first name components of the full name.
    missing_part_name_components = __update_lexical_name_components(
        full_name_word_lexical_name_map,
        full_name_lowercase_components if strict else full_name_normalized_components,
        LexicalNameComponent.FIRST_NAME,
        first_name_lowercase_components if strict else first_name_normalized_components,
        lexical_name_order
    )

    if missing_part_name_components:
        raise MissingNameComponentsError(LexicalNameComponent.FIRST_NAME, missing_part_name_components)

    # Return the full name components with their lexical name information.
    return full_name_word_lexical_name_map


def cleanse_name(name: str | None) -> str | None:
    """
    Normalize a person's name by removing punctuation and extra spaces.


    :param name: A given name, surname, or full name of a person.


    :return: The cleaned name with punctuation replaced by spaces and
        consecutive spaces reduced to a single space.


    :raise ValueError: If `name` is None.
    """
    if name is None:
        raise ValueError("The argument `name` must not be null")

    # Replace any punctuation character with space.
    punctuationless_string = re.sub(r'[.,\\/#!$%^&*;:{}=\-_`~()<>"\']', ' ', name)

    # Remove any duplicate space characters.
    return ' '.join(punctuationless_string.split())


def format_first_name(first_name: str) -> str:
    """
    Format a person's first name by normalizing spaces and capitalizing
    each word.


    :param first_name: Forename (also known as *given name*) of the person.


    :return: The formatted first name with proper capitalization.


    :raise ValueError: If `first_name` is empty after cleansing.
    """
    first_name = cleanse_name(first_name)

    if first_name is None:
        raise ValueError('A first name must be provided')

    formatted_first_name = ' '.join(map(str.capitalize, first_name.split()))  # type: ignore
    return formatted_first_name


def format_full_name(
        first_name: str,
        last_name: str,
        country: Country = None,
        default_lexical_name_order: LexicalNameOrder = None,
        full_name: str = None,
        strict: bool = True
) -> str:
    """
    Formats a person's full name based on cultural naming conventions.

    The order of the first and last names depends on the specified country:

    - **Western order (First Last)**: Common in French and English-speaking countries.
    - **Eastern order (Last First)**: Used in Vietnamese and Korean naming conventions.

    Each word in the first and last names must be present in the full name
    with the appropriate capitalization.

    Examples:

    ```python
    >>> format_full_name(
    ...     "aline minh anh",
    ...     "caune ly",
    ...     full_name="caune ly aline minh anh",
    ...     country=Country.from_string('FR')
    ... )
    'Aline Minh Anh CAUNE LY'

    >>> format_full_name(
    ...     "truc",
    ...     "nguyen",
    ...     full_name="nguyen thi thanh truc",
    ...     country=Country.from_string('VN')
    ... )
    'NGUYEN Thi Thanh Truc'
    ```

    :param first_name: The given name(s).

    :param last_name: The surname or family name.

    :param country: The person's nationality, determining the name order
        and formatting rules.

    :param default_lexical_name_order: The default name order if the
        country does not define one.

    :param full_name: The complete name. If not provided, it is
        constructed from `first_name` and `last_name`.

    :param strict: Ensure that name components strictly follow cultural
        conventions.


    :return: The formatted full name.


    :raise MissingNameComponentsException: If parts of `first_name` or
        `last_name` are missing from `full_name`.

    :raise UndefinedLexicalNameOrderException: If the name order cannot be
        determined and `default_lexical_name_order` is not provided.
    """
    # Determine the lexical name order to use depending on the locale.
    lexical_name_order = COUNTRY_LEXICAL_NAME_ORDERS.get(country and country.country_code, default_lexical_name_order)

    # Cleanse and format the first and the last names.
    first_name = format_first_name(first_name)
    last_name = format_last_name(last_name)

    # If no full name is passed, build it from the first and the last names.
    if not full_name:
        if not lexical_name_order:
            raise IndeterminateLexicalNameOrderError()

        full_name = (
            f'{last_name} {first_name}' if lexical_name_order == LexicalNameOrder.EASTERN_ORDER
            else f'{first_name} {last_name}'
        )
        return full_name

    # Split the first, last, and full names into components.
    full_name = cleanse_name(full_name)
    full_name_components = full_name.split()
    first_name_components = first_name.split()
    last_name_components = last_name.split()

    # Find the lexical name component of each word of the full name, either
    # a first name or a last name component.  Full name's words that are not
    # described are middle names (i.e., not part of the first and last names).
    full_name_description = __describe_full_name_components(
        full_name_components,
        first_name_components,
        last_name_components,
        lexical_name_order,
        strict=strict
    )

    reformatted_last_name_components = ' '.join([
        format_last_name(full_name_components[i])
        for i in range(len(full_name_components))
        if full_name_description[i] == LexicalNameComponent.LAST_NAME
    ])

    reformatted_first_name_components = ' '.join([
        format_first_name(full_name_components[i])
        for i in range(len(full_name_components))
        if full_name_description[i] == LexicalNameComponent.FIRST_NAME
           or not full_name_description[i]
    ])

    reformatted_full_name_components = [
        reformatted_first_name_components,
        reformatted_last_name_components
    ]

    if lexical_name_order == LexicalNameOrder.EASTERN_ORDER:
        reformatted_full_name_components = reversed(reformatted_full_name_components)

    reformatted_full_name = ' '.join(reformatted_full_name_components)

    return reformatted_full_name


def format_last_name(last_name: str) -> str:
    """
    Format a person's last name by normalizing spaces and converting it
    to uppercase.


    :param last_name: Surname (also known as *family name*) of the person.


    :return: The formatted last name in uppercase.


    :raise ValueError: If `last_name` is empty after cleansing.
    """
    last_name = cleanse_name(last_name)

    if last_name is None:
        raise ValueError('A surname must be provided')

    formatted_last_name = ' '.join(map(str.upper, last_name.split()))  # type: ignore
    return formatted_last_name


def is_first_name_well_formatted(first_name: str) -> bool:
    """
    Determine whether a first name is correctly formatted.

    A well-formatted first name when each word starts with an uppercase
    letter and all other letters in each word are lowercase.


    :param first_name: The first name to check.


    :return: ``True`` if the first name is correctly formatted, ``False``
        otherwise.
    """
    return first_name == format_first_name(first_name)


def is_full_name_well_formatted(
        first_name: str,
        last_name: str,
        full_name: str,
        country: Country = None,
        default_lexical_name_order: LexicalNameOrder = None,
        strict: bool = True
) -> bool:
    """
    Determine whether a full name is correctly formatted.

    A full name is considered well formatted if:

    - Its components (first name and last name) adhere to their respective
      formatting rules.

    - If ``strict`` is enabled, the name follows the expected lexical
      order based on cultural conventions.


    :param first_name: The given name (or personal name) that is part of
        the full name.

    :param last_name: The surname (or family name) that is part of the
        full name.

    :param full_name: The full name to check.

    :param country: The country representing the naming system
        associated with the person's culture, which influences name
        formatting and ordering.

    :param default_lexical_name_order: The default name order to apply
        when no specific lexical order is defined for the given
        ``country_code``.

    :param strict: Whether to enforce the expected lexical order for the
        specified culture.


    :return: ``True`` if the full name is correctly formatted, ``False``
        otherwise.
    """
    return full_name == format_full_name(
        first_name,
        last_name,
        country=country,
        default_lexical_name_order=default_lexical_name_order,
        full_name=full_name,
        strict=strict
    )


def is_last_name_well_formatted(last_name: str) -> bool:
    """
    Determine whether a last name (surname) is correctly formatted.

    A well-formatted last name when each word is entirely in uppercase.


    :param last_name: The last name to check.


    :return: ``True`` if the last name is correctly formatted, ``False``
        otherwise.
    """
    return last_name == format_last_name(last_name)
