class Game:
    #   id hry
    def __init__(self, id):
        self.ready = False
        self.id = id
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
        self.is_it_the_end = False

    #   Pokud jsou oba připojení
    def connected(self):
        return self.ready

    def change_player_turn(self):
        if self.p_turn == 0:
            self.p_turn = 1
        else:
            self.p_turn = 0
        # print(self.p_turn)

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

    def end(self):
        result = False

        if len(self.c1) > 0:
            result = all(elem == self.c1[0] for elem in self.c1)
        if result and self.c1 == self.c2 and self.c1 == self.c3 and self.c1 == self.c4 and self.c1 == self.c5 and self.c1 == self.c6:
            self.is_it_the_end = True
