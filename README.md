# The Little Hackers Python Prosoponym Library
A Python library for formatting personal names, also known as prosoponyms in onomastics.

A personal name is the collection of names by which an individual is known, all of which refer to the same person.  It typically consists of a first name, middle name(s), and last name, though the order varies across cultures, following either Western or Eastern naming conventions.

```python
from thelittlehackers.model.country import Country
from thelittlehackers import prosoponym

prosoponym.format_first_name("aline maria")
'Aline Maria'

prosoponym.format_last_name("caune ly")
'CAUNE LY'

prosoponym.format_full_name(
    "aline maria", 
    "caune ly",
    Country.from_string('FR')
)
'Aline Maria CAUNE LY'

prosoponym.format_full_name(
    "aline maria",
    "caune ly", 
    Country.from_string('VN')
)
'CAUNE LY Aline Maria'

prosoponym.format_full_name(
    "Aline Minh Anh Maria", 
    "CAUNE LY",
    full_name="Aline CAUNE LY"
)
thelittlehackers.prosoponym.exceptions.MissingNameComponentsError: Missing first name: "Maria"

prosoponym.format_full_name(
    "Aline", 
    "CAUNE LY", 
    Country.from_string('FR'), 
    full_name="Aline CAUNE"
)
thelittlehackers.prosoponym.exceptions.MissingNameComponentsError: Missing last name: "LY"


prosoponym.format_full_name(
    "Minh Anh", 
    "LÝ CAUNE",
    Country.from_string('VN'),
    full_name="Ly Thi Minh Anh Caune"
)
thelittlehackers.prosoponym.exceptions.MissingNameComponentsError: Missing last name: "LÝ"

prosoponym.format_full_name(
    "Minh Anh", 
    "LÝ CAUNE",
    Country.from_string('VN'),
    full_name="Ly Thi Minh Anh Caune",
    strict=False
)
'LY CAUNE Thi Minh Anh'

# # If a last name is composed of two or more words, while the full name
# # follows western lexical order, this two or more words SHOULD be 
# # in the full name (otherwise the function won't be able to determine
# # included in the full name), but not necessary.
# prosoponym.format_full_name(
#     "Aline", 
#     "Caune ly", 
#     Country.from_string('FR'), 
#     full_name="aline minh anh maria caune ly"
# )  # OK
# 'Aline Minh Anh Maria CAUNE LY'
# 
# prosoponym.format_full_name(
#     "Aline", 
#     "Caune",
#     Country.from_string('FR'),
#     full_name="aline minh anh maria caune ly"
# )  # Still OK, even if incoherent input
# 'Aline Minh Anh Maria CAUNE LY'
# 
# prosoponym.format_full_name(
#     "truc", 
#     "nguyen",
#     Country.from_string('VN'),
#     full_name="nguyen thi thanh truc maria"
# )
# 'NGUYEN Thi Thanh Truc Maria'
# 
# # If a last name is composed of two or more words, while the full name
# # follows eastern lexical order, this two or more words MUST be included
# # in the full name (otherwise the function won't be able to determine
# # which parts of the name correspond to the last name or to the 
# # possible middle name).
# prosoponym.format_full_name(
#     "Thao nguyen", 
#     "nguyen le",
#     Country.from_string('VN'), 
#     full_name="Nguyễn Lê thị Thảo Nguyên"
# )
# 'NGUYỄN LÊ Thị Thảo Nguyên'  # OK
# 
# prosoponym.format_full_name(
#     "Thao nguyen",
#     "nguyen le",
#     Country.from_string('VN'),
#     full_name="Nguyễn LÊ thị Thảo Nguyên"
# )  # Still OK, even if incoherent input
# 'NGUYỄN LÊ Thị Thảo Nguyên'
# 
# prosoponym.format_full_name(
#     "Thao nguyen", 
#     "nguyen",
#     Country.from_string('VN'),
#     full_name="Nguyễn Lê thị Thảo Nguyên"
# )  # Not OK! Part of the last name is missing.
# 'NGUYỄN Lê Thị Thảo Nguyên'
```