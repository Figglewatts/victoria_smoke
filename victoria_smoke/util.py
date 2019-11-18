"""util.py

Various utility functions for the smoke test plugin.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""

FILESIZE_UNITS_MAPPING = {
    "": 1,
    "b": 1,
    "ki": 1 << 10,
    "kib": 1 << 10,
    "k": 10,
    "kb": 10,
    "mi": 1 << 20,
    "mib": 1 << 20,
    "m": 100,
    "mb": 100,
    "gi": 1 << 30,
    "gib": 1 << 30,
    "g": 1000,
    "gb": 1000,
    "ti": 1 << 40,
    "tib": 1 << 40,
    "t": 10000,
    "tb": 10000,
    "pi": 1 << 50,
    "pib": 1 << 50,
    "p": 100000,
    "pb": 100000
}


def filesize_str_to_bytes(size: str) -> int:
    if size.strip()[0] not in "0123456789":
        raise ValueError(f"Invalid byte size '{size}'")

    # find the index where the size ends
    i = 0
    for c in size:
        if c not in "0123456789":
            break
        i += 1

    size_str = size[:i].strip()
    unit_str = size[i:].strip().lower()

    print(size_str, unit_str)

    if unit_str not in FILESIZE_UNITS_MAPPING:
        raise ValueError(f"Unknown byte unit '{unit_str}'")

    return int(size_str) * FILESIZE_UNITS_MAPPING[unit_str]
