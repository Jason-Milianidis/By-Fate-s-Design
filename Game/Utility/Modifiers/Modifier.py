from __future__ import annotations
from abc import abstractmethod

import pygame

import Engine.GameContainer as GameContainer
from Game.Utility.Bullets.Bullet import Bullet
import Engine.Vectors as v


class Modifier:
    def __init__(self):
        self.bullet = None
        self.pos = v.Vector(0, 0)

    @abstractmethod
    def initialize(self) -> Modifier:
        return self

    @abstractmethod
    def link(self, bullet: Bullet) -> Modifier:
        self.bullet = bullet
        return self

    @abstractmethod
    def update(self, gc: GameContainer, dt: float, dt_normalized: float):
        pass

    @abstractmethod
    def render(self, gc: GameContainer, screen: pygame.Surface):
        pass

    @abstractmethod
    def duplicate(self) -> Modifier:
        pass

    def on_death(self, gc: GameContainer) -> None:
        pass


"""
    GRAVITY,
    BOUNCE,
    SPLIT,
    REWIND,
    EXPLODING
"""