from Card import Card
from Consts import CARDS


class Shot:
    def __init__(self, cards='', type=0, team=0):
        self.cards = cards
        self.type = type
        self.team = team

    def is_friend(self, t):
        return self.team == t

    def __str__(self):
        return self.cards if self.type != 0 else 'pass'

    # True if next shot bigger than current shot
    def check_big(self, next_cards):
        if isinstance(next_cards, str):
            next_cards = [CARDS.index(char) for char in next_cards]
        cur_cards = [CARDS.index(char) for char in self.cards]
        if len(cur_cards) != 5:
            return next_cards[-1] > cur_cards[-1]
        # type = 5
        my_level = Card.get_5_level(next_cards)
        cur_level = Card.get_5_level(cur_cards)
        if my_level > cur_level:
            return True
        elif my_level < cur_level:
            return False
        else:
            next_big = next_cards[0]
            for card in next_cards:
                if next_cards.count(card) == my_level:
                    next_big = card
            cur_big = cur_cards[0]
            for card in cur_cards:
                if cur_cards.count(card) == my_level:
                    cur_big = card
            return next_big > cur_big
