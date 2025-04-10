# The Little Hackers Python Prosoponym Library
A Python library for formatting personal names, also known as prosoponyms in onomastics.

A personal name is the collection of names by which an individual is known, all of which refer to the same person.  It typically consists of a first name, middle name(s), and last name, though the order varies across cultures, following either Western or Eastern naming conventions.

```python
>>> from thelittlehackers.model.country import Country
>>> from thelittlehackers.prosoponym import LexicalNameOrder
>>> from thelittlehackers.prosoponym import format_first_name
>>> from thelittlehackers.prosoponym import format_full_name
>>> from thelittlehackers.prosoponym import format_last_name

>>> format_first_name("Aline Maria")
'Aline Maria'
>>> format_last_name("caune ly")
'CAUNE LY'

>>> format_full_name("alfred thanh phuc", "pham", Country.from_string('fra'))
'Alfred Thanh Phuc PHAM'
>>> format_full_name("alfred thanh phuc", "pham", Country.from_string('vie'))
'PHAM Alfred Thanh Phuc'

>>> format_full_name("alfred", "pham", Locale('vie'), full_name="pham thanh phuc")
ValueError: None of the first name words has been found in the full name
>>> format_full_name("alfred phuc", "pham", Locale('fra'), full_name="pham thanh phuc")
ValueError: The parts of the full name are not written in the expected order
>>> format_full_name("alfred phuc", "pham", Locale('fra'), full_name="alfred thanh phuc pham")
'Alfred Thanh Phuc PHAM'
>>> format_full_name("alfred phuc", "pham", Locale('vie'), full_name="Phạm thanh phúc alfred")
'PHẠM Thanh Phúc Alfred'

>>> # If a last name is composed of two or more words, while the full name
>>> # follows western lexical order, this two or more words SHOULD be 
>>> # in the full name (otherwise the function won't be able to determine
>>> # included in the full name, but not necessary.
>>> format_full_name("Aline", "Caune ly", Country.from_string('fra'), full_name="aline minh anh maria caune ly")  # OK
'Aline Minh Anh Maria CAUNE LY'
>>> format_full_name("Aline", "Caune", Country.from_string('fra'), full_name="aline minh anh maria caune ly")  # Still OK, even if incoherent input
'Aline Minh Anh Maria CAUNE LY'

>>> format_full_name("truc", "nguyen", Country.from_string('vie'), full_name="nguyen thi thanh truc maria")
'NGUYEN Thi Thanh Truc Maria'

>>> # If a last name is composed of two or more words, while the full name
>>> # follows eastern lexical order, this two or more words MUST be included
>>> # in the full name (otherwise the function won't be able to determine
>>> # which parts of the name correspond to the last name or to the 
>>> # possible middle name).
>>> format_full_name("Thao nguyen", "nguyen le", Country.from_string('vie'), "Nguyễn Lê thị Thảo Nguyên")
'NGUYỄN LÊ Thị Thảo Nguyên'  # OK
>>> format_full_name("Thao nguyen", "nguyen le", Country.from_string('vie'), "Nguyễn thị Thảo Nguyên")  # Still OK, even if incoherent input
'NGUYỄN Thị Thảo Nguyên'
>>> format_full_name("Thao nguyen", "nguyen", Country.from_string('vie'), "Nguyễn Lê thị Thảo Nguyên")  # Not OK! Part of the last name is missing.
'NGUYỄN Lê Thị Thảo Nguyên'
```