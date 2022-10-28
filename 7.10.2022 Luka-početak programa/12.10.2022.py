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
XISIC = pygame.image.load(os.path.join("potapanje brodova", "xisic.png"))
FULANO = pygame.image.load(os.path.join("potapanje brodova", "fulano.png"))
ODABRANI_KVADRAT = pygame.image.load(os.path.join("potapanje brodova", "odabrani_kvadrat.png"))
VLASTITI_POGODEN = pygame.image.load(os.path.join("potapanje brodova", "pogoden_vlastiti_brod.png"))

#Sve za Brod spriteove i provjere postavljanja
Kvadrat_x, Kvadrat_y = 0, 0
brod = None
brod_velkiX = None

lista_rect_kvadrata_A = []
lista_imena_kvadrata_A = []
lista_imena_kvadrata_B = []
lista_rect_kvadrata_B = []

#Služi da se određeni programi izvrše samo jednom
PROVJERA= True
izrada_liste_A = True
izrada_liste_B = True
zapis_rezultata_jednom = True

#Sve za profile i biranje
PLAYERI_SELEKTIRANI = {}
PLAYERI_IMENA = {}
PLAYERI_LISTA_GUMBOVA = []
selektirani_profili = []


class Brod(pygame.sprite.Sprite):
    def __init__(self,picture_path,poz_x,poz_y):
        super().__init__()
        #rectangle
        self.pozx = poz_x
        self.pozy = poz_y
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.topleft =(poz_x, poz_y)
       
    
    def rotacija_poz_90(self,brod_velkiX,poz_broda_x,poz_broda_y):    
        brod_velkiX.image = pygame.transform.rotate(brod_velkiX.image, 90)
        brod_velkiX.rect = brod_velkiX.image.get_rect()
        brod_velkiX.rect.topleft =(poz_broda_x+590, poz_broda_y)
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.topleft =(poz_broda_x, poz_broda_y)
        

    def rotacija_neg_90(self,brod_velkiX,poz_broda_x,poz_broda_y):
        brod_velkiX.image = pygame.transform.rotate(brod_velkiX.image, -90)
        brod_velkiX.rect = brod_velkiX.image.get_rect()
        brod_velkiX.rect.topleft =(poz_broda_x+590, poz_broda_y)
        self.image = pygame.transform.rotate(self.image, -90)
        self.rect = self.image.get_rect()
        self.rect.topleft =(poz_broda_x, poz_broda_y)


        
        

    def collide(self):
        global brod_collidean
        global duljina_broda
        global brod_izabran
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
            brod_izabran = True
            brod_collidean = self
    
    def vrati_nazad(self,brod_velkiX,brodovi_rotacija,brodovi_pozicije):#Vraća brodove na prvobitne pozicije brodova 
        global vrati_nazad_provjera
        vrati_nazad_provjera = True
        poz_x = self.pozx
        poz_y = self.pozy
        if brodovi_rotacija.get(self) == 1:
            self.image = pygame.transform.rotate(self.image, -90)
            brod_velkiX.image = pygame.transform.rotate(brod_velkiX.image, -90)
            brodovi_rotacija.update({self:0})
        brod_velkiX.rect.topleft = poz_x + 590, poz_y
        self.rect.topleft = poz_x, poz_y
        brodovi_pozicije.update({self:(poz_x, poz_y)})
       

        
class Veliki_Xevi(pygame.sprite.Sprite):
     def __init__(self,picture_path,poz_x,poz_y):
        super().__init__()
        self.pozx = poz_x
        self.pozy = poz_y
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.topleft =(poz_x, poz_y)
        
               
def čekanje_za_odabir(brod,brod_r,brod_velkiX,brodovi_rotacija,Brodovi_grupa,lista_rect_kvadrata,brodovi_pozicije,crtanje_imena):
    global idi
    global Kvadrat_x, Kvadrat_y
    idi = True
    while idi:
        čekanje_mouse_poz = pygame.mouse.get_pos()
        PROZOR.fill(WHITE)
        gridA('lijevo')
        gridB('desno')
        Brodovi_grupa.draw(PROZOR)
        PROZOR.blit(crtanje_imena[0],crtanje_imena[1])
        if len(postavljeni_brodovi) < 5:
            CONFIRM_GUMB_PLAY = Button('Confirm', 30, 'Black', 200, 40, 'Grey', 'Grey', (1040,70))
            CONFIRM_GUMB_PLAY.update(PROZOR)
        else:
            CONFIRM_GUMB_PLAY = Button('Confirm', 30, 'Black', 200, 40, '#475F77', '#77dd77', (1040,70))
            CONFIRM_GUMB_PLAY.changeColor(play_mouse_pos)
            CONFIRM_GUMB_PLAY.update(PROZOR) 
        
        poz_broda_x, poz_broda_y = čekanje_mouse_poz
        brod.rect.topleft = (poz_broda_x-24, poz_broda_y-24) #brod prati cursor
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN and event.key == K_r:
                if brod_r == 0:
                    brod.rotacija_poz_90(brod_velkiX,poz_broda_x, poz_broda_y)
                    brodovi_rotacija.update({brod:1})
                    brod_r = 1
                   
                elif brod_r == 1: 
                    brod.rotacija_neg_90(brod_velkiX,poz_broda_x, poz_broda_y)
                    brodovi_rotacija.update({brod:0})
                    brod_r = 0
                    
                
            if event.type == MOUSEBUTTONDOWN:
                collide_kvadrat(brod_velkiX,brodovi_rotacija,lista_rect_kvadrata,brodovi_pozicije,brod)
                
       pygame.display.update()
                
def collide_kvadrat(brod_velkiX,brodovi_rotacija,lista_rect_kvadrata,brodovi_pozicije,brod):
    global Kvadrat_x, Kvadrat_y
    global idi
    global PROVJERA
    collide_mouse_poz = pygame.mouse.get_pos()
    for kvadrat in lista_rect_kvadrata:
            if kvadrat.collidepoint(collide_mouse_poz):
                if pygame.mouse.get_pressed()[0]:
                    Kvadrat_x, Kvadrat_y = kvadrat.x, kvadrat.y
                    brod.rect.topleft = (Kvadrat_x, Kvadrat_y)
                    brodovi_pozicije.update({brod:(Kvadrat_x,Kvadrat_y)})
                    brod_velkiX.rect.topleft = (Kvadrat_x + 590, Kvadrat_y)
                    while PROVJERA:
                        provjera(Kvadrat_x, Kvadrat_y, duljina_broda,brod,brod_velkiX,brodovi_rotacija,brodovi_pozicije)
                    idi = False
    PROVJERA= True    
 
 
                   

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
            
    def checkForClick(self, igrac):
        global run_pA
        global run_pB
        mouse_poz = pygame.mouse.get_pos()
        if self.main_rect.collidepoint(mouse_poz):
            zapis(igrac)
            run_pA = False
            run_pB = False

def provjera(x,y,duljinabroda,brod,brod_velkiX,brodovi_rotacija,brodovi_pozicije): #Provjerava stanu li brodovi u polje i preklapaju li se
    
    j = (y-100)/48 - 1
    i = (x-50)/48 - 1
    global PROVJERA
    if brodovi_rotacija.get(brod) == 1:
        if j + duljinabroda > 10:
            brod.vrati_nazad(brod_velkiX,brodovi_rotacija,brodovi_pozicije)
        else:
            for brodek in LISTA_BRODOVA:
                if brod != brodek:
                    if pygame.sprite.collide_rect(brodek,brod) == True:
                        brod.vrati_nazad(brod_velkiX,brodovi_rotacija,brodovi_pozicije)                                                                               
    if brodovi_rotacija.get(brod) == 0:
        if i + duljinabroda > 10:
            brod.vrati_nazad(brod_velkiX,brodovi_rotacija,brodovi_pozicije)
        else:
            for brodek in LISTA_BRODOVA:
                if brod != brodek:
                    if pygame.sprite.collide_rect(brodek,brod) == True:
                        brod.vrati_nazad(brod_velkiX,brodovi_rotacija,brodovi_pozicije)
    PROVJERA = False
    
