import Engine.GameContainer as GameContainer
from typing import Optional
from Engine.GameObject import GameObject
from Engine.SceneManager import Scene
from Game.Objects.Player import Player
import Engine.Vectors as v
import os
import sys
import inspect
import re

_directory: str = "resources/levels/"
_extension: str = ".lvl"
_delimiter: str = ", "
_dictionary: [str, object] = {}
_gc: GameContainer = None
_initialized: bool = False


def initialize(gc: GameContainer) -> None:
    global _dictionary, _gc, _initialized
    _gc = gc
    _initialized = True

    """
    # import everything
    import_directory("Game/Objects")
    import_directory("Game/Utility")
    """
    _import_objects()

    # categorize everything
    for mod in sys.modules.keys():
        if load_from_directory(mod, "Game.Objects."):
            continue
        if load_from_directory(mod, "Game.Utility."):
            continue


def import_directory(path: str) -> None:
    # get absolute filepath of target directory
    p = os.path.join("", path)

    # for all *.py files found in the directory, import them
    for py in [f[:-3] for f in os.listdir(p) if f.endswith('.py') and f != '__init__.py']:
        directory_path = path.split('/')
        directory_path.append(py)
        mod = __import__('.'.join(directory_path), fromlist=[py])
        classes = [getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type)]
        for cls in classes:
            setattr(sys.modules['.'.join(path.split('/'))], cls.__name__, cls)

    # recursively import all *.py files found in subdirectories too
    for folder in [f[0] for f in os.walk(path)]:
        if '__pycache__' in folder or folder == path:
            continue
        import_directory(re.sub("\\\\", "/", folder))


def load_from_directory(mod, path: str) -> bool:
    global _dictionary
    if mod.startswith(path):
        for name, obj in inspect.getmembers(sys.modules.get(mod)):
            # only store the classes found in the imported files
            if inspect.isclass(obj) and re.sub(".*\\.", "", mod) == name:
                _dictionary[name] = obj
                return True
    return False


def list_item(key: str, __object: object):
    global _dictionary
    _dictionary[key] = __object


def save(scene: Scene, filename: str) -> None:
    if not _initialized:
        return
    file = open(_directory+filename+_extension, "w")

    # noinspection PyUnresolvedReferences
    scaling = tuple([1 / i for i in _gc.Window.scale()])

    for o in scene.objects:
        sav = get_saved_string(o, scaling=scaling)
        if sav is None:
            continue

        file.write(sav+"\n")

    file.close()


def get_saved_string(__object: GameObject, delimiter: str = _delimiter, scaling: (float, float) = None) -> Optional[str]:
    if __object is None:
        return None

    if scaling is None:
        # noinspection PyUnresolvedReferences
        scaling = tuple([1 / i for i in _gc.Window.scale()])

    prev_pos = v.Vector(0, 0)
    if hasattr(__object, "pos"):
        prev_pos = v.duplicate(__object.pos)
        __object.pos.scale(scaling)

    prev_hit_box = v.Vector(-1, -1)
    if hasattr(__object, "hit_box"):
        prev_hit_box = v.duplicate(__object.hit_box)
        __object.hit_box.scale(scaling)

    sav = get_save_attributes(__object)

    if hasattr(__object, "pos"):
        __object.pos = prev_pos
    if hasattr(__object, "hit_box"):
        __object.hit_box = prev_hit_box

    if sav is None:
        return None
    return delimiter.join(sav)


def get_save_attributes(__object: GameObject) -> Optional[str]:
    sav = __object.save()
    if sav is None:
        return None
    sav.insert(0, __object.__class__.__name__)
    return sav


def load(scene: Scene, filename: str):
    if not _initialized:
        return

    scene.instance_destroy_all()
    try:
        file = open(_directory+filename+_extension, "r")
    except FileNotFoundError:
        print("\033[0;31;2mLevel '" + _directory + filename + _extension + "' not found. Empty Scene Loaded\033[0;2;2m")
        return

    # noinspection PyUnresolvedReferences
    scale = _gc.Window.scale()
    for args in file:
        o = load_object(args, scale=scale)
        if o is None:
            continue

        if isinstance(o, Player):
            scene.player = o

        # create the object in the scene
        scene.instance_create(o)
    file.close()


def load_object(args: str, delimiter: str = _delimiter, scale: (float, float) = None) -> Optional[GameObject]:
    if not _initialized:
        return

    if scale is None:
        # noinspection PyUnresolvedReferences
        scale = _gc.Window.scale()

    # get identifier
    vals = args.split(delimiter)
    identifier = vals[0]

    if identifier not in _dictionary:
        return None

    if identifier == "Player":  # special case for Player object
        o = Player(_gc)
    else:  # create object depending on the identifier
        o = _dictionary[identifier](_gc)

    # finish initialization of object through the arguments given
    o.load(_gc, vals)

    if hasattr(o, "pos"):
        o.pos.scale(scale)

    if hasattr(o, "hit_box"):
        o.hit_box.scale(scale)

    if hasattr(o, "animation"):
        o.animation.recalculate_dimensions()

    return o


def instantiate_attributeless_object(key: str) -> Optional[object]:
    if not _initialized:
        return None
    global _dictionary

    if key in _dictionary:
        return _dictionary[key](_gc)
    return None


def get_object_list() -> [str, object]:
    global _dictionary
    return _dictionary.copy()


def _import_objects() -> None:
    # imports = ["ContinueButton", "LevelComplete", "LabelButton", "ObjectDisplayButton", "Patterns.LazerBlast"]
    # for i in imports:
    #     __import__("Game.Utility." + i)
    import Game.Utility.ContinueButton as a
    import Game.Utility.LevelComplete as b
    import Game.Utility.LabelButton as c
    import Game.Utility.ObjectDisplayButton as d
    import Game.Utility.Patterns.LazerBlast as e
    reference = [a, b, c, d, e]
    print(reference)
