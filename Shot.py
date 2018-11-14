class Shot:
    def __init__(self, cards='', type=0, big=0, team=0):
        self.cards = cards
        self.type = type
        self.big = big
        self.team = team

    def is_friend(self, t):
        return self.team == t

    def __str__(self):
        return self.cards if self.type != 0 else 'pass'
