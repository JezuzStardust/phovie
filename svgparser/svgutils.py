import re

################################################################################
# Regular Expressions
################################################################################

# Match number e.g. -0.232E-23 or .23e1
# Breakdown:
# Optional minus sign
# One or more digits
# Optional group: Period followed by zero or more digits.
# Optional group: e or E followed by optional sign followed by one or more digits.
# The optional pattern after | is for the cases where the integer part is not present.
match_number = r"([+-]?(\d+(\.\d*)?|[+-]?(\.\d+))([eE][+-]?\d+)?)"
# match_number = r'(-?\d+(\.\d*)?([eE][-+]?\d+)?)|(-?\.\d+([eE][-+]?\d+)?)'
re_match_number = re.compile(match_number)

# Match color.
# Colors can be '#' <hex> <hex> <hex> ( <hex> <hex> <hex> ) ')'
# or 'rgb(' wsp* <int> comma <int> comma <int> wsp* ')'
# or 'rgb(' wsp* <int> '%' comma <int> '%' comma <int> '%' wsp* ')'
# or a color keyword.
# Where comma = wsp* ',' wsp*
match_rgb = r"rgb\(\s*(\d+)(%)?\s*,\s*(\d+)(%)?\s*,\s*(\d+)(%)?\s*\)"
re_match_rgb = re.compile(match_rgb)

################################################################################
# End: Regular Expressions
################################################################################

################################################################################
# Reading Coordinates
################################################################################

# For 96 dpi:
# 1 in = 96 px
# 1 cm = 96 / 2.54 px
# 1 mm = 96 / 25.4 px
# 1 pt = 1 / 72 in = 96 / 72 px = 1.33... px
# 1 pc = 16 px
# Fix em an ex if SVG text support is added.
# The em and ex are relative to the font-size if present.
# E.g. if font-size="150" is used, then 1 em = 150 px.
# em units. Equivalent to the computed font-size in effect for an element.
# ex units. Equivalent to the height of a lower-case letter in the font.
# If the font doesn’t include lower-case letters, or doesn’t include the metadata about the ex-height, then 1ex = 0.5em.

SVG_UNITS = {
    "": 1.0,
    "px": 1.0,
    "in": 96.0,
    "mm": 96.0 / 25.4,
    "cm": 96.0 / 2.54,
    "pt": 96 / 72,  # 1 / 72 in = 96 / 72 px
    "pc": 15.0,
    "em": 1.0,
    "ex": 1.0,
}


def svg_parse_coord(coord, size=0):  # Perhaps the size should always be used.
    """
    Parse a coordinate component from a string.
    Converts the number to a common unit (pixels).
    The size of the surrounding dimension is used in case
    the value is given in percentage.
    """
    value_string, end_index = read_float(coord)
    value = float(value_string)
    unit = coord[end_index:].strip()  # removes extra spaces.
    if unit == "%":
        return float(size) / 100 * value
    else:
        return value * SVG_UNITS[unit]


def read_float(text, start_index=0):
    """
    Reads a float value from a string, starting from start_index.

    Returns the value as a string and the index to the first character after the value.
    """

    n = len(text)

    # Skip leading white spaces and commas.
    while start_index < n and (text[start_index].isspace() or text[start_index] == ","):
        start_index += 1

    if start_index == n:
        return "0", start_index

    text_part = text[start_index:]
    match = re_match_number.match(text_part)

    if match is None:
        raise Exception(
            "Invalid float value near " + text[start_index : start_index + 10]
        )

    value_string = match.group(0)
    end_index = start_index + match.end(0)

    return value_string, end_index
