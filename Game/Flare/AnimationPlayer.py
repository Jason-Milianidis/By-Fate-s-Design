import pygame

from Engine import GameContainer, Vectors as v
from Engine.GameObject import GameObject
from Engine.AnimationManager import Animation


class AnimationPlayer(GameObject):
    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), hit_box: v.Vector = v.Vector(-1, -1),
                 animation: Animation = None, destroy_on_end: bool = True):
        super().__init__(gc, pos, hit_box)
        self.animation = animation
        self.destroy_on_end = destroy_on_end

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        if self.animation is not None:
            self.animation.update(dt)
            if self.animation.animation_ended() and self.destroy_on_end:
                gc.current_scene.instance_destroy(self)

    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        self.animation.draw_frame(screen, self.pos)

    def save(self) -> [str]:
        return [self.pos.save(),
                self.hit_box.save(),
                str(self.destroy_on_end),
                self.animation.save()]

    def load(self, gc: GameContainer, args: [str]) -> None:
        self.pos = v.load_vector(args[1])
        self.hit_box = v.load_vector(args[2])
        self.destroy_on_end = bool(args[3])
        self.animation = gc.AnimationManager.load(args[4])
