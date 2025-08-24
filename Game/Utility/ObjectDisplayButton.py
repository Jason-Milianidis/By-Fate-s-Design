import pygame

import Engine.LevelManager
from Engine import GameContainer
from Engine.GameObject import GameObject
from Game.Utility.Button import Button
import Engine.Vectors as v
from typing import Optional


class ObjectDisplayButton(Button):
    default_color: tuple = (255, 0, 0)
    highlight_color: tuple = (0, 255, 0)
    border: tuple = (20, 20)
    display: Optional[GameObject]
    _camera: pygame.Surface
    _drawing_offset: v.Vector

    def __init__(self, gc: GameContainer, __object: GameObject = None,
                 pos: v.Vector = v.Vector(0, 0), display_size: v.Vector = v.Vector(32, 32)):
        super().__init__(gc, pos, display_size)
        self.display = __object
        if __object is None:
            self.value = None
            return
        self.value = __object.__class__.__name__
        self._drawing_offset = v.duplicate(__object.display_box).scale(0.5)
        self._camera = pygame.Surface(v.to_tuple(__object.display_box))

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        super().update_logic(gc)
        super().update_highlighted_color(self.default_color, self.highlight_color)
        if self.display is not None:
            if hasattr(self.display, 'animation'):
                self.display.animation.update(dt)
            self.display.pos = self.pos

    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        if self.display is not None:
            self.display.pos = self._drawing_offset
            self._camera.fill((0, 0, 0))
            self.display.render(gc, self._camera)
            drawing_screen = pygame.transform.scale(self._camera, v.to_tuple(self.hit_box))
            screen.blit(drawing_screen, (self.pos.x - self.hit_box.x / 2, self.pos.y - self.hit_box.y / 2))
            self.display.pos = self.pos
        super().render_centered(gc, screen, 1, 5)
        if self.is_highlighted:
            gc.Font.set_alignment(gc.Font.Alignment.LEFT)
            gc.Font.draw_string(screen, self.value, (self.pos.x + self.hit_box.x, self.pos.y))

    def save(self) -> [str]:
        if self.display is None:
            return ["None", self.pos.save(), self.hit_box.save()]
        return [Engine.LevelManager.get_saved_string(self.display, ';'), self.pos.save(), self.hit_box.save()]

    def load(self, gc: GameContainer, args: [str]) -> None:
        if args[1] == "None":
            self.display = None
        else:
            self.display = Engine.LevelManager.load_object(args[1], ';')
        self.pos = v.load_vector(args[2])
        self.hit_box = v.load_vector(args[3])
