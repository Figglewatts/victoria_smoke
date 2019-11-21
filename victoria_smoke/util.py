"""util.py

Various utility functions for the smoke test plugin.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""

FILESIZE_UNITS_MAPPING = {
    "": 1000**0,
    "b": 1000**0,
    "ki": 1 << 10,
    "kib": 1 << 10,
    "k": 1000**1,
    "kb": 1000**1,
    "mi": 1 << 20,
    "mib": 1 << 20,
    "m": 1000**2,
    "mb": 1000**2,
    "gi": 1 << 30,
    "gib": 1 << 30,
    "g": 1000**3,
    "gb": 1000**3,
    "ti": 1 << 40,
    "tib": 1 << 40,
    "t": 1000**4,
    "tb": 10000**4,
    "pi": 1 << 50,
    "pib": 1 << 50,
    "p": 1000**5,
    "pb": 1000**5
}
"""Mapping of filesize suffixes to scaling factors (power terms)."""


def filesize_str_to_bytes(size: str) -> int:
    """Convert a filesize as a string into the number of bytes.
    I.e. '5kb' -> 5000, or '1kib' -> 1024.

    Args:
        size (str): The filesize to convert. Case-insensitive. 
            Support suffixes of form 'k', 'kb', 'ki', 'kib'. You can even not
            supply a suffix for raw byte values.
    
    Returns:
        int: The converted number of bytes represented by the str.
    """
    if size.strip()[0] not in "0123456789.":
        raise ValueError(f"Invalid byte size '{size}'")

    # find the index where the size ends
    i = 0
    for c in size:
        if c not in "0123456789.":
            break
        i += 1

    # split the string into its significand and unit suffix
    size_str = size[:i].strip()
    unit_str = size[i:].strip().lower()  # make sure it's case-insensitive

    if unit_str not in FILESIZE_UNITS_MAPPING:
        raise ValueError(f"Unknown byte unit '{unit_str}'")

    # return the significand multiplied by it's looked-up power term
    return float(size_str) * FILESIZE_UNITS_MAPPING[unit_str]
