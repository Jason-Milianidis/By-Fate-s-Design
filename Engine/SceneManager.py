from __future__ import annotations
from abc import abstractmethod
import Engine.GameContainer as GameContainer
from typing import Optional
from Engine.GameObject import GameObject, overlaps
from Game.Objects.Player import Player
from Engine.Vectors import Vector

_gc: GameContainer = None
_scenes: [str, Scene] = {}


class Scene:
    player: Optional[Player]
    objects: [GameObject]

    @abstractmethod
    def __init__(self, child: Scene, name: str, gc: GameContainer, player: Player = None, __objects: [GameObject] = None):
        # handle objects variable
        if __objects is None:
            self.objects = []
        else:
            self.objects = __objects
        # handle player variable
        if player is not None:
            self.player = player
            self.objects.append(player)
        else:
            self.player = None
        # link scene with dictionary
        link_scene(name, child)
        self.gc = gc
        self.name = name

    def on_load(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    def update_objects(self) -> None:
        for o in self.objects:
            o.update(self.gc, self.gc.Window.dt, self.gc.Window.dt_normalized)

    @abstractmethod
    def render(self) -> None:
        pass

    def render_objects(self) -> None:
        for o in self.objects:
            o.render(self.gc, self.gc.Window.screen)

    def instance_create(self, __object: GameObject) -> None:
        self.objects.append(__object)

    def instance_destroy(self, __object: GameObject) -> None:
        if __object in self.objects:
            __object.on_death(self.gc)
            self.objects.remove(__object)

    def instance_destroy_all(self) -> None:
        self.player = None
        self.objects = []

    def exists(self, __object: GameObject) -> bool:
        return __object in self.objects

    def collides_with_player(self, __object: GameObject) -> bool:
        if self.player is None:
            return False
        player_sides = self.player.calculate_object_sides()
        object_sides = __object.calculate_object_sides()
        return overlaps(player_sides, object_sides)

    def collides_with_anything(self, __object: GameObject) -> [GameObject]:
        object_sides = __object.calculate_object_sides()
        collisions: [GameObject] = []
        for x in self.objects:
            if x is __object:
                continue
            target_sides = x.calculate_object_sides()
            if overlaps(object_sides, target_sides):
                collisions.append(x)
        return collisions

    def valid_spot(self, pos: Vector) -> bool:
        if pos.x < 0 or pos.x > self.gc.Window.game_size[0] or pos.y < 0 or pos.y > self.gc.Window.game_size[1]:
            return False
        for wall in [o for o in self.objects if o.collision]:
            wall_sides = wall.calculate_object_sides()
            if wall_sides[0] <= pos.x <= wall_sides[1] and wall_sides[2] <= pos.y <= wall_sides[3]:
                return False
        return True


def initialize(gc: GameContainer):
    global _gc
    _gc = gc


def get_scene(scene: str) -> Optional[Scene]:
    if scene in _scenes:
        return _scenes[scene]
    return None


def link_scene(name: str, scene: Scene) -> None:
    _scenes[name] = scene


def reference() -> None:
    pass


# noinspection PyUnresolvedReferences
def load_last_level() -> None:
    from Game.Objects.Wall import Wall
    match _gc.Save.get_attribute("last scene"):
        case "Level Editor" | "Level Editor Simulator":
            from Game.Scenes.LevelEditor import LevelEditor
            from Game.Scenes.LevelEditorSimulator import LevelEditorSimulator

            editor = LevelEditor(_gc)
            scene = LevelEditorSimulator(_gc, editor)

            _gc.LevelManager.load(editor, "edited_level")
            _gc.LevelManager.load(scene, "current_level")
        case "Floor Scene":
            from Game.Scenes.FloorScene import FloorScene
            scene = FloorScene(_gc)
            _gc.LevelManager.load(scene, "current_level")
            background = _gc.Save.get_attribute("last background")
            _gc.Renderer.set_background(background)
        case "Main Scene":
            from Game.Scenes.MainScene import MainScene
            scene = MainScene(_gc)
            _gc.LevelManager.load(scene, "current_level")
        case _:
            from Game.Scenes.MainScene import MainScene
            scene = MainScene(_gc)
    _gc.current_scene = scene
