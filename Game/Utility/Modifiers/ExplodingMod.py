from __future__ import annotations

import random

import pygame
from Engine import GameContainer as GameContainer
from Game.Utility.Modifiers.Modifier import Modifier
from Game.Utility.Bullets.Bullet import Bullet
from Game.Utility.Bullets.BasicBullet import BasicBullet
from Game.Flare.Particle import Particle
import Engine.Vectors as v
from Game.Utility.Modifiers.FrictionMod import FrictionMod


class ExplodingMod(Modifier):
    def __init__(self):
        super().__init__()
        self.bullets = 8
        self.friction = None
        self.destroy_threshold = 0.5
        self.speed = None

    def initialize(self, bullets: int = 8, friction: float = None, destroy_threshold: float = 0.5, speed: float = None) -> ExplodingMod:
        self.bullets = bullets
        self.friction = friction
        self.destroy_threshold = destroy_threshold
        self.speed = speed
        return self

    def link(self, bullet: Bullet) -> ExplodingMod:
        super().link(bullet)
        return self

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        pass

    def on_death(self, gc: GameContainer) -> None:
        spacing = 360 / self.bullets
        offset = random.random() * spacing

        if self.friction is None and self.destroy_threshold is None:
            friction = FrictionMod()
        elif self.friction is None:
            friction = FrictionMod().initialize(destroy_threshold=self.destroy_threshold)
        elif self.destroy_threshold is None:
            # noinspection PyTypeChecker
            friction = FrictionMod().initialize(self.friction)
        else:
            friction = FrictionMod().initialize(self.friction, self.destroy_threshold)

        if self.speed is None:
            self.speed = self.bullet.velocity.magnitude() / 2

        for i in range(0, 360, int(spacing)):
            direction = v.direction(i).rotate(offset).scale(self.speed)
            bullet = BasicBullet(gc, v.duplicate(self.bullet.pos), direction)
            bullet.add_modifier(friction.duplicate().link(bullet))
            gc.current_scene.instance_create(bullet)

        for i in range(0, 360, 10):
            direction = v.direction(i).rotate(random.randint(-5, 5)).\
                scale(self.speed * v.map_value(random.random(), 0, 1, 1.5, 2))
            gc.current_scene.instance_create(
                Particle(gc, v.duplicate(self.bullet.pos), v.Vector(1, 1), momentum=direction, friction=0.03, time=0.5)
            )

    def render(self, gc: GameContainer, screen: pygame.Surface):
        pass

    def duplicate(self) -> ExplodingMod:
        mod = ExplodingMod()
        mod.initialize(self.bullets)
        return mod
