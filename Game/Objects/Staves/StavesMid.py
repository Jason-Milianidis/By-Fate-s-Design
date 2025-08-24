import pygame

import Engine.GameContainer as GameContainer
from Engine.AnimationManager import Animation
from Game.Utility.MinorArcanaType import MinorArcanaType
from Game.Utility.Patterns.DelayedTargeting import DelayedTargeting
import Engine.Vectors as v


class StavesMid(MinorArcanaType):

    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), power: int = 5, image: str = "Five"):
        super().__init__(gc, pos, v.Vector(20, 48), power, 4)
        self.display_box = v.Vector(64, 64)
        self.time = 0
        self.attack_spd = 8
        self.speed = 0.8
        self.edit_box = (50, 130)
        self.make_button = False

        sprite = gc.ImageManager.get_image("Staves/"+image, scale=(2.5, 2.5))

        self.animation = Animation(sprite, 21, 4, 2)\
            .add_stage_fps("Idle", 0, 3, 1, "Idle") \
            .add_stage_fps("Attack", 1, 21, 3, "Idle") \
            .add_stage_fps("Death", 2, 21, 2) \
            .add_stage_fps("Spawn", 3, 19, 1, "Idle") \
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
            if super().keep_player_distance(gc, min_dist_away=350) >= 350 and self.time >= self.attack_spd:
                self.time = 0
                self.animation.set_stage("Attack")

        if self.animation.trigger_at("Attack", 17):
            pattern = DelayedTargeting(gc, v.duplicate(self.pos), 4, self.power, 0.5)
            gc.current_scene.instance_create(pattern)
            # bullet = Bullet(gc, v.duplicate(self.pos), direction)
            # gc.current_scene.instance_create(bullet)

    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        self.animation.draw_frame(screen, self.pos)
        super().render(gc, screen)
