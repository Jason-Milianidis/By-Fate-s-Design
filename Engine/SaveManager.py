import Engine.GameContainer as GameContainer
from typing import Optional
import re

_directory: str = "resources/saves/"
_extension: str = ".sav"
_delimiter: str = ", "
_file: str = "save"
_metadata: [str, object] = {}
_gc: GameContainer = None


def initialize(gc: GameContainer) -> None:
    global _gc
    _gc = gc
    set_default_values()


def save(filename: str = _file) -> None:
    file = open(_directory+filename+_extension, "w")

    for atr in _metadata:
        file.write(_delimiter.join([
            atr,
            re.sub(".*\'(.*)\'.*", "\\1", str(type(_metadata[atr]))),
            str(_metadata[atr])
        ])+"\n")

    file.close()


def load(filename: str = _file):
    try:
        file = open(_directory+filename+_extension, "r")
    except FileNotFoundError:
        print("\033[0;31;2mSave '" + _directory + filename + _extension + "' not found. Default save loaded.\033[0;2;2m")
        set_default_values()
        return

    for args in file:
        vals = args.split(_delimiter)
        match vals[1]:
            case "int":
                _metadata[vals[0]] = int(vals[2])
            case "float":
                _metadata[vals[0]] = float(vals[2])
            case _:
                _metadata[vals[0]] = vals[2][:-1]

    file.close()


def get_metadata() -> [str, object]:
    global _metadata
    return _metadata.copy()


def get_attribute(key: str) -> Optional[any]:
    if key in _metadata:
        return _metadata[key]
    return None


def set_attribute(key: str, value: any) -> None:
    global _metadata
    _metadata[key] = value


def set_default_values() -> None:
    global _metadata
    _metadata = {
        "attack": 1,
        "gold": 0,
        "health": 3,
        "special": "None",

        "last scene": "MainScene",
        "last background": "0",

        "card number": 2,
        "min card number": 0,
        "temp card number": -1,
    }
