from __future__ import annotations
from abc import abstractmethod

import pygame

from Engine import GameContainer, Vectors as v
from Engine.GameObject import GameObject


class Bullet(GameObject):
    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), hit_box: v.Vector = v.Vector(-1, -1)):
        super().__init__(gc, pos, hit_box)
        self.velocity = v.Vector(0, 0)

        from Game.Utility.Modifiers.Modifier import Modifier
        self.modifiers: [Modifier] = []

    def add_modifier(self, mod) -> Bullet:
        self.modifiers.append(mod)
        return self

    def update_mods(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        for mod in self.modifiers:
            mod.update(gc, dt, dt_normalized)

    def on_death(self, gc: GameContainer) -> None:
        for mod in self.modifiers:
            mod.on_death(gc)

    def render_mods(self, gc: GameContainer, screen: pygame.Surface) -> None:
        for mod in self.modifiers:
            mod.render(gc, screen)

    @abstractmethod
    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        pass

    @abstractmethod
    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        pass

    @abstractmethod
    def save(self) -> [str]:
        pass

    @abstractmethod
    def load(self, gc: GameContainer, args: [str]) -> None:
        pass
