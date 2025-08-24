import pygame
from typing import Optional, TypedDict
import os
import re

_ImageInfo = TypedDict("_ImageInfo", {"image": pygame.Surface, "original_dimensions": tuple, "dimensions": tuple, "scaled": tuple})
_dict: [str, _ImageInfo] = {}
_failed: [str] = []
_gc = None


def initialize(gc) -> None:
    global _gc
    _gc = gc
    _import_directory("resources/sprites")

    icon = get_image("icon")
    pygame.display.set_icon(icon)


def _import_directory(path: str) -> None:
    # get absolute filepath of target directory
    p = os.path.join("", path)
    # for all files found in the directory, try to import them
    sub = path[len("resources/sprites")+1:]
    if sub:
        sub += "/"
    for file in [f for f in os.listdir(p) if "." in f]:
        get_image(sub+file[:-4], extension=file[-4:], handle_error=False)

    # recursively import all *.py files found in subdirectories too
    for folder in [f[0] for f in os.walk(path)]:
        if '__pycache__' in folder or folder == path:
            continue
        _import_directory(re.sub("\\\\", "/", folder))


def get_image(filename: str, resize: (int, int) = None, scale: (float, float) = None,
              directory: str = "sprites", extension: str = ".png", handle_error: bool = True, save: bool = True) -> Optional[pygame.Surface]:
    if scale is not None:
        # noinspection PyUnresolvedReferences
        scale = (scale[0] * _gc.Window.scale()[0], scale[1] * _gc.Window.scale()[1])

    if filename in _dict:
        if resize is not None:
            _dict[filename]["image"] = pygame.transform.scale(_dict[filename]["image"], resize)
            _dict[filename]["dimensions"] = resize
            _dict[filename]["scaled"] = (1, 1)
        if scale is not None and scale != _dict[filename]["scaled"]:
            if scale[0] != 0 and scale[1] != 0:
                size = _dict[filename]["dimensions"]
                scaling = (scale[0] / _dict[filename]["scaled"][0], scale[1] / _dict[filename]["scaled"][1])
                resized = (size[0] * scaling[0], size[1] * scaling[1])

                _dict[filename]["image"] = pygame.transform.scale(_dict[filename]["image"], resized)
                _dict[filename]["dimensions"] = resized
                _dict[filename]["scaled"] = scale
        return _dict[filename]["image"]
    if filename in _failed:
        return None
    try:
        image = pygame.image.load("resources/"+directory+"/"+filename+extension)
        resized = None
        scaled = (1, 1)
        if resize is not None:
            image = pygame.transform.scale(image, resize)
            resized = resize
        if scale is not None:
            if scale[0] != 0 and scale[1] != 0:
                size = image.get_size()
                image = pygame.transform.scale(image, (size[0] * scale[0], size[1] * size[1]))
                scaled = scale
        if save:
            _dict[filename] = _get_image_info(image, resized, scaled)
        return image
    except FileNotFoundError as e:
        if handle_error:
            print("\033[0;31;2m" + e.__str__() + "\033[0;2;2m")
            _failed.append(filename)
        return None


def get_name(sprite: pygame.Surface) -> Optional[str]:
    global _dict
    try:
        return next(key for key, value in _dict.items() if value["image"] == sprite)
    except StopIteration:
        return None


def _get_image_info(sprite: pygame.Surface, dimensions: (int, int) = None, scaled: tuple = (1, 1)) -> _ImageInfo:
    if dimensions is None:
        dimensions = sprite.get_size()
    return {
        "image": sprite,
        "original_dimensions": sprite.get_size(),
        "dimensions": dimensions,
        "scaled": scaled
    }