def zapis(igrac): #zapisuje pozicije brodova u listu
    global lista_imena_kvadrata_A
    global lista_imena_kvadrata_B
    global LISTA_BRODOVA
    index = 0
    if igrac == 'A':
        for z in range(0,100):
            Kvadrat = ["a" + str(z)]
            lista_imena_kvadrata_A.append(Kvadrat)
        for kvadrat in lista_rect_kvadrata_A:
            if pygame.Rect.colliderect(kvadrat,LISTA_BRODOVA[0].rect):
                lista_imena_kvadrata_A[index].append("c")

            if pygame.Rect.colliderect(kvadrat,LISTA_BRODOVA[1].rect):
                lista_imena_kvadrata_A[index].append("b")

            if pygame.Rect.colliderect(kvadrat,LISTA_BRODOVA[2].rect):
                lista_imena_kvadrata_A[index].append("d")

            if pygame.Rect.colliderect(kvadrat,LISTA_BRODOVA[3].rect):
                lista_imena_kvadrata_A[index].append("s")

            if pygame.Rect.colliderect(kvadrat,LISTA_BRODOVA[4].rect):
                lista_imena_kvadrata_A[index].append("p")
            index += 1
    if igrac == 'B':
        for z in range(0,100):
            Kvadrat = ["b" + str(z)]
            lista_imena_kvadrata_B.append(Kvadrat)
        for kvadrat in lista_rect_kvadrata_B:
            if pygame.Rect.colliderect(kvadrat,LISTA_BRODOVA[0].rect):
                lista_imena_kvadrata_B[index].append("c")

            if pygame.Rect.colliderect(kvadrat,LISTA_BRODOVA[1].rect):
                lista_imena_kvadrata_B[index].append("b")

            if pygame.Rect.colliderect(kvadrat,LISTA_BRODOVA[2].rect):
                lista_imena_kvadrata_B[index].append("d")

            if pygame.Rect.colliderect(kvadrat,LISTA_BRODOVA[3].rect):
                lista_imena_kvadrata_B[index].append("s")

            if pygame.Rect.colliderect(kvadrat,LISTA_BRODOVA[4].rect):
                lista_imena_kvadrata_B[index].append("p")
            index += 1
    
def gridA(pozicija):
    global izrada_liste_A
    global lista_rect_kvadrata_A
    y = 100
    if pozicija == 'lijevo':
        #crtanje grida
        x = 50
        for i in range(10):
            y = y + 48
            x = 50
            for j in range (10):
                x = x + 48
                KVADRAT_RECT = KVADRAT.get_rect(topleft = (x,y))
                if izrada_liste_A == True:
                    lista_rect_kvadrata_A.append(KVADRAT_RECT)
                PROZOR.blit(KVADRAT,KVADRAT_RECT)
        izrada_liste_A = False

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
            slovo_rect = slovo.get_rect(topleft = (slovo_x, slovo_y))
            PROZOR.blit(slovo, slovo_rect)
            slovo_x = slovo_x + 48

    elif pozicija == 'desno':
        #crtanje grida
        x = 640
        for i in range(10):
            y = y + 48
            x = 640
            for j in range (10):
                x = x + 48
                KVADRAT_RECT = KVADRAT.get_rect(topleft = (x,y))
                if izrada_liste_A == True:
                    lista_rect_kvadrata_A.append(KVADRAT_RECT)
                PROZOR.blit(KVADRAT,KVADRAT_RECT)
        izrada_liste_A = False

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
            slovo_rect = slovo.get_rect(topleft = (slovo_x, slovo_y))
            PROZOR.blit(slovo, slovo_rect)
            slovo_x = slovo_x + 48

