import pygame
from Engine import GameContainer
from Engine.SceneManager import Scene


class MainScene(Scene):
    def __init__(self, gc: GameContainer):
        super().__init__(self, "Main Scene", gc)
        gc.LevelManager.load(self, "layout0")
        gc.Renderer.set_background("0")

    def on_load(self) -> None:
        self.gc.Save.set_default_values()
        self.gc.CardSpawner.load()
        self.player.update_hp_from_attributes()

    def update(self) -> None:
        self.gc.Input.update()
        if self.gc.Input.get_input(pygame.K_ESCAPE):
            self.gc.EventManager.close_game()

        super().update_objects()

    def render(self) -> None:
        super().render_objects()
