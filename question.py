import pygame

button_height = 100
button_width = 166


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
    def __init__(self, text, x, y, color):
        super().__init__(text, x, y, color)
        self.is_shown = True

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


# def button_display(b_row, b_index):
#     if int(b_row) == 1:
#         for button in btns1:
#            if button.text == str(1000):
#                print("_-_-_-_-_-")
#                # del btns1[int(button.text[0]) - 1]
#                print(button.is_shown)
#                button.is_shown = False
#                print(button.is_shown)
#         btns1[0].is_shown = False
#         #btns1[b_index].is_shown = False
#         print(f"{b_index}----------------------------")


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