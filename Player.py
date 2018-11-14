import functools
from Shot import Shot
from Card import Card


COLORS = ['spade', 'heart', 'club', 'diamond']
CARDS = ['3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A', '2', '小', '大']


class Player:
    def __init__(self):
        self.cards = list()
        self.team = 2
        self.type = 'AI'

    def sort(self):
        self.cards = sorted(self.cards, key=functools.cmp_to_key(Card.cmp), reverse=True)

    def show_cards(self):
        rs = ''.join([each.card for each in self.cards])
        print(f"{rs}, len={len(rs)}")

    def add_card(self, card):
        color = card // len(CARDS)
        num = card % len(CARDS)
        self.cards.append(Card(num, color, CARDS[num]))
        if len(self.cards) == 27:
            self.sort()

    def next_shot(self, cur_shot):
        if cur_shot.is_friend(self.team) and cur_shot.big > CARDS.index('0'):
            return Shot(team=self.team)
        else:
            return self.shot_by_type(cur_shot)

    def shot_by_type(self, cur_shot):
        # Bigger than my biggest
        if self.cards[0].num <= cur_shot.big:
            return Shot(team=self.team)
        if cur_shot.type == 0:
            num = self.cards[-1].num
            type = 1
            i = len(self.cards) - 2
            while i >= 0 and self.cards[i].num == num:
                i -= 1
                type += 1
                if type == 3:
                    break
            self.remove_card(num, type)
            return Shot(cards=''.join([CARDS[num] for i in range(type)]), type=type, big=num, team=self.team)
        i = len(self.cards) - 1
        # Locate bigger
        while i >= 0 and self.cards[i].num <= cur_shot.big:
            i -= 1
        # Locate type
        while i >= 0:
            num = self.cards[i].num
            type = 1
            while type < cur_shot.type and i > 0 and self.cards[i-1].num == num:
                i -= 1
                type += 1
            if type == cur_shot.type:
                self.remove_card(num, type)
                return Shot(cards=''.join([CARDS[num] for i in range(type)]), type=type, big=num, team=self.team)
            else:
                i -= 1
        return Shot(team=self.team)

    def remove_card(self, card_num, num):
        cards = self.cards.copy()
        for i in range(len(self.cards)-1, -1, -1):
            if num == 0:
                break
            elif cards[i].num == card_num:
                cards.pop(i)
                num -= 1
        self.cards = cards

    def is_finish(self):
        return len(self.cards) == 0
