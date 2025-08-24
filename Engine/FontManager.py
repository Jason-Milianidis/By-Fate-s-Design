from __future__ import annotations
import pygame
import pygame.freetype
from os import walk
from os.path import exists
from enum import Enum

_gc = None
_dict: [str, pygame.freetype.Font] = {}
_loaded_font: pygame.freetype.Font
_directory: str = "resources/fonts/"
_extension: str = ".ttf"
_offset: (float, float) = (0, 0)


def initialize(gc) -> None:
    global _gc
    _gc = gc
    # noinspection PyTypeChecker
    for font in next(walk("resources/fonts"), (None, None, []))[2]:
        load_font(font[:-4])
    load_font('Arial')


def load_font(font: str) -> None:
    global _dict, _loaded_font

    # use the loaded font if it exists
    if font in _dict:
        _loaded_font = _dict[font]
        return

    # try and import a custom font from resources
    if exists(_directory+font+_extension):
        _loaded_font = pygame.freetype.Font(_directory+font+_extension, 24)
        _dict[font] = _loaded_font
        return

    # try and import the font from system
    _loaded_font = pygame.freetype.SysFont(font, 30)
    _dict[font] = _loaded_font


def draw_string(screen: pygame.Surface, text: str, pos: tuple = (0, 0),
                color: tuple = (255, 255, 255), background_color: tuple = (0, 0, 0, 0)) -> None:
    global _loaded_font, _offset
    dims = get_text_dims(text, False)
    off = (dims[0] * _offset[0], dims[1] * _offset[1])
    starting_position = (pos[0] - off[0], pos[1] - off[1])
    lines = text.split('\n')
    for i in range(0, len(lines)):
        final_position = (starting_position[0], starting_position[1] + i * dims[2])
        _loaded_font.render_to(screen, final_position, lines[i], color, background_color)


def get_text_dims(text: str, normalized: bool = True) -> (int, int, int):  # width, height, line height
    if normalized:
        # noinspection PyUnresolvedReferences
        scale = [1/i for i in _gc.Window.scale()]
    else:
        scale = (1, 1)

    lines = text.split('\n')
    longest = max(lines, key=len)
    rect = _loaded_font.get_rect(longest)
    t = (rect.width * scale[0], rect.height * len(lines) * scale[1], rect.height * scale[1])
    return t


def set_alignment(__type: Alignment) -> None:
    global _offset
    _offset = __type.value


class Alignment(Enum):
    TOP_LEFT = (0, 0)
    TOP = (0.5, 0)
    TOP_RIGHT = (1, 0)
    LEFT = (0, 0.5)
    CENTER = (0.5, 0.5)
    RIGHT = (1, 0.5)
    BOTTOM_LEFT = (0, 1)
    BOTTOM = (0.5, 1)
    BOTTOM_RIGHT = (1, 1)
