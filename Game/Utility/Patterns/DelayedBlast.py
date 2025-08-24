from Game.Utility.Patterns.BulletPattern import BulletPattern
from Engine import GameContainer
import Engine.Vectors as v
from Game.Utility.Bullets.BasicBullet import BasicBullet


class DelayedBlast(BulletPattern):
    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), direction: v.Vector = v.Vector(0, 0),
                 bullets: int = 1, time: float = 1):
        super().__init__(gc, pos, 0)
        self.direction = direction
        self.bullets = bullets
        if bullets == 0:
            self.interval = time
            return
        self.interval = time / self.bullets

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        self.time += dt
        if self.time >= self.interval:
            self.time %= self.interval
            self.shoot(gc, BasicBullet(gc, v.duplicate(self.pos), v.duplicate(self.direction)))
            self.bullets -= 1
            if self.bullets == 0:
                gc.current_scene.instance_destroy(self)

    def save(self) -> [str]:
        return [self.pos.save(), self.direction.save(), str(self.bullets), str(self.interval), str(self.time)]

    def load(self, gc: GameContainer, args: [str]) -> None:
        self.pos = v.load_vector(args[1])
        self.direction = v.load_vector(args[2])
        self.bullets = int(args[3])
        self.interval = float(args[4])
        self.time = float(args[5])
