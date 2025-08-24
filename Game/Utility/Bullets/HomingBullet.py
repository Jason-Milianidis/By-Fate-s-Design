import pygame
import Engine.GameContainer as GameContainer
from Engine.GameObject import GameObject, overlaps
from Game.Utility.Bullets.Bullet import Bullet
import Engine.Vectors as v


class HomingBullet(Bullet):
    direction: v.Vector = v.Vector(0, 0)
    speed: float = 10

    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), direction: v.Vector = v.Vector(0, 0),
                 rotational_speed: float = 5, target: GameObject = None,
                 minimum_flying_time: float = 1, maximum_flying_time: float = 10):
        super().__init__(gc, pos, v.Vector(2, 2))
        self.direction = direction
        self.display_box = v.Vector(16, 16)
        self.rotational_speed = rotational_speed
        self.target = target
        self.time = 0
        self.minimum_flying_time = minimum_flying_time
        self.maximum_flying_time = maximum_flying_time

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        self.time += dt

        if self.target is not None:
            target_dir = v.point_to(self.pos, self.target.pos).normalize(self.direction.magnitude())
            cross = target_dir.x * self.direction.x + target_dir.y * self.direction.y
            if cross < 0:
                self.direction.rotate(self.rotational_speed)
            else:
                self.direction.rotate(-self.rotational_speed)

            if self.time >= self.minimum_flying_time:
                target_sides = self.target.calculate_object_sides()
                bullet_sides = self.calculate_object_sides()
                if overlaps(target_sides, bullet_sides):
                    gc.current_scene.instance_destroy(self)

        if self.time >= self.maximum_flying_time:
            gc.current_scene.instance_destroy(self)

        self.pos.x += self.direction.x * dt_normalized
        self.pos.y += self.direction.y * dt_normalized

        if gc.current_scene.collides_with_player(self):
            gc.current_scene.instance_destroy(self)
            gc.current_scene.player.damage()

    def render(self, gc: GameContainer, screen: pygame.Surface):
        pygame.draw.circle(screen, "white", v.to_vector2(self.pos), 2)

    def save(self) -> [str]:
        return [self.pos.save(), self.hit_box.save(), self.direction.save()]

    def load(self, gc: GameContainer, args: [str]) -> None:
        self.pos = v.load_vector(args[1])
        self.hit_box = v.load_vector(args[2])
        self.direction = v.load_vector(args[3])
