import pygame
import Engine.GameContainer as GameContainer
from Engine.AnimationManager import Animation
from Game.Utility.MinorArcanaType import MinorArcanaType
import Engine.Vectors as v
from Game.Utility.Patterns.DelayedExplodingTargeting import DelayedExplodingTargeting
from Game.Utility.Bullets.BasicBullet import BasicBullet
from Game.Utility.Modifiers.FrictionMod import FrictionMod


class ChalicesHigh(MinorArcanaType):
    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), power: int = 9, image: str = "Nine"):
        super().__init__(gc, pos, v.Vector(20, 56), power, 4)
        self.display_box = v.Vector(64, 64)
        self.time = 0
        self.attack_cd_melee = 4
        self.attack_cd_range = 8
        self.speed = 1
        self.edit_box = (80, 160)
        self.make_button = False

        sprite = gc.ImageManager.get_image("Chalices/" + image, scale=(3, 3))

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

        if self.animation.trigger_at("Attack Range", 29):
            self._attack_range(gc)

        if self.animation.current_stage != "Idle":
            return
        self.time += dt
        distance = v.point_to(self.pos, gc.current_scene.player.pos).magnitude()
        if distance < 400 and self.time >= self.attack_cd_melee:
            if super().keep_player_distance(gc, self.speed * 1.8 * dt_normalized, max_dist_away=150) <= 150:
                self.time = 0
                self.animation.set_stage("Attack Melee")
        else:
            if super().keep_player_distance(gc, min_dist_away=600) >= 600 \
                    and self.time >= self.attack_cd_range:
                self.time = 0
                self.animation.set_stage("Attack Range")

    def _attack_range(self, gc: GameContainer) -> None:
        gc.current_scene.instance_create(
            DelayedExplodingTargeting(gc, v.duplicate(self.pos).add(v.Vector(0, -32)), 8, 20, 1)
        )

    def _attack_melee(self, gc: GameContainer) -> None:
        angle = v.point_to(self.pos, gc.current_scene.player.pos).get_direction()
        for i in range(-90, 90, 10):
            direction = v.direction(i).rotate(angle).scale(8)
            for j in [0.001, 0.03, 0.1]:
                bullet = BasicBullet(gc, v.duplicate(self.pos), direction)
                bullet.add_modifier(FrictionMod().initialize(j, 0.1).link(bullet))
                gc.current_scene.instance_create(bullet)

    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        self.animation.draw_frame(screen, self.pos)
        super().render(gc, screen)
