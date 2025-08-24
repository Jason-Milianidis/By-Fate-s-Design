import pygame
import random
from Engine import GameContainer
from Game.Utility.Button import Button
import Engine.Vectors as v
from Game.Objects.Card import Card
from Game.Scenes.FloorScene import FloorScene
import Game.Utility.MinorArcanaSummoner as mas


class ContinueButton(Button):

    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), cards: [Card] = None, major_card: Card = None,
                 go_to_pos: v.Vector = None, time_to_go: float = 1):
        super().__init__(gc, pos, v.tuple_to_vector(gc.Font.get_text_dims(" Continue x/x ")).scale((1, 1.3)))
        if cards is None:
            cards = []
        self.value = 0
        self.selected_cards = []
        self.cards = cards
        self.major_card = major_card
        self._min_selected = gc.CardSpawner.min_card_number()
        self.go_to_pos = go_to_pos
        self.time_to_move = time_to_go
        self.moving_offset = v.Vector(0, 0)
        self._calculate_sliding_animation()
        self._time = 0

    def _calculate_sliding_animation(self) -> None:
        if self.go_to_pos is None:
            self.go_to_pos = v.duplicate(self.pos)
            self.time_to_move = 0
            self.moving_offset = v.Vector(0, 0)
        else:
            self.go_to_pos = self.go_to_pos
            self.time_to_move = self.time_to_move
            self.moving_offset = v.point_to(self.pos, self.go_to_pos).scale(1 / self.time_to_move)

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        if self._time > 0:
            self._time -= dt
            if self._time <= 0:
                self.major_card = None
                self._create_level(gc)
            return

        super().update_logic(gc)

        if self.time_to_move > 0:
            self.time_to_move -= dt
            self.pos.add(v.duplicate(self.moving_offset).scale(dt))

        self.selected_cards = [card for card in self.cards if card.visible]
        self.value = len(self.selected_cards)
        if self.value < self._min_selected:
            self.color = (255, 50, 50)
        elif self.value == self._min_selected:
            self.color = (50, 255, 50)
        else:
            self.color = (180, 180, 30)

        if self.is_pressed and self.value >= self._min_selected:
            self._create_level(gc)

    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        super().render_centered(gc, screen, border_radius=5)
        gc.Font.set_alignment(gc.Font.Alignment.CENTER)
        gc.Font.draw_string(screen, "Continue " + str(self.value) + "/" + str(self._min_selected), v.to_tuple(self.pos))

    def _create_level(self, gc: GameContainer) -> None:
        if self.major_card is None:
            value = -1
        else:
            value = self.major_card.value

        match value:
            case mas.ArcanaType.THE_FOOL.value:
                self._time = 3
                for card in random.sample(self.cards, gc.CardSpawner.get_normal_card_selection_number()):
                    card.visible = True
                    self.selected_cards.append(card)
            case mas.ArcanaType.DEATH.value:
                gc.Audio.play_unique()
                self._instantiate_the_next_level(gc)
            case _:
                gc.Audio.play_background()
                self._instantiate_the_next_level(gc)

    def _instantiate_the_next_level(self, gc: GameContainer) -> None:
        floor = gc.Scene.get_scene("Floor Scene")
        if floor is None:
            floor = FloorScene(gc)
        gc.current_scene = floor

        variation = random.randint(1, 5)
        gc.LevelManager.load(floor, "layout" + str(variation))
        gc.Renderer.set_background(str(variation))
        gc.Save.set_attribute("last background", str(variation))

        for card in self.selected_cards:
            mas.create_enemy(gc, card.suit, card.value + 1)

    def save(self) -> [str]:
        return [self.pos.save(), self.hit_box.save(), self.go_to_pos.save(), self.moving_offset.save(),
                str(self.value),
                str(self.time_to_move)
                ]

    def load(self, gc: GameContainer, args: [str]) -> None:
        self.pos = v.load_vector(args[1])
        self.hit_box = v.load_vector(args[2])
        self.go_to_pos = v.load_vector(args[3])
        self.moving_offset = v.load_vector(args[4])

        self.value = int(args[5])

        self.time_to_move = float(args[6])
