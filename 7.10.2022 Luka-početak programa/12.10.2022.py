from ast import main
import pygame, sys
from pygame.locals import *
import os
import time
pygame.init()
pygame.mixer.init()

#Definiranje displaya
ŠIRINA, VISINA = 1280, 720
PROZOR = pygame.display.set_mode((ŠIRINA, VISINA))
pygame.display.set_caption("Potapanje brodova")

#clock i boje
WHITE = (255,255,255)
FPS = 30
clock = pygame.time.Clock()

#Slike, zvuk, font
LOGO = pygame.image.load(os.path.join("potapanje brodova", "MLKJR_LOGO.png" ))
INTRO = pygame.mixer.Sound(os.path.join("potapanje brodova", "INTRO.ogg"))
KVADRAT = pygame.image.load(os.path.join("potapanje brodova", "kvadrat.png"))
FONT_BROJ_SLOVO = pygame.font.Font(None, 40)

#Sve za Brod spriteove i provjere postavljanja
BRODOVI_GRUPA = pygame.sprite.Group()
lista_imena_kvadrata = []
lista_rect_kvadrata = []
Kvadrat_x, Kvadrat_y = 0, 0
brod = None


class Brod(pygame.sprite.Sprite):
    def __init__(self,picture_path,poz_x,poz_y):
        super().__init__()
        #rectangle
        self.pozx = poz_x
        self.pozy = poz_y
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.topleft =(poz_x, poz_y)
       
    
    def rotacija_poz_90(self): 
        PROZOR.fill(WHITE)
        GRID_LIJEVO()
        GRID_DESNO()
        self.image = pygame.transform.rotate(self.image, 90)
        BRODOVI_GRUPA.draw(PROZOR)
        pygame.display.update()

    def rotacija_neg_90(self):
        PROZOR.fill(WHITE)
        GRID_LIJEVO()
        GRID_DESNO()
        self.image = pygame.transform.rotate(self.image, -90)
        BRODOVI_GRUPA.draw(PROZOR)
        pygame.display.update()
        

    def collide(self):
        global brod
        global duljina_broda
        mouse_poz = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_poz):
            if self.rect.width / 5 == 48:
                duljina_broda = 5
            if self.rect.width / 4 == 48:
                duljina_broda = 4  
            if self.rect.width / 3 == 48:
                duljina_broda = 3
            if self.rect.width / 2 == 48:
                duljina_broda = 2
            brod = self
       
    
def čekanje_za_odabir(brod,brod_r):
    global idi
    idi = True
    while idi:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_r:
                if brod_r == 0:
                    brod.rotacija_poz_90()
                    brodovi_rotacija.update({brod:1})
                    print(brodovi_rotacija.values())
                    brod_r = 1
                    print("poz")
                elif brod_r == 1: 
                    brod.rotacija_neg_90()
                    brodovi_rotacija.update({brod:0})
                    brod_r = 0
                    print("neg")
                
            if event.type == MOUSEBUTTONDOWN:
                collide_kvadrat()
                
def collide_kvadrat():
    global Kvadrat_x, Kvadrat_y
    global idi
    mouse_poz = pygame.mouse.get_pos()
    for kvadrat in lista_rect_kvadrata:
            if kvadrat.collidepoint(mouse_poz):
                if pygame.mouse.get_pressed()[0]:
                    Kvadrat_x, Kvadrat_y = kvadrat.x, kvadrat.y
                    brod.rect.topleft = (Kvadrat_x, Kvadrat_y)
                    idi = False
                   

class Button:
    def __init__(self, text_input, text_size, text_color, rect_width, rect_height, rect_color, hoveringRect_color, pos):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        #rectangle ispod teksta
        self.main_rect = pygame.Rect(self.x_pos-(rect_width/2), self.y_pos-(rect_height/2), rect_width, rect_height)
        self.main_rect_color, self.hovering_rect_color= rect_color, hoveringRect_color
        #tekst u gumbu
        self.font = pygame.font.Font(None, text_size)
        self.text_surf = self.font.render(text_input, False, text_color)
        self.text_rect = self.text_surf.get_rect(center = self.main_rect.center)

    def update(self, screen):
        pygame.draw.rect(screen, self.main_rect_color, self.main_rect)
        screen.blit(self.text_surf, self.text_rect)

    def checkForInput(self,position):
        if position[0] in range(self.main_rect.left, self.main_rect.right) and position[1] in range(self.main_rect.top, self.main_rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.main_rect.left, self.main_rect.right) and position[1] in range(self.main_rect.top, self.main_rect.bottom):
            self.main_rect_color = self.hovering_rect_color






        



    
def GRIDLIJEVO():
    y = 100
    x = 50
    global KVADRAT_RECT
    for i in range(10):
        y = y + 48
        x = 50
        for j in range (10):
            x = x + 48
            KVADRAT_RECT = KVADRAT.get_rect(topleft = (x,y))
            Kvadrat = "a" + str(i) + str(j)
            lista_imena_kvadrata.append(Kvadrat)
            lista_rect_kvadrata.append(KVADRAT_RECT)
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


