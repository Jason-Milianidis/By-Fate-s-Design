from __future__ import annotations

import pygame
from Engine import GameContainer as GameContainer
from Game.Utility.Modifiers.Modifier import Modifier
from Game.Utility.Bullets.Bullet import Bullet
from Game.Flare.Particle import Particle
import Engine.Vectors as v


class ExpireMod(Modifier):
    def __init__(self):
        super().__init__()
        self.delay = 1
        self.expire_time = 0
        self.time = 0
        self.time_max = 0.25

    def initialize(self, delay: float = 1) -> ExpireMod:
        self.delay = delay
        return self

    def link(self, bullet: Bullet) -> ExpireMod:
        super().link(bullet)
        return self

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        if self.bullet is None:
            return

        self.time += dt
        if self.time >= self.time_max:
            self.time %= self.time_max
            size = v.map_value(self.expire_time, 0, self.delay, 5, 1)
            gc.current_scene.instance_create(Particle(gc, v.duplicate(self.bullet.pos), v.Vector(size, size), (100, 20, 220)))

        self.expire_time += dt
        if self.expire_time > self.delay:
            gc.current_scene.instance_destroy(self.bullet)

    def render(self, gc: GameContainer, screen: pygame.Surface):
        pass

    def duplicate(self) -> ExpireMod:
        mod = ExpireMod()
        mod.initialize(self.delay)
        return mod
