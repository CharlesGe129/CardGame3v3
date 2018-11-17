from Consts import CARDS


class Card:
    def __init__(self, num, color, card):
        self.num = num
        self.color = color
        self.card = card

    def cmp(self, other):
        if self.num < other.num:
            return -1
        elif self.num == other.num:
            return 0
        else:
            return 1

    @staticmethod
    def split_cards(ori_cards):
        cards = [ori_cards[len(ori_cards) - 1 - i] for i in range(len(ori_cards))].copy()
        rs = {1: list(), 2: list(), 3: list(), 4: list(), 5: list(), 6: list()}
        cur_card = CARDS[cards[0].num]
        cur_num = 0
        cards.append(Card(num=1, color=1, card='null'))
        for card in cards:
            if cur_num == 0:
                cur_card = CARDS[card.num]
                cur_num = 1
            elif CARDS[card.num] == cur_card[0]:
                cur_num += 1
                cur_card += CARDS[card.num]
                if cur_num == 5:
                    rs[cur_num].append(cur_card)
                    cur_num = 0
            else:
                if cur_card[0] in ['大', '小']:
                    rs[6].append(cur_card)
                else:
                    rs[cur_num].append(cur_card)
                cur_card = CARDS[card.num]
                cur_num = 1
        rs[6] = [''.join(rs[6])] if rs[6] else []
        return rs

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
