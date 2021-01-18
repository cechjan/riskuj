import pygame
import json
from network import Network
import question
import pickle
pygame.font.init()

width = 1300
height = 1000

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


button_height = 100
button_width = 166

n = Network()


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
    # print(answer_button.text[0])
    if answer_button.text[0] == q.get_correct_ans():
        # print("Spravna odpoved")
        # print(p)
        if p == 0:
            game = n.send(f"1{q.points}")
        else:
            game = n.send(f"2{q.points}")

    game = n.send("end")

    font = pygame.font.SysFont("comicsans", 100)
    text = font.render("Správně" if answer_button.text[0] == q.get_correct_ans() else "Špatně", 1,
                       (4, 237, 0) if answer_button.text[0] == q.get_correct_ans() else (237, 103, 0))
    win.blit(text, (width - text.get_width() - 20, 670))
    pygame.display.flip()
    pygame.time.wait(1000)


def draw_question(p, win, game):
    # print(f"Bodíky: {game.current_q}, kategorie: {game.category}") - kontrola platnosti
    with open(f"json/kategorie{game.category}.json", encoding="utf-8") as f:
        data = json.load(f)
    for que in data["questions"]:
        if que["points"] == game.current_q:
            q = question.Question(que["q"], que["a1"], que["a2"], que["a3"], que["a4"], que["correct_ans"], que["points"])

    ANSWER_CLR = (52, 47, 222)
    q.draw(win)
    answer_button1 = question.Button(f"1) {q.a1}", 455, 750, ANSWER_CLR)
    answer_button1.width = 380
    answer_button2 = question.Button(f"2) {q.a2}", 455, 875, ANSWER_CLR)
    answer_button2.width = 380
    answer_button3 = question.Button(f"3) {q.a3}", 450 + 380 + 40, 750, ANSWER_CLR)
    answer_button3.width = 380
    answer_button4 = question.Button(f"4) {q.a4}", 450 + 380 + 40, 875, ANSWER_CLR)
    answer_button4.width = 380

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
                    # print(answer_button1.text)
                    compare_and_change(p, game, answer_button1, q)
                elif answer_button2.click(pos) and game.connected():
                    # print(answer_button2.text)
                    compare_and_change(p, game, answer_button2, q)
                elif answer_button3.click(pos) and game.connected():
                    # print(answer_button3.text)
                    compare_and_change(p, game, answer_button3, q)
                elif answer_button4.click(pos) and game.connected():
                    # print(answer_button4.text)
                    compare_and_change(p, game, answer_button4, q)


def draw_button(btns, c):
    i = 0
    for btn in btns:
        if c[i] == True:
            btn.draw(win)
        i = i + 1


def check_clicked_button(btns, c, pos, num, game):
    i = 0
    for button in btns:
        if button.click(pos) and game.connected() and c[i] == True:
            game = n.send("questionDisplay")
            game = n.send(f"btn{num}{button.text}")
            game = n.send(f"sb{num}{int(button.text[0]) - 1}")
        i = i + 1


def who_wins(win, status):
    font = pygame.font.SysFont("comicsans", 150)
    text = font.render(status, 1, (4, 237, 0) if status == "Vyhrál jsi" else (237, 103, 0))
    win.blit(text, (width / 2 - text.get_width() / 2, 250))

    font = pygame.font.SysFont("comicsans", 50)
    text = font.render(f"Hráč 1: {interface1.score}", 1, (255, 255, 255))
    win.blit(text, (width / 2 - text.get_width() / 2, 500))

    font = pygame.font.SysFont("comicsans", 50)
    text = font.render(f"Hráč 2: {interface2.score}", 1, (255, 255, 255))
    win.blit(text, (width / 2 - text.get_width() / 2, 600))


def redrawWindow(win, game, p):
    win.fill((41, 50, 65))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 100)
        text = font.render("Čekání na druhého hráče...", 1, (237, 103, 0))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        if not game.is_it_the_end:
            draw_button(question.btns1, game.c1)
            draw_button(question.btns2, game.c2)
            draw_button(question.btns3, game.c3)
            draw_button(question.btns4, game.c4)
            draw_button(question.btns5, game.c5)
            draw_button(question.btns6, game.c6)

            for category in question.ctg:
                category.draw(win)

            #       Aktualizuování skóre
            interface1.score = game.p1_score
            interface2.score = game.p2_score

            if(p == 0 and p == int(game.get_player_turn())):
                interface1.draw(win, (255, 255, 255))
                interface2.draw(win, (155, 155, 155))
            elif(p == 0 and p != int(game.get_player_turn())):
                interface1.draw(win, (155, 155, 155))
                interface2.draw(win, (255, 255, 255))

            elif(p == 1 and p == int(game.get_player_turn())):
                interface1.draw(win, (155, 155, 155))
                interface2.draw(win, (255, 255, 255))
            else:
                interface1.draw(win, (255, 255, 255))
                interface2.draw(win, (155, 155, 155))

            if p == int(game.get_player_turn()):
                # print(f"jsem hráč {p} a jsem na tahu") - kontrola platnosti
                if game.get_question_display() == True:
                    draw_question(p, win, game)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()

                        check_clicked_button(question.btns1, game.c1, pos, 1, game)
                        check_clicked_button(question.btns2, game.c2, pos, 2, game)
                        check_clicked_button(question.btns3, game.c3, pos, 3, game)
                        check_clicked_button(question.btns4, game.c4, pos, 4, game)
                        check_clicked_button(question.btns5, game.c5, pos, 5, game)
                        check_clicked_button(question.btns6, game.c6, pos, 6, game)

            elif p != int(game.get_player_turn()):
                if game.get_question_display() == True:
                    draw_question(p, win, game)
                # print(f"jsem hráč {p} a nejsem na tahu") - kontrola platnosti
        else:
            font = pygame.font.SysFont("comicsans", 100)
            if interface1.score > interface2.score:
                if p == 0:
                    who_wins(win, "Vyhrál jsi")
                elif p == 1:
                    who_wins(win, "Prohrál jsi")
            else:
                if p == 0:
                    who_wins(win, "Prohrál jsi")
                elif p == 1:
                    who_wins(win, "Vyhrál jsi")

    pygame.display.update()


interface1 = Interface('Hráč 1: ', 100, 785, (255, 255, 255), 0)
interface2 = Interface('Hráč 2: ', 100, 910, (255, 255, 255), 0)


def main():
    run = True
    clock = pygame.time.Clock()
    player = int(n.getP())
    print("Jsi hráč ", player)

    while run:
        clock.tick(60)
        try:
            #   Pokud nedostaneme odpověd tak ta hra neexistuje
            game = n.send("get")
        except:
            run = False
            print("Nepodařilo se připojit")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        redrawWindow(win, game, player)


#   Napíše click to Play pokud se zapne klient a pokud se jeden odpojí tak druhého to dá zase k textu click to Play
def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((41, 50, 65))
        font = pygame.font.SysFont("comicsans", 100)
        text = font.render("Kliknutím se připoj do hry!", 1, (252, 163, 17))
        win.blit(text, ((1300-text.get_width())/2, (1000-text.get_height())/2))
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
