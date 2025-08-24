from __future__ import annotations
import pygame
import Engine.GameContainer as Game


pygame.init()
Game.initialize()
Game.initialize_components(Game)
Game.Save.load()
Game.CardSpawner.load()
Game.Scene.load_last_level()

running = True
while running:
    Game.update_new_scene_logic()

    Game.EventManager.update()

    Game.current_scene.update()

    Game.Renderer.render()

    running = Game.EventManager.get_game_state()

    Game.Window.tick()

    Game.Window.update_fps_counter()

    Game.Audio.update_background_music()

Game.CardSpawner.save()
Game.Save.save()
Game.LevelManager.save(Game.current_scene, "current_level")

pygame.quit()
