from __future__ import annotations

import random

import pygame
from Engine import GameContainer as GameContainer
from Game.Utility.Modifiers.Modifier import Modifier
from Game.Utility.Bullets.Bullet import Bullet
import Engine.Vectors as v
from Game.Flare.DistanceParticle import DistanceParticle
from Game.Utility.Modifiers.DestroyOnPositionMod import DestroyOnPositionMod
from Engine.GameObject import overlaps


class RewindMod(Modifier):
    def __init__(self):
        super().__init__()
        self.starting_pos = v.Vector(0, 0)

    def initialize(self) -> RewindMod:
        return self

    def link(self, bullet: Bullet) -> RewindMod:
        super().link(bullet)
        self.starting_pos = v.duplicate(bullet.pos)
        return self

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        if self.bullet is None:
            return
        # make particle
        angle = self.bullet.velocity.get_direction()
        random_offset = v.direction(angle + random.randint(-15, 15)).scale(random.randint(30, 60))
        particle = DistanceParticle(gc, v.duplicate(self.bullet.pos).add(random_offset), v.Vector(2, 2), (150, 0, 255),
                                    v.duplicate(random_offset).normalize(-4), random_offset.magnitude())
        gc.current_scene.instance_create(particle)

        # get next position
        prev_pos = v.duplicate(self.bullet.pos)
        self.bullet.pos.add(v.duplicate(self.bullet.velocity).scale(dt_normalized))

        # check out-of-window bounds
        if self.bullet.pos.x < 0 or self.bullet.pos.x > gc.Window.game_size[0] or \
           self.bullet.pos.y < 0 or self.bullet.pos.y > gc.Window.game_size[1]:
            self.bullet.velocity.scale(-1)
            self.bullet.destroy_on_collision = False
            self.bullet.pos = prev_pos
            self.bullet.modifiers.remove(self)
            self.bullet.add_modifier(DestroyOnPositionMod().initialize(self.starting_pos).link(self.bullet))
            return

        # check wall collisions
        sides = self.bullet.calculate_object_sides()
        for wall in [o for o in gc.current_scene.objects if o.collision]:
            wall_sides = wall.calculate_object_sides()
            if overlaps(sides, wall_sides):
                self.bullet.velocity.scale(-1)
                self.bullet.destroy_on_collision = False
                self.bullet.pos = prev_pos
                self.bullet.modifiers.remove(self)
                self.bullet.add_modifier(DestroyOnPositionMod().initialize(self.starting_pos).link(self.bullet))
                return

        self.bullet.pos = prev_pos

    def render(self, gc: GameContainer, screen: pygame.Surface):
        pass

    def duplicate(self) -> RewindMod:
        mod = RewindMod()
        return mod
