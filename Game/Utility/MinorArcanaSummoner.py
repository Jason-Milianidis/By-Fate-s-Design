from __future__ import annotations
from typing import Optional
from Engine.Vectors import Vector, map_value
import Engine.GameContainer as GameContainer
from Engine.SceneManager import Scene
from enum import Enum
import random

from Game.Objects.EnemySpawningArea import EnemySpawningArea

from Game.Objects.Staves.StavesLow import StavesLow
from Game.Objects.Staves.StavesMid import StavesMid
from Game.Objects.Staves.StavesHigh import StavesHigh

from Game.Objects.Moons.MoonsLow import MoonsLow
from Game.Objects.Moons.MoonsMid import MoonsMid
from Game.Objects.Moons.MoonsHigh import MoonsHigh

from Game.Objects.Chalices.ChalicesLow import ChalicesLow
from Game.Objects.Chalices.ChalicesMid import ChalicesMid
from Game.Objects.Chalices.ChalicesHigh import ChalicesHigh

from Game.Objects.Tombs.TombsLow import TombsLow
from Game.Objects.Tombs.TombsMid import TombsMid
from Game.Objects.Tombs.TombsHigh import TombsHigh


# noinspection PyTypeChecker
def create_enemy(gc: GameContainer, suit: int | ArcanaType = None, number: int | ArcanaType = None, pos: Vector = None, scene: Scene = None) -> None:
    if scene is None:
        scene = gc.current_scene

    if suit is None:
        suit = random.choice([ArcanaType.STAVES, ArcanaType.TOMBS, ArcanaType.CHALICES, ArcanaType.MOONS])
    if isinstance(suit, int):
        suit = to_suit(suit)

    if number is None:
        number = random.choice([ArcanaType.TWO, ArcanaType.THREE, ArcanaType.FOUR, ArcanaType.FIVE, ArcanaType.SIX,
                                ArcanaType.SEVEN, ArcanaType.EIGHT, ArcanaType.NINE, ArcanaType.TEN])
    if isinstance(number, int):
        number = to_minor_arcana_number(number)

    if pos is None:
        area = random.choice([area for area in gc.current_scene.objects if isinstance(area, EnemySpawningArea)])
        pos = Vector(
            map_value(random.random(), 0, 1, area.pos.x - area.hit_box.x, area.pos.x + area.hit_box.x),
            map_value(random.random(), 0, 1, area.pos.y - area.hit_box.y, area.pos.y + area.hit_box.y)
        )

    enemy = None
    match suit:
        case ArcanaType.STAVES:
            match number:
                case ArcanaType.TWO | ArcanaType.THREE | ArcanaType.FOUR:
                    enemy = StavesLow(gc, pos, number.value, _get_sprite(number.value))
                case ArcanaType.FIVE | ArcanaType.SIX | ArcanaType.SEVEN | ArcanaType.EIGHT:
                    enemy = StavesMid(gc, pos, number.value, _get_sprite(number.value))
                case ArcanaType.NINE | ArcanaType.TEN:
                    enemy = StavesHigh(gc, pos, number.value, _get_sprite(number.value))
        case ArcanaType.MOONS:
            match number:
                case ArcanaType.TWO | ArcanaType.THREE | ArcanaType.FOUR:
                    enemy = MoonsLow(gc, pos, number.value, _get_sprite(number.value))
                case ArcanaType.FIVE | ArcanaType.SIX | ArcanaType.SEVEN | ArcanaType.EIGHT:
                    enemy = MoonsMid(gc, pos, number.value, _get_sprite(number.value))
                case ArcanaType.NINE | ArcanaType.TEN:
                    enemy = MoonsHigh(gc, pos, number.value, _get_sprite(number.value))
        case ArcanaType.CHALICES:
            match number:
                case ArcanaType.TWO | ArcanaType.THREE | ArcanaType.FOUR:
                    enemy = ChalicesLow(gc, pos, number.value, _get_sprite(number.value))
                case ArcanaType.FIVE | ArcanaType.SIX | ArcanaType.SEVEN | ArcanaType.EIGHT:
                    enemy = ChalicesMid(gc, pos, number.value, _get_sprite(number.value))
                case ArcanaType.NINE | ArcanaType.TEN:
                    enemy = ChalicesHigh(gc, pos, number.value, _get_sprite(number.value))
        case ArcanaType.TOMBS:
            match number:
                case ArcanaType.TWO | ArcanaType.THREE | ArcanaType.FOUR:
                    enemy = TombsLow(gc, pos, number.value, _get_sprite(number.value))
                case ArcanaType.FIVE | ArcanaType.SIX | ArcanaType.SEVEN | ArcanaType.EIGHT:
                    enemy = TombsMid(gc, pos, number.value, _get_sprite(number.value))
                case ArcanaType.NINE | ArcanaType.TEN:
                    enemy = TombsHigh(gc, pos, number.value, _get_sprite(number.value))

    if enemy is not None:
        scene.instance_create(enemy)


def _get_sprite(number: int) -> str:
    match number:
        case 2: return "Two"
        case 3: return "Three"
        case 4: return "Four"
        case 5: return "Five"
        case 6: return "Six"
        case 7: return "Seven"
        case 8: return "Eight"
        case 9: return "Nine"
        case 10: return "Ten"
        case 11: return "Page"
        case 12: return "Knight"
        case 13: return "Queen"
        case 14: return "King"
        case 15: return "Ace"


def to_suit(suit: int) -> Optional[ArcanaType]:
    match suit:
        case 0: return ArcanaType.STAVES
        case 1: return ArcanaType.TOMBS
        case 2: return ArcanaType.CHALICES
        case 3: return ArcanaType.MOONS
        case _: return None


def to_minor_arcana_number(suit: int) -> Optional[ArcanaType]:
    match suit:
        case 2: return ArcanaType.TWO
        case 3: return ArcanaType.THREE
        case 4: return ArcanaType.FOUR
        case 5: return ArcanaType.FIVE
        case 6: return ArcanaType.SIX
        case 7: return ArcanaType.SEVEN
        case 8: return ArcanaType.EIGHT
        case 9: return ArcanaType.NINE
        case 10: return ArcanaType.TEN
        case _: return None


class ArcanaType(Enum):
    # Minor Arcana Suits
    STAVES = 0
    TOMBS = 1
    CHALICES = 2
    MOONS = 3

    # Minor Arcana Numbers
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    PAGE = 11
    KNIGHT = 12
    QUEEN = 13
    KING = 14
    ACE = 15

    # Major Arcana
    THE_FOOL = 1
    THE_MAGICIAN = 2
    WHEEL_OF_FORTUNE = 3
    THE_HANGED_MAN = 4
    DEATH = 5
    TEMPERANCE = 6
    THE_TOWER = 7
    THE_MOON = 8
    THE_WORLD = 9
