from __future__ import annotations
import pygame

from abc import abstractmethod
from Engine import GameContainer, Vectors as v
from Engine.GameObject import GameObject
from Game.Utility.Modifiers.Modifier import Modifier
from Game.Utility.Bullets.Bullet import Bullet


class BulletPattern(GameObject):
    @abstractmethod
    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), time: float = 1):
        super().__init__(gc, pos, v.Vector(-1, -1))
        self.time = time
        self.modifiers: [Modifier] = []

    def add_modifier(self, mod: Modifier) -> BulletPattern:
        self.modifiers.append(mod)
        return self

    def shoot(self, gc: GameContainer, bullet: Bullet) -> None:
        for mod in self.modifiers:
            bullet.add_modifier(mod.duplicate().link(bullet))
        gc.current_scene.instance_create(bullet)

    @abstractmethod
    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        pass

    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        pass

    @abstractmethod
    def save(self) -> [str]:
        return None

    @abstractmethod
    def load(self, gc: GameContainer, args: [str]) -> None:
        pass
