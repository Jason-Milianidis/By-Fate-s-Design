import pygame
from typing import Optional
from os import walk
import numpy as np

clear_color: tuple = (50, 50, 50)
_backgrounds: [str, np.ndarray] = {}
_background: Optional[np.ndarray] = None
_current_background: Optional[str] = None
_gc = None


def initialize(gc) -> None:
    global _backgrounds, _background, _gc

    _gc = gc
    img = gc.ImageManager
    scale = gc.Window.game_size

    # noinspection PyTypeChecker
    for bg in next(walk("resources/backgrounds"), (None, None, []))[2]:
        image = img.get_image(bg[:-4], resize=scale, directory="backgrounds", extension=bg[-4:], save=False)
        _backgrounds[bg[:-4]] = np.zeros((scale[0], scale[1], 3), dtype=np.int16)
        pygame.pixelcopy.surface_to_array(_backgrounds[bg[:-4]], image)
        # _backgrounds[bg[:-4]] = image
        if _background is None:
            _background = _backgrounds[bg[:-4]]


# noinspection PyUnresolvedReferences
def render() -> None:
    _clear()
    _gc.current_scene.render()
    transform = pygame.transform.scale(_gc.Window.screen, _gc.Window.window_size)
    _gc.Window.display_window.blit(transform, (0, 0))
    pygame.display.flip()


# noinspection PyUnresolvedReferences
def _clear() -> None:
    global _background
    if _background is None:
        _gc.Window.screen.fill(clear_color)
    else:
        # _gc.Window.screen.blit(_background, (0, 0), ((0, 0), _gc.Window.game_size))
        pygame.pixelcopy.array_to_surface(_gc.Window.screen, _background)


def set_background(bg: str) -> None:
    global _backgrounds, _background, _current_background
    if bg in _backgrounds:
        _background = _backgrounds[bg]
        _current_background = bg
    else:
        _background = _current_background = None


def get_current_background() -> Optional[str]:
    return _current_background
