import pygame

from Engine.AnimationManager import Animation
from Engine import GameContainer, Vectors as v
from Engine.GameObject import GameObject


class FadingAnimation(GameObject):
    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), animation: Animation = None, time: float = 1):
        super().__init__(gc, pos, v.Vector(-1, -1))
        self.time = time
        self.starting_time = time
        self.animation = animation
        self.current_frame = self.animation.current_frame
        self.current_variant = animation.get_current_variant() + animation.variant_offset * animation.variants
        self.alpha = 255

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        self.time -= dt
        self.alpha = v.map_value(self.time, 0, self.starting_time, 0, 255)
        if self.time <= 0:
            gc.current_scene.instance_destroy(self)

    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        self.animation.draw_frame(screen, self.pos, self.current_frame, self.current_variant, self.alpha)

    def save(self) -> [str]:
        return None

    def load(self, gc: GameContainer, args: [str]) -> None:
        pass
