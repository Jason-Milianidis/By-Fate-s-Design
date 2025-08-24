import pygame
from Engine import GameContainer
from Engine.SceneManager import Scene
import Engine.Vectors as v

from Game.Utility.Button import Button
from Game.Utility.ObjectDisplayButton import ObjectDisplayButton as DisplayButton
from Game.Utility.Draggable import Draggable


class LevelEditor(Scene):
    _buttons: [Button] = []
    _simulator = None
    _level_name = "edited_level"

    def __init__(self, gc: GameContainer):
        super().__init__(self, "Level Editor", gc)
        from Game.Scenes.LevelEditorSimulator import LevelEditorSimulator
        self._simulator = LevelEditorSimulator(gc, self)

        gc.LevelManager.load(self, "layout5")
        gc.Renderer.set_background("5")

        offset = v.Vector(40, 40)
        d: [str, object] = gc.LevelManager.get_object_list()
        for val, obj in d.items():
            if 'Game.Objects.' in str(obj):
                attributeless_object = gc.LevelManager.instantiate_attributeless_object(val)
                if not attributeless_object.make_button:
                    continue

                button = DisplayButton(
                    gc,
                    attributeless_object,
                    v.duplicate(offset),
                    v.Vector(64, 64)
                )
                self.instance_create(button)
                self._buttons.append(button)
                offset.y += 80

    def update(self) -> None:
        self.gc.Input.update()
        if self.gc.Input.get_input(pygame.K_ESCAPE):
            self.gc.EventManager.close_game()
            self.save(self.gc)
            return

        if self.gc.Input.get_input_pressed(pygame.K_p):
            self.save(self.gc)
            self.gc.LevelManager.load(self._simulator, self._level_name)
            self.gc.current_scene = self._simulator
            return

        for o in self.objects:
            if o in self._buttons:
                o.update(self.gc, self.gc.Window.dt, self.gc.Window.dt_normalized)
                if o.get_value() is not None:
                    drag = Draggable(self.gc, self.gc.LevelManager.instantiate_attributeless_object(o.get_value()), storable=False)
                    self.instance_create(drag)
                continue
            if isinstance(o, Draggable):
                o.update(self.gc, self.gc.Window.dt, self.gc.Window.dt_normalized)
                continue
            if hasattr(o, 'animation'):
                o.animation.update(self.gc.Window.dt)
            o.edit(self.gc)

    def save(self, gc: GameContainer):
        for button in self._buttons:
            self.instance_destroy(button)

        for o in self.objects:
            if hasattr(o, 'animation'):
                o.animation.reset()
        gc.LevelManager.save(self, self._level_name)

        for button in self._buttons:
            self.instance_create(button)

    def render(self) -> None:
        super().render_objects()