def gridB(pozicija):
    global izrada_liste_B
    global lista_rect_kvadrata_B
    y = 100
    if pozicija == 'lijevo':
        #crtanje grida
        x = 50
        for i in range(10):
            y = y + 48
            x = 50
            for j in range (10):
                x = x + 48
                KVADRAT_RECT = KVADRAT.get_rect(topleft = (x,y))
                if izrada_liste_B == True:
                    lista_rect_kvadrata_B.append(KVADRAT_RECT)
                PROZOR.blit(KVADRAT,KVADRAT_RECT)
        izrada_liste_B = False

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
            slovo_rect = slovo.get_rect(topleft = (slovo_x, slovo_y))
            PROZOR.blit(slovo, slovo_rect)
            slovo_x = slovo_x + 48

    else:
        #crtanje grida
        x = 640
        for i in range(10):
            y = y + 48
            x = 640
            for j in range (10):
                x = x + 48
                KVADRAT_RECT = KVADRAT.get_rect(topleft = (x,y))
                if izrada_liste_B == True:
                    lista_rect_kvadrata_B.append(KVADRAT_RECT)
                PROZOR.blit(KVADRAT,KVADRAT_RECT)
        izrada_liste_B = False

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

        
def postavljanje_igracaA():
    global run_pA
    global zmaj
    global play_mouse_pos
    global vrati_nazad_provjera
    global brod_izabran
    global postavljeni_brodovi
    global BRODOVI_GRUPA_A
    global VELIKI_XEVI_GRUPA_A
    global LISTA_BRODOVA
    global VELIKI_XEVI_LISTA_A
    global lista_rect_kvadrata_A
    global player_A
    global player_A_render
    global player_A_rect
    global PLAYERI_FONT

    player_A = selektirani_profili[0]
    postavljeni_brodovi = []
    LISTA_BRODOVA = []
    vrati_nazad_provjera = False
    brod_izabran = False
    
    PLAYERI_FONT = pygame.font.Font(None, 35)
    player_A_render = PLAYERI_FONT.render(player_A,1,'Black')
    player_A_rect = player_A_render.get_rect(center = (630, 20))
    
    crtanje_imena_lista_A = [player_A_render,player_A_rect]
    
    CARRIER = Brod(os.path.join("potapanje brodova", "carrier5.png"), 93, 35)
    BATTLESHIP = Brod(os.path.join("potapanje brodova", "battleship4.png"), 360, 35)
    DESTROYER = Brod(os.path.join("potapanje brodova", "destroyer3.png"), 225, 90)
    SUBMARINE = Brod(os.path.join("potapanje brodova", "submarine3.png"), 400, 90)
    PATROL = Brod(os.path.join("potapanje brodova", "patrol2.png"), 97, 90)
    
    BRODOVI_GRUPA_A = pygame.sprite.Group()
    BRODOVI_GRUPA_A.add(CARRIER,BATTLESHIP,DESTROYER,SUBMARINE,PATROL)
    LISTA_BRODOVA = BRODOVI_GRUPA_A.sprites()
    
    
    VELIKI_XEVI_GRUPA_A = pygame.sprite.Group()
    
    CARRIER_X = Veliki_Xevi(os.path.join("potapanje brodova", "carrier_X.png"), 93, 35)
    BATTLESHIP_X = Veliki_Xevi(os.path.join("potapanje brodova", "battleship_X.png"), 360, 35)
    DESTROYER_X = Veliki_Xevi(os.path.join("potapanje brodova", "sub,dest_X.png"), 225, 90)
    SUBMARINE_X = Veliki_Xevi(os.path.join("potapanje brodova", "sub,dest_X.png"), 400, 90)
    PATROL_X = Veliki_Xevi(os.path.join("potapanje brodova", "patrol_X.png"), 97, 90)
    VELIKI_XEVI_GRUPA_A.add(CARRIER_X,BATTLESHIP_X,DESTROYER_X,SUBMARINE_X,PATROL_X)
    
    CARRIER_X_GRUPA_A = pygame.sprite.GroupSingle(CARRIER_X)
    BATTLESHIP_X_GRUPA_A = pygame.sprite.GroupSingle(BATTLESHIP_X)
    DESTROYER_X_GRUPA_A = pygame.sprite.GroupSingle(DESTROYER_X)
    SUBMARINE_X_GRUPA_A = pygame.sprite.GroupSingle(SUBMARINE_X)
    PATROL_X_GRUPA_A = pygame.sprite.GroupSingle(PATROL_X)
    
    VELIKI_XEVI_LISTA_A = [CARRIER_X_GRUPA_A, BATTLESHIP_X_GRUPA_A, DESTROYER_X_GRUPA_A, SUBMARINE_X_GRUPA_A, PATROL_X_GRUPA_A]
    
    
    run_pA = True
    brodovi_pozicije_A = {CARRIER: (CARRIER.pozx, CARRIER.pozy), BATTLESHIP: (BATTLESHIP.pozx, BATTLESHIP.pozy), DESTROYER: (DESTROYER.pozx, DESTROYER.pozy), SUBMARINE: (SUBMARINE.pozx, SUBMARINE.pozy), PATROL: (PATROL.pozx, PATROL.pozy)}
    brodovi_rotacija_A = {CARRIER: 0, BATTLESHIP: 0, DESTROYER: 0, SUBMARINE: 0, PATROL: 0}
    while run_pA == True:
        play_mouse_pos = pygame.mouse.get_pos()
        zmaj = False
        PROZOR.fill('White')
        gridA('lijevo')
        gridB('desno')
        PROZOR.blit(player_A_render,player_A_rect)
        BRODOVI_GRUPA_A.draw(PROZOR)
        if len(postavljeni_brodovi) < 5:
            CONFIRM_GUMB_PLAY = Button('Confirm', 30, 'Black', 200, 40, 'Grey', 'Grey', (1040,70))
            CONFIRM_GUMB_PLAY.update(PROZOR)
        else:
            CONFIRM_GUMB_PLAY = Button('Confirm', 30, 'Black', 200, 40, '#475F77', '#77dd77', (1040,70))
            CONFIRM_GUMB_PLAY.changeColor(play_mouse_pos)
            CONFIRM_GUMB_PLAY.update(PROZOR)
            
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    esc_screen('Are you sure you want to exit current game?', PROZOR)
                    if zmaj == True:
                        run_pA = False
                    else: pass
            if event.type == MOUSEBUTTONDOWN:
                CARRIER.collide()
                BATTLESHIP.collide()
                DESTROYER.collide()
                SUBMARINE.collide()
                PATROL.collide()
                if len(postavljeni_brodovi) == 5:
                    CONFIRM_GUMB_PLAY.checkForClick('A')
                if run_pA == True:
                    if brod_izabran == True:
                        if brod_collidean == CARRIER:
                            čekanje_za_odabir(CARRIER,brodovi_rotacija_A.get(CARRIER),CARRIER_X,brodovi_rotacija_A,BRODOVI_GRUPA_A,lista_rect_kvadrata_A,brodovi_pozicije_A,crtanje_imena_lista_A)
                            if "C" not in postavljeni_brodovi and vrati_nazad_provjera == False:
                                postavljeni_brodovi.append("C")
                            elif vrati_nazad_provjera == True:
                                vrati_nazad_provjera = False
                                if "C" in postavljeni_brodovi:
                                    postavljeni_brodovi.remove("C")
                            brod_izabran = False
            
                        elif brod_collidean == BATTLESHIP:
                            čekanje_za_odabir(BATTLESHIP,brodovi_rotacija_A.get(BATTLESHIP),BATTLESHIP_X,brodovi_rotacija_A,BRODOVI_GRUPA_A,lista_rect_kvadrata_A,brodovi_pozicije_A,crtanje_imena_lista_A)
                            if "B" not in postavljeni_brodovi and vrati_nazad_provjera == False:
                                postavljeni_brodovi.append("B")
                            elif vrati_nazad_provjera == True:
                                vrati_nazad_provjera = False
                                if "B" in postavljeni_brodovi:
                                    postavljeni_brodovi.remove("B")
                            brod_izabran = False

                        elif brod_collidean == SUBMARINE:
                            čekanje_za_odabir(SUBMARINE,brodovi_rotacija_A.get(SUBMARINE),SUBMARINE_X,brodovi_rotacija_A,BRODOVI_GRUPA_A,lista_rect_kvadrata_A,brodovi_pozicije_A,crtanje_imena_lista_A)
                            if "S" not in postavljeni_brodovi and vrati_nazad_provjera == False:
                                postavljeni_brodovi.append("S")
                            elif vrati_nazad_provjera == True:
                                vrati_nazad_provjera = False
                                if "S" in postavljeni_brodovi:
                                    postavljeni_brodovi.remove("S")
                            brod_izabran = False
                                                    
                        elif brod_collidean == DESTROYER:
                            čekanje_za_odabir(DESTROYER,brodovi_rotacija_A.get(DESTROYER),DESTROYER_X,brodovi_rotacija_A,BRODOVI_GRUPA_A,lista_rect_kvadrata_A,brodovi_pozicije_A,crtanje_imena_lista_A)
                            if "D" not in postavljeni_brodovi and vrati_nazad_provjera == False:
                                postavljeni_brodovi.append("D")
                            elif vrati_nazad_provjera == True:
                                vrati_nazad_provjera = False
                                if "D" in postavljeni_brodovi:
                                    postavljeni_brodovi.remove("D")
                            brod_izabran = False

                        elif brod_collidean == PATROL:
                            čekanje_za_odabir(PATROL,brodovi_rotacija_A.get(PATROL),PATROL_X,brodovi_rotacija_A,BRODOVI_GRUPA_A,lista_rect_kvadrata_A,brodovi_pozicije_A,crtanje_imena_lista_A)
                            if "P" not in postavljeni_brodovi and vrati_nazad_provjera == False:
                                postavljeni_brodovi.append("P")
                            elif vrati_nazad_provjera == True:
                                vrati_nazad_provjera = False
                                if "P" in postavljeni_brodovi:
                                    postavljeni_brodovi.remove("P")
                            brod_izabran = False
                    
                   
                

        pygame.display.update()
        clock.tick(FPS)
        
