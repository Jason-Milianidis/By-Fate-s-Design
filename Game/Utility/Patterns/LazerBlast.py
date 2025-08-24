import random

from Game.Utility.Patterns.BulletPattern import BulletPattern
from Engine import GameContainer
import Engine.Vectors as v
from Game.Utility.Bullets.BasicBullet import BasicBullet


class LazerBlast(BulletPattern):
    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), direction: v.Vector = v.Vector(0, 0),
                 width: int = 1, time: float = 1):
        super().__init__(gc, pos, time)
        self.direction = direction
        self.width = width

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        self.time -= dt

        starting_pos = v.duplicate(self.pos).add(v.duplicate(self.direction).normalize(self.width).rotate(90))
        adding_v = v.duplicate(self.direction).normalize().rotate(-90)
        for i in range(-self.width, self.width, 8):
            gc.current_scene.instance_create(BasicBullet(gc, v.duplicate(starting_pos), v.duplicate(self.direction)
                                                         .scale(v.map_value(random.random(), 0, 1, 0.95, 1.05))))
            starting_pos.add(adding_v)

        if self.time <= 0:
            gc.current_scene.instance_destroy(self)

    def save(self) -> [str]:
        return [self.pos.save(), self.direction.save(), str(self.width), str(self.time)]

    def load(self, gc: GameContainer, args: [str]) -> None:
        self.pos = v.load_vector(args[1])
        self.direction = v.load_vector(args[2])
        self.width = int(args[3])
        self.time = float(args[4])
