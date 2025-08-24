import pygame
import random

from Engine import GameContainer, Vectors as v
from Engine.GameObject import GameObject


class DistanceParticle(GameObject):
    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), hit_box: v.Vector = v.Vector(0, 0),
                 color: (int, int, int) = (255, 255, 255), momentum: v.Vector = v.Vector(0, 0), distance: float = 10):
        super().__init__(gc, pos, v.Vector(-1, -1))
        self.color = color
        self.alpha = 255
        self.momentum = momentum
        self.starting_pos = v.duplicate(pos)
        self.distance = distance
        self.area = v.to_tuple(v.duplicate(hit_box).scale(2))
        self.dimensions = hit_box
        self.screen = pygame.Surface(self.area, pygame.SRCALPHA)

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        self.pos.add(self.momentum)

        distance = v.point_to(self.pos, self.starting_pos).magnitude()
        self.alpha = v.map_value(distance, 0, self.distance, 255, 0)
        if self.alpha <= 0:
            gc.current_scene.instance_destroy(self)

    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        self.screen.fill((self.color + (self.alpha,)))
        screen.blit(self.screen, v.to_tuple(v.duplicate(self.pos).sub(self.dimensions)))

    def save(self) -> [str]:
        return [
            self.pos.save(),
            self.starting_pos.save(),
            str(self.distance),
            _save_tuple(self.area),
            _save_tuple(self.color)
        ]

    def load(self, gc: GameContainer, args: [str]) -> None:
        self.pos = v.load_vector(args[1])
        self.starting_pos = v.load_vector(args[2])
        self.distance = float(args[3])
        self.area = _load_tuple(args[4])
        self.color = _load_tuple(args[5])
        distance = v.point_to(self.pos, self.starting_pos).magnitude()
        self.alpha = v.map_value(distance, 0, self.distance, 255, 0)


def _save_tuple(t: tuple) -> str:
    return "x".join([str(i) for i in t])


def _load_tuple(arg: str) -> tuple:
    vals = arg.split("x")
    t = tuple([tuple(map(int, val)) for val in vals])
    return t


def create_splatter(gc: GameContainer, obj_from: GameObject, obj_target: GameObject) -> None:
    direction = v.point_to(obj_from.pos, obj_target.pos).normalize(10)
    for i in range(0, 40):
        rand_dir = v.duplicate(direction)\
            .rotate(random.randint(-6, 6))\
            .scale(v.map_value(random.random(), 0, 1, 0.8, 1.2))
        particle = DistanceParticle(gc, v.duplicate(obj_target.pos), v.Vector(1, 1), (0, 0, 0), rand_dir)
        gc.current_scene.instance_create(particle)