def postavljanje_igracaB():
    global run_pB
    global zmaj
    global play_mouse_pos
    global vrati_nazad_provjera
    global brod_izabran
    global postavljeni_brodovi
    global BRODOVI_GRUPA_B
    global VELIKI_XEVI_GRUPA_B
    global LISTA_BRODOVA
    global VELIKI_XEVI_LISTA_B
    global lista_rect_kvadrata_B
    global player_B
    global player_B_render
    global player_B_rect
    
    player_B = selektirani_profili[1]
    postavljeni_brodovi = []
    LISTA_BRODOVA = []
    vrati_nazad_provjera = False
    brod_izabran = False
    
    player_B_render = PLAYERI_FONT.render(player_B,1,'Black')
    player_B_rect = player_B_render.get_rect(center = (630, 20))
    
    crtanje_imena_lista_B = [player_B_render,player_B_rect]
    
    CARRIER = Brod(os.path.join("potapanje brodova", "carrier5.png"), 93, 35)
    BATTLESHIP = Brod(os.path.join("potapanje brodova", "battleship4.png"), 360, 35)
    DESTROYER = Brod(os.path.join("potapanje brodova", "destroyer3.png"), 225, 90)
    SUBMARINE = Brod(os.path.join("potapanje brodova", "submarine3.png"), 400, 90)
    PATROL = Brod(os.path.join("potapanje brodova", "patrol2.png"), 97, 90)
    
    BRODOVI_GRUPA_B = pygame.sprite.Group()
    BRODOVI_GRUPA_B.add(CARRIER,BATTLESHIP,DESTROYER,SUBMARINE,PATROL)
    LISTA_BRODOVA = BRODOVI_GRUPA_B.sprites()
    
    
    VELIKI_XEVI_GRUPA_B = pygame.sprite.Group()
    
    CARRIER_X = Veliki_Xevi(os.path.join("potapanje brodova", "carrier_X.png"), 93, 35)
    BATTLESHIP_X = Veliki_Xevi(os.path.join("potapanje brodova", "battleship_X.png"), 360, 35)
    DESTROYER_X = Veliki_Xevi(os.path.join("potapanje brodova", "sub,dest_X.png"), 225, 90)
    SUBMARINE_X = Veliki_Xevi(os.path.join("potapanje brodova", "sub,dest_X.png"), 400, 90)
    PATROL_X = Veliki_Xevi(os.path.join("potapanje brodova", "patrol_X.png"), 97, 90)
    VELIKI_XEVI_GRUPA_B.add(CARRIER_X,BATTLESHIP_X,DESTROYER_X,SUBMARINE_X,PATROL_X)
    
    CARRIER_X_GRUPA_B = pygame.sprite.GroupSingle(CARRIER_X)
    BATTLESHIP_X_GRUPA_B = pygame.sprite.GroupSingle(BATTLESHIP_X)
    DESTROYER_X_GRUPA_B = pygame.sprite.GroupSingle(DESTROYER_X)
    SUBMARINE_X_GRUPA_B = pygame.sprite.GroupSingle(SUBMARINE_X)
    PATROL_X_GRUPA_B = pygame.sprite.GroupSingle(PATROL_X)
    
    VELIKI_XEVI_LISTA_B = [CARRIER_X_GRUPA_B,BATTLESHIP_X_GRUPA_B,DESTROYER_X_GRUPA_B,SUBMARINE_X_GRUPA_B,PATROL_X_GRUPA_B]
    
    
    run_pB = True
    brodovi_pozicije_B = {CARRIER: (CARRIER.pozx, CARRIER.pozy), BATTLESHIP: (BATTLESHIP.pozx, BATTLESHIP.pozy), DESTROYER: (DESTROYER.pozx, DESTROYER.pozy), SUBMARINE: (SUBMARINE.pozx, SUBMARINE.pozy), PATROL: (PATROL.pozx, PATROL.pozy)}
    brodovi_rotacija_B = {CARRIER: 0, BATTLESHIP: 0, DESTROYER: 0, SUBMARINE: 0, PATROL: 0}
    while run_pB == True:
        play_mouse_pos = pygame.mouse.get_pos()
        zmaj = False
        PROZOR.fill('White')
        gridA('desno')
        gridB('lijevo')
        PROZOR.blit(player_B_render,player_B_rect)
        BRODOVI_GRUPA_B.draw(PROZOR)
        
        if len(postavljeni_brodovi) < 5:
            CONFIRM_GUMB_PLAY = Button('Confirm', 30, 'Black', 200, 40, 'Grey', 'Grey', (1040,70))
            CONFIRM_GUMB_PLAY.update(PROZOR)
        else:
            CONFIRM_GUMB_PLAY = Button('Confirm', 30, 'Black', 200, 40, '#475F77', '#77dd77', (1040,70))
            CONFIRM_GUMB_PLAY.changeColor(play_mouse_pos)
            CONFIRM_GUMB_PLAY.update(PROZOR)
            
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    esc_screen('Are you sure you want to exit current game?', PROZOR)
                    if zmaj == True:
                        run_pB = False
                    else: pass
            if event.type == MOUSEBUTTONDOWN:
                CARRIER.collide()
                BATTLESHIP.collide()
                DESTROYER.collide()
                SUBMARINE.collide()
                PATROL.collide()
                if len(postavljeni_brodovi) == 5:
                    CONFIRM_GUMB_PLAY.checkForClick('B')
                if run_pB == True:
                    if brod_izabran == True:
                        if brod_collidean == CARRIER:
                            čekanje_za_odabir(CARRIER,brodovi_rotacija_B.get(CARRIER),CARRIER_X,brodovi_rotacija_B,BRODOVI_GRUPA_B,lista_rect_kvadrata_B,brodovi_pozicije_B,crtanje_imena_lista_B)
                            if "C" not in postavljeni_brodovi and vrati_nazad_provjera == False:
                                postavljeni_brodovi.append("C")
                            elif vrati_nazad_provjera == True:
                                vrati_nazad_provjera = False
                                if "C" in postavljeni_brodovi:
                                    postavljeni_brodovi.remove("C")
                            brod_izabran = False
            
                        elif brod_collidean == BATTLESHIP:
                            čekanje_za_odabir(BATTLESHIP,brodovi_rotacija_B.get(BATTLESHIP),BATTLESHIP_X,brodovi_rotacija_B,BRODOVI_GRUPA_B,lista_rect_kvadrata_B,brodovi_pozicije_B,crtanje_imena_lista_B)
                            if "B" not in postavljeni_brodovi and vrati_nazad_provjera == False:
                                postavljeni_brodovi.append("B")
                            elif vrati_nazad_provjera == True:
                                vrati_nazad_provjera = False
                                if "B" in postavljeni_brodovi:
                                    postavljeni_brodovi.remove("B")
                            brod_izabran = False

                        elif brod_collidean == SUBMARINE:
                            čekanje_za_odabir(SUBMARINE,brodovi_rotacija_B.get(SUBMARINE),SUBMARINE_X,brodovi_rotacija_B,BRODOVI_GRUPA_B,lista_rect_kvadrata_B,brodovi_pozicije_B,crtanje_imena_lista_B)
                            if "S" not in postavljeni_brodovi and vrati_nazad_provjera == False:
                                postavljeni_brodovi.append("S")
                            elif vrati_nazad_provjera == True:
                                vrati_nazad_provjera = False
                                if "S" in postavljeni_brodovi:
                                    postavljeni_brodovi.remove("S")
                            brod_izabran = False
                                                    
                        elif brod_collidean == DESTROYER:
                            čekanje_za_odabir(DESTROYER,brodovi_rotacija_B.get(DESTROYER),DESTROYER_X,brodovi_rotacija_B,BRODOVI_GRUPA_B,lista_rect_kvadrata_B,brodovi_pozicije_B,crtanje_imena_lista_B)
                            if "D" not in postavljeni_brodovi and vrati_nazad_provjera == False:
                                postavljeni_brodovi.append("D")
                            elif vrati_nazad_provjera == True:
                                vrati_nazad_provjera = False
                                if "D" in postavljeni_brodovi:
                                    postavljeni_brodovi.remove("D")
                            brod_izabran = False

                        elif brod_collidean == PATROL:
                            čekanje_za_odabir(PATROL,brodovi_rotacija_B.get(PATROL),PATROL_X,brodovi_rotacija_B,BRODOVI_GRUPA_B,lista_rect_kvadrata_B,brodovi_pozicije_B,crtanje_imena_lista_B)
                            if "P" not in postavljeni_brodovi and vrati_nazad_provjera == False:
                                postavljeni_brodovi.append("P")
                            elif vrati_nazad_provjera == True:
                                vrati_nazad_provjera = False
                                if "P" in postavljeni_brodovi:
                                    postavljeni_brodovi.remove("P")
                            brod_izabran = False
                    
                   
                

        pygame.display.update()
        clock.tick(FPS)

def crtanje_fulanih_podrucja():  # Funkcija crta područja na gridu gdje su oba igrača fulala brod
    for i in range(0,100):
            rectA = lista_rect_kvadrata_A[i]
            rectB = lista_rect_kvadrata_B[i]
            if len(lista_imena_kvadrata_A[i]) == 2:
                if lista_imena_kvadrata_A[i][1] == 'x':
                    fulano_rectA = FULANO.get_rect(topleft = (rectA.topleft))
                    PROZOR.blit(FULANO, fulano_rectA)
            if len(lista_imena_kvadrata_B[i]) == 2:
                if lista_imena_kvadrata_B[i][1] == 'x':
                    fulano_rectB = FULANO.get_rect(topleft = (rectB.topleft))
                    PROZOR.blit(FULANO, fulano_rectB)

