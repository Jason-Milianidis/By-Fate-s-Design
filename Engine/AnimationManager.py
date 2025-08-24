from __future__ import annotations
import pygame
from typing import Optional, TypedDict
import Engine.Vectors as v
import Engine.ImageManager as ImageManager

_dict_sep = "! "
_key_sep = " - "
_StageInfo = TypedDict("_StageInfo", {"variant": int, "max_frame": int, "frame_delay": float, "next": Optional[str]})


def initialize():
    pass


class Animation:
    sprite: pygame.Surface
    sprite_name: str
    frames: int = 1
    variants: int = 1
    variant_categories: int = 1
    variant_offset: int = 0
    variant_types: [str, int] = {}
    dimensions: (float, float) = (1, 1)
    current_frame: int = 0

    _stages: [str, _StageInfo] = {}
    _stage_vals: _StageInfo
    current_stage: str

    _triggers: [str, bool] = {}
    _time: float = 0

    _starting_stage = "default"

    def __init__(self, __sprite: pygame.Surface, __frames: int, __variants: int, __variant_categories: int = 1,
                 __variant: int = 0, __fps: float = 1, __max_frame: int = 1, __next: str = None):
        self.sprite = __sprite
        self.sprite_name = str(ImageManager.get_name(self.sprite))
        self.frames = __frames
        self.variants = __variants
        self.variant_categories = __variant_categories
        self.variant_offset = 0
        self.variant_types = {}
        self.dimensions = (__sprite.get_width() / __frames, __sprite.get_height() / (__variants * __variant_categories))
        self.current_frame = 0
        self._stages = {}
        self.current_stage = "default"
        self.current_variant = ""
        self._stage_vals = _make_stage(__variant, __max_frame, __fps, __next)
        self._stages[self.current_stage] = self._stage_vals
        self._triggers = {}
        self._time = 0

    def draw_frame(self, screen: pygame.Surface, pos: v.Vector, frame: int = None, variant: int = None, alpha: int = 255) -> None:
        if frame is None:
            frame = self.current_frame
        if variant is None:
            variant = self.get_current_variant() + self.variant_offset * self.variants
        origin = (self.dimensions[0] * frame, self.dimensions[1] * variant)
        self.sprite.set_alpha(alpha)
        screen.blit(
            self.sprite,
            (pos.x - self.dimensions[0] / 2, pos.y - self.dimensions[1] / 2),
            (origin, self.dimensions)
        )

    def update(self, dt: float) -> None:
        self._time += dt
        if self._time >= self._stage_vals["frame_delay"]:
            self._time %= self._stage_vals["frame_delay"]
            if self._stage_vals["next"] is not None and self.current_frame == self._stage_vals["max_frame"] - 1:
                self.set_stage(self._stage_vals["next"])
                return

            if self.current_frame < self._stage_vals["max_frame"] - 1:
                self.current_frame += 1

    def set_stage(self, tag: str) -> Animation:
        if tag in self._stages:
            self.current_stage = tag
            self._stage_vals = self._stages[tag]
            self.current_frame = 0
            self._time = 0
            if self._starting_stage == "default":
                self._starting_stage = tag
        return self

    def add_stage(self, tag: str, variant: int, max_frame: int, frame_delay: float, __next: str = None) -> Animation:
        if variant < self.variants and max_frame <= self.frames:
            self._stages[tag] = _make_stage(variant, max_frame, frame_delay, __next)
        return self

    def add_stage_fps(self, tag: str, variant: int, max_frame: int, frame_delay: float, __next: str = None) -> Animation:
        self.add_stage(tag, variant, max_frame, frame_delay / max_frame, __next)
        return self

    def set_variant(self, variant: str) -> Animation:
        if variant in self.variant_types:
            self.variant_offset = self.variant_types[variant]
            self.current_variant = variant
        return self

    def add_variant(self, variant: str, offset: int) -> Animation:
        if offset < self.variant_categories:
            self.variant_types[variant] = offset
        return self

    def get_current_variant(self) -> int:
        return self._stage_vals["variant"]

    def set_fps(self, fps: float, tag: str = None) -> None:
        if tag is None:
            tag = self.current_stage
        if tag in self._stages:
            self._stages[tag]["frame_delay"] = fps
            if tag == self.current_stage:
                self._stage_vals = self._stages[tag]

    def animation_ended(self) -> bool:
        return self._stage_vals["next"] is None and self.current_frame == self._stage_vals["max_frame"] - 1

    def trigger_at(self, stage: str, frame: int) -> bool:
        if stage in self._stages:
            trigger = stage + str(frame)
            val = self.current_stage == stage and self.current_frame == frame
            result = val and (not self._triggers[trigger] or self._triggers[trigger] is None)
            self._triggers[trigger] = val
            return result
        return False

    def reset(self) -> None:
        self.set_stage(self._starting_stage)

    def recalculate_dimensions(self) -> None:
        self.sprite = ImageManager.get_image(self.sprite_name)
        self.dimensions = (self.sprite.get_width() / self.frames, self.sprite.get_height() / (self.variants * self.variant_categories))

    def duplicate(self) -> Animation:
        animation = Animation(
            ImageManager.get_image(self.sprite_name),
            self.frames, self.variants, self.variant_categories
        )
        animation.dimensions = self.dimensions
        animation.current_frame = self.current_frame
        animation._time = self._time
        animation.set_stage(self.current_stage)
        animation.variant_offset = self.variant_offset
        animation.load(_save_stages(self._stages), _save_variants(self.variant_types))
        return animation

    def save(self) -> str:
        return ';'.join(['Animation',
                         self.sprite_name,
                         str(self.frames),
                         str(self.variants),
                         str(self.variant_categories),
                         v.tuple_to_vector(self.dimensions).save(),
                         str(self.current_frame),
                         str(self._time),
                         self.current_stage,
                         str(self.variant_offset),
                         _save_stages(self._stages),
                         _save_variants(self.variant_types)
                         ])

    def load(self, stages: str, variants: str) -> None:
        self._stages = _load_stages(stages)
        self.variant_types = _load_variants(variants)


