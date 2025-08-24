import pygame
import os
from screeninfo import get_monitors
from enum import Enum
from Engine.Vectors import map_value

window_size: tuple = (get_monitors()[0].width, get_monitors()[0].height)
game_size: tuple = (1920, 1080)  # (720, 480)  # (1280, 720)  # (1920, 1080)
_scale = (game_size[0] / 1920, game_size[1] / 1080)
match game_size[0]:
    case 720: _horizontal_collision_fix = 0
    case 1280: _horizontal_collision_fix = 8
    case 1920: _horizontal_collision_fix = 8
    case _: _horizontal_collision_fix = map_value(game_size[0], 720, 1280, 0, 8)
window_title: str = "By Fate's Design"
screen: pygame.Surface
display_window: pygame.Surface
clock: pygame.time.Clock
dt: float = 0
dt_normalized: float = 0
space_normalization_value = game_size[0] / 10
target_fps: int = 30
_gc = None

_fps = 0
_t = 0


def initialize(gc) -> None:
    global screen, display_window, clock, _gc
    _gc = gc
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen = pygame.Surface(game_size)
    display_window = pygame.display.set_mode(window_size, pygame.NOFRAME)
    pygame.display.set_caption(window_title)
    clock = pygame.time.Clock()


def set_title(title) -> None:
    global window_title
    window_title = title
    pygame.display.set_caption(title)


def resize(size) -> None:
    global window_size, screen
    window_size = size
    screen = pygame.display.set_mode(size)


def tick() -> None:
    global dt, dt_normalized
    dt = clock.tick(target_fps) / 1000
    dt_normalized = dt * space_normalization_value


def get_dimensions() -> tuple:
    return window_size


def scale() -> (float, float):
    return _scale


def collision_fix() -> float:
    return _horizontal_collision_fix


# noinspection PyUnresolvedReferences
def update_fps_counter() -> None:
    global _t, _fps
    _t += _gc.Window.dt
    _fps += 1
    if _t >= 1:
        _t %= 1
        if _fps < _gc.Window.target_fps * 0.92:
            print("\033[0;2;41m " + str(_fps) + " \033[0;0;2m")
        else:
            print("\033[0;2;42m " + str(_fps) + " \033[0;0;2m")
        _fps = 0


class Resolutions(Enum):
    STANDARD_480 = (720, 480)
    STANDARD_720 = (1280, 720)
    HD_1080 = (1920, 1080)
    HD_4K = (3840, 2160)
