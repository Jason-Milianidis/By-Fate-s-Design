import pygame
from abc import abstractmethod
from Engine import GameContainer
from Engine.GameObject import GameObject
import Engine.Vectors as v
from typing import Optional


class Button(GameObject):

    @abstractmethod
    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0),
                 dimensions: v.Vector = v.Vector(20, 20)):
        super().__init__(gc, pos, dimensions)
        self.is_highlighted: bool = False
        self.is_pressed: bool = False
        self.is_right_clicked: bool = False
        self.value: Optional = None
        self.color: tuple = (255, 255, 255)

    def update_logic(self, gc: GameContainer) -> None:
        mouse = gc.Input.mouse_pos
        self.is_highlighted = \
            self.pos.x - self.hit_box.x / 2 <= mouse[0] <= self.pos.x + self.hit_box.x / 2 and \
            self.pos.y - self.hit_box.y / 2 <= mouse[1] <= self.pos.y + self.hit_box.y / 2

        self.is_pressed = self.is_highlighted and gc.Input.get_button_pressed(0)
        self.is_right_clicked = self.is_highlighted and gc.Input.get_button_pressed(2)

    def get_value(self):
        if self.is_pressed:
            return self.value
        return None

    def update_highlighted_color(self, default_color: tuple = (255, 255, 255), highlighted_color: tuple = (0, 255, 0)) -> None:
        if self.is_highlighted:
            self.color = highlighted_color
        else:
            self.color = default_color

    # noinspection PyUnusedLocal
    def render_centered(self, gc: GameContainer, screen: pygame.Surface, width: int = 0, border_radius: int = -1) -> None:
        pygame.draw.rect(
            screen,
            self.color,
            rect=(self.pos.x - self.hit_box.x / 2, self.pos.y - self.hit_box.y / 2, self.hit_box.x, self.hit_box.y),
            width=width,
            border_radius=border_radius
        )

    @abstractmethod
    def save(self) -> [str]:
        return [self.pos.save(), self.hit_box.save()]

    @abstractmethod
    def load(self, gc: GameContainer, args: [str]) -> None:
        self.pos = v.load_vector(args[1])
        self.hit_box = v.load_vector(args[2])
