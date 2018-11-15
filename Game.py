import random
from Player import Player, CARDS
from Shot import Shot


class Game:
    def __init__(self):
        self.players = [Player() for i in range(6)]
        for i in range(3):
            self.players[2*i].team = 1
        self.players[0].type = 'USER'
        self.finish_players = list()

    def start(self):
        self.assign_cards()
        cur_shot = Shot()
        cur_player = random.randint(0, 5)
        big_player = cur_player
        num_pass = self.reset_num_pass()
        while not self.is_finish():
            # print(f"cur_shot={cur_shot}, cur={cur_player}, big={big_player}, finish={self.finish_players}")
            if num_pass == 0:
                cur_shot = Shot()
                self.show_all_cards()
                num_pass = self.reset_num_pass()
            shot = self.players[cur_player].next_shot(cur_shot)
            if shot.type != 0:
                cur_shot = shot
                big_player = cur_player
                num_pass = self.reset_num_pass()
            else:
                num_pass -= 1
            print(f"Player{cur_player}: {str(shot)}, num_pass={num_pass}")
            if self.players[cur_player].is_finish():
                print(f"Player{cur_player} finishes")
                self.finish_players.append(cur_player)
                big_player = self.next_player(big_player)
            cur_player = self.next_player(cur_player)

    def reset_num_pass(self):
        return 6 - 1 - len(self.finish_players)

    def is_finish(self):
        if {0, 2, 4}.issubset(set(self.finish_players)):
            print(f'Team 1 wins!\n{str(self.finish_players)}')
        elif {1, 3, 5}.issubset(set(self.finish_players)):
            print(f'Team 2 wins!\n{str(self.finish_players)}')
        else:
            return False
        return True

    def next_player(self, cur_player):
        cur_player = cur_player + 1 if cur_player < 5 else 0
        while cur_player in self.finish_players:
            cur_player = cur_player + 1 if cur_player < 5 else 0
        return cur_player

    @staticmethod
    def initial_cards():
        cards = []
        for i in range(len(CARDS) - 2):
            for j in range(4):
                cards += [i + len(CARDS)*j for k in range(3)]
        for i in range(len(CARDS) - 2, len(CARDS)):
            cards += [i for j in range(3)]
        return cards

    def assign_cards(self):
        cards = self.initial_cards()
        random.shuffle(cards)
        for i in range(len(cards)):
            self.players[i % 6].add_card(cards[i])
        self.show_all_cards()

    def show_all_cards(self):
        print('======== all cards ========')
        for i in range(6):
            print(f"Player{i}: ", end='')
            self.players[i].show_cards()
        print('===========================')

if __name__ == '__main__':
    g = Game()
    g.start()
