import pygame

_running = True


def initialize() -> None:
    pass


def update() -> None:
    global _running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_game()


def close_game() -> None:
    global _running
    _running = False


def get_game_state() -> bool:
    global _running
    return _running
