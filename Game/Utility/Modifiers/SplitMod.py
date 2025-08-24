from __future__ import annotations

import pygame
from Engine import GameContainer as GameContainer
from Game.Utility.Modifiers.Modifier import Modifier
from Game.Utility.Bullets.Bullet import Bullet
from Game.Utility.Bullets.BasicBullet import BasicBullet
from Game.Flare.Particle import Particle
import Engine.Vectors as v


class SplitMod(Modifier):
    def __init__(self):
        super().__init__()
        self.bullets = 2
        self.delay = 1
        self.spread = 60

    def initialize(self, bullets: int = 2, delay: float = 1, spread: int = 60) -> SplitMod:
        self.bullets = bullets
        self.delay = delay
        self.spread = spread
        return self

    def link(self, bullet: Bullet) -> SplitMod:
        super().link(bullet)
        return self

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        if self.bullet is None:
            return

        gc.current_scene.instance_create(Particle(gc, v.duplicate(self.bullet.pos), v.Vector(1, 1), (210, 100, 30)))

        self.delay -= dt
        if self.delay <= 0:
            self.bullet.modifiers.remove(self)
            gc.current_scene.instance_destroy(self.bullet)

            if self.bullets <= 0:
                return

            if self.bullets == 1:
                offset = self.spread / 2
                spacing = self.spread
            else:
                offset = 0
                spacing = self.spread / (self.bullets - 1)

            angle = self.bullet.velocity.get_direction()
            magnitude = self.bullet.velocity.magnitude()
            for i in range(int(-self.spread / 2 + offset), int(self.spread / 2) + 1, int(spacing)):
                velocity = v.direction(angle + i).scale(magnitude)
                bullet = BasicBullet(gc, v.duplicate(self.bullet.pos), velocity)
                for mod in self.bullet.modifiers:
                    bullet.add_modifier(mod.duplicate().link(bullet))
                gc.current_scene.instance_create(bullet)

    def render(self, gc: GameContainer, screen: pygame.Surface):
        pass

    def duplicate(self) -> SplitMod:
        mod = SplitMod()
        mod.initialize(self.bullets, self.delay, self.spread)
        return mod
