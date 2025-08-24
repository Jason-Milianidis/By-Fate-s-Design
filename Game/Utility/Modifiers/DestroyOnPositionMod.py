from __future__ import annotations

import random

import pygame
from Engine import GameContainer as GameContainer
from Game.Utility.Modifiers.Modifier import Modifier
from Game.Utility.Bullets.Bullet import Bullet
import Engine.Vectors as v
from Game.Flare.DistanceParticle import DistanceParticle


class DestroyOnPositionMod(Modifier):
    def __init__(self):
        super().__init__()
        self.pos = v.Vector(0, 0)
        self.prev_mag = None

    def initialize(self, pos: v.Vector = v.Vector(0, 0)) -> DestroyOnPositionMod:
        self.pos = pos
        return self

    def link(self, bullet: Bullet) -> DestroyOnPositionMod:
        super().link(bullet)
        return self

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        if self.bullet is None:
            return
        # make particle
        angle = self.bullet.velocity.get_direction()
        random_offset = v.direction(angle + random.randint(-15, 15)).scale(-random.randint(30, 60))
        particle = DistanceParticle(gc, v.duplicate(self.bullet.pos).add(random_offset), v.Vector(2, 2), (150, 0, 255),
                                    v.duplicate(random_offset).normalize(-4), random_offset.magnitude())
        gc.current_scene.instance_create(particle)

        # get next position
        prev_pos = v.duplicate(self.bullet.pos)
        self.bullet.pos.add(v.duplicate(self.bullet.velocity).scale(dt_normalized))
        distance_away = v.point_to(self.bullet.pos, self.pos).magnitude()

        if self.prev_mag is None:
            self.prev_mag = distance_away
            self.bullet.pos = prev_pos
            return

        if self.prev_mag < distance_away:
            gc.current_scene.instance_destroy(self.bullet)
            return

        self.prev_mag = distance_away
        self.bullet.pos = prev_pos

    def render(self, gc: GameContainer, screen: pygame.Surface):
        pass

    def duplicate(self) -> DestroyOnPositionMod:
        mod = DestroyOnPositionMod()
        mod.initialize(self.pos)
        return mod
