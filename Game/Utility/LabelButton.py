import pygame
from Engine import GameContainer
import Engine.Vectors as v
from Engine.FontManager import Alignment
from Game.Utility.Button import Button


class LabelButton(Button):
    label: str
    default_color: tuple = (255, 0, 0)
    highlight_color: tuple = (0, 255, 0)
    border: tuple = (20, 10)

    def __init__(self, gc: GameContainer, label: str, pos: v.Vector = v.Vector(0, 0)):
        super().__init__(gc, pos)
        self.label = label
        rect = gc.Font.get_text_dims(self.label)
        self.hit_box = v.Vector(rect[0] + self.border[0], rect[1] + self.border[1])
        self.color = self.default_color
        self.value = None

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        super().update_logic(gc)
        super().update_highlighted_color(self.default_color, self.highlight_color)

    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        super().render_centered(gc, screen, 0, 5)
        gc.Font.set_alignment(Alignment.CENTER)
        gc.Font.draw_string(screen, self.label, v.to_tuple(self.pos))

    def save(self) -> [str]:
        return [self.label, self.pos.save(), self.hit_box.save()]

    def load(self, gc: GameContainer, args: [str]) -> None:
        self.label = args[1]
        self.pos = v.load_vector(args[2])
        self.hit_box = v.load_vector(args[3])
