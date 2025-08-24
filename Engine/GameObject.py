from __future__ import annotations
from abc import abstractmethod
import pygame
import Engine.GameContainer as GameContainer
import Engine.Vectors as v


class GameObject:
    @abstractmethod
    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), hit_box: v.Vector = v.Vector(-1, -1),
                 edit_box: (float, float) = None):
        self.pos = pos
        self.prev_pos = pos
        self.hit_box = hit_box.scale(gc.Window.scale())
        self.display_box = v.duplicate(hit_box)
        self.collision = False
        if gc is not None:
            gc.reference()

        self.edit_highlight = False
        self.edit_offset = v.Vector(0, 0)
        if edit_box is None:
            self.edit_box = v.to_tuple(self.hit_box)
        else:
            self.edit_box = tuple([edit_box[i] * gc.Window.scale()[i] for i in [0, 1]])
            # (edit_box[0] * gc.Window.scale()[0], edit_box[1] * gc.Window.scale()[1])

        self.make_button = True

    @abstractmethod
    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        pass

    def edit(self, gc: GameContainer) -> None:
        pass

    def movable(self, gc: GameContainer) -> None:
        mouse = gc.Input.mouse_pos

        if (gc.Input.get_button_pressed(2) or (gc.Input.get_input(pygame.K_LSHIFT) and gc.Input.get_button(2))) \
                and self.edit_highlight:
            gc.current_scene.instance_destroy(self)

        if gc.Input.get_button_pressed(0) and self.edit_highlight:
            self.edit_offset = v.point_to(v.tuple_to_vector(mouse), self.pos)

        if gc.Input.get_button(0):
            if self.edit_highlight:
                self.pos = v.tuple_to_vector(mouse).add(self.edit_offset)
        else:
            self.edit_highlight = self.pos.x - self.edit_box[0] / 2 <= mouse[0] <= self.pos.x + self.edit_box[0] / 2 and \
                                  self.pos.y - self.edit_box[1] / 2 <= mouse[1] <= self.pos.y + self.edit_box[1] / 2

    @abstractmethod
    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        pass

    @abstractmethod
    def save(self) -> [str]:
        pass

    @abstractmethod
    def load(self, gc: GameContainer, args: [str]) -> None:
        pass

    def on_death(self, gc: GameContainer) -> None:
        pass

    def show_hit_box(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, "white", (
            self.pos.x - self.hit_box.x, self.pos.y - self.hit_box.y,
            self.hit_box.x * 2, self.hit_box.y * 2
        ), 2, 1)

    def move_in_bounds(self, gc: GameContainer, movement: v.Vector, destroy_on_collision: bool = False) -> float:
        prev_pos = v.duplicate(self.pos)
        self.pos.add(movement)

        if destroy_on_collision and (self.pos.x < 0 or self.pos.x > gc.Window.game_size[0] or
                                     self.pos.y < 0 or self.pos.y > gc.Window.game_size[1]):
            gc.current_scene.instance_destroy(self)
            return v.point_to(prev_pos, self.pos).magnitude()

        # check collision with collidable objects
        sides = self.calculate_object_sides()
        for wall in [o for o in gc.current_scene.objects if hasattr(o, "collision") and o.collision]:
            wall_sides = wall.calculate_object_sides()
            if overlaps(sides, wall_sides):
                if destroy_on_collision:
                    gc.current_scene.instance_destroy(self)
                    return v.point_to(prev_pos, self.pos).magnitude()

                # calculate the overlap
                overlapping_box = (
                    max(sides[0], wall_sides[0]),
                    min(sides[1], wall_sides[1]),
                    max(sides[2], wall_sides[2]),
                    min(sides[3], wall_sides[3])
                )
                # get the magnitude of overlap on both axis
                offset = v.Vector(overlapping_box[1] - overlapping_box[0], overlapping_box[3] - overlapping_box[2])

                # get player to wall angle, and wall to its hit box corner angle
                angle = v.point_to(wall.pos, self.pos).get_direction()
                wall_angle = v.point_to(wall.pos, v.duplicate(wall.pos).add(wall.hit_box)).get_direction()

                # side of overlap determines offset applied
                if angle > 180 - wall_angle or angle <= -180 + wall_angle:  # left
                    self.pos.x -= offset.x + gc.Window.collision_fix()
                elif -180 + wall_angle < angle <= -wall_angle:  # top
                    self.pos.y -= offset.y
                elif -wall_angle < angle <= wall_angle:  # right
                    self.pos.x += offset.x + gc.Window.collision_fix()
                else:  # bottom
                    self.pos.y += offset.y

                # recalculate object sides for future collision checks in the same frame
                sides = self.calculate_object_sides()

        # check bounds of screen
        self.pos.x = min(max(self.pos.x, self.hit_box.x), gc.Window.game_size[0] - self.hit_box.x)
        self.pos.y = min(max(self.pos.y, self.hit_box.y), gc.Window.game_size[1] - self.hit_box.y)

        return v.point_to(prev_pos, self.pos).magnitude()

    def collides(self, obj2: GameObject) -> bool:
        sides_1 = self.calculate_object_sides()
        sides_2 = obj2.calculate_object_sides()
        return overlaps(sides_1, sides_2)

    def calculate_object_sides(self) -> tuple:
        return (
            self.pos.x - self.hit_box.x,  # left
            self.pos.x + self.hit_box.x,  # right
            self.pos.y - self.hit_box.y,  # top
            self.pos.y + self.hit_box.y  # bottom
        )


def overlaps(sides_a: tuple, sides_b: tuple) -> bool:
    if sides_a[0] > sides_b[1] or\
       sides_a[1] < sides_b[0] or\
       sides_a[2] > sides_b[3] or\
       sides_a[3] < sides_b[2]:
        return False
    return True
