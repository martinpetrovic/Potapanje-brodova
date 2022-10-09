from ast import main
import pygame, sys
from pygame.locals import *
import os
import time
pygame.init()
pygame.mixer.init()


ŠIRINA, VISINA = 1280, 720
PROZOR = pygame.display.set_mode((ŠIRINA, VISINA))
pygame.display.set_caption("Potapanje brodova")

FPS = 60
clock = pygame.time.Clock()

LOGO = pygame.image.load(os.path.join("potapanje brodova", "MLKJR_LOGO.png" ))
INTRO = pygame.mixer.Sound(os.path.join("potapanje brodova", "INTRO.ogg"))
KVADRAT = pygame.image.load(os.path.join("potapanje brodova", "kvadrat.png"))
FONT_BROJ_SLOVO = pygame.font.Font(None, 40)

BRODOVI_GRUPA = pygame.sprite.Group()

class Brod(pygame.sprite.Sprite):
    def __init__(self,picture_path,poz_x,poz_y):
        super().__init__()
        #rectangle
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.topleft =(poz_x, poz_y)

class Button:
    def __init__(self, text_input, text_size, text_color, rect_width, rect_height, rect_color, hoveringRect_color, pos):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        #rectangle ispod teksta
        self.main_rect = pygame.Rect(self.x_pos-(rect_width/2), self.y_pos-(rect_height/2), rect_width, rect_height)
        self.main_rect_color, self.hovering_rect_color= rect_color, hoveringRect_color
        #tekst u gumbu
        self.font = pygame.font.Font(None, text_size)
        self.text_input = text_input
        self.text_color = text_color
        self.text = self.font.render(self.text_input, False, self.text_color)

    def update(self, screen):
        pygame.draw.rect(screen, self.main_rect_color, self.main_rect)
        screen.blit(self.text, self.main_rect)

    def checkForInput(self,position):
        if position[0] in range(self.main_rect.left, self.main_rect.right) and position[1] in range(self.main_rect.top, self.main_rect.bottom):
            return True
        return False

    def changeColor(self, position, screen):
        if position[0] in range(self.main_rect.left, self.main_rect.right) and position[1] in range(self.main_rect.top, self.main_rect.bottom):
            pygame.draw.rect(screen, self.hovering_rect_color, self.main_rect)
            screen.blit(self.text, self.main_rect)
        else:
            pygame.draw.rect(screen, self.main_rect_color, self.main_rect)

def GRIDLIJEVO():
    y = 100
    x = 50
    for i in range(10):
        KVADRAT_RECT = KVADRAT.get_rect(topleft = (x,y))
        y = y + 48
        x = 50
        for i in range (10):
            x = x + 48
            KVADRAT_RECT = KVADRAT.get_rect(topleft = (x,y))
            PROZOR.blit(KVADRAT,KVADRAT_RECT)
    #brojevi
    broj_x = 70
    broj_y = 160
    for i in range(1,11):
        broj = FONT_BROJ_SLOVO.render(str(i),1,'Black')
        if i == 10:
            broj_x = broj_x - 10
        broj_rect = broj.get_rect(topleft = (broj_x, broj_y))
        PROZOR.blit(broj, broj_rect)
        broj_y = broj_y + 48

    #slova
    slovo_x = 113
    slovo_y = 637
    for i in range(0,10):
        slovo = FONT_BROJ_SLOVO.render(str(chr(ord("A")+i)),1,'Black')
        #if i == 10:
        #    broj_x = broj_x - 10
        slovo_rect = slovo.get_rect(topleft = (slovo_x, slovo_y))
        PROZOR.blit(slovo, slovo_rect)
        slovo_x = slovo_x + 48

def GRIDDESNO():
    #PROZOR.fill(WHITE)
    y = 100
    x = 640
    for i in range(10):
        KVADRAT_RECT = KVADRAT.get_rect(topleft = (x,y))
        y = y + 48
        x = 640
        for i in range (10):
            x = x + 48
            KVADRAT_RECT = KVADRAT.get_rect(topleft = (x,y))
            PROZOR.blit(KVADRAT,KVADRAT_RECT)
    #brojevi
    broj_x = 659
    broj_y = 160
    for i in range(1,11):
        broj = FONT_BROJ_SLOVO.render(str(i),1,'Black')
        if i == 10:
            broj_x = broj_x - 10
        broj_rect = broj.get_rect(topleft = (broj_x, broj_y))
        PROZOR.blit(broj, broj_rect)
        broj_y = broj_y + 48

    #slova
    slovo_x = 704
    slovo_y = 637
    for i in range(0,10):
        slovo = FONT_BROJ_SLOVO.render(str(chr(ord("A")+i)),1,'Black')
        #if i == 10:
        #    broj_x = broj_x - 10
        slovo_rect = slovo.get_rect(topleft = (slovo_x, slovo_y))
        PROZOR.blit(slovo, slovo_rect)
        slovo_x = slovo_x + 48

def LOADING_SCREEN():
    PROZOR.fill('White')
    PROZOR.blit(LOGO,(150,0))
    pygame.mixer.Sound.play(INTRO)
    pygame.display.update()
    time.sleep(4)                
    PROZOR.fill('White')

CARRIER = Brod(os.path.join("potapanje brodova", "carrier5.png"), 93, 35)
BATTLESHIP = Brod(os.path.join("potapanje brodova", "battleship4.png"), 360, 35)
DESTROYER = Brod(os.path.join("potapanje brodova", "destroyer3.png"), 225, 90)
SUBMARINE = Brod(os.path.join("potapanje brodova", "submarine3.png"), 400, 90)
PATROL = Brod(os.path.join("potapanje brodova", "patrol2.png"), 97, 90)

BRODOVI_GRUPA.add(CARRIER,BATTLESHIP,PATROL,DESTROYER,SUBMARINE)

def play():
    run = True
    while run:
        PROZOR.fill('White')
        GRIDLIJEVO()
        GRIDDESNO()
        BRODOVI_GRUPA.draw(PROZOR)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    #esc_screen
                    run = False
        pygame.display.update()
        clock.tick(FPS)

def main_menu():
    #LOADING_SCREEN()
    while True:
        PROZOR.fill('White')
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        GUMB_PLAY = Button(text_input = "Play", text_size = 30, text_color = 'Black', rect_width = 200, rect_height = 40, rect_color = '#475F77', hoveringRect_color = 'Green', pos = (640,200))
        GUMB_SCORE = Button(text_input = "Score", text_size = 30, text_color = 'Black', rect_width = 200, rect_height = 40, rect_color = '#475F77', hoveringRect_color = 'Green', pos = (640,275))
        GUMB_EXIT = Button(text_input = "Exit", text_size = 30, text_color = 'Black', rect_width = 200, rect_height = 40, rect_color = '#475F77', hoveringRect_color = 'Red', pos = (640,350))
        for gumb in [GUMB_PLAY, GUMB_SCORE, GUMB_EXIT]:
            gumb.changeColor(MENU_MOUSE_POS, PROZOR)
            gumb.update(PROZOR)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    #esc_screen
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if GUMB_PLAY.checkForInput(MENU_MOUSE_POS):
                    play()
                if GUMB_SCORE.checkForInput(MENU_MOUSE_POS):
                    pass
                if GUMB_EXIT.checkForInput(MENU_MOUSE_POS):
                    #esc_screen()
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
        clock.tick(FPS)

main_menu()

