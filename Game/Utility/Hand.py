import pygame
from Engine.GameObject import GameObject
import Engine.GameContainer as GameContainer
import Engine.Vectors as v
import Game.Flare.Particle as p
from Game.Utility.MinorArcanaType import MinorArcanaType


class Hand(GameObject):
    
    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), direction: v.Vector = v.Vector(0, 0)):
        super().__init__(gc, pos, v.Vector(16, 16))
        self.display_box = v.Vector(48, 36)
        self.flying = 1
        self.direction = direction
        self.screen = pygame.Surface(v.to_tuple(self.display_box), pygame.SRCALPHA)
        self.timer = 30
        self._damaged = []

        sprite = gc.ImageManager.get_image("Hand", scale=(1.5, 1.5))
        self.animation = gc.AnimationManager.Animation(sprite, 7, 3, 2) \
            .add_stage_fps("Idle", 0, 7, 1.0, "Idle") \
            .add_stage_fps("Pickup", 1, 7, 1.0) \
            .add_stage_fps("Settle", 2, 5, 1.0, "Idle") \
            .add_variant("Left", 1) \
            .add_variant("Right", 0) \
            .set_stage("Settle")

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        if self.flying > 0:
            self.flying -= dt
            super().move_in_bounds(gc, v.duplicate(self.direction).scale(dt_normalized))
            gc.current_scene.instance_create(p.Particle(gc, v.duplicate(self.pos), v.Vector(1.5, 1.5)))

            for obj in [o for o in gc.current_scene.objects if isinstance(o, MinorArcanaType) and o not in self._damaged]:
                if self.collides(obj):
                    obj.lives -= 3
                    self._damaged.append(obj)
                    p.create_splatter(gc, self, obj)

            return

        if self.animation.trigger_at("Pickup", 6):
            gc.current_scene.instance_destroy(self)

        if self.animation.current_stage != "Pickup":
            self.timer -= dt
            if self.timer <= 0 or (gc.current_scene.collides_with_player(self) and gc.current_scene.player.pick_hand()):
                self.animation.set_stage("Pickup")

        self.animation.update(dt)

    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        self.screen.fill((0, 0, 0, 0))
        self.animation.draw_frame(self.screen, v.duplicate(self.display_box).scale(0.5))
        screen.blit(
            pygame.transform.rotate(self.screen, 180-self.direction.get_direction()),
            v.to_tuple(v.duplicate(self.pos).sub(v.duplicate(self.display_box).scale(0.5)))
        )

    def save(self) -> [str]:
        return [self.pos.save(), self.hit_box.save(), self.animation.save()]

    def load(self, gc: GameContainer, args: [str]) -> None:
        self.pos = v.load_vector(args[1])
        self.hit_box = v.load_vector(args[2])
        self.animation = gc.AnimationManager.load(args[3])
