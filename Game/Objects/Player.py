import pygame

from Engine.GameObject import GameObject, overlaps
from Engine.AnimationManager import Animation
import Engine.GameContainer as GameContainer
import Engine.Vectors as v
from Game.Utility.MinorArcanaType import MinorArcanaType
from Game.Utility.Hand import Hand
from typing import Optional
from Game.Flare.FadingAnimation import FadingAnimation
import Game.Flare.Particle as p


class Player(GameObject):
    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0)):
        super().__init__(gc, pos, v.Vector(10, 24))
        self.display_box = v.Vector(40, 40)
        self.dash = v.Vector(0, 0)
        self.direction = v.Vector(0, 0)
        self.speed = 2
        self._hit_box_values = v.duplicate(self.hit_box)
        self.invincible = 0
        self._hand_removed = False
        self._hand_timer = 0
        self._sav = gc.Save
        self._audio = gc.Audio
        self._hp = self._sav.get_attribute("health")
        self._death_time = 0

        self.melee_area = (75, 25)

        sprite = gc.ImageManager.get_image("Player", scale=(1.5, 1.5))
        self.animation = Animation(sprite, 17, 16, 2) \
            .add_stage_fps("Idle2", 0, 10, 1.0, "Idle2") \
            .add_stage_fps("Idle1", 1, 10, 1.0, "Idle1") \
            .add_stage_fps("Idle0", 2, 10, 1.0, "Idle0") \
            .add_stage_fps("Dash2", 3, 5, 0.25, "Idle2") \
            .add_stage_fps("Dash1", 4, 5, 0.25, "Idle1") \
            .add_stage_fps("Dash0", 5, 5, 0.25, "Idle0") \
            .add_stage_fps("Melee2", 6, 8, 0.5, "Idle2") \
            .add_stage_fps("Melee1", 7, 8, 0.5, "Idle1") \
            .add_stage_fps("Range2", 8, 12, 1, "Idle1") \
            .add_stage_fps("Range1", 9, 13, 1, "Idle0") \
            .add_stage_fps("Hand2", 10, 2, 0.3, "Idle2") \
            .add_stage_fps("Hand1", 11, 2, 0.3, "Idle1") \
            .add_stage_fps("Death2", 12, 17, 2.0) \
            .add_stage_fps("Death1", 13, 17, 2.0) \
            .add_stage_fps("Death0", 14, 17, 2.0) \
            .add_stage_fps("Spawn", 15, 9, 1.0, "Idle2") \
            .add_variant("Left", 1) \
            .add_variant("Right", 0) \
            .set_stage("Spawn")

        scale = gc.Window.scale()
        self._extra_lives = gc.ImageManager.get_image("ExtraLife", resize=(64 * scale[0], 64 * scale[1]))

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        if self._death_time > 0:
            self.animation.update(dt)
            self._death_time -= dt
            if self._death_time <= 0:
                gc.current_scene = gc.Scene.get_scene("Main Scene")
                if gc.current_scene is None:
                    from Game.Scenes.MainScene import MainScene
                    gc.current_scene = MainScene(gc)
            return

        if self._hand_timer > 0:
            self._hand_timer -= dt
            if self._hand_timer <= 0 and not self.pick_hand():
                self._hand_timer = dt

        if self.invincible > 0:
            self.invincible -= dt

        self.prev_pos = self.pos
        match self.animation.current_stage:
            case "Idle2":
                self.hit_box = self._hit_box_values
                self._move(gc, dt_normalized)
                self._look()
                if gc.Input.get_input_pressed(pygame.K_LSHIFT):
                    self._dash("Dash2")
                if gc.Input.get_input_pressed(pygame.K_q):
                    self.animation.set_stage("Melee2")
                if gc.Input.get_input_pressed(pygame.K_e):
                    self.animation.set_stage("Range2")
            case "Idle1" | "Hand2":
                self.hit_box = self._hit_box_values
                self._move(gc, dt_normalized)
                self._look()
                if gc.Input.get_input_pressed(pygame.K_LSHIFT):
                    self._dash("Dash1")
                if gc.Input.get_input_pressed(pygame.K_q):
                    self.animation.set_stage("Melee1")
                if gc.Input.get_input_pressed(pygame.K_e):
                    self.animation.set_stage("Range1")
            case "Idle0" | "Hand1":
                self.hit_box = self._hit_box_values
                self._move(gc, dt_normalized)
                self._look()
                if gc.Input.get_input_pressed(pygame.K_LSHIFT):
                    self._dash("Dash0")
            case "Dash2" | "Dash1" | "Dash0":
                self.hit_box = self._hit_box_values
                super().move_in_bounds(gc, v.duplicate(self.dash).scale(dt_normalized))
                self.hit_box = v.Vector(-1, -1)
                gc.current_scene.instance_create(FadingAnimation(gc, v.duplicate(self.pos), self.animation))
            case "Melee2" | "Melee1":
                self._move(gc, dt_normalized)
            case "Range2":
                if gc.Input.get_input_pressed(pygame.K_LSHIFT):
                    self._move(gc, 0)
                    if self._hand_removed:
                        self._dash("Dash1")
                    else:
                        self._dash("Dash2")
            case "Range1":
                if gc.Input.get_input_pressed(pygame.K_LSHIFT):
                    self._move(gc, 0)
                    if self._hand_removed:
                        self._dash("Dash0")
                    else:
                        self._dash("Dash1")

        if self.animation.trigger_at("Melee2", 3):
            self._attack_melee_2(gc)
        if self.animation.trigger_at("Melee1", 3):
            self._attack_melee_1(gc)
        if self.animation.trigger_at("Range2", 5):
            self._attack_range_2(gc)
            self._hand_removed = True
            self._hand_timer = 30
        if self.animation.trigger_at("Range1", 5):
            self._attack_range_1(gc)
            self._hand_removed = True

        if self.animation.trigger_at("Range2", 0):
            self._hand_removed = False
        if self.animation.trigger_at("Range1", 0):
            self._hand_removed = False

        self.animation.update(dt)

    def pick_hand(self) -> bool:
        match self.animation.current_stage:
            case "Idle0" | "Dash0":
                self.animation.set_stage("Hand1")
                self._hand_timer = 30
                return True
            case "Idle1" | "Dash1":
                self.animation.set_stage("Hand2")
                return True
            case _:
                return False

    def damage(self) -> None:
        if self.invincible == -1 or self.invincible > 0:
            return

        match self.animation.current_stage:
            case "Dash2" | "Dash1" | "Dash0" | "Death2" | "Death1" | "Death0":
                return
            case "Idle2" | "Melee2":
                if not self._remove_life():
                    self.animation.set_stage("Death2")
                    self._death_time = 5
                    self._audio.play("fail.wav")
            case "Idle1" | "Melee1" | "Range2" | "Hand2":
                if not self._remove_life():
                    self.animation.set_stage("Death1")
                    self._death_time = 5
                    self._audio.play("fail.wav")
            case _:
                if not self._remove_life():
                    self.animation.set_stage("Death0")
                    self._death_time = 5
                    self._audio.play("fail.wav")

    def _remove_life(self) -> bool:
        if self._hp > 0:
            self._hp -= 1
            self._sav.set_attribute("health", self._hp)
            self.invincible = 1
            self._audio.play("hit.wav")
            return True
        return False

    def _dash(self, dash: str) -> bool:
        if self.direction.magnitude() == 0:
            return False
        self.dash = v.duplicate(self.direction).normalize(self.speed * 2)
        self.animation.set_stage(dash)
        return True

    def _move(self, gc: GameContainer, dt_normalized: float) -> float:
        self.direction = v.Vector(0, 0)
        if gc.Input.get_input(pygame.K_w):
            self.direction.y -= 1
        if gc.Input.get_input(pygame.K_a):
            self.direction.x -= 1
        if gc.Input.get_input(pygame.K_s):
            self.direction.y += 1
        if gc.Input.get_input(pygame.K_d):
            self.direction.x += 1
        return super().move_in_bounds(gc, v.duplicate(self.direction).normalize(self.speed * dt_normalized))

    def _look(self) -> None:
        if self.direction.x < 0:
            self.animation.set_variant("Left")
        elif self.direction.x > 0:
            self.animation.set_variant("Right")

    def _attack_melee_2(self, gc: GameContainer) -> None:
        for obj in [o for o in gc.current_scene.objects if isinstance(o, MinorArcanaType)]:
            if overlaps(
                    obj.calculate_object_sides(),
                    (self.pos.x - self.melee_area[0], self.pos.x + self.melee_area[0],
                     self.pos.y - self.melee_area[1], self.pos.y + self.melee_area[1])
            ):
                obj.lives -= 1
                p.create_splatter(gc, self, obj)

    def _attack_melee_1(self, gc: GameContainer) -> None:
        for obj in [o for o in gc.current_scene.objects if isinstance(o, MinorArcanaType)]:
            if self.animation.current_variant == "Right":
                if overlaps(
                        obj.calculate_object_sides(),
                        (self.pos.x, self.pos.x + self.melee_area[0],
                         self.pos.y - self.melee_area[1] / 2, self.pos.y + self.melee_area[1] / 2)
                ):
                    obj.lives -= 1
                    p.create_splatter(gc, self, obj)
            else:
                if overlaps(
                        obj.calculate_object_sides(),
                        (self.pos.x - self.melee_area[0], self.pos.x,
                         self.pos.y - self.melee_area[1] / 2, self.pos.y + self.melee_area[1] / 2)
                ):
                    obj.lives -= 1
                    p.create_splatter(gc, self, obj)

    def _attack_range_2(self, gc: GameContainer) -> None:
        obj = self._get_closest_enemy(gc)
        if obj is not None:
            direction = v.point_to(self.pos, obj.pos).normalize(4)
        else:
            direction = v.direction().normalize(4)
        gc.current_scene.instance_create(Hand(gc, v.duplicate(self.pos), direction))

    def _attack_range_1(self, gc: GameContainer) -> None:
        self._attack_range_2(gc)

    def _get_closest_enemy(self, gc: GameContainer) -> Optional[MinorArcanaType]:
        target = None
        min_dist = v.tuple_to_vector(gc.Window.game_size).scale(10).magnitude()
        for obj in [o for o in gc.current_scene.objects if isinstance(o, MinorArcanaType) and o.lives > 0]:
            if v.point_to(self.pos, obj.pos).magnitude() < min_dist:
                target = obj
                min_dist = v.point_to(self.pos, obj.pos).magnitude()
        return target

    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        self.animation.draw_frame(screen, self.pos)
        if self.edit_highlight:
            pygame.draw.rect(screen, "red", (self.pos.x - 20, self.pos.y - 40,
                                             40, 80), 2, 5)
        scale = gc.Window.scale()
        pos = v.Vector(36 * scale[0], gc.Window.game_size[1] - 76 * scale[1])
        offset = v.Vector(80, 0).scale(scale)
        for i in range(self._hp):
            screen.blit(self._extra_lives, v.to_tuple(pos))
            pos.add(offset)

    def _draw_melee1_area(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, "white", (self.pos.x - self.melee_area[0], self.pos.y - self.melee_area[1],
                                           self.melee_area[0] * 2, self.melee_area[1] * 2), 1, 5)

    def _draw_melee2_area(self, screen: pygame.Surface) -> None:
        if self.animation.current_variant == "Right":
            pygame.draw.rect(screen, "white", (self.pos.x, self.pos.y - self.melee_area[1] / 2,
                                               self.melee_area[0], self.melee_area[1]), 1, 5)
        else:
            pygame.draw.rect(screen, "white", (self.pos.x - self.melee_area[0], self.pos.y - self.melee_area[1] / 2,
                                               self.melee_area[0], self.melee_area[1]), 1, 5)

    def update_hp_from_attributes(self) -> None:
        self._hp = self._sav.get_attribute("health")

    def edit(self, gc: GameContainer) -> None:
        mouse = gc.Input.mouse_pos

        if gc.Input.get_button_pressed(2) and self.edit_highlight:
            gc.current_scene.instance_destroy(self)

        if gc.Input.get_button_pressed(0) and self.edit_highlight:
            self.edit_offset = v.point_to(v.tuple_to_vector(mouse), self.pos)

        if gc.Input.get_button(0):
            if self.edit_highlight:
                self.pos = v.tuple_to_vector(mouse).add(self.edit_offset)
        else:
            self.edit_highlight = self.pos.x - 20 <= mouse[0] <= self.pos.x + 20 and \
                                  self.pos.y - 40 <= mouse[1] <= self.pos.y + 40

    def save(self) -> [str]:
        return [self.pos.save(), self.hit_box.save(), self.animation.save()]

    def load(self, gc: GameContainer, args: [str]) -> None:
        self.pos = v.load_vector(args[1])
        self.hit_box = v.load_vector(args[2])
        self.animation = gc.AnimationManager.load(args[3])
