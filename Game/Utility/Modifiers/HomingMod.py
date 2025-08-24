from __future__ import annotations
import pygame
from Engine import GameContainer as GameContainer
from Game.Utility.Modifiers.Modifier import Modifier
from Game.Utility.Bullets.Bullet import Bullet
import Engine.Vectors as v
from Game.Flare.DistanceParticle import DistanceParticle


class HomingMod(Modifier):
    def __init__(self):
        super().__init__()
        self.strength = 0

    def initialize(self, strength: float = 0) -> HomingMod:
        self.strength = strength
        return self

    def link(self, bullet: Bullet) -> HomingMod:
        super().link(bullet)
        return self

    def update(self, gc: GameContainer, dt: float, dt_normalized: float):
        if self.bullet is None:
            return
        player = gc.current_scene.player
        vector = v.point_to(self.bullet.pos, player.pos)

        direction = vector.get_direction()
        bullet_direction = self.bullet.velocity.get_direction()
        if (bullet_direction - 180 < direction <= bullet_direction) or \
           (bullet_direction + 180 < direction <= bullet_direction + 360):
            direction = -1
        else:
            direction = 1
        self.bullet.velocity.rotate(direction * self.strength)

        particle = DistanceParticle(gc, v.duplicate(self.bullet.pos), v.Vector(1, 1), (150, 0, 255),
                                    v.direction(direction).scale(2), 50)
        gc.current_scene.instance_create(particle)

    def render(self, gc: GameContainer, screen: pygame.Surface):
        pass

    def duplicate(self) -> HomingMod:
        mod = HomingMod()
        mod.initialize(self.strength)
        return mod
