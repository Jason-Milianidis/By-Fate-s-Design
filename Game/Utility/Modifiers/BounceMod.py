from __future__ import annotations

import random

import pygame
from Engine import GameContainer as GameContainer
from Game.Utility.Modifiers.Modifier import Modifier
from Game.Utility.Bullets.Bullet import Bullet
import Engine.Vectors as v
from Game.Flare.Particle import Particle
from Engine.GameObject import overlaps


class BounceMod(Modifier):
    def __init__(self):
        super().__init__()

    def initialize(self) -> BounceMod:
        return self

    def link(self, bullet: Bullet) -> BounceMod:
        super().link(bullet)
        return self

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        if self.bullet is None:
            return
        # make particle
        random_offset = v.Vector(random.randint(-3, 3), random.randint(-3, 3))
        particle = Particle(gc, v.duplicate(self.bullet.pos).add(random_offset), v.Vector(2, 2), (0, 255, 100), time=0.25)
        gc.current_scene.instance_create(particle)

        # get next position
        prev_pos = v.duplicate(self.bullet.pos)
        self.bullet.pos.add(v.duplicate(self.bullet.velocity).scale(dt_normalized))

        # check out-of-window bounds
        if self.bullet.pos.x < 0 or self.bullet.pos.x > gc.Window.game_size[0]:
            self.bullet.velocity.x *= -1
            self.bullet.destroy_on_collision = False
            self.bullet.pos = prev_pos
            self.bullet.modifiers.remove(self)
            return
        elif self.bullet.pos.y < 0 or self.bullet.pos.y > gc.Window.game_size[1]:
            self.bullet.velocity.y *= -1
            self.bullet.destroy_on_collision = False
            self.bullet.pos = prev_pos
            self.bullet.modifiers.remove(self)
            return

        # check wall collisions
        sides = self.bullet.calculate_object_sides()
        for wall in [o for o in gc.current_scene.objects if o.collision]:
            wall_sides = wall.calculate_object_sides()
            if overlaps(sides, wall_sides):
                angle = v.point_to(wall.pos, self.pos).get_direction()
                wall_angle = v.point_to(wall.pos, v.duplicate(wall.pos).add(wall.hit_box)).get_direction()

                # side of overlap determines offset applied
                if angle > 180 - wall_angle or angle <= -180 + wall_angle or -wall_angle < angle <= wall_angle:  # left - right
                    self.bullet.velocity.x *= -1
                else:  # top - bottom
                    self.bullet.velocity.y *= -1

                self.bullet.destroy_on_collision = False
                self.bullet.pos = prev_pos
                self.bullet.modifiers.remove(self)
                return

        self.bullet.pos = prev_pos

    def render(self, gc: GameContainer, screen: pygame.Surface):
        pass

    def duplicate(self) -> BounceMod:
        mod = BounceMod()
        return mod
