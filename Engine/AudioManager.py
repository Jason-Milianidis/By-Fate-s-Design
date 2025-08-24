import random

import pygame
from typing import Optional

_dict: [str, pygame.mixer.Sound] = {}
_failed: [str] = []
_background: [pygame.mixer.Sound] = []
_unique: pygame.mixer.Sound
_playing_unique: bool = False
_background_playing: int
_t: float
_gc = None


def initialize(gc) -> None:
    global _background, _unique, _background_playing, _t, _gc
    _gc = gc
    _background = [_get_audio("Mesmerizing Galaxy Loop.wav"), _get_audio("Kick Shock.wav")]
    _unique = _get_audio("Obliteration.wav")
    _background_playing = random.randrange(len(_background))
    _background[_background_playing].play()
    _t = _background[_background_playing].get_length()


def _get_audio(audio: str) -> Optional[pygame.mixer.Sound]:
    if audio in _dict:
        return _dict[audio]
    try:
        sound = pygame.mixer.Sound("resources/audio/"+audio)
        _dict[audio] = sound
        return sound
    except FileNotFoundError:
        print("\033[0;31;2m Audio 'resources/audio/"+str(audio)+"' not found.\033[0;2;2m")
        _failed.append(audio)
        return None


def play(audio: str) -> None:
    if audio in _failed:
        return
    if audio not in _dict:
        sound = _get_audio(audio)
        if sound is not None:
            sound.play()
        return
    _dict[audio].play()


# noinspection PyUnresolvedReferences
def update_background_music() -> None:
    global _t, _background_playing, _playing_unique
    _t -= _gc.Window.dt
    if _t <= 0:
        _playing_unique = False
        _background[_background_playing].stop()
        _background_playing = (_background_playing + 1) % len(_background)
        _background[_background_playing].play()
        _t = _background[_background_playing].get_length()


def play_unique() -> None:
    global _t, _playing_unique
    if not _playing_unique:
        _playing_unique = True
        _background[_background_playing].fadeout(1000)
        _unique.play()
        _t = _unique.get_length()


def play_background() -> None:
    global _t, _background_playing, _playing_unique
    if _playing_unique:
        _playing_unique = False
        _unique.fadeout(1000)
        _background_playing = random.randrange(len(_background))
        _background[_background_playing].play()
        _t = _background[_background_playing].get_length()
