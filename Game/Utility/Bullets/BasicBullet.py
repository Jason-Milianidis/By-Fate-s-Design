import pygame
import Engine.GameContainer as GameContainer
import Engine.Vectors as v
from Game.Utility.Bullets.Bullet import Bullet


class BasicBullet(Bullet):
    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), velocity: v.Vector = v.Vector(0, 0)):
        super().__init__(gc, pos, v.Vector(2, 2))
        self.velocity = velocity
        self.display_box = v.Vector(16, 16)
        self.speed = 10
        self.destroy_on_collision = True

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        self.destroy_on_collision = True
        super().update_mods(gc, dt, dt_normalized)
        super().move_in_bounds(gc, v.duplicate(self.velocity).scale(dt_normalized), self.destroy_on_collision)
        if gc.current_scene.collides_with_player(self):
            gc.current_scene.instance_destroy(self)
            gc.current_scene.player.damage()

    def render(self, gc: GameContainer, screen: pygame.Surface):
        pygame.draw.circle(screen, "white", v.to_vector2(self.pos), 2)
        super().render_mods(gc, screen)

    def save(self) -> [str]:
        return [self.pos.save(), self.hit_box.save(), self.velocity.save()]

    def load(self, gc: GameContainer, args: [str]) -> None:
        self.pos = v.load_vector(args[1])
        self.hit_box = v.load_vector(args[2])
        self.velocity = v.load_vector(args[3])
