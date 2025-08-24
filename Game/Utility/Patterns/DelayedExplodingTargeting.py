from Game.Utility.Patterns.BulletPattern import BulletPattern
from Engine import GameContainer
import Engine.Vectors as v
from Game.Utility.Bullets.BasicBullet import BasicBullet
from Game.Utility.Modifiers.SplitMod import SplitMod
from Game.Utility.Modifiers.ExplodingMod import ExplodingMod


class DelayedExplodingTargeting(BulletPattern):
    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), speed: float = 1,
                 bullets: int = 1, time: float = 1):
        super().__init__(gc, pos, 0)
        self.speed = speed
        self.bullets = bullets
        if bullets == 0:
            self.interval = time
            return
        self.interval = time / self.bullets

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        self.time += dt
        while self.time >= self.interval:
            self.time -= self.interval

            to_player = v.point_to(self.pos, gc.current_scene.player.pos)
            time_to_explode = to_player.magnitude() / self.speed / gc.Window.space_normalization_value
            bullet = BasicBullet(gc, v.duplicate(self.pos), to_player.normalize(self.speed))
            bullet.add_modifier(SplitMod().initialize(0, time_to_explode, 360).link(bullet))
            bullet.add_modifier(ExplodingMod().initialize(4, 0.1, speed=2).link(bullet))
            self.shoot(gc, bullet)

            self.bullets -= 1
            if self.bullets == 0:
                gc.current_scene.instance_destroy(self)
                return

    def save(self) -> [str]:
        return [self.pos.save(), str(self.speed), str(self.bullets), str(self.interval), str(self.time)]

    def load(self, gc: GameContainer, args: [str]) -> None:
        self.pos = v.load_vector(args[1])
        self.speed = float(args[2])
        self.bullets = int(args[3])
        self.interval = float(args[4])
        self.time = float(args[5])
