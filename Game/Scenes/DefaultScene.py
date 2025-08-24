import pygame
from Engine import GameContainer
from Engine.SceneManager import Scene


class DefaultScene(Scene):
    def __init__(self, gc: GameContainer):
        super().__init__(self, "Default Scene", gc)
        gc.LevelManager.load(self, "default_level")

    def update(self) -> None:
        self.gc.Input.update()
        if self.gc.Input.get_input(pygame.K_ESCAPE):
            self.gc.EventManager.close_game()

        if self.gc.Input.get_input(pygame.K_p):
            self.gc.LevelManager.save(self, "test")

        super().update_objects()

    def render(self) -> None:
        super().render_objects()
