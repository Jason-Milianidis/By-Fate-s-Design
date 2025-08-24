import pygame

from abc import abstractmethod
from Engine import GameContainer, Vectors as v
from Engine.GameObject import GameObject
from Engine.AnimationManager import Animation, load


class MinorArcanaType(GameObject):

    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), hit_box: v.Vector = v.Vector(-1, -1),
                 power: int = 0, speed: float = 0, edit_box: (float, float) = (40, 80)):
        super().__init__(gc, pos, hit_box, edit_box)
        self.power = power
        self.speed = speed
        self.lives = power

        scale = gc.Window.scale()
        sprite = gc.ImageManager.get_image("Star", resize=(64 * scale[0] * 2, 64 * scale[1]))
        self.animation = Animation(sprite, 2, 1) \
            .add_stage_fps("Loop", 0, 2, 1, "Loop") \
            .set_stage("Loop")

    def edit(self, gc: GameContainer) -> None:
        super().movable(gc)

    @abstractmethod
    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        pass

    @abstractmethod
    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        if self.edit_highlight:
            pygame.draw.rect(screen, "red", (self.pos.x - self.edit_box[0] / 2, self.pos.y - self.edit_box[1] / 2,
                                             self.edit_box[0], self.edit_box[1]), 2, 5)

    def save(self) -> [str]:
        return [
            self.pos.save(),
            self.hit_box.save(),

            str(self.power),
            str(self.lives),

            str(self.speed),

            self.animation.save()
        ]

    def load(self, gc: GameContainer, args: [str]) -> None:
        self.pos = v.load_vector(args[1])
        self.hit_box = v.load_vector(args[2])

        self.power = int(args[3])
        self.lives = int(args[4])

        self.speed = float(args[5])

        self.animation = load(args[6])

    def keep_player_distance(self, gc: GameContainer, speed: float = None, min_dist_away: float = None, max_dist_away: float = None) -> float:
        distance = v.point_to(self.pos, gc.current_scene.player.pos).magnitude()
        if speed is None:
            speed = self.speed * gc.Window.dt_normalized

        if min_dist_away is not None:
            if distance < min_dist_away:
                self.move_towards_player(gc, -speed)

        if max_dist_away is not None:
            if distance > max_dist_away:
                self.move_towards_player(gc, speed)

        return distance

    def move_towards_player(self, gc: GameContainer, speed: float) -> None:
        direction = v.point_to(self.pos, gc.current_scene.player.pos)\
                     .normalize(speed)
        super().move_in_bounds(gc, direction)
