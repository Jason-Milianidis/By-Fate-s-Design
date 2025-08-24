import pygame

from Engine import GameContainer, Vectors as v
from Engine.GameObject import GameObject
from Game.Utility.MinorArcanaType import MinorArcanaType
from Game.Utility.ContinueButton import ContinueButton
from Engine.AnimationManager import Animation


class LevelComplete(GameObject):
    def __init__(self, gc: GameContainer):
        super().__init__(gc, v.Vector(gc.Window.game_size[0]/2, 40), v.Vector(32, 32))
        self.enemies_left = -1
        self.time = 0

        scale = gc.Window.scale()
        sprite = gc.ImageManager.get_image("Star", resize=(64 * scale[0] * 2, 64 * scale[1]))
        self._animation = Animation(sprite, 2, 1) \
            .add_stage_fps("Loop", 0, 2, 1, "Loop") \
            .set_stage("Loop")

        self.editing = False
        self.edit_highlight = False
        self.edit_offset = v.Vector(0, 0)
        self.edit_box = (32 * gc.Window.scale()[0], 32 * gc.Window.scale()[1])
        self.major_card = None
        self.minor_cards = None
        self.continue_button = None
        self._gc = gc

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        self._animation.update(dt)

        self.time += dt
        if self.time >= 1:
            self.time %= 1
            self.enemies_left = len([o for o in gc.current_scene.objects if isinstance(o, MinorArcanaType) and o.lives > 0])

        if self.major_card is not None:
            self.major_card.update(gc, dt, dt_normalized)
        if self.minor_cards is not None:
            [card.update(gc, dt, dt_normalized) for card in self.minor_cards]
        if self.continue_button is not None:
            self.continue_button.update(gc, dt, dt_normalized)

        if self.major_card is None and self.enemies_left == 0 and gc.current_scene.collides_with_player(self):
            self.major_card = gc.CardSpawner.create_major_card(self.pos)

        if self.minor_cards is None and self.major_card is not None and self.major_card.visible:
            self.minor_cards = gc.CardSpawner.create_minor_cards(self.major_card)
            self.continue_button = ContinueButton(gc, v.duplicate(self.pos), self.minor_cards, self.major_card,
                                                  v.Vector(gc.Window.game_size[0]/2, gc.Window.game_size[1]/6*5), 1)

    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        if (self.enemies_left == 0 and self.major_card is None) or self.editing:
            self._animation.draw_frame(screen, self.pos)
            # pygame.draw.rect(screen, "white", (self.pos.x - self.hit_box.x / 2, self.pos.y - self.hit_box.y / 2,
            #                                    self.hit_box.x, self.hit_box.y), 1, 5)

        if self.edit_highlight:
            pygame.draw.rect(screen, "red", (self.pos.x - self.edit_box[0] / 2, self.pos.y - self.edit_box[1] / 2,
                                             self.edit_box[0], self.edit_box[1]), 2, 5)

        if self.major_card is not None:
            self.major_card.render(gc, screen)
        if self.minor_cards is not None:
            [card.render(gc, screen) for card in self.minor_cards]
        if self.continue_button is not None:
            self.continue_button.render(gc, screen)

    def edit(self, gc: GameContainer) -> None:
        self.editing = True
        mouse = gc.Input.mouse_pos

        if gc.Input.get_button_pressed(2) and self.edit_highlight:
            gc.current_scene.instance_destroy(self)

        if gc.Input.get_button_pressed(0) and self.edit_highlight:
            self.edit_offset = v.point_to(v.tuple_to_vector(mouse), self.pos)

        if gc.Input.get_button(0):
            if self.edit_highlight:
                self.pos = v.tuple_to_vector(mouse).add(self.edit_offset)
        else:
            self.edit_highlight = self.pos.x - self.edit_box[0] / 2 <= mouse[0] <= self.pos.x + self.edit_box[0] / 2 and \
                                  self.pos.y - self.edit_box[1] / 2 <= mouse[1] <= self.pos.y + self.edit_box[1] / 2

    def save(self) -> [str]:
        if self.minor_cards is None:
            sav = 'None'
        else:
            sav = "$".join([self._gc.LevelManager.get_saved_string(card, "%") for card in self.minor_cards])

        return [
            self.pos.save(),
            self.hit_box.save(),

            str(self.time),

            str(self.enemies_left),

            str(self._gc.LevelManager.get_saved_string(self.major_card, "%")),
            sav,
            str(self._gc.LevelManager.get_saved_string(self.continue_button, "%"))
        ]

    def load(self, gc: GameContainer, args: [str]) -> None:
        self.pos = v.load_vector(args[1])
        self.hit_box = v.load_vector(args[2])

        self.time = float(args[3])

        self.enemies_left = int(args[4])

        self.major_card = gc.LevelManager.load_object(args[5], "%")
        if args[6] == 'None':
            self.minor_cards = None
        else:
            self.minor_cards = [gc.LevelManager.load_object(a, "%") for a in args[6].split("$")]
        self.continue_button = gc.LevelManager.load_object(args[7], "%")

        if self.continue_button is not None:
            self.continue_button.cards = self.minor_cards
            self.continue_button.major_card = self.major_card
