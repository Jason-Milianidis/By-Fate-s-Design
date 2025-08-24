current_scene = None
_prev_current_scene = None
_imported = False

Window = None
Input = None
Renderer = None
Scene = None
EventManager = None
ImageManager = None
AnimationManager = None
Audio = None
LevelManager = None
Font = None
CardSpawner = None
Save = None


def initialize() -> None:
    global _imported
    if _imported:
        return
    _imported = True

    # import everything
    import Engine.WindowManager as __Window
    import Engine.InputManager as __Input
    import Engine.Renderer as __Renderer
    import Engine.SceneManager as __Scene
    import Engine.EventManager as __EventManager
    import Engine.ImageManager as __ImageManager
    import Engine.AnimationManager as __AnimationManager
    import Engine.AudioManager as __Audio
    import Engine.LevelManager as __LevelManager
    import Engine.FontManager as __Font
    import Engine.CardSpawner as __CardSpawner
    import Engine.SaveManager as __Save

    # store everything
    global Window, Input, Renderer, Scene, EventManager, ImageManager, AnimationManager, Audio, LevelManager, Font, CardSpawner, Save
    Window = __Window
    Input = __Input
    Renderer = __Renderer
    Scene = __Scene
    EventManager = __EventManager
    ImageManager = __ImageManager
    AnimationManager = __AnimationManager
    Audio = __Audio
    LevelManager = __LevelManager
    Font = __Font
    CardSpawner = __CardSpawner
    Save = __Save


# noinspection PyUnresolvedReferences
def initialize_components(game) -> None:
    global Window, Input, Renderer, Scene, EventManager, ImageManager, AnimationManager, Audio, LevelManager, Font, CardSpawner, Save
    Window.initialize(game)
    Input.initialize(Window)
    Renderer.initialize(game)
    Scene.initialize(game)
    EventManager.initialize()
    ImageManager.initialize(game)
    AnimationManager.initialize()
    Audio.initialize(game)
    LevelManager.initialize(game)
    Font.initialize(game)
    CardSpawner.initialize(game)
    Save.initialize(game)


def reference() -> None:
    pass


# noinspection PyUnresolvedReferences
def update_new_scene_logic() -> None:
    global _prev_current_scene
    if _prev_current_scene != current_scene:
        if current_scene is not None:
            current_scene.on_load()
            Save.set_attribute("last scene", current_scene.name)
    _prev_current_scene = current_scene
