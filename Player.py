import functools
from Shot import Shot
from Card import Card
from Consts import COLORS, CARDS


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
        if len(self.cards) == 0:
            return
        # for k, v in Card.split_cards(self.cards).items():
        #     print(f"{k}: {str(v)}")
        # print(f"All 5 combo: {str(self.form_5())}")

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
        if self.check_friend_shot(cur_shot):
            return Shot(team=self.team)
        else:
            return self.shot_by_type(cur_shot)

    def check_friend_shot(self, cur_shot):
        # True if pass
        if not cur_shot.is_friend(self.team):
            return False
        if cur_shot.type < 5 and cur_shot.big > CARDS.index('0'):
            return True
        cards = cur_shot.cards
        cards_5_level = self.get_5_level(cards)
        if cards_5_level < 3:
            return False
        elif cards_5_level > 3:
            return True
        else:
            big_card = cards[0] if cards.count(cards[0]) == 3 else 0
            big_card = cards[1] if cards.count(cards[1]) == 3 else big_card
            big_card = cards[2] if cards.count(cards[2]) == 3 else big_card
            return CARDS.index(big_card) > CARDS.index('0')

    def shot_by_input(self, cur_shot):
        print('Current cards: ', end='')
        self.show_cards()
        print(f"Please type your next shot, friend={cur_shot.is_friend(self.team)}:")
        cards_str = input().strip(' \n')
        if cards_str == 'pass':
            return Shot(team=self.team)
        cards_list = sorted([CARDS.index(char) for char in cards_str])
        if self.check_cards_valid(cards_list):
            print("valid card")
            if len(cards_list) == 5:
                if cur_shot.type == 0 or \
                        self.check_big(cards_list, [CARDS.index(card) for card in cur_shot.cards]):
                    [self.remove_card(card) for card in cards_list]
                    return Shot(cards=cards_str, type=5, big=-1, team=self.team)
            else:
                big = cards_list[0]
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
        # type 5
        cur_cards = [card.num for card in self.cards]
        for shot_card in shot_cards:
            # print(f"card={shot_card}, cards={str(cur_cards)}")
            if shot_card not in cur_cards:
                return False
            cur_cards.remove(shot_card)
        # TODO: Need to check type 5
        return True

    @staticmethod
    def check_big(next_cards, cur_cards):
        if len(cur_cards) != 5:
            return next_cards[-1] > cur_cards[-1]
        # type = 5
        my_level = Player.get_5_level(next_cards)
        cur_level = Player.get_5_level(cur_cards)
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

    @staticmethod
    def get_5_level(cards):
        # straight, flush, full house, four, flush straight, five
        big = 0
        for card in cards:
            big = max(big, cards.count(card))
        if big >= 3:
            return big
        # straight, flush, flush straight
        return 1

    def shot_by_type(self, cur_shot):
        # Bigger than my biggest
        if self.cards[0].num <= cur_shot.big:
            return Shot(team=self.team)
        if cur_shot.type == 0:
            return self.new_round_shot()
        elif cur_shot.type == 5:
            for cards in self.form_5():
                if len(cards) != 5:
                    break
                cards_list = [CARDS.index(card) for card in cards]
                if self.check_big(cards_list, [CARDS.index(card) for card in cur_shot.cards]):
                    [self.remove_card(card_num) for card_num in cards_list]
                    return Shot(cards=cards, type=5, big=-1, team=self.team)
            return Shot(team=self.team)
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

    def new_round_shot(self):
        cards_5 = self.form_5()
        if len(cards_5[0]) == 5:
            cards = cards_5[0]
            [self.remove_card(CARDS.index(cards[i])) for i in range(len(cards))]
            return Shot(cards=cards_5[0], type=5, big=-1, team=self.team)
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

    def form_5(self):
        cards = Card.split_cards(self.cards)
        cards_4 = [cards[4][i] + cards[1][i] for i in range(len(cards[4]) if len(cards[4]) <= len(cards[1]) else len(cards[1]))]
        cards_3 = [cards[3][i] + cards[2][i] for i in range(len(cards[3]) if len(cards[3]) <= len(cards[2]) else len(cards[2]))]
        cards_remain = [] if len(cards[4]) <= len(cards[1]) else cards[4][len(cards[1]):]
        cards_remain += [] if len(cards[3]) <= len(cards[2]) else cards[3][len(cards[2]):]
        return cards_3 + cards_4 + cards[5] + [''.join(cards[6])] + cards_remain