def load(arguments: str) -> Optional[Animation]:
    args = arguments.split(';')
    if args[1] is None:
        return None
    animation = Animation(ImageManager.get_image(args[1]), int(args[2]), int(args[3]), int(args[4]))
    animation.dimensions = v.to_tuple(v.load_vector(args[5]))
    animation.current_frame = int(args[6])
    animation.variant_offset = int(args[9])
    animation._time = float(args[7])
    animation.load(args[10], args[11])
    animation.set_stage(args[8])
    return animation


def _save_stages(dictionary: dict) -> str:
    s = []
    for a in dictionary:
        val = [a]
        for b in dictionary[a]:
            val.append(str(dictionary[a][b]))
        s.append(_key_sep.join(val))
    return _dict_sep.join(s)


def _load_stages(arg: str) -> [str, _StageInfo]:
    d = {}
    # print(arg.split(_dict_sep))
    for a in arg.split(_dict_sep):
        val = a.split(_key_sep)
        __next = str(val[4])
        if __next == "None":
            __next = None
        d[val[0]] = _make_stage(int(val[1]), int(val[2]), float(val[3]), __next)
    return d


def _save_variants(dictionary: dict) -> str:
    s = []
    for val in dictionary:
        s.append(val + _key_sep + str(dictionary[val]))
    return _dict_sep.join(s)


def _load_variants(arg: str) -> [str, int]:
    d = {}
    # print(arg[:-1].split(_dict_sep))
    for val in arg[:-1].split(_dict_sep):
        if _key_sep not in val:
            continue
        sep = val.split(_key_sep)
        d[sep[0]] = int(sep[1])
    return d


def _make_stage(variant: int, max_frame: int, frame_delay: float, __next: str = None) -> _StageInfo:
    return {
        "variant": variant,
        "max_frame": max_frame,
        "frame_delay": frame_delay,
        "next": __next
    }
