from ast import main
import pygame, sys
import os
import time
pygame.init()
pygame.mixer.init()
from pygame.locals import * 

ŠIRINA, VISINA = 1280, 720
PROZOR = pygame.display.set_mode((ŠIRINA, VISINA))
pygame.display.set_caption("Potapanje brodova")
PROZOR.fill('White')

FONT = pygame.font.Font(None, 30)
FONT_BROJ_SLOVO = pygame.font.Font(None, 40)
FPS = 60

WHITE = (255,255,255)
LOGO = pygame.image.load(os.path.join("potapanje brodova", "MLKJR_LOGO.png" ))
INTRO = pygame.mixer.Sound(os.path.join("potapanje brodova", "INTRO.ogg"))

KVADRAT = pygame.image.load(os.path.join("potapanje brodova", "kvadrat.png"))
#CARRIER_SLIKA = pygame.image.load(os.path.join("potapanje brodova", "carrier5.png"))
#BATTLESHIP_SLIKA = pygame.image.load(os.path.join("potapanje brodova", "battleship4.png"))
#DESTROYER_SLIKA = pygame.image.load(os.path.join("potapanje brodova", "destroyer3.png"))
#SUBMARINE_SLIKA = pygame.image.load(os.path.join("potapanje brodova", "submarine3.png"))
#PATROL_SLIKA = pygame.image.load(os.path.join("potapanje brodova", "patrol2.png"))

BRODOVI_GRUPA = pygame.sprite.Group()

class Brod(pygame.sprite.Sprite):
    def __init__(self,picture_path,poz_x,poz_y):
        super().__init__()
        #rectangle
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.topleft =(poz_x, poz_y)
    





        

## OVO MORA LUKA DOVRŠIT
class Button:
    def __init__(self, text, width, height, poz):
        #top rectangle izgled
        self.top_rect = pygame.Rect(poz, (width,height))
        self.top_boja = '#475F77'
        #tekst u gumbu
        self.text_surf = FONT.render(text,1,'Black')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        self.name = text


    def CrtajGumb(self):
        pygame.draw.rect(PROZOR,self.top_boja, self.top_rect,)
        PROZOR.blit(self.text_surf, self.text_rect)
        pygame.display.update()
    
    def provjeri_klik(self):
        mouse_poz = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_poz):
            if pygame.mouse.get_pressed()[0]:
                if self.name == 'Play':
                    play()
                if self.name == 'Exit game':
                    #Možemo dodat da iskoči prozor i pita 'Are you sure you want to exit the game?'
                    pygame.quit()


def play():
    GRIDLIJEVO()
    GRIDDESNO()
    Brojevi()
    Slova()
    BRODOVI_GRUPA.draw(PROZOR)
    pygame.display.update()

def LOADING_SCREEN():
    PROZOR.fill(WHITE)
    PROZOR.blit(LOGO,(150,0))
    pygame.mixer.Sound.play(INTRO)
    pygame.display.update()
    time.sleep(4)                
    PROZOR.fill(WHITE)       
              
def GRIDLIJEVO():
    PROZOR.fill(WHITE)
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
    pygame.display.update()

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
    pygame.display.update()


def Brojevi():
    broj_x = 70
    broj_y = 160
    for i in range(1,11):
        broj = FONT_BROJ_SLOVO.render(str(i),1,'Black')
        if i == 10:
            broj_x = broj_x - 10
        broj_rect = broj.get_rect(topleft = (broj_x, broj_y))
        PROZOR.blit(broj, broj_rect)
        pygame.display.update()
        broj_y = broj_y + 48

def Slova():
    slovo_x = 113
    slovo_y = 637
    for i in range(0,10):
        slovo = FONT_BROJ_SLOVO.render(str(chr(ord("A")+i)),1,'Black')
        #if i == 10:
        #    broj_x = broj_x - 10
        slovo_rect = slovo.get_rect(topleft = (slovo_x, slovo_y))
        PROZOR.blit(slovo, slovo_rect)
        pygame.display.update()
        slovo_x = slovo_x + 48





CARRIER = Brod(os.path.join("potapanje brodova", "carrier5.png"), 93, 35)
BATTLESHIP = Brod(os.path.join("potapanje brodova", "battleship4.png"), 360, 35)
DESTROYER = Brod(os.path.join("potapanje brodova", "destroyer3.png"), 225, 90)
SUBMARINE = Brod(os.path.join("potapanje brodova", "submarine3.png"), 400, 90)
PATROL = Brod(os.path.join("potapanje brodova", "patrol2.png"), 97, 90)

BRODOVI_GRUPA.add(CARRIER,BATTLESHIP,PATROL,DESTROYER,SUBMARINE)


def main():
    clock = pygame.time.Clock()
    run = True
    #LOADING_SCREEN()
    
    GUMB_PLAY = Button('Play',200,40,(ŠIRINA/2 - 100,200))
    GUMB_EXIT = Button('Exit game',200,40,(ŠIRINA/2 - 100,350))
    GUMB_SCORE = Button('View score',200,40,(ŠIRINA/2 - 100,275))
    GUMB_PLAY.CrtajGumb()
    GUMB_SCORE.CrtajGumb()
    GUMB_EXIT.CrtajGumb()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        GUMB_PLAY.provjeri_klik()
        GUMB_EXIT.provjeri_klik()
        
    

    pygame.quit()



if __name__ == "__main__":
    main()