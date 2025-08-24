import pygame
import Engine.GameContainer as GameContainer
from Engine.AnimationManager import Animation
from Game.Utility.MinorArcanaType import MinorArcanaType
import Engine.Vectors as v
from Game.Utility.Patterns.DelayedBlast import DelayedBlast


class ChalicesLow(MinorArcanaType):
    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), power: int = 2, image: str = "Two"):
        super().__init__(gc, pos, v.Vector(12, 32), power, 4)
        self.display_box = v.Vector(64, 64)
        self.time = 0
        self.attack_spd = 4
        self.damaged = 0
        self.speed = 1
        self.edit_box = (40, 100)
        self.make_button = False

        sprite = gc.ImageManager.get_image("Chalices/" + image, scale=(2, 2))

        self.animation = Animation(sprite, 19, 4, 2) \
            .add_stage_fps("Idle", 0, 9, 1, "Idle") \
            .add_stage_fps("Attack", 1, 13, 0.8, "Idle") \
            .add_stage_fps("Death", 2, 19, 2) \
            .add_stage_fps("Spawn", 3, 15, 1, "Idle") \
            .set_stage("Spawn")

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        self.animation.update(dt)

        if gc.current_scene.player is None or self.animation.current_stage == "Death":
            return

        if self.lives <= 0:
            self.animation.set_stage("Death")

        if gc.current_scene.player.pos.x < self.pos.x:
            self.animation.variant_offset = 1
        else:
            self.animation.variant_offset = 0

        if self.animation.current_stage == "Idle":
            self.time += dt
            if super().keep_player_distance(gc, min_dist_away=350) and self.time >= self.attack_spd:
                self.time = 0
                self.animation.set_stage("Attack")

        if self.animation.trigger_at("Attack", 7):
            gc.current_scene.instance_create(DelayedBlast(gc, v.duplicate(self.pos),
                                                          v.point_to(self.pos, gc.current_scene.player.pos).normalize(
                                                              self.power + 2),
                                                          self.power, 0.2))

    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        self.animation.draw_frame(screen, self.pos)
        super().render(gc, screen)
