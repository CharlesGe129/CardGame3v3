import functools
from Shot import Shot
from Card import Card
from Consts import COLORS, CARDS


class Player:
    def __init__(self):
        self.cards = list()
        self.team = 2
        self.type = 'AI'
        self.split_cards = None

    def sort(self):
        self.cards = sorted(self.cards, key=functools.cmp_to_key(Card.cmp), reverse=True)

    def show_cards(self):
        self.split_cards = Card.split_cards(self.cards)
        rs = ''.join([each.card for each in self.cards])
        print(f"{rs}, len={len(rs)}")
        # for k, v in Card.split_cards(self.cards).items():
        #     print(f"{k}: {str(v)}")
        print(f"All 5 combo: {str(self.form_5())}")

    def add_card(self, card):
        color = card // len(CARDS)
        num = card % len(CARDS)
        self.cards.append(Card(num, color, CARDS[num]))
        if len(self.cards) == 27:
            self.sort()

    def next_shot(self, cur_shot):
        self.split_cards = Card.split_cards(self.cards)
        if self.type == 'USER':
            while True:
                try:
                    return self.shot_by_input(cur_shot)
                except:
                    print('Oops, wrong card!')
        if cur_shot.type == 0:
            return self.new_round_shot()
        elif self.check_friend_shot(cur_shot):
            return Shot(team=self.team)
        else:
            return self.shot_by_type(cur_shot)

    def check_friend_shot(self, cur_shot):
        # True if pass
        if not cur_shot.is_friend(self.team):
            return False
        if cur_shot.type < 5 and CARDS.index(cur_shot.cards[0]) > CARDS.index('0'):
            return True
        cards = cur_shot.cards
        cards_5_level = Card.get_5_level(cards)
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
        if cards_str.lower() == 'pass':
            return Shot(team=self.team)
        cards_list = sorted([CARDS.index(char) for char in cards_str])
        if (cur_shot.type == 0 or len(cards_list) == cur_shot.type) \
                and self.check_cards_valid(cards_list):
            if len(cards_list) == 5:
                if cur_shot.type == 0 or cur_shot.check_big(cards_list):
                    self.remove_cards(cards_list)
                    return Shot(cards=cards_str, type=5, team=self.team)
            else:
                # print(f"cards_str={cards_str}, cards_list={cards_list}, big={big}")
                if cur_shot.type == 0 or cur_shot.check_big(cards_list):
                    self.remove_cards(cards_list)
                    return Shot(cards=cards_str, type=len(cards_str), team=self.team)
        print('Oops, wrong card!')
        return self.shot_by_input(cur_shot)

    def check_cards_valid(self, shot_cards: list):
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

    def shot_by_type(self, cur_shot):
        if cur_shot.type == 5:
            for cards in self.form_5():
                if len(cards) != 5:
                    break
                if cur_shot.check_big(cards):
                    self.remove_cards(cards)
                    return Shot(cards=cards, type=5, team=self.team)
            return Shot(team=self.team)
        # type 1, 2, 3
        for card_type, v in self.split_cards.items():
            for iter_cards in v:
                if len(iter_cards) < cur_shot.type:
                    break
                cards = iter_cards[:cur_shot.type]
                # print(f"check card_type={card_type}, iter_cards={iter_cards}, cards={cards}")
                if cur_shot.check_big(cards):
                    self.remove_cards(cards)
                    return Shot(cards=cards, type=len(cards), team=self.team)
        return Shot(team=self.team)

    def new_round_shot(self):
        # type 5
        cards_5 = self.form_5()
        if len(cards_5[0]) == 5:
            cards = cards_5[0]
            self.remove_cards(cards)
            return Shot(cards=cards_5[0], type=5, team=self.team)
        # type 1, 2, 3
        for card_type, v in self.split_cards.items():
            for cards in v:
                self.remove_cards(cards)
                return Shot(cards=cards, type=card_type, team=self.team)

    def remove_cards(self, cards):
        if isinstance(cards, str):
            cards = [CARDS.index(char) for char in cards]
        for card_num in cards:
            cards_temp = self.cards.copy()
            for i in range(len(self.cards) - 1, -1, -1):
                if cards_temp[i].num == card_num:
                    cards_temp.pop(i)
                    break
            self.cards = cards_temp

    def is_finish(self):
        return len(self.cards) == 0

    def form_5(self):
        cards = self.split_cards
        cards_4 = [cards[4][i] + cards[1][i] for i in range(len(cards[4]) if len(cards[4]) <= len(cards[1]) else len(cards[1]))]
        cards_3 = [cards[3][i] + cards[2][i] for i in range(len(cards[3]) if len(cards[3]) <= len(cards[2]) else len(cards[2]))]
        cards_remain = [] if len(cards[4]) <= len(cards[1]) else cards[4][len(cards[1]):]
        cards_remain += [] if len(cards[3]) <= len(cards[2]) else cards[3][len(cards[2]):]
        return cards_3 + cards_4 + cards[5] + [''.join(cards[6])] + cards_remain
