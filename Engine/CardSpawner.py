from Game.Objects.Card import Card
import Engine.Vectors as v
from Game.Utility.MinorArcanaSummoner import ArcanaType as at
import random

_gc = None
_card_number = 2
_min_card_number = 0
_temp_min_card_number = -1


def initialize(gc) -> None:
    global _gc
    _gc = gc


# noinspection PyUnresolvedReferences
def make_card(pos: v.Vector, major: bool = None, card_id: at = None, suit: at = None,
              go_to_pos: v.Vector = None, time_to_go: float = 1, movable: bool = True) -> Card:
    if major is None:
        major = random.random() < 0.5

    if major:
        if card_id is None:
            card_id = random.randint(1, 9)
        else:
            card_id = card_id.value

        card = Card(_gc, pos, True, card_id, None, go_to_pos, time_to_go, movable)
    else:
        if card_id is None:
            card_id = random.randint(1, 9)
        else:
            card_id = card_id.value - 1

        if suit is None:
            suit = random.randint(0, 3)
        else:
            suit = suit.value

        card = Card(_gc, pos, False, card_id, suit, go_to_pos, time_to_go, movable)

    return card


# noinspection PyTypeChecker
def create_major_card(pos: v.Vector) -> Card:
    # noinspection PyUnresolvedReferences
    d = _gc.Window.game_size

    selected_card = None
    # noinspection PyUnresolvedReferences
    if _gc.current_scene.name == "Main Scene":
        selected_card = at.THE_TOWER

    card = make_card(v.duplicate(pos), True, selected_card, go_to_pos=v.Vector(d[0] / 2, d[1] / 3), movable=False)
    card.closable = False
    return card


# noinspection PyUnresolvedReferences
def create_minor_cards(card: Card) -> [Card]:
    if not card.major:
        return []

    global _temp_min_card_number, _card_number, _min_card_number
    cards = []
    pos = card.pos
    _temp_min_card_number = -1

    match card.value:
        case at.THE_FOOL.value:
            for card in _add_cards_of_type(cards, pos):
                card.visible = card.openable = False
            _temp_min_card_number = 0
            _gc.Audio.play("Fool.wav")
        case at.THE_MAGICIAN.value:
            _add_cards_of_type(cards, pos, at.STAVES)
            _gc.Audio.play("Magician.mp3")
        case at.WHEEL_OF_FORTUNE.value:
            if random.random() < 0.5:
                _add_cards_of_type(cards, pos, [at.STAVES, at.TOMBS, at.CHALICES, at.MOONS], at.TWO,
                                   time_delay=0.5, fixed_lists=True, card_number=4)
                _temp_min_card_number = 1
            else:
                _add_cards_of_type(cards, pos, [at.STAVES, at.TOMBS, at.CHALICES, at.MOONS], at.TEN,
                                   time_delay=0.5, fixed_lists=True, card_number=4)
                _temp_min_card_number = min(_min_card_number, 4)
            _gc.Audio.play("Wheel of Fortune.wav")
        case at.THE_HANGED_MAN.value:
            _add_cards_of_type(cards, pos, at.TOMBS)
            _gc.Audio.play("Hanged Man.wav")
        case at.DEATH.value:
            _add_cards_of_type(cards, pos, number=[at.EIGHT, at.NINE, at.TEN])
            _temp_min_card_number = _card_number
            _gc.Audio.play("Death.wav")
        case at.TEMPERANCE.value:
            _add_cards_of_type(cards, pos, at.CHALICES)
            _gc.Audio.play("Temperance.wav")
        case at.THE_TOWER.value:
            _card_number += 1
            _min_card_number += 1
            _add_cards_of_type(cards, pos)
            _gc.Audio.play("Tower.wav")
        case at.THE_MOON.value:
            _add_cards_of_type(cards, pos, at.MOONS, time_delay=0.5)
            _gc.Audio.play("Moon.wav")
        case at.THE_WORLD.value:
            _add_cards_of_type(cards, pos,
                               random.choice([at.STAVES, at.MOONS, at.CHALICES, at.TOMBS]),
                               [at.TWO, at.THREE, at.FOUR, at.FIVE, at.SIX, at.SEVEN, at.EIGHT, at.NINE, at.TEN],
                               time_delay=1,
                               fixed_lists=True,
                               ordered_lists=True,
                               card_number=9
                               )
            _gc.Audio.play("World.wav")

    return cards


def _add_cards_of_type(cards: [Card],
                       pos: v.Vector,
                       suit: [at] or at = None,
                       number: [at] or at = None,
                       time_to_go: float = 1,
                       time_delay: float = 0,
                       left_to_right: bool = False,
                       fixed_lists: bool = False,
                       ordered_lists: bool = False,
                       card_number: int = None) -> [Card]:
    if card_number is None:
        card_number = _card_number
    if card_number <= 0:
        return cards

    # if empty list is given, default to random
    if isinstance(number, list) and len(number) == 0:
        number = None
    if isinstance(suit, list) and len(suit) == 0:
        suit = None

    # noinspection PyUnresolvedReferences
    d = _gc.Window.game_size
    c = []
    number_selected = number
    suit_selected = suit

    if left_to_right:
        time_delay /= card_number
    else:
        time_delay /= card_number / 2

    # keep a copy of the original lists
    number_list = suit_list = []
    if fixed_lists:
        if isinstance(number, list):
            number_list = [i for i in number]
        if isinstance(suit, list):
            suit_list = [i for i in suit]

    # create _card_number cards
    for i in range(1, card_number + 1):
        # if a list is given, select an element from it
        if isinstance(number, list):
            if ordered_lists:
                number_selected = number[0]
            else:
                number_selected = random.choice(number)

            if fixed_lists:
                number.remove(number_selected)
                if len(number) == 0:
                    number = [i for i in number_list]
        if isinstance(suit, list):
            if ordered_lists:
                suit_selected = suit[0]
            else:
                suit_selected = random.choice(suit)

            if fixed_lists:
                suit.remove(suit_selected)
                if len(suit) == 0:
                    suit = [i for i in suit_list]

        # calculate additional movement delay
        if left_to_right:
            extra_delay = time_delay * (i - 1)
        else:
            extra_delay = time_delay * abs(i - 1 - (card_number - 1) / 2)

        # create the card and add it to the list
        card = make_card(
            v.duplicate(pos),
            False,
            number_selected,
            suit_selected,
            go_to_pos=v.Vector(d[0] / (card_number + 1) * i, d[1] / 3 * 2),
            time_to_go=time_to_go + extra_delay,
            movable=False
        )
        card.visible = True
        c.append(card)

    # add cards generated to the list given
    [cards.append(card) for card in c]
    return cards


def min_card_number() -> int:
    if _temp_min_card_number >= 0:
        return _temp_min_card_number
    return _min_card_number


def get_normal_card_selection_number() -> int:
    return _min_card_number


# noinspection PyUnresolvedReferences
def save() -> None:
    _gc.Save.set_attribute("card number", _card_number)
    _gc.Save.set_attribute("min card number", _min_card_number)
    _gc.Save.set_attribute("temp card number", _temp_min_card_number)


# noinspection PyUnresolvedReferences
def load() -> None:
    global _card_number, _min_card_number, _temp_min_card_number
    _card_number = _gc.Save.get_attribute("card number")
    _min_card_number = _gc.Save.get_attribute("min card number")
    _temp_min_card_number = _gc.Save.get_attribute("temp card number")
