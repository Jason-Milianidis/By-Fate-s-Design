import pygame

from Engine import GameContainer, Vectors as v
# from Engine.Collidable import Collidable
from Engine.GameObject import GameObject


class EnemySpawningArea(GameObject):
    def __init__(self, gc: GameContainer, pos: v.Vector = v.Vector(0, 0), hit_box: v.Vector = v.Vector(100, 50)):
        super().__init__(gc, pos, hit_box)

        scale = gc.Window.scale()
        self.minimum_hit_box = v.Vector(100 * scale[0], 50 * scale[1])
        # self.minimum_hit_box = v.Vector(0, 0)
        self.highlight = [False, False, False, False, False]
        self.leeway = tuple([20 * i for i in scale])
        self.offset = v.Vector(0, 0)
        self.editing = False

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        pass

    def edit(self, gc: GameContainer) -> None:
        self.editing = True
        if gc.Input.get_input(pygame.K_LCTRL):
            return

        if (self.highlight[0] or self.highlight[1] or self.highlight[2] or self.highlight[3] or self.highlight[4]) and gc.Input.get_input(pygame.K_z):
            self.hit_box = v.Vector(50, 50)

        mouse = gc.Input.mouse_pos

        if gc.Input.get_button_pressed(2) and self.highlight[4]:
            gc.current_scene.instance_destroy(self)

        if gc.Input.get_button_pressed(0):
            self.offset = v.point_to(v.tuple_to_vector(mouse), self.pos)

        if gc.Input.get_button(0):
            if self.highlight[4]:
                self.pos = v.tuple_to_vector(mouse).add(self.offset)
            else:
                new_box = [self.pos.x - self.hit_box.x, self.pos.y - self.hit_box.y,
                           self.pos.x + self.hit_box.x, self.pos.y + self.hit_box.y]
                if self.highlight[0]:
                    new_box[0] = min(mouse[0], new_box[2] - self.minimum_hit_box.x)
                if self.highlight[1]:
                    new_box[1] = min(mouse[1], new_box[3] - self.minimum_hit_box.y)
                if self.highlight[2]:
                    new_box[2] = max(mouse[0], new_box[0] + self.minimum_hit_box.x)
                if self.highlight[3]:
                    new_box[3] = max(mouse[1], new_box[1] + self.minimum_hit_box.y)
                self.pos = v.Vector((new_box[0] + new_box[2]) / 2, (new_box[1] + new_box[3]) / 2)
                self.hit_box = v.Vector(
                    abs(new_box[0] - new_box[2]) / 2,
                    abs(new_box[1] - new_box[3]) / 2)
        else:
            self.highlight[0] = self.pos.x - self.hit_box.x - self.leeway[0] < mouse[0] < self.pos.x - self.hit_box.x + self.leeway[0] \
                and self.pos.y - self.hit_box.y - self.leeway[1] < mouse[1] < self.pos.y + self.hit_box.y + self.leeway[1]  # left
            self.highlight[1] = self.pos.x - self.hit_box.x - self.leeway[0] < mouse[0] < self.pos.x + self.hit_box.x + self.leeway[0] \
                and self.pos.y - self.hit_box.y - self.leeway[1] < mouse[1] < self.pos.y - self.hit_box.y + self.leeway[1]  # top
            self.highlight[2] = self.pos.x + self.hit_box.x - self.leeway[0] < mouse[0] < self.pos.x + self.hit_box.x + self.leeway[0] \
                and self.pos.y - self.hit_box.y - self.leeway[1] < mouse[1] < self.pos.y + self.hit_box.y + self.leeway[1]  # right
            self.highlight[3] = self.pos.x - self.hit_box.x - self.leeway[0] < mouse[0] < self.pos.x + self.hit_box.x + self.leeway[0] \
                and self.pos.y + self.hit_box.y - self.leeway[1] < mouse[1] < self.pos.y + self.hit_box.y + self.leeway[1]  # bottom
            self.highlight[4] = self.pos.x - self.hit_box.x + self.leeway[0] < mouse[0] < self.pos.x + self.hit_box.x - self.leeway[0] \
                and self.pos.y - self.hit_box.y + self.leeway[1] < mouse[1] < self.pos.y + self.hit_box.y - self.leeway[1]

    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        if not self.editing:
            return
        pygame.draw.rect(screen, "orange", (self.pos.x - self.hit_box.x, self.pos.y - self.hit_box.y,
                                            self.hit_box.x * 2, self.hit_box.y * 2), 3, 5)
        if self.highlight[0]:
            pygame.draw.line(screen, "red", (self.pos.x - self.hit_box.x, self.pos.y + self.hit_box.y),
                             (self.pos.x - self.hit_box.x, self.pos.y - self.hit_box.y), 2)
        if self.highlight[1]:
            pygame.draw.line(screen, "red", (self.pos.x - self.hit_box.x, self.pos.y - self.hit_box.y),
                             (self.pos.x + self.hit_box.x, self.pos.y - self.hit_box.y), 2)
        if self.highlight[2]:
            pygame.draw.line(screen, "red", (self.pos.x + self.hit_box.x, self.pos.y - self.hit_box.y),
                             (self.pos.x + self.hit_box.x, self.pos.y + self.hit_box.y), 2)
        if self.highlight[3]:
            pygame.draw.line(screen, "red", (self.pos.x + self.hit_box.x, self.pos.y + self.hit_box.y),
                             (self.pos.x - self.hit_box.x, self.pos.y + self.hit_box.y), 2)
        if self.highlight[4]:
            pygame.draw.rect(screen, "red", (self.pos.x - self.hit_box.x, self.pos.y - self.hit_box.y,
                                             self.hit_box.x * 2, self.hit_box.y * 2), 3, 5)

    def save(self) -> [str]:
        return [self.pos.save(), self.hit_box.save()]

    def load(self, gc: GameContainer, args: [str]) -> None:
        self.pos = v.load_vector(args[1])
        self.hit_box = v.load_vector(args[2])