def esc_screen(ulazni_tekst, screen):
    run = True
    global zmaj
    while run:
        zmaj = False
        ESC_MOUSE_POS = pygame.mouse.get_pos()

        trans_background = pygame.Surface((1280,720))
        trans_background.fill('Black')
        trans_background.set_alpha(1)
        sivo = pygame.Surface((640,360))
        sivo.fill('Grey')
        okvir_surf = pygame.Surface((600,320))
        okvir_rect = okvir_surf.get_rect(center = (640,360))

        font = pygame.font.Font(None, 30)
        tekst_surf = font.render(ulazni_tekst, False, 'Black')
        tekst_rect = tekst_surf.get_rect(midtop = (640,280))

        screen.blit(trans_background,(0,0))
        screen.blit(sivo, (320,180))
        pygame.draw.rect(screen,'Black', okvir_rect, 6)
        screen.blit(tekst_surf, tekst_rect)

        CANCEL_GUMB = Button('Cancel', 30, 'Black', 200, 40, '#475F77', '#D74B4B', (490, 410))
        CONFIRM_GUMB = Button('Confirm', 30, 'Black', 200, 40, '#475F77', '#77dd77', (790, 410))

        for gumb in [CANCEL_GUMB, CONFIRM_GUMB]:
            gumb.changeColor(ESC_MOUSE_POS)
            gumb.update(screen)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if CONFIRM_GUMB.checkForInput(ESC_MOUSE_POS):
                    zmaj = True
                    run = False
                if CANCEL_GUMB.checkForInput(ESC_MOUSE_POS):
                    run = False
        pygame.display.update()
        clock.tick(FPS)

        



def play():
    CARRIER = Brod(os.path.join("potapanje brodova", "carrier5.png"), 93, 35)
    BATTLESHIP = Brod(os.path.join("potapanje brodova", "battleship4.png"), 360, 35)
    DESTROYER = Brod(os.path.join("potapanje brodova", "destroyer3.png"), 225, 90)
    SUBMARINE = Brod(os.path.join("potapanje brodova", "submarine3.png"), 400, 90)
    PATROL = Brod(os.path.join("potapanje brodova", "patrol2.png"), 97, 90)
    BRODOVI_GRUPA.add(CARRIER,BATTLESHIP,PATROL,DESTROYER,SUBMARINE)
    run = True
    global zmaj
    global brodovi_rotacija
    brodovi_rotacija = {CARRIER: 0, BATTLESHIP: 0, DESTROYER: 0, SUBMARINE: 0, PATROL: 0}
    while run:
        zmaj = False
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
                    esc_screen('Are you sure you want to exit current game?', PROZOR)
                    if zmaj == True:
                        run = False
                    else: pass
            if event.type == MOUSEBUTTONDOWN:
                CARRIER.collide()
                BATTLESHIP.collide()
                DESTROYER.collide()
                SUBMARINE.collide()
                PATROL.collide()
                if brod == CARRIER:
                    čekanje_za_odabir(CARRIER,brodovi_rotacija.get(CARRIER))
        
                elif brod == BATTLESHIP:
                    čekanje_za_odabir(BATTLESHIP,brodovi_rotacija.get(BATTLESHIP))

                elif brod == SUBMARINE:
                    čekanje_za_odabir(SUBMARINE,brodovi_rotacija.get(SUBMARINE))

                elif brod == DESTROYER:
                    čekanje_za_odabir(DESTROYER,brodovi_rotacija.get(DESTROYER))

                elif brod == PATROL:
                    čekanje_za_odabir(PATROL,brodovi_rotacija.get(PATROL))

                

        pygame.display.update()
        clock.tick(FPS)

def main():
    #LOADING_SCREEN()
    global zmaj
    while True:
        zmaj = False
        PROZOR.fill('White')
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        GUMB_PLAY = Button(text_input = "Play", text_size = 30, text_color = 'Black', rect_width = 200, rect_height = 40, rect_color = '#475F77', hoveringRect_color = '#77dd77', pos = (640,200))
        GUMB_SCORE = Button(text_input = "Score", text_size = 30, text_color = 'Black', rect_width = 200, rect_height = 40, rect_color = '#475F77', hoveringRect_color = '#77dd77', pos = (640,275))
        GUMB_EXIT = Button(text_input = "Exit", text_size = 30, text_color = 'Black', rect_width = 200, rect_height = 40, rect_color = '#475F77', hoveringRect_color = '#D74B4B', pos = (640,350))
        for gumb in [GUMB_PLAY, GUMB_SCORE, GUMB_EXIT]:
            gumb.changeColor(MENU_MOUSE_POS)
            gumb.update(PROZOR)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    esc_screen('Are you sure you want to quit the game?', PROZOR)
                    if zmaj == True:
                        pygame.quit()
                        sys.exit()
                    else: pass
            if event.type == MOUSEBUTTONDOWN:
                if GUMB_PLAY.checkForInput(MENU_MOUSE_POS):
                    play()
                if GUMB_SCORE.checkForInput(MENU_MOUSE_POS):
                    pass
                if GUMB_EXIT.checkForInput(MENU_MOUSE_POS):
                    esc_screen('Are you sure you want to quit the game?', PROZOR)
                    if zmaj == True:
                        pygame.quit()
                        sys.exit()
                    else: pass
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