def zbrajanje_pogodenih_dijelova_brodova():  # Funkcija sprema u zasebne varijable zbroj koliko je puta neki brod pogoden; informacije potrebne za funkciju crtanje_xeva()
    global patrolA_counter, submarineA_counter, destroyerA_counter, battleshipA_counter, carrierA_counter, patrolB_counter, submarineB_counter, destroyerB_counter, battleshipB_counter, carrierB_counter
    patrolA_counter, submarineA_counter, destroyerA_counter, battleshipA_counter, carrierA_counter = 0, 0, 0, 0, 0
    patrolB_counter, submarineB_counter, destroyerB_counter, battleshipB_counter, carrierB_counter = 0, 0, 0, 0, 0
    for i in range(0,100):
        if len(lista_imena_kvadrata_A[i]) == 3:
            if lista_imena_kvadrata_A[i][1] == 'p' and lista_imena_kvadrata_A[i][2] == 'x':
                patrolA_counter += 1
            elif lista_imena_kvadrata_A[i][1] == 's' and lista_imena_kvadrata_A[i][2] == 'x':
                submarineA_counter += 1
            elif lista_imena_kvadrata_A[i][1] == 'd' and lista_imena_kvadrata_A[i][2] == 'x':
                destroyerA_counter += 1
            elif lista_imena_kvadrata_A[i][1] == 'b' and lista_imena_kvadrata_A[i][2] == 'x':
                battleshipA_counter += 1
            elif lista_imena_kvadrata_A[i][1] == 'c' and lista_imena_kvadrata_A[i][2] == 'x':
                carrierA_counter += 1
        if len(lista_imena_kvadrata_B[i]) == 3:
            if lista_imena_kvadrata_B[i][1] == 'p' and lista_imena_kvadrata_B[i][2] == 'x':
                patrolB_counter += 1
            elif lista_imena_kvadrata_B[i][1] == 's' and lista_imena_kvadrata_B[i][2] == 'x':
                submarineB_counter += 1
            elif lista_imena_kvadrata_B[i][1] == 'd' and lista_imena_kvadrata_B[i][2] == 'x':
                destroyerB_counter += 1
            elif lista_imena_kvadrata_B[i][1] == 'b' and lista_imena_kvadrata_B[i][2] == 'x':
                battleshipB_counter += 1
            elif lista_imena_kvadrata_B[i][1] == 'c' and lista_imena_kvadrata_B[i][2] == 'x':
                carrierB_counter += 1

def crtanje_xeva(igrac):  # Funkcija provjerava jesu li pogodeni suparnicki brodovi i crta x-eve ako jesu, crta jedan veliki x ako je cijeli brod unisten
    if igrac == 'A':
        if patrolB_counter == 2:
            VELIKI_XEVI_LISTA_B[4].draw(PROZOR)
        else:
            for i in range(0,100):
                recB = lista_rect_kvadrata_B[i]
                if len(lista_imena_kvadrata_B[i]) == 3:
                    if lista_imena_kvadrata_B[i][1] == 'p' and lista_imena_kvadrata_B[i][2] == 'x':
                        xisic_rectB = XISIC.get_rect(topleft = (recB.topleft))
                        PROZOR.blit(XISIC, xisic_rectB)
        if submarineB_counter == 3:
            VELIKI_XEVI_LISTA_B[3].draw(PROZOR)
        else:
            for i in range(0,100):
                recB = lista_rect_kvadrata_B[i]
                if len(lista_imena_kvadrata_B[i]) == 3:
                    if lista_imena_kvadrata_B[i][1] == 's' and lista_imena_kvadrata_B[i][2] == 'x':
                        xisic_rectB = XISIC.get_rect(topleft = (recB.topleft))
                        PROZOR.blit(XISIC, xisic_rectB)
        if destroyerB_counter == 3:
            VELIKI_XEVI_LISTA_B[2].draw(PROZOR)
        else:
            for i in range(0,100):
                recB = lista_rect_kvadrata_B[i]
                if len(lista_imena_kvadrata_B[i]) == 3:
                    if lista_imena_kvadrata_B[i][1] == 'd' and lista_imena_kvadrata_B[i][2] == 'x':
                        xisic_rectB = XISIC.get_rect(topleft = (recB.topleft))
                        PROZOR.blit(XISIC, xisic_rectB)
        if battleshipB_counter == 4:
            VELIKI_XEVI_LISTA_B[1].draw(PROZOR)
        else:
            for i in range(0,100):
                recB = lista_rect_kvadrata_B[i]
                if len(lista_imena_kvadrata_B[i]) == 3:
                    if lista_imena_kvadrata_B[i][1] == 'b' and lista_imena_kvadrata_B[i][2] == 'x':
                        xisic_rectB = XISIC.get_rect(topleft = (recB.topleft))
                        PROZOR.blit(XISIC, xisic_rectB)
        if carrierB_counter == 5:
            VELIKI_XEVI_LISTA_B[0].draw(PROZOR)
        else:
            for i in range(0,100):
                recB = lista_rect_kvadrata_B[i]
                if len(lista_imena_kvadrata_B[i]) == 3:
                    if lista_imena_kvadrata_B[i][1] == 'c' and lista_imena_kvadrata_B[i][2] == 'x':
                        xisic_rectB = XISIC.get_rect(topleft = (recB.topleft))
                        PROZOR.blit(XISIC, xisic_rectB)
    elif igrac == 'B':
        if patrolA_counter == 2:
            VELIKI_XEVI_LISTA_A[4].draw(PROZOR)
        else:
            for i in range(0,100):
                recA = lista_rect_kvadrata_A[i]
                if len(lista_imena_kvadrata_A[i]) == 3:
                    if lista_imena_kvadrata_A[i][1] == 'p' and lista_imena_kvadrata_A[i][2] == 'x':
                        xisic_rectA = XISIC.get_rect(topleft = (recA.topleft))
                        PROZOR.blit(XISIC, xisic_rectA)
        if submarineA_counter == 3:
            VELIKI_XEVI_LISTA_A[3].draw(PROZOR)
        else:
            for i in range(0,100):
                recA = lista_rect_kvadrata_A[i]
                if len(lista_imena_kvadrata_A[i]) == 3:
                    if lista_imena_kvadrata_A[i][1] == 's' and lista_imena_kvadrata_A[i][2] == 'x':
                        xisic_rectA = XISIC.get_rect(topleft = (recA.topleft))
                        PROZOR.blit(XISIC, xisic_rectA)
        if destroyerA_counter == 3:
            VELIKI_XEVI_LISTA_A[2].draw(PROZOR)
        else:
            for i in range(0,100):
                recA = lista_rect_kvadrata_A[i]
                if len(lista_imena_kvadrata_A[i]) == 3:
                    if lista_imena_kvadrata_A[i][1] == 'd' and lista_imena_kvadrata_A[i][2] == 'x':
                        xisic_rectA = XISIC.get_rect(topleft = (recA.topleft))
                        PROZOR.blit(XISIC, xisic_rectA)
        if battleshipA_counter == 4:
            VELIKI_XEVI_LISTA_A[1].draw(PROZOR)
        else:
            for i in range(0,100):
                recA = lista_rect_kvadrata_A[i]
                if len(lista_imena_kvadrata_A[i]) == 3:
                    if lista_imena_kvadrata_A[i][1] == 'b' and lista_imena_kvadrata_A[i][2] == 'x':
                        xisic_rectA = XISIC.get_rect(topleft = (recA.topleft))
                        PROZOR.blit(XISIC, xisic_rectA)
        if carrierA_counter == 5:
            VELIKI_XEVI_LISTA_A[0].draw(PROZOR)
        else:
            for i in range(0,100):
                recA = lista_rect_kvadrata_A[i]
                if len(lista_imena_kvadrata_A[i]) == 3:
                    if lista_imena_kvadrata_A[i][1] == 'c' and lista_imena_kvadrata_A[i][2] == 'x':
                        xisic_rectA = XISIC.get_rect(topleft = (recA.topleft))
                        PROZOR.blit(XISIC, xisic_rectA)          

def crtanje_pogodenih_vlastitih(igrac):  # Funkcija provjerava i crta vatru ondje gdje je brod pogođen SAMO NA GRIDU IGRACA KOJI IGRA
    if igrac == 'A':
        for i in range(0,100):
            recA = lista_rect_kvadrata_A[i]
            if len(lista_imena_kvadrata_A[i]) == 3:
                if lista_imena_kvadrata_A[i][2] == 'x':
                    pogoden_rectA = VLASTITI_POGODEN.get_rect(topleft = (recA.topleft))
                    PROZOR.blit(VLASTITI_POGODEN, pogoden_rectA)
    elif igrac == 'B':   
        for i in range(0,100):
            recB = lista_rect_kvadrata_B[i]
            if len(lista_imena_kvadrata_B[i]) == 3:
                if lista_imena_kvadrata_B[i][2] == 'x':
                    pogoden_rectB = VLASTITI_POGODEN.get_rect(topleft = (recB.topleft))
                    PROZOR.blit(VLASTITI_POGODEN, pogoden_rectB)                 

