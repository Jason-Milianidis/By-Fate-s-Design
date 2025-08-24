import pygame
from Engine import GameContainer
from Engine.SceneManager import Scene


class FloorScene(Scene):
    def __init__(self, gc: GameContainer):
        super().__init__(self, "Floor Scene", gc)

    def update(self) -> None:
        self.gc.Input.update()
        if self.gc.Input.get_input(pygame.K_ESCAPE):
            self.gc.EventManager.close_game()

        super().update_objects()

    def render(self) -> None:
        super().render_objects()
