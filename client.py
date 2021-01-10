import pygame
import json
from network import Network
import pickle
pygame.font.init()

width = 1300
height = 1000

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


button_height = 100
button_width = 166

n = Network()

class Category:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 166
        self.height = 100

    def draw(self, win):
        #   win -> window
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        #   Centrování textu
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

class Button(Category):
    # def __init__(self, text, x, y, color):
    #     self.text = text
    #     self.x = x
    #     self.y = y
    #     self.color = color
    #     self.width = 150
    #     self.height = 100

    # def draw(self, win):
    #     #   win -> window
    #     pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
    #     font = pygame.font.SysFont("comicsans", 40)
    #     text = font.render(self.text, 1, (255,255,255))
    #     #   Centrování textu
    #     win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        #   Rozpoznání jestli se kliklo na určitý button
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

class Question(Button):
    def __init__(self, q, a1, a2, a3, a4, correct_ans, points):
        self.q = q
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4
        self.correct_ans = correct_ans
        self.points = points

    def draw(self, win):
        font = pygame.font.SysFont("comicsans", 40)
        self.q = font.render(self.q, 1, (255,255,255))
        win.blit(self.q, (10, 0))

    def get_correct_ans(self):
        return self.correct_ans


class Q():
    def __init__(self):
        self.is_question_displayed = False


class Interface(pygame.Surface):
    def __init__(self, text, x, y, color, score):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.score = score

    def draw(self, win, current_color):
        #   win -> window
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, current_color)
        text_score = font.render(str(self.score), 1, current_color)
        win.blit(text, (self.x, self.y))
        win.blit(text_score, (self.x + 140, self.y))


def compare_and_change(p, game, answer_button, q):
    game = n.send("change")
    game = n.send("questionDisplay")
    print(answer_button.text[0])
    if answer_button.text[0] == q.get_correct_ans():
        print("Spravna odpoved")
        print(p)
        if p == 0:
            interface1.score += int(q.points)
        else:
            interface2.score += int(q.points)


def draw_question(p, win, game):
    #q = Question("Ahoj, jak se máš?", "1", "2", "3", "4", "3")
    with open("json/kategorie1.json", encoding="utf-8") as f:
        data = json.load(f)
    for que in data["questions"]:
        if que["points"] == str(1000):
            q = Question(que["q"], que["a1"], que["a2"], que["a3"], que["a4"], que["correct_ans"], que["points"])
    q.draw(win)
    answer_button1 = Button(f"1) {q.a1}", 100, 800, (147, 120, 47))
    answer_button2 = Button(f"2) {q.a2}", 100, 900, (147, 120, 47))
    answer_button3 = Button(f"3) {q.a3}", 300, 800, (147, 120, 47))
    answer_button4 = Button(f"4) {q.a4}", 300, 900, (147, 120, 47))

    answer_button1.draw(win)
    answer_button2.draw(win)
    answer_button3.draw(win)
    answer_button4.draw(win)
    if p == int(game.get_player_turn()):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if answer_button1.click(pos) and game.connected():
                    print(answer_button1.text)
                    # game = n.send("change")
                    # game = n.send("questionDisplay")
                    compare_and_change(p, game, answer_button1, q)
                elif answer_button2.click(pos) and game.connected():
                    print(answer_button2.text)
                    compare_and_change(p, game, answer_button2, q)
                elif answer_button3.click(pos) and game.connected():
                    print(answer_button3.text)
                    compare_and_change(p, game, answer_button3, q)
                elif answer_button4.click(pos) and game.connected():
                    print(answer_button4.text)
                    compare_and_change(p, game, answer_button4, q)


