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
