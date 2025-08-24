import pygame
from Engine import GameContainer
from Engine.SceneManager import Scene
from Game.Scenes.LevelEditor import LevelEditor


class LevelEditorSimulator(Scene):
    _editor: LevelEditor

    def __init__(self, gc: GameContainer, scene: LevelEditor):
        super().__init__(self, "Level Editor Simulator", gc)
        self._editor = scene

    def update(self) -> None:
        self.gc.Input.update()
        if self.gc.Input.get_input(pygame.K_ESCAPE):
            self.gc.EventManager.close_game()
            return

        if self.gc.Input.get_input_pressed(pygame.K_p):
            self.gc.current_scene = self._editor
            return

        super().update_objects()

    def render(self) -> None:
        super().render_objects()
