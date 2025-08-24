import pygame
import Engine.GameContainer as GameContainer
from Engine.AnimationManager import Animation
from Game.Utility.MinorArcanaType import MinorArcanaType
import Engine.Vectors as v
from Game.Utility.Patterns.DelayedTargeting import DelayedTargeting
from Game.Flare.FadingAnimation import FadingAnimation
from Game.Utility.Modifiers.HomingMod import HomingMod
from Game.Utility.Modifiers.ExpireMod import ExpireMod
from Engine.GameObject import overlaps


class TombsHigh(MinorArcanaType):
    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), power: int = 9, image: str = "Nine"):
        super().__init__(gc, pos, v.Vector(20, 56), power, 4)
        self.display_box = v.Vector(64, 64)
        self.time = 0
        self.attack_cd_melee = 4
        self.attack_cd_range = 8
        self.speed = 1
        self.velocity = v.Vector(0, 0)
        self.dash_time = 0
        self.particle_time = 0
        self.particle_time_max = 0.05

        self.edit_box = (80, 160)
        self.make_button = False

        sprite = gc.ImageManager.get_image("Tombs/" + image, scale=(3, 3))

        self.animation = Animation(sprite, 49, 5, 2) \
            .add_stage_fps("Idle", 0, 9, 1, "Idle") \
            .add_stage_fps("Attack Range", 1, 49, 4, "Idle") \
            .add_stage_fps("Attack Melee", 2, 42, 2, "Idle") \
            .add_stage_fps("Death", 3, 18, 2) \
            .add_stage_fps("Spawn", 4, 14, 1, "Idle") \
            .add_variant("Left", 1) \
            .add_variant("Right", 0) \
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

        if gc.current_scene.player.pos.x < self.pos.x:
            self.animation.set_variant("Left")
        else:
            self.animation.set_variant("Right")

        if self.lives <= 0:
            self.animation.set_stage("Death")

        if self.animation.trigger_at("Attack Melee", 20):
            self._attack_melee(gc)

        if self.animation.trigger_at("Attack Melee", 21):
            my_sides = (self.pos.x - 80, self.pos.x + 80, self.pos.y - 30, self.pos.y + 30)
            player_sides = gc.current_scene.player.calculate_object_sides()
            if overlaps(my_sides, player_sides):
                gc.current_scene.player.damage()

        if self.animation.trigger_at("Attack Range", 29):
            self._attack_range(gc)

        if self.animation.current_stage != "Idle":
            return
        self.time += dt
        distance = v.point_to(self.pos, gc.current_scene.player.pos).magnitude()
        if distance < 400 and self.time >= self.attack_cd_melee:
            if super().keep_player_distance(gc, self.speed * 1.8 * dt_normalized, max_dist_away=250) <= 250:
                self.time = 0
                self.animation.set_stage("Attack Melee")
        else:
            if super().keep_player_distance(gc, min_dist_away=600) >= 600 and self.time >= self.attack_cd_range:
                self.time = 0
                self.animation.set_stage("Attack Range")

    def _attack_range(self, gc: GameContainer) -> None:
        gc.current_scene.instance_create(
            DelayedTargeting(gc, v.duplicate(self.pos).add(v.Vector(0, -32)), 2, 20, 1, 30)
            .add_modifier(HomingMod().initialize(2))
            .add_modifier(ExpireMod().initialize(10))
        )

    def _attack_melee(self, gc: GameContainer) -> None:
        to_player = v.point_to(self.pos, gc.current_scene.player.pos)
        speed = self.power
        self.dash_time = to_player.magnitude() / speed / gc.Window.space_normalization_value
        self.velocity = to_player.normalize(speed)
        self.particle_time = 0

    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        self.animation.draw_frame(screen, self.pos)
        super().render(gc, screen)
        # super().show_hit_box(screen)
        # pygame.draw.rect(screen, "red", (self.pos.x-2, self.pos.y-2, 4, 4))
