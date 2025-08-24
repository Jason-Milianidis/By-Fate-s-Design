import pygame
import Engine.WindowManager as WindowManager
from Engine.Vectors import map_value

_keys: pygame.key.ScancodeWrapper
_keys_prev: pygame.key.ScancodeWrapper
_buttons: tuple
_buttons_prev: tuple
_window_size: tuple
_display_size: tuple
mouse_pos: tuple = (0, 0)


def initialize(window: WindowManager) -> None:
    global _keys, _buttons, _window_size, _display_size, mouse_pos
    _window_size = window.window_size
    _display_size = window.game_size
    _keys = pygame.key.get_pressed()
    _buttons = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()


def update() -> None:
    global _keys, _buttons, _keys_prev, _buttons_prev, _window_size, mouse_pos
    _keys_prev = _keys
    _buttons_prev = _buttons
    _keys = pygame.key.get_pressed()
    _buttons = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = (map_value(mouse_pos[0], 0, _window_size[0], 0, _display_size[0]),
                 map_value(mouse_pos[1], 0, _window_size[1], 0, _display_size[1]))


def get_input(key: int) -> bool:
    global _keys
    return _keys[key]


def get_input_pressed(key: int) -> bool:
    global _keys, _keys_prev
    return _keys[key] and not _keys_prev[key]


def get_input_released(key: int) -> bool:
    global _keys, _keys_prev
    return not _keys[key] and _keys_prev[key]


def get_button(button: int) -> bool:
    global _buttons
    return _buttons[button]


def get_button_pressed(key: int) -> bool:
    global _buttons, _buttons_prev
    return _buttons[key] and not _buttons_prev[key]


def get_button_released(key: int) -> bool:
    global _buttons, _buttons_prev
    return not _buttons[key] and _buttons_prev[key]
