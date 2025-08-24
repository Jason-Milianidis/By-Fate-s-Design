import pygame
import Engine.GameContainer as GameContainer
from Engine.AnimationManager import Animation
from Game.Utility.MinorArcanaType import MinorArcanaType
from Game.Flare.AnimationPlayer import AnimationPlayer
import Engine.Vectors as v
from Engine.GameObject import overlaps


class MoonsLow(MinorArcanaType):
    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), power: int = 2, image: str = "Two"):
        super().__init__(gc, pos, v.Vector(12, 32), power, 4, (40, 100))
        self.display_box = v.Vector(64, 64)
        self.time = 0
        self.special_time = 0
        self.attack_spd = 4
        self.damaged = 0
        self.speed = 1
        self.special_cd = 10 - power
        self.make_button = False

        sprite = gc.ImageManager.get_image("Moons/"+image, scale=(2, 2))
        self.animation = Animation(sprite, 19, 4, 2)\
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
            self.special_time += dt

            if self.special_time >= self.special_cd:
                to_player = v.point_to(self.pos, gc.current_scene.player.pos)
                end_pos = v.duplicate(to_player).scale(2).add(self.pos)
                if to_player.magnitude() > 120 and gc.current_scene.valid_spot(end_pos):
                    self.special_time = 0
                    animation = self.animation.duplicate().set_stage("Death")
                    animation_player = AnimationPlayer(gc, v.duplicate(self.pos), animation=animation)
                    gc.current_scene.instance_create(animation_player)
                    self.pos = end_pos
                    self.animation.set_stage("Spawn")

            if self.time >= self.attack_spd:
                if super().keep_player_distance(gc, max_dist_away=80) <= 80:
                    self.time = 0
                    self.animation.set_stage("Attack")
            else:
                super().keep_player_distance(gc, min_dist_away=350)

        if self.animation.trigger_at("Attack", 7):
            my_sides = (self.pos.x - 60, self.pos.x + 60, self.pos.y - 15, self.pos.y + 15)
            player_sides = gc.current_scene.player.calculate_object_sides()
            if overlaps(my_sides, player_sides):
                gc.current_scene.player.damage()

    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        self.animation.draw_frame(screen, self.pos)
        super().render(gc, screen)