def redrawWindow(win, game, p):
    win.fill((128, 128, 128))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255, 0, 0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255, 255))
        win.blit(text, (80, 200))

        text = font.render("Opponents", 1, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            #   Pokud hráč 1 dal tah a já jsem ten hráč
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            #   Pokud hráč 2 dal tah a já jsem ten hráč
            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        #   Získat ze serveru
        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns1:
            btn.draw(win)

        for btn in btns2:
            btn.draw(win)

        for btn in btns3:
            btn.draw(win)

        for btn in btns4:
            btn.draw(win)

        for btn in btns5:
            btn.draw(win)

        for btn in btns6:
            btn.draw(win)

        for category in ctg:
            category.draw(win)

        # interface1.draw(win)
        # interface2.draw(win)

        if(p == 0 and p == int(game.get_player_turn())):
            interface1.draw(win, (155, 155, 155))
            interface2.draw(win, (255, 255, 255))
        elif(p == 0 and p != int(game.get_player_turn())):
            interface1.draw(win, (255, 255, 255))
            interface2.draw(win, (155, 155, 155))

        elif(p == 1 and p == int(game.get_player_turn())):
            interface1.draw(win, (255, 255, 255))
            interface2.draw(win, (155, 155, 155))
        else:
            interface1.draw(win, (155, 155, 155))
            interface2.draw(win, (255, 255, 255))

        # heh = True
        # if heh == True:
        #     if p == 0 and game.get_player_turn() == int(0):
        #         print("jsem hráč 0 a jsem na tahu")
        #     elif p == 0 and game.get_player_turn() == int(1):
        #         print("jsem hráč 0 a nejsem na tahu")
        #     elif p == 1 and game.get_player_turn() == int(0):
        #         print("jsme hráč 1 a jsem na tahu")
        #     elif p == 1 and game.get_player_turn() == int(1):
        #         print("jsem hráč 1 a nejsem na tahu")

        #n = Network()
        #run = True
        #game.change_player_turn()
        if p == int(game.get_player_turn()):
            print(f"jsem hráč {p} a jsem na tahu")
            # while run:
            #     for event in pygame.event.get():
            #         if event.type == pygame.QUIT:
            #             pygame.quit()
            #             run = False
            #         if event.type == pygame.MOUSEBUTTONDOWN:
            #             game.change_player_turn()
            #             game = n.send("change")
            #             print("hehe")
            #             run = False
            if game.get_question_display() == True:
                draw_question(p, win, game)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # draw_question(p, win)
                    # game = n.send("questionDisplay")
                    # if game.get_question_display() == False:
                    #     game = n.send("questionDisplay")
                    # game.change_player_turn()
                    # game = n.send("change")
                    pos = pygame.mouse.get_pos()
                    for button in btns1:
                        if button.click(pos) and game.connected():
                            game = n.send("questionDisplay")
                    for button in btns2:
                        if button.click(pos) and game.connected():
                            game = n.send("questionDisplay")
                    for button in btns3:
                        if button.click(pos) and game.connected():
                            game = n.send("questionDisplay")
                    for button in btns4:
                        if button.click(pos) and game.connected():
                            game = n.send("questionDisplay")
                    for button in btns5:
                        if button.click(pos) and game.connected():
                            game = n.send("questionDisplay")
                    for button in btns6:
                        if button.click(pos) and game.connected():
                            game = n.send("questionDisplay")

        elif p != int(game.get_player_turn()):
            if game.get_question_display() == True:
                draw_question(p, win, game)
            print(f"jsem hráč {p} a nejsem na tahu")

    pygame.display.update()

#   First column
fc = 43

#   Kategorie
ctg = [Category("Poznej město", fc, 10, (0, 0, 0)), Category("Najdi slovo", fc, button_height + 20, (255, 0, 0)), Category("Slova na mik", fc, 2 * button_height + 30, (0, 255, 0)),\
       Category("Naši sousedé", fc, 3 * button_height + 40, (0, 255, 0)), Category("Sci-fi postavy", fc, 4 * button_height + 50, (0, 255, 0)), Category("Curling", fc, 5 * button_height + 60, (0, 255, 0))]

#   První řada
btns1 = [Button("1000", (fc - 1) * 2 + button_width, 10, (0, 0, 0)), Button("2000", (fc - 1) * 3 + button_width * 2, 10, (0, 0, 0)),\
         Button("3000", (fc - 1) * 4 + button_width * 3, 10, (0, 0, 0)), Button("4000", (fc - 1) * 5 + button_width * 4, 10, (0, 0, 0)),\
         Button("5000", (fc - 1) * 6 + button_width * 5, 10, (0, 0, 0))]

#   Druhá řada
btns2 = [Button("1000", (fc - 1) * 2 + button_width, button_height + 20, (0, 0, 0)), Button("2000", (fc - 1) * 3 + button_width * 2, button_height + 20, (0, 0, 0)),\
         Button("3000", (fc - 1) * 4 + button_width * 3, button_height + 20, (0, 0, 0)), Button("4000", (fc - 1) * 5 + button_width * 4, button_height + 20, (0, 0, 0)),\
         Button("5000", (fc - 1) * 6 + button_width * 5, button_height + 20, (0, 0, 0))]

#   Třetí řada
btns3 = [Button("1000", (fc - 1) * 2 + button_width, 2 * button_height + 30, (0, 0, 0)), Button("2000", (fc - 1) * 3 + button_width * 2, 2 * button_height + 30, (0, 0, 0)),\
         Button("3000", (fc - 1) * 4 + button_width * 3, 2 * button_height + 30, (0, 0, 0)), Button("4000", (fc - 1) * 5 + button_width * 4, 2 * button_height + 30, (0, 0, 0)),\
         Button("5000", (fc - 1) * 6 + button_width * 5, 2 * button_height + 30, (0, 0, 0))]

#   Čtvrtá řada
btns4 = [Button("1000", (fc - 1) * 2 + button_width, 3 * button_height + 40, (0, 0, 0)), Button("2000", (fc - 1) * 3 + button_width * 2, 3 * button_height + 40, (0, 0, 0)),\
         Button("3000", (fc - 1) * 4 + button_width * 3, 3 * button_height + 40, (0, 0, 0)), Button("4000", (fc - 1) * 5 + button_width * 4, 3 * button_height + 40, (0, 0, 0)),\
         Button("5000", (fc - 1) * 6 + button_width * 5, 3 * button_height + 40, (0, 0, 0))]

#   Pátá řada
btns5 = [Button("1000", (fc - 1) * 2 + button_width, 4 * button_height + 50, (0, 0, 0)), Button("2000", (fc - 1) * 3 + button_width * 2, 4 * button_height + 50, (0, 0, 0)),\
         Button("3000", (fc - 1) * 4 + button_width * 3, 4 * button_height + 50, (0, 0, 0)), Button("4000", (fc - 1) * 5 + button_width * 4, 4 * button_height + 50, (0, 0, 0)),\
         Button("5000", (fc - 1) * 6 + button_width * 5, 4 * button_height + 50, (0, 0, 0))]

#   Šestá řada
btns6 = [Button("1000", (fc - 1) * 2 + button_width, 5 * button_height + 60, (0, 0, 0)), Button("2000", (fc - 1) * 3 + button_width * 2, 5 * button_height + 60, (0, 0, 0)),\
         Button("3000", (fc - 1) * 4 + button_width * 3, 5 * button_height + 60, (0, 0, 0)), Button("4000", (fc - 1) * 5 + button_width * 4, 5 * button_height + 60, (0, 0, 0)),\
         Button("5000", (fc - 1) * 6 + button_width * 5, 5 * button_height + 60, (0, 0, 0))]

interface1 = Interface('Player1: ', 100, 800, (255, 255, 255), 0)
interface2 = Interface('Player2: ', width - 400, 800, (255, 255, 255), 0)

def main():
    run = True
    clock = pygame.time.Clock()
    #n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            #   Pokud nedostaneme odpověd tak ta hra neexistuje
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                #   Pošle string reset na server
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255, 0, 0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255, 0, 0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     pos = pygame.mouse.get_pos()
                # for btn in btns:
                #     #   Pokud bylo kliknuto na button a zároveň jsou oba hráči připojení
                #     if btn.click(pos) and game.connected():
                #         if player == 0:
                #             if not game.p1Went:
                #                 #   Pošle se text buttonu (Rock, Paper, Scissors)
                #                 n.send(btn.text)
                #         else:
                #             if not game.p2Went:
                #                 n.send(btn.text)

        redrawWindow(win, game, player)

#   Napíš click to Play pokud se zapne klient a pokud se jeden odpojí tak druhého to dá zase k textu click to Play
def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 0, 0))
        win.blit(text, (100, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()
