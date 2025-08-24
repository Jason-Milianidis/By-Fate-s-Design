from __future__ import annotations
import pygame
from Engine import GameContainer as GameContainer
from Game.Utility.Modifiers.Modifier import Modifier
from Game.Utility.Bullets.Bullet import Bullet
import Engine.Vectors as v
from Game.Flare.DistanceParticle import DistanceParticle


class GravityMod(Modifier):
    def __init__(self):
        super().__init__()
        self.influence_radius = 0
        self.strength = 0

    def initialize(self, influence_radius: float = 0, strength: float = 0) -> GravityMod:
        self.influence_radius = influence_radius
        self.strength = strength
        return self

    def link(self, bullet: Bullet) -> GravityMod:
        super().link(bullet)
        return self

    def update(self, gc: GameContainer, dt: float, dt_normalized: float):
        if self.bullet is None:
            return
        player = gc.current_scene.player
        vector = v.point_to(self.bullet.pos, player.pos)
        if vector.magnitude() < self.influence_radius:
            self.bullet.velocity.add(vector.normalize(self.strength * dt))

        particle = DistanceParticle(gc, v.duplicate(self.bullet.pos), v.Vector(1, 1), (0, 255, 255), v.direction().scale(4), self.influence_radius)
        gc.current_scene.instance_create(particle)

    def render(self, gc: GameContainer, screen: pygame.Surface):
        if self.bullet is not None:
            pygame.draw.circle(screen, (0, 255, 255), v.to_tuple(self.bullet.pos), self.influence_radius, 1)

    def duplicate(self) -> GravityMod:
        mod = GravityMod()
        mod.initialize(self.influence_radius, self.strength)
        return mod
