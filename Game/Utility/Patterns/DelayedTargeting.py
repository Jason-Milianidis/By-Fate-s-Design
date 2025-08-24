import random

from Game.Utility.Patterns.BulletPattern import BulletPattern
from Engine import GameContainer
import Engine.Vectors as v
from Game.Utility.Bullets.BasicBullet import BasicBullet


class DelayedTargeting(BulletPattern):
    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), speed: float = 1,
                 bullets: int = 1, time: float = 1, spread: float = 0):
        super().__init__(gc, pos, 0)
        self.speed = speed
        self.bullets = bullets
        self.spread = spread
        if bullets == 0:
            self.interval = time
            return
        self.interval = time / self.bullets

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        self.time += dt
        while self.time >= self.interval:
            self.time -= self.interval
            spread = (random.random() - 0.5) * 2 * self.spread
            direction = v.point_to(self.pos, gc.current_scene.player.pos).normalize(self.speed).rotate(spread)
            self.shoot(gc, BasicBullet(gc, v.duplicate(self.pos), direction))
            self.bullets -= 1
            if self.bullets == 0:
                gc.current_scene.instance_destroy(self)
                return

    def save(self) -> [str]:
        return [self.pos.save(), str(self.speed), str(self.bullets), str(self.spread), str(self.interval), str(self.time)]

    def load(self, gc: GameContainer, args: [str]) -> None:
        self.pos = v.load_vector(args[1])
        self.speed = float(args[2])
        self.bullets = int(args[3])
        self.spread = float(args[4])
        self.interval = float(args[5])
        self.time = float(args[6])