def hoveranje_animacija(igrac, mis_poz):  # Funkcija provjerava nalazi li se mis iznad kvadratica, ako da onda nacrta poseban kvadratic da to oznaci
    HOVERANI_KVADRAT = pygame.image.load(os.path.join("potapanje brodova", "hoverani_kvadrat.png"))
    if igrac == 'A':
        for i in range(0,100):
            rect = lista_rect_kvadrata_B[i]
            hoverani_rect = HOVERANI_KVADRAT.get_rect(topleft = (rect.topleft))
            if rect.collidepoint(mis_poz):
                if len(lista_imena_kvadrata_B[i]) == 1:
                    PROZOR.blit(HOVERANI_KVADRAT, hoverani_rect)
                elif len(lista_imena_kvadrata_B[i]) == 2:
                    if lista_imena_kvadrata_B[i][1] != 'x':
                        PROZOR.blit(HOVERANI_KVADRAT, hoverani_rect)
    if igrac == 'B':
        for i in range(0,100):
            rect = lista_rect_kvadrata_A[i]
            hoverani_rect = HOVERANI_KVADRAT.get_rect(topleft = (rect.topleft))
            if rect.collidepoint(mis_poz):
                if len(lista_imena_kvadrata_A[i]) == 1:
                    PROZOR.blit(HOVERANI_KVADRAT, hoverani_rect)
                elif len(lista_imena_kvadrata_A[i]) == 2:
                    if lista_imena_kvadrata_A[i][1] != 'x':
                        PROZOR.blit(HOVERANI_KVADRAT, hoverani_rect)                

def crtanje_odabranog_kvadrata(igrac):  # Funkcija na ekranu crta označeni kvadratić na gridu
    global postavljen_kvadratA
    global postavljen_kvadratB
    if igrac == 'A':
        if postavljen_kvadratA:
            PROZOR.blit(ODABRANI_KVADRAT, odabrani_kvadrat_rectA)
        pass
    if igrac == 'B':
        if postavljen_kvadratB:
            PROZOR.blit(ODABRANI_KVADRAT, odabrani_kvadrat_rectB)
        pass              
   
def promjena_poz_odabranog_kvadrata(igrac, mis_poz):  # Funkcija mijenja poziciju kvadrata koji označuje odabrani kvadratić na gridu
    global postavljen_kvadratA
    global postavljen_kvadratB
    global odabrani_kvadrat_rectA
    global odabrani_kvadrat_rectB
    global lista_brod
    lista_brod = ['p','s','d','c','b']
    if igrac == 'A':
        for i in range(0,100):
            rect = lista_rect_kvadrata_B[i]
            if rect.collidepoint(mis_poz):
                if len(lista_imena_kvadrata_B[i]) == 1:
                    odabrani_kvadrat_rectA = ODABRANI_KVADRAT.get_rect(topleft = (rect.topleft))
                    postavljen_kvadratA = True
                for brod in lista_brod:
                    if len(lista_imena_kvadrata_B[i]) == 2:
                        if lista_imena_kvadrata_B[i][1] == brod:
                            odabrani_kvadrat_rectA = ODABRANI_KVADRAT.get_rect(topleft = (rect.topleft))
                            postavljen_kvadratA = True
    elif igrac == 'B':
        for i in range(0,100):
            rect = lista_rect_kvadrata_A[i]
            if rect.collidepoint(mis_poz):
                if len(lista_imena_kvadrata_A[i]) == 1:
                    odabrani_kvadrat_rectB = ODABRANI_KVADRAT.get_rect(topleft = (rect.topleft))
                    postavljen_kvadratB = True
                for brod in lista_brod:
                    if len(lista_imena_kvadrata_A[i]) == 2:
                        if lista_imena_kvadrata_A[i][1] == brod:
                            odabrani_kvadrat_rectB = ODABRANI_KVADRAT.get_rect(topleft = (rect.topleft))
                            postavljen_kvadratB = True

def gadanje(igrac):  # Funkcija u listi imena kvadrata upisuje x i updejta rezultat
    global rezultat_A_igrac, rezultat_B_igrac, provjera_gadanja
    provjera_gadanja = False
    if igrac == 'A':
        if postavljen_kvadratA:
            for i in range(0,100):
                rect = lista_rect_kvadrata_B[i]
                if rect.collidepoint((odabrani_kvadrat_rectA.topleft)):
                    lista_imena_kvadrata_B[i].append('x')
                    provjera_gadanja = True
                    if lista_imena_kvadrata_B[i][1] != 'x':
                        rezultat_B_igrac -= 1
    if igrac == 'B':
        if postavljen_kvadratB:
            for i in range(0,100):
                rect = lista_rect_kvadrata_A[i]
                if rect.collidepoint((odabrani_kvadrat_rectB.topleft)):
                    lista_imena_kvadrata_A[i].append('x')
                    provjera_gadanja = True
                    if lista_imena_kvadrata_A[i][1] != 'x':
                        rezultat_A_igrac -= 1                         
 
def igranje_A_ekran():
    global zmaj
    run = True
    while run == True:
        PROZOR.fill('White')
        gridA('lijevo')
        gridB('desno')
        PROZOR.blit(player_A_render,player_A_rect)
        BRODOVI_GRUPA_A.draw(PROZOR)
        crtanje_fulanih_podrucja()
        zbrajanje_pogodenih_dijelova_brodova()
        crtanje_xeva('A')
        crtanje_pogodenih_vlastitih('A')
        mouse_pos = pygame.mouse.get_pos()
        hoveranje_animacija('A', mouse_pos)
        GUMB_SHOOT = Button(text_input = "Shoot", text_size = 30, text_color = 'Black', rect_width = 200, rect_height = 40, rect_color = '#475F77', hoveringRect_color = '#D74B4B', pos = (1000,50))
        GUMB_SHOOT.changeColor(mouse_pos)
        GUMB_SHOOT.update(PROZOR)
        crtanje_odabranog_kvadrata('A')

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
                if GUMB_SHOOT.checkForInput(mouse_pos):
                    gadanje('A')
                    if provjera_gadanja == True:
                        run = False
                promjena_poz_odabranog_kvadrata('A', mouse_pos)
                pass
        pygame.display.update()
        clock.tick(FPS)

def igranje_B_ekran():
    global zmaj
    run = True
    while run == True:
        PROZOR.fill('White')
        gridA('desno')
        gridB('lijevo')
        PROZOR.blit(player_B_render,player_B_rect)
        BRODOVI_GRUPA_B.draw(PROZOR)
        crtanje_fulanih_podrucja()
        zbrajanje_pogodenih_dijelova_brodova()
        crtanje_xeva('B')
        crtanje_pogodenih_vlastitih('B')
        mouse_pos = pygame.mouse.get_pos()
        hoveranje_animacija('B', mouse_pos)
        GUMB_SHOOT = Button(text_input = "Shoot", text_size = 30, text_color = 'Black', rect_width = 200, rect_height = 40, rect_color = '#475F77', hoveringRect_color = '#D74B4B', pos = (1000,50))
        GUMB_SHOOT.changeColor(mouse_pos)
        GUMB_SHOOT.update(PROZOR)
        crtanje_odabranog_kvadrata('B')

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
                if GUMB_SHOOT.checkForInput(mouse_pos):
                    gadanje('B')
                    if provjera_gadanja == True:
                        run = False
                promjena_poz_odabranog_kvadrata('B', mouse_pos)
                pass
        pygame.display.update()
        clock.tick(FPS)        
        
