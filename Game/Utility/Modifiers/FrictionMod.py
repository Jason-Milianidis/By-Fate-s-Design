from __future__ import annotations

import pygame
from Engine import GameContainer as GameContainer
from Game.Utility.Modifiers.Modifier import Modifier
from Game.Utility.Bullets.Bullet import Bullet


class FrictionMod(Modifier):
    def __init__(self):
        super().__init__()
        self.friction = 0.05
        self.destroy_threshold = 0.1

    def initialize(self, friction: float = 0.05, destroy_threshold: float = 0.1) -> FrictionMod:
        self.friction = friction
        self.destroy_threshold = destroy_threshold
        return self

    def link(self, bullet: Bullet) -> FrictionMod:
        super().link(bullet)
        return self

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        if self.bullet is None:
            return

        self.bullet.velocity.scale(1 - self.friction)
        if self.bullet.velocity.magnitude() <= self.destroy_threshold:
            gc.current_scene.instance_destroy(self.bullet)

    def render(self, gc: GameContainer, screen: pygame.Surface):
        pass

    def duplicate(self) -> FrictionMod:
        mod = FrictionMod()
        mod.initialize(self.friction, self.destroy_threshold)
        return mod
