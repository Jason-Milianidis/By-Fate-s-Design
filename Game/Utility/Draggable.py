import pygame

import Engine.LevelManager
from Engine.GameObject import GameObject
import Engine.Vectors as v
import Engine.GameContainer as GameContainer
from Game.Objects.Wall import Wall


class Draggable(GameObject):
    __object: GameObject
    pos: v.Vector
    _storable: bool
    _offset: v.Vector

    def __init__(self, gc: GameContainer, obj: GameObject = None, pos: v.Vector = None,
                 offset: v.Vector = v.Vector(0, 0), storable: bool = True):
        self.__object = obj
        if pos is None:
            self.pos = v.tuple_to_vector(gc.Input.mouse_pos)
        else:
            self.pos = pos
        self._storable = storable
        self._offset = offset

    def update(self, gc: GameContainer, dt: float, dt_normalized: float) -> None:
        if not gc.Input.get_button(0):
            gc.current_scene.instance_destroy(self)
            gc.current_scene.instance_create(self.__object)
            return

        if self._storable:
            self.__object.update(gc, dt, dt_normalized)
        elif hasattr(self.__object, 'animation'):
            self.__object.animation.update(dt)

        self.pos = v.tuple_to_vector(gc.Input.mouse_pos).sub(self._offset)
        self.__object.pos = self.pos

    def render(self, gc: GameContainer, screen: pygame.Surface) -> None:
        if isinstance(self.__object, Wall):
            self.__object.editing = True
            self.__object.render(gc, screen)
            return

        if getattr(self.__object, 'render', False):
            self.__object.render(gc, screen)

    def save(self) -> [str]:
        if self._storable:
            return [Engine.LevelManager.get_saved_string(self.__object, ';')]
        return None

    def load(self, gc: GameContainer, args: [str]) -> None:
        if args[1] is not None:
            gc.current_scene.instance_create(Engine.LevelManager.load_object(args[1], ';'))
            gc.current_scene.instance_destroy(self)