def end_screen(rezultat1, rezultat2): #end screen i dugotrajni zapis rezultata igrača i restart gumb i
    global zapis_rezultata_jednom
    global rezultat_desno
    global rezultat_lijevo
    global restart
    PROZOR.fill(WHITE)

    Miš_pozicija= pygame.mouse.get_pos()

    font = pygame.font.Font(None, 100)
    RESTART_BUTTON = Button('Restart', 30, 'Black', 200, 40, '#475F77', '#77dd77', (620,500))
    RESTART_BUTTON.update(PROZOR)
    RESTART_BUTTON.changeColor(Miš_pozicija)
    RESTART_BUTTON.update(PROZOR)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if RESTART_BUTTON.checkForInput(Miš_pozicija):
                restart = True
    pobjednik = ""
    if rezultat1 == 0:
        pobjednik = "Igrač 2 je pobijedio"
        a=1
    if rezultat2 == 0:
        pobjednik = "Igrač 1 je pobijedio"
        a=0
    while zapis_rezultata_jednom==True:
        with open("potapanje brodova\score.txt", encoding="utf-8") as datoteka:
            rezultati = datoteka.readlines()
            print(rezultati)
            rezultati[a] = str(int(rezultati[a]) + 1) + "\n"
            print(rezultati)
            if int(rezultati[0])>int(rezultati[1]):
                boja_lijevo = "#32CD32"
                boja_desno = "#FF0000"  
            elif int(rezultati[1])>int(rezultati[0]):
                boja_lijevo = "#FF0000"
                boja_desno = "#32CD32"  
            elif int(rezultati[1])== int(rezultati[0]):
                boja_desno= "#32CD32"
                boja_lijevo = boja_desno
        with open("potapanje brodova\score.txt", "wt") as datoteka:
            datoteka.writelines(rezultati)
            rezultat_lijevo = font.render(rezultati[0][:-1],True,boja_lijevo)
            rezultat_desno = font.render(rezultati[1][:-1],True,boja_desno)
            
        zapis_rezultata_jednom = False
    
    winner = font.render(pobjednik,True,"#32CD32",)
    dvotocka = font.render(":",True,"#000000")
    PROZOR.blit(winner,(340, 210))
    PROZOR.blit(rezultat_lijevo,(550,310))
    PROZOR.blit(rezultat_desno,(650,310))
    PROZOR.blit(dvotocka,(605,305))
    
    pygame.display.update()
def imenovanje_profila(): #upisivanje imena igrača/profila za pamćenje rezultata
    global PLAYERI_IMENA
    global PLAYERI_SELEKTIRANI
    global PLAYERI_LISTA_GUMBOVA
    imenovanje_profila = True
    
    for i in range(1,9):
        PLAYERI_SELEKTIRANI.update({f"player_{i}":False})
        PLAYERI_IMENA.update({f"player{i}": f"Player {i}"})
    
    while imenovanje_profila == True:
        
        score_mouse_pos = pygame.mouse.get_pos()
        
        PROZOR.fill(WHITE)
        PLAYER_BUTTON1 = Button(PLAYERI_IMENA.get("player1"), 30, 'Black', 200, 40, '#475F77', '#77dd77', (0*400+200, 0*100+100))
        PLAYER_BUTTON2 = Button(PLAYERI_IMENA.get("player2"), 30, 'Black', 200, 40, '#475F77', '#77dd77', (0*400+200, 1*100+100))
        PLAYER_BUTTON3 = Button(PLAYERI_IMENA.get("player3"), 30, 'Black', 200, 40, '#475F77', '#77dd77', (0*400+200, 2*100+100))
        PLAYER_BUTTON4 = Button(PLAYERI_IMENA.get("player4"), 30, 'Black', 200, 40, '#475F77', '#77dd77', (0*400+200, 3*100+100))
        
        
        PLAYER_BUTTON5 = Button(PLAYERI_IMENA.get("player5"), 30, 'Black', 200, 40, '#475F77', '#77dd77', (1*400+200, 0*100+100)) 
        PLAYER_BUTTON6 = Button(PLAYERI_IMENA.get("player6"), 30, 'Black', 200, 40, '#475F77', '#77dd77', (1*400+200, 1*100+100))        
        PLAYER_BUTTON7 = Button(PLAYERI_IMENA.get("player7"), 30, 'Black', 200, 40, '#475F77', '#77dd77', (1*400+200, 2*100+100))
        PLAYER_BUTTON8 = Button(PLAYERI_IMENA.get("player8"), 30, 'Black', 200, 40, '#475F77', '#77dd77', (1*400+200, 3*100+100)) 
        
        

        PLAYERI_LISTA_GUMBOVA = [PLAYER_BUTTON1,PLAYER_BUTTON2,PLAYER_BUTTON3,PLAYER_BUTTON4,PLAYER_BUTTON5,PLAYER_BUTTON6,PLAYER_BUTTON7,PLAYER_BUTTON8]
        
        PROZOR.fill(WHITE)
        for player_gumb in PLAYERI_LISTA_GUMBOVA:
            player_gumb.update(PROZOR)
            player_gumb.changeColor(score_mouse_pos)
            player_gumb.update(PROZOR)                    
        CHOOSE_PROFILE = Button("Procede to profile choosing", 30, 'Black', 350, 40, '#475F77', '#77dd77', (900,600))
        CHOOSE_PROFILE.update(PROZOR)
        CHOOSE_PROFILE.changeColor(score_mouse_pos)
        CHOOSE_PROFILE.update(PROZOR)                   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == MOUSEBUTTONDOWN:
                for i in range(8):
                    if PLAYERI_LISTA_GUMBOVA[i].checkForInput(score_mouse_pos):
                        
                        for k in range (8):
                            PLAYERI_SELEKTIRANI.update({f"player_{k+1}":False})
                        PLAYERI_SELEKTIRANI.update({f"player_{i+1}":True})                    
                        PLAYERI_IMENA.update({f"player{i+1}":""})
                    if CHOOSE_PROFILE.checkForInput(score_mouse_pos):
                        imenovanje_profila = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    imenovanje_profila = False
                for i in range(8):
                    if PLAYERI_SELEKTIRANI.get(f"player_{i+1}") == True:
                        if event.key == pygame.K_BACKSPACE:
                            trenutno_ime_izbris = PLAYERI_IMENA.get(f"player{i+1}")
                            trenutno_ime_izbris = trenutno_ime_izbris[:-1]
                            PLAYERI_IMENA.update({f"player{i+1}": trenutno_ime_izbris})
                        
                        elif event.key == pygame.K_RETURN:
                            PLAYERI_SELEKTIRANI.update({f"player_{i+1}":False})
                        
                        else:
                            trenutno_ime_upis = PLAYERI_IMENA.get(f"player{i+1}")
                            trenutno_ime_upis += event.unicode
                            PLAYERI_IMENA.update({f"player{i+1}": trenutno_ime_upis})

        pygame.display.update()    

