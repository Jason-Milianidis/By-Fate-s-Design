import pygame

import Engine.GameContainer as GameContainer
from Engine.AnimationManager import Animation
from Game.Utility.MinorArcanaType import MinorArcanaType
import Engine.Vectors as v
from Game.Flare.FadingAnimation import FadingAnimation
from Engine.GameObject import overlaps


class TombsMid(MinorArcanaType):

    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), power: int = 5, image: str = "Five"):
        super().__init__(gc, pos, v.Vector(20, 48), power, 4)
        self.display_box = v.Vector(64, 64)
        self.time = 0
        self.attack_spd = 12 - power
        self.speed = 0.8
        self.velocity = v.Vector(0, 0)
        self.dash_time = 0
        self.particle_time = 0
        self.particle_time_max = 0.05

        self.edit_box = (50, 130)
        self.make_button = False

        sprite = gc.ImageManager.get_image("Tombs/"+image, scale=(2.5, 2.5))

        self.animation = Animation(sprite, 22, 4, 2)\
            .add_stage_fps("Idle", 0, 9, 1, "Idle") \
            .add_stage_fps("Attack", 1, 22, 3, "Idle") \
            .add_stage_fps("Death", 2, 21, 2) \
            .add_stage_fps("Spawn", 3, 19, 1, "Idle") \
            .set_stage("Spawn")

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        if self.dash_time > 0:
            self.dash_time -= dt
            velocity = v.duplicate(self.velocity).scale(dt_normalized)
            super().move_in_bounds(gc, velocity)

            self.particle_time += dt
            if self.particle_time >= self.particle_time_max:
                self.particle_time %= self.particle_time_max
                gc.current_scene.instance_create(FadingAnimation(gc, v.duplicate(self.pos), self.animation, 0.5))
            return

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
            super().keep_player_distance(gc, min_dist_away=350)
            self.time += dt
            if self.time >= self.attack_spd:
                self.time = 0
                self.animation.set_stage("Attack")

        if self.animation.trigger_at("Attack", 17):
            to_player = v.point_to(self.pos, gc.current_scene.player.pos)
            speed = self.power
            self.dash_time = to_player.magnitude() / speed / gc.Window.space_normalization_value
            self.velocity = to_player.normalize(speed)
            self.particle_time = 0

        if self.animation.trigger_at("Attack", 18):
            my_sides = (self.pos.x - 90, self.pos.x + 90, self.pos.y - 30, self.pos.y + 30)
            player_sides = gc.current_scene.player.calculate_object_sides()
            if overlaps(my_sides, player_sides):
                gc.current_scene.player.damage()

    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        self.animation.draw_frame(screen, self.pos)
        super().render(gc, screen)
