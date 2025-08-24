import random

import pygame

from Engine.AnimationManager import Animation
from Engine import GameContainer
from Game.Utility.Draggable import Draggable
from Game.Utility.Button import Button
import Engine.Vectors as v


class Card(Button):
    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0),
                 major: bool = None, card_id: int = None, suit: int = None,
                 go_to_pos: v.Vector = None, time_to_go: float = 1, movable: bool = True
                 ):
        super().__init__(gc, pos, v.Vector(143, 247))
        self.go_to_pos = go_to_pos
        self.time_to_move = time_to_go
        self.moving_offset = v.Vector(0, 0)
        self._calculate_sliding_animation()
        self.is_movable = movable
        self.display_box = v.Vector(825, 1425)

        self.major = major
        self.suit = suit
        self.value = card_id
        if self.major:
            self.hit_box.scale(1.5)

        self.openable = True
        self.closable = True
        self.visible = False
        self._t = 0
        self._t_max = 0.5

        self._sprite = self._animation = self._closed_card = self._opened_card = None
        self._remake_card_sides(gc)

        self.edit_offset = v.Vector(0, 0)
        self.dragging = False

    def _calculate_sliding_animation(self) -> None:
        if self.go_to_pos is None:
            self.go_to_pos = v.duplicate(self.pos)
            self.time_to_move = 0
            self.moving_offset = v.Vector(0, 0)
        else:
            self.moving_offset = v.point_to(self.pos, self.go_to_pos).scale(1 / self.time_to_move)

    def _remake_card_sides(self, gc: GameContainer) -> None:
        if self.major is None:
            self.major = random.random() < 0.5
            if self.major:
                self.hit_box.scale(1.5)

        if self.major:
            # card_n = 23
            card_n = 10
            card_images = gc.ImageManager.get_image("MajorArcana")
            card_images = pygame.transform.scale(card_images, (self.hit_box.x * card_n, self.hit_box.y))
            self.suit = 0
            variants = 1
            self._sprite = Animation(card_images, card_n, variants)
            self._sprite.sprite_name = "MajorArcana"
        else:
            # card_n = 15
            card_n = 10
            card_images = gc.ImageManager.get_image("MinorArcana")
            card_images = pygame.transform.scale(card_images, (self.hit_box.x * card_n, self.hit_box.y * 4))
            if self.suit is None:
                self.suit = random.randint(0, 3)
            variants = 4
            self._sprite = Animation(card_images, card_n, variants)
            self._sprite.sprite_name = "MinorArcana"

        # scale = gc.Window.scale()
        card_border = gc.ImageManager.get_image("CardBorder")
        card_border = pygame.transform.scale(card_border, (self.hit_box.x * 4, self.hit_box.y))

        self._animation = Animation(card_border, 4, 1) \
            .add_stage("Loop", 0, 4, 0.5, "Loop") \
            .set_stage("Loop")
        self._animation.sprite_name = "CardBorder"

        if self.value is None:
            self.value = random.randrange(1, card_n)

        center = v.duplicate(self.hit_box).scale(0.5)
        self._closed_card = pygame.Surface(v.to_tuple(self.hit_box), pygame.SRCALPHA, 32)
        self._closed_card.convert_alpha()
        self._sprite.draw_frame(self._closed_card, center, 0)

        self._opened_card = pygame.Surface(v.to_tuple(self.hit_box), pygame.SRCALPHA, 32)
        self._opened_card.convert_alpha()
        self._sprite.draw_frame(self._opened_card, center, self.value, self.suit)

    def edit(self, gc: GameContainer) -> None:
        super().update_logic(gc)

        if self.is_right_clicked:
            gc.current_scene.instance_destroy(self)

        if self.is_pressed:
            self.edit_offset = v.point_to(v.tuple_to_vector(gc.Input.mouse_pos), self.pos)
            self.dragging = True

        if gc.Input.get_button(0) and self.dragging:
            self.pos = v.tuple_to_vector(gc.Input.mouse_pos).add(self.edit_offset)

        if gc.Input.get_button_released(0) and self.dragging:
            self.dragging = False

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        self._animation.update(dt)

        if self.time_to_move > 0:
            self.time_to_move -= dt
            self.pos.add(v.duplicate(self.moving_offset).scale(dt))
            return

        if self.visible:
            self._t = min(self._t + dt, self._t_max)
        else:
            self._t = max(self._t - dt, 0)

        super().update_logic(gc)
        if self.is_movable and self.is_right_clicked and self.time_to_move <= 0 and gc.current_scene.exists(self):
            offset = v.tuple_to_vector(gc.Input.mouse_pos).sub(self.pos)
            gc.current_scene.instance_create(Draggable(gc, self, self.pos, offset))
            gc.current_scene.instance_destroy(self)

        if self.is_pressed:
            if self.visible and self.closable:
                self.visible = False
            elif not self.visible and self.openable:
                self.visible = True

    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        if self._t > self._t_max / 2:
            area = (v.map_value(self._t, self._t_max / 2, self._t_max, 0, self.hit_box.x), self.hit_box.y)
            transform = pygame.transform.scale(self._opened_card, area)
            screen.blit(
                transform,
                (v.map_value(self._t, self._t_max / 2, self._t_max, self.pos.x, self.pos.x - self.hit_box.x / 2),
                 self.pos.y - self.hit_box.y / 2)
            )
        else:
            area = (v.map_value(self._t, 0, self._t_max / 2, self.hit_box.x, 0), self.hit_box.y)
            transform = pygame.transform.scale(self._closed_card, area)
            screen.blit(
                transform,
                (v.map_value(self._t, 0, self._t_max / 2, self.pos.x - self.hit_box.x / 2, self.pos.x),
                 self.pos.y - self.hit_box.y / 2))
        self._animation.draw_frame(screen, self.pos)

    def save(self) -> [str]:
        return [
            self.pos.save(),
            self.hit_box.save(),
            self.go_to_pos.save(),
            self.moving_offset.save(),

            str(self.is_movable),
            str(self.openable),
            str(self.closable),
            str(self.visible),
            str(self.major),

            str(self.value),
            str(self.suit),

            str(self._t),
            str(self.time_to_move)
        ]

    def load(self, gc: GameContainer, args: [str]) -> None:
        self.pos = v.load_vector(args[1])
        self.hit_box = v.load_vector(args[2]).scale(gc.Window.scale())
        self.go_to_pos = v.load_vector(args[3])
        self.moving_offset = v.load_vector(args[4])

        self.is_movable = args[5] == 'True'
        self.openable = args[6] == 'True'
        self.closable = args[7] == 'True'
        self.visible = args[8] == 'True'
        self.major = args[9] == 'True'

        self.value = int(args[10])
        self.suit = int(args[11])

        self._t = float(args[12])
        self.time_to_move = float(args[13])

        # self._calculate_sliding_animation()
        self._remake_card_sides(gc)

        self.hit_box = v.load_vector(args[2])