def biranje_profila(): #biranje igrača koji će igrati
    global selektirani_profili
    global PLAYERI_IMENA
    global PLAYERI_SELEKTIRANI
    global PLAYERI_LISTA_GUMBOVA
    biranje_profila = True
    PROZOR.fill(WHITE)
    PLAYER_BUTTON1 = Button(PLAYERI_IMENA.get("player1"), 30, 'Black', 200, 40, '#475F77', '#77dd77', (0*400+200, 0*100+100))
    PLAYER_BUTTON2 = Button(PLAYERI_IMENA.get("player2"), 30, 'Black', 200, 40, '#475F77', '#77dd77', (0*400+200, 1*100+100))
    PLAYER_BUTTON3 = Button(PLAYERI_IMENA.get("player3"), 30, 'Black', 200, 40, '#475F77', '#77dd77', (0*400+200, 2*100+100))
    PLAYER_BUTTON4 = Button(PLAYERI_IMENA.get("player4"), 30, 'Black', 200, 40, '#475F77', '#77dd77', (0*400+200, 3*100+100))
        
        
    PLAYER_BUTTON5 = Button(PLAYERI_IMENA.get("player5"), 30, 'Black', 200, 40, '#475F77', '#77dd77', (1*400+200, 0*100+100)) 
    PLAYER_BUTTON6 = Button(PLAYERI_IMENA.get("player6"), 30, 'Black', 200, 40, '#475F77', '#77dd77', (1*400+200, 1*100+100))        
    PLAYER_BUTTON7 = Button(PLAYERI_IMENA.get("player7"), 30, 'Black', 200, 40, '#475F77', '#77dd77', (1*400+200, 2*100+100))
    PLAYER_BUTTON8 = Button(PLAYERI_IMENA.get("player8"), 30, 'Black', 200, 40, '#475F77', '#77dd77', (1*400+200, 3*100+100)) 
        

    
    GUMBOVI_POZICIJE = [(0*400+200, 0*100+100),(0*400+200, 1*100+100),(0*400+200, 2*100+100),(0*400+200, 3*100+100),(1*400+200, 0*100+100),(1*400+200, 1*100+100),(1*400+200, 2*100+100),(1*400+200, 3*100+100)]
    PLAYERI_LISTA_GUMBOVA=[PLAYER_BUTTON1,PLAYER_BUTTON2,PLAYER_BUTTON3,PLAYER_BUTTON4,PLAYER_BUTTON5,PLAYER_BUTTON6,PLAYER_BUTTON7,PLAYER_BUTTON8]
    GUMBOVI_METAMORFOZA = {PLAYER_BUTTON1:0, PLAYER_BUTTON2:0, PLAYER_BUTTON3:0, PLAYER_BUTTON4:0 ,PLAYER_BUTTON5:0 ,PLAYER_BUTTON6:0 ,PLAYER_BUTTON7:0 ,PLAYER_BUTTON8:0}
    
    while biranje_profila == True:
        biranje_mouse_poz = pygame.mouse.get_pos()
        
        
        for player_gumb in PLAYERI_LISTA_GUMBOVA:
            if GUMBOVI_METAMORFOZA.get(player_gumb) == 0:
                player_gumb = Button(PLAYERI_IMENA.get(f"player{PLAYERI_LISTA_GUMBOVA.index(player_gumb)+1}"), 30, 'Black', 200, 40, '#475F77', '#77dd77',GUMBOVI_POZICIJE[PLAYERI_LISTA_GUMBOVA.index(player_gumb)])
                player_gumb.update(PROZOR)
                player_gumb.changeColor(biranje_mouse_poz)
                player_gumb.update(PROZOR)
        CONFIRM_SELECTED =  Button(("Confirm selected profiles"), 30, 'Black', 300, 40, '#475F77', '#77dd77', ((900,600)))        
        CONFIRM_SELECTED.update(PROZOR)
        CONFIRM_SELECTED.changeColor(biranje_mouse_poz)
        CONFIRM_SELECTED.update(PROZOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()   
            if event.type == MOUSEBUTTONDOWN:
                if CONFIRM_SELECTED.checkForInput(biranje_mouse_poz):
                    if len(selektirani_profili) == 2:
                        biranje_profila = False
                if len(selektirani_profili) <= 2:
                    for i in range(8):
                        if PLAYERI_LISTA_GUMBOVA[i].checkForInput(biranje_mouse_poz):
                            if len(selektirani_profili)<2:
                                PLAYERI_LISTA_GUMBOVA[i] = Button(PLAYERI_IMENA.get(f"player{i+1}"), 30, 'Black', 200, 40, '#D74B4B', '#77dd77',GUMBOVI_POZICIJE[i])
                                PLAYERI_LISTA_GUMBOVA[i].update(PROZOR)
                                GUMBOVI_METAMORFOZA.update({PLAYERI_LISTA_GUMBOVA[i]:1})
                            if PLAYERI_IMENA.get(f"player{i+1}") in selektirani_profili:
                                selektirani_profili.remove(PLAYERI_IMENA.get(f"player{i+1}")) 
                                PLAYERI_LISTA_GUMBOVA[i] = Button(PLAYERI_IMENA.get(f"player{i+1}"), 30, 'Black', 200, 40, '#475F77', '#77dd77',GUMBOVI_POZICIJE[i])
                                PLAYERI_LISTA_GUMBOVA[i].update(PROZOR)
                                GUMBOVI_METAMORFOZA.update({PLAYERI_LISTA_GUMBOVA[i]:0})
                            elif PLAYERI_IMENA.get(f"player{i+1}") not in selektirani_profili:
                                selektirani_profili.append(PLAYERI_IMENA.get(f"player{i+1}"))
                            if len(selektirani_profili) == 3:
                                selektirani_profili.remove(selektirani_profili[2])
                    
                print(selektirani_profili)
                            
        pygame.display.update()
    
def resetiranje_prije_igre(): # Resetira listu rectangleova prije svakog igranja
    global lista_rect_kvadrata_A, lista_rect_kvadrata_B, izrada_liste_A, izrada_liste_B, postavljen_kvadratA, postavljen_kvadratB
    postavljen_kvadratA = False
    postavljen_kvadratB = False
    lista_rect_kvadrata_A = []
    lista_rect_kvadrata_B = []
    izrada_liste_A = True
    izrada_liste_B = True

def pauza_prije_promjene_igraca():  # Napravi pauzu od 3 sek između igrača
    TAJMER3 = pygame.image.load(os.path.join("potapanje brodova", "tajmer_3sec.png"))
    TAJMER2 = pygame.image.load(os.path.join("potapanje brodova", "tajmer_2sec.png"))
    TAJMER1 = pygame.image.load(os.path.join("potapanje brodova", "tajmer_1sec.png"))
    font = pygame.font.Font(None, 30)
    tekst_surf = font.render('Next player in:', False, 'White')
    tekst_rect = tekst_surf.get_rect(midtop = (640,160))
    tajmer_rect = TAJMER3.get_rect(midtop = (640, 210))
    PROZOR.fill("Black")
    PROZOR.blit(tekst_surf, tekst_rect)
    PROZOR.blit(TAJMER3, tajmer_rect)
    pygame.display.update()
    time.sleep(1)
    tajmer_rect = TAJMER2.get_rect(midtop = (640, 210))
    PROZOR.fill("Black")
    PROZOR.blit(tekst_surf, tekst_rect)
    PROZOR.blit(TAJMER2, tajmer_rect)
    pygame.display.update()
    time.sleep(1)
    tajmer_rect = TAJMER1.get_rect(midtop = (640, 210))
    PROZOR.fill("Black")
    PROZOR.blit(tekst_surf, tekst_rect)
    PROZOR.blit(TAJMER1, tajmer_rect)
    pygame.display.update()
    time.sleep(1)        
    
def play():
    global lista_imena_kvadrata_A
    global lista_imena_kvadrata_B
    global restart
    global zmaj
    global postavljen_kvadratA
    global postavljen_kvadratB
    global rezultat_A_igrac
    global rezultat_B_igrac
    play_run = True
    resetiranje_prije_igre()
    imenovanje_profila()
    biranje_profila()
    while play_run == True:
        postavljanje_igracaA()
        if zmaj == True:
            play_run == False
            break
        pauza_prije_promjene_igraca()
        resetiranje_prije_igre()
        postavljanje_igracaB()
        if zmaj == True:
            play_run == False
            break
        rezultat_A_igrac = 17
        rezultat_B_igrac = 17
        run = True
        while run == True:
            pauza_prije_promjene_igraca()
            resetiranje_prije_igre()
            igranje_A_ekran()
            if zmaj == True:
                play_run == False
                run = False
                break
            if rezultat_A_igrac == 0 or rezultat_B_igrac == 0:
                run = False
            pauza_prije_promjene_igraca()
            resetiranje_prije_igre()
            igranje_B_ekran()
            if zmaj == True:
                play_run == False
                run = False
                break
            if rezultat_A_igrac == 0 or rezultat_B_igrac == 0:
                run = False
        if zmaj == True:
            play_run = False
            break
        restart = False
        while restart == False:
            end_screen(rezultat_A_igrac,rezultat_B_igrac)
        lista_imena_kvadrata_A= []   
        lista_imena_kvadrata_B = [] 
        resetiranje_prije_igre()

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
                    #score()
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
