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
        if self.type == 'USER':
            while True:
                try:
                    return self.shot_by_input(cur_shot)
                except:
                    print('Oops, wrong card!')
        if cur_shot.is_friend(self.team) and cur_shot.big > CARDS.index('0'):
            return Shot(team=self.team)
        else:
            return self.shot_by_type(cur_shot)

    def shot_by_input(self, cur_shot):
        print('Current cards: ', end='')
        self.show_cards()
        print('Please type your next shot:')
        cards_str = input().strip(' \n')
        if cards_str == 'pass':
            return Shot(team=self.team)
        cards_list = sorted([CARDS.index(char) for char in cards_str])
        if self.check_cards_valid(cards_list):
            big = self.get_big(cards_list)
            # print(f"cards_str={cards_str}, cards_list={cards_list}, big={big}")
            if cur_shot.type == 0 \
                    or cur_shot.type == len(cards_list) and big > cur_shot.big:
                [self.remove_card(card) for card in cards_list]
                return Shot(cards=cards_str, type=len(cards_str), big=big, team=self.team)
        print('Oops, wrong card!')
        return self.shot_by_input(cur_shot)

    def check_cards_valid(self, shot_cards):
        if len(shot_cards) not in [1, 2, 3, 5] \
                or len(shot_cards) in [1, 2, 3] and len(set(shot_cards)) != 1:
            # print(f"len={len(shot_cards)}, len_set={len(set(shot_cards))}")
            return False
        cur_cards = [card.num for card in self.cards]
        for shot_card in shot_cards:
            # print(f"card={shot_card}, cards={str(cur_cards)}")
            if shot_card not in cur_cards:
                return False
            cur_cards.remove(shot_card)
        return True

    @staticmethod
    def get_big(cards):
        # type = 1, 2, 3 or straight
        if len(cards) in [1, 2, 3] \
                or cards[0] + 1 == cards[1] and cards[1] + 1 == cards[2]:
            return cards[-1]
        # type = 5
        for card in cards:
            if cards.count(card) >= 3:
                return card

    def shot_by_type(self, cur_shot):
        # Bigger than my biggest
        if self.cards[0].num <= cur_shot.big:
            return Shot(team=self.team)
        if cur_shot.type == 0:
            return self.new_round_shot(cur_shot)
        i = len(self.cards) - 1
        # Locate bigger
        while i >= 0 and self.cards[i].num <= cur_shot.big:
            i -= 1
        # Locate type
        while i >= 0:
            num = self.cards[i].num
            card_type = 1
            while card_type < cur_shot.type and i > 0 and self.cards[i-1].num == num:
                i -= 1
                card_type += 1
            if card_type == cur_shot.type:
                [self.remove_card(num) for i in range(card_type)]
                return Shot(cards=''.join([CARDS[num] for i in range(card_type)]), type=card_type, big=num, team=self.team)
            else:
                i -= 1
        return Shot(team=self.team)

    def new_round_shot(self, cur_shot):
        num = self.cards[-1].num
        card_type = 1
        i = len(self.cards) - 2
        while i >= 0 and self.cards[i].num == num:
            i -= 1
            card_type += 1
            if card_type == 3:
                break
        [self.remove_card(num) for i in range(card_type)]
        return Shot(cards=''.join([CARDS[num] for i in range(card_type)]), type=card_type, big=num, team=self.team)

    def remove_card(self, card_num):
        cards = self.cards.copy()
        for i in range(len(self.cards)-1, -1, -1):
            if cards[i].num == card_num:
                cards.pop(i)
                break
        self.cards = cards

    def is_finish(self):
        return len(self.cards) == 0
