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

from enum import auto
from enum import StrEnum


class LexicalNameOrder(StrEnum):
    # The family name comes first, while the given name comes last. This
    # order is primarily used in East Asia (for example in China, Japan and
    # Korea), as well as in Southeast Asia (Cambodia and Vietnam), and
    # Southern and North Eastern parts of India.  Also in Central Europe is
    # used by Hungarians.
    EASTERN_ORDER = auto()

    # The given name comes first, while the family name comes last.  This
    # order is usually used in most European countries and in countries that
    # have cultures predominantly influenced by Western Europe (e.g. North
    # and South America, North, East, Central and West India, Thailand,
    # Australia, New Zealand and the Philippines).
    WESTERN_ORDER = auto()


class LexicalNameComponent(StrEnum):
    FIRST_NAME = auto()
    LAST_NAME = auto()


class ProsoponymErrorCode(StrEnum):
    INCOMPLETE_FULL_NAME = auto()
    INVALID_LEXICAL_NAME_ORDER = auto()
    MISSING_NAME_COMPONENTS = auto()
    INDETERMINATE_LEXICAL_NAME_ORDER = auto()


# List of the lexical name orders per country.
COUNTRY_LEXICAL_NAME_ORDERS = {
    'US': LexicalNameOrder.WESTERN_ORDER,
    'GB': LexicalNameOrder.WESTERN_ORDER,
    'CA': LexicalNameOrder.WESTERN_ORDER,
    'CA': LexicalNameOrder.WESTERN_ORDER,
    'AU': LexicalNameOrder.WESTERN_ORDER,
    'IN': LexicalNameOrder.EASTERN_ORDER,
    'IN': LexicalNameOrder.WESTERN_ORDER,
    'CN': LexicalNameOrder.EASTERN_ORDER,
    'RU': LexicalNameOrder.WESTERN_ORDER,
    'BR': LexicalNameOrder.WESTERN_ORDER,
    'MX': LexicalNameOrder.WESTERN_ORDER,
    'FR': LexicalNameOrder.WESTERN_ORDER,
    'DE': LexicalNameOrder.EASTERN_ORDER,
    'JP': LexicalNameOrder.EASTERN_ORDER,
    'KR': LexicalNameOrder.EASTERN_ORDER,
    'IT': LexicalNameOrder.WESTERN_ORDER,
    'ES': LexicalNameOrder.WESTERN_ORDER,
    'AR': LexicalNameOrder.WESTERN_ORDER,
    'ZA': LexicalNameOrder.WESTERN_ORDER,
    'ZA': LexicalNameOrder.WESTERN_ORDER,
    'ZA': LexicalNameOrder.WESTERN_ORDER,
    'NG': LexicalNameOrder.WESTERN_ORDER,
    'KE': LexicalNameOrder.WESTERN_ORDER,
    'KE': LexicalNameOrder.WESTERN_ORDER,
    'EG': LexicalNameOrder.EASTERN_ORDER,
    'SA': LexicalNameOrder.EASTERN_ORDER,
    'IR': LexicalNameOrder.EASTERN_ORDER,
    'TR': LexicalNameOrder.EASTERN_ORDER,
    'PK': LexicalNameOrder.EASTERN_ORDER,
    'PK': LexicalNameOrder.WESTERN_ORDER,
    'ID': LexicalNameOrder.WESTERN_ORDER,
    'TH': LexicalNameOrder.WESTERN_ORDER,
    'VN': LexicalNameOrder.EASTERN_ORDER,
    'SS': LexicalNameOrder.WESTERN_ORDER,
    'BE': LexicalNameOrder.WESTERN_ORDER,
    'BE': LexicalNameOrder.EASTERN_ORDER,
    'PT': LexicalNameOrder.WESTERN_ORDER,
    'CL': LexicalNameOrder.WESTERN_ORDER,
    'CO': LexicalNameOrder.WESTERN_ORDER,
    'ET': LexicalNameOrder.EASTERN_ORDER,
    'ET': LexicalNameOrder.EASTERN_ORDER,
    'DZ': LexicalNameOrder.EASTERN_ORDER,
    'MA': LexicalNameOrder.EASTERN_ORDER,
    'TN': LexicalNameOrder.EASTERN_ORDER,
    'LY': LexicalNameOrder.EASTERN_ORDER,
    'SD': LexicalNameOrder.EASTERN_ORDER,
    'SD': LexicalNameOrder.WESTERN_ORDER,
    'CD': LexicalNameOrder.WESTERN_ORDER,
    'CD': LexicalNameOrder.WESTERN_ORDER,
    'CD': LexicalNameOrder.WESTERN_ORDER,
    'UG': LexicalNameOrder.WESTERN_ORDER,
    'UG': LexicalNameOrder.WESTERN_ORDER,
    'TZ': LexicalNameOrder.WESTERN_ORDER,
    'TZ': LexicalNameOrder.WESTERN_ORDER,
    'PE': LexicalNameOrder.WESTERN_ORDER,
    'VE': LexicalNameOrder.WESTERN_ORDER,
    'BO': LexicalNameOrder.WESTERN_ORDER,
    'BO': LexicalNameOrder.EASTERN_ORDER,
    'PY': LexicalNameOrder.WESTERN_ORDER,
    'UY': LexicalNameOrder.WESTERN_ORDER,
    'HU': LexicalNameOrder.EASTERN_ORDER,
    'AT': LexicalNameOrder.EASTERN_ORDER,
    'CH': LexicalNameOrder.EASTERN_ORDER,
    'CH': LexicalNameOrder.WESTERN_ORDER,
    'CH': LexicalNameOrder.WESTERN_ORDER,
    'SE': LexicalNameOrder.EASTERN_ORDER,
    'FI': LexicalNameOrder.EASTERN_ORDER,
    'FI': LexicalNameOrder.EASTERN_ORDER,
    'DK': LexicalNameOrder.EASTERN_ORDER,
    'PL': LexicalNameOrder.WESTERN_ORDER,
    'LU': LexicalNameOrder.WESTERN_ORDER,
    'LU': LexicalNameOrder.EASTERN_ORDER,
    'IE': LexicalNameOrder.WESTERN_ORDER,
    'CY': LexicalNameOrder.EASTERN_ORDER,
    'LT': LexicalNameOrder.EASTERN_ORDER,
    'LV': LexicalNameOrder.EASTERN_ORDER,
    'EE': LexicalNameOrder.EASTERN_ORDER,
    'RO': LexicalNameOrder.WESTERN_ORDER,
    'AZ': LexicalNameOrder.EASTERN_ORDER,
    'AZ': LexicalNameOrder.WESTERN_ORDER,
    'KZ': LexicalNameOrder.WESTERN_ORDER,
    'UZ': LexicalNameOrder.EASTERN_ORDER,
    'KG': LexicalNameOrder.EASTERN_ORDER,
    'TJ': LexicalNameOrder.WESTERN_ORDER,
    'TM': LexicalNameOrder.WESTERN_ORDER,
    'NP': LexicalNameOrder.EASTERN_ORDER,
    'LK': LexicalNameOrder.EASTERN_ORDER,
    'LK': LexicalNameOrder.EASTERN_ORDER,
    'MM': LexicalNameOrder.WESTERN_ORDER,
}
