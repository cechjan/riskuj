class Game:
    #   id hry
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0
        self.p_turn = 0
        self.is_question_displayed = False
        self.p1_score = 0
        self.p2_score = 0
        self.current_q = 0
        self.category = 0
        self.c1 = [True, True, True, True, True]
        self.c2 = [True, True, True, True, True]
        self.c3 = [True, True, True, True, True]
        self.c4 = [True, True, True, True, True]
        self.c5 = [True, True, True, True, True]
        self.c6 = [True, True, True, True, True]
        self.g = True

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    #   Pokud jsou oba připojení
    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):

        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        #   -1, protože to může být remíza
        winner = -1
        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False

    def change_player_turn(self):
        if self.p_turn == 0:
            self.p_turn = 1
        else:
            self.p_turn = 0
        print(self.p_turn)
        #return self.p_turn

    def get_player_turn(self):
        return self.p_turn

    def change_question_display(self):
        if self.is_question_displayed == False:
            self.is_question_displayed = True
        else:
            self.is_question_displayed = False

    def get_question_display(self):
        return self.is_question_displayed

    def add_score(self, p, points):
        if p == 1:
            self.p1_score += int(points)
        elif p == 2:
            self.p2_score += int(points)

    def print_score1(self):
        return self.p1_score
    def print_score2(self):
        return self.p2_score

    def change_current_q(self, points, category):
        self.current_q = points
        self.category = category

    def button_display(self, b_row, b_index):
        if int(b_row) == 1:
            self.c1[int(b_index)] = False
        elif int(b_row) == 2:
            self.c2[int(b_index)] = False
        elif int(b_row) == 3:
            self.c3[int(b_index)] = False
        elif int(b_row) == 4:
            self.c4[int(b_index)] = False
        elif int(b_row) == 5:
            self.c5[int(b_index)] = False
        elif int(b_row) == 6:
            self.c6[int(b_index)] = False
