from ast import main
from turtle import left
import pygame, sys
from pygame.locals import *
import os
import time
pygame.init()#instalira sve pygame module
pygame.mixer.init()#učitava i omogućuje reprodukciju zvukova

#Definiranje displaya
ŠIRINA, VISINA = 1280, 720
PROZOR = pygame.display.set_mode((ŠIRINA, VISINA))#stvara suraface
pygame.display.set_caption("Potapanje brodova")

#clock i boje
WHITE = (255,255,255)
FPS = 60
clock = pygame.time.Clock()#prati/pamti vrijeme


#Slike, zvuk, font
#Loading screen
LOGO = pygame.image.load(os.path.join("potapanje brodova", "MLKJR_LOGO.png" )).convert_alpha()
INTRO = pygame.mixer.Sound(os.path.join("potapanje brodova", "INTRO.ogg"))

#Grid/mreža
KVADRAT = pygame.image.load(os.path.join("potapanje brodova", "kvadrat.png")).convert_alpha()
OKOLNI_GRID = pygame.image.load(os.path.join("potapanje brodova", "okolni_grid.png")).convert_alpha()
FONT_BROJ_SLOVO = pygame.font.Font(None, 30)

#Play_score
LINIJA_SCORE_PISANJE = pygame.image.load(os.path.join("potapanje brodova", "linija_za_pisanje.png")).convert_alpha()
LINIJA_SCORE_PRAZNINA = pygame.image.load(os.path.join("potapanje brodova", "linija_za_pisanje_praznina.png")).convert_alpha()
linija_key_index = 0
linija_playscore_animacija_lista = [LINIJA_SCORE_PISANJE,LINIJA_SCORE_PRAZNINA]
linija_playscore_surf = linija_playscore_animacija_lista[linija_key_index]


#Igranje/gađaje brodova
XISIC = pygame.image.load(os.path.join("potapanje brodova", "xisic.png")).convert_alpha()
FULANO = pygame.image.load(os.path.join("igranje", "fulano.png")).convert_alpha()
ODABRANI_KVADRAT = pygame.image.load(os.path.join("potapanje brodova", "odabrani_kvadrat.png")).convert_alpha()
VATRA1 = pygame.image.load(os.path.join("igranje", "vatra1.png")).convert_alpha()
VATRA2 = pygame.image.load(os.path.join("igranje", "vatra2.png")).convert_alpha()
VATRA3 = pygame.image.load(os.path.join("igranje", "vatra3.png")).convert_alpha()
VATRA4 = pygame.image.load(os.path.join("igranje", "vatra4.png")).convert_alpha()
vatra_lista = [VATRA1, VATRA2, VATRA3, VATRA4]
vatra_index = 0
vatra_surf = vatra_lista[vatra_index]

vlastito_pogodeno_lista = []
vlas_pog_index = 0
pogodeno_lista = []
pog_index = 0
bomba_fulano_lista = []
bomb_ful_index = 0
fulano_lista = []
fulano_index = 0
for i in range(1,10):
    slika = pygame.image.load(os.path.join("igranje", f"bomba_padanje{i}.png")).convert_alpha()
    pogodeno_lista.append(slika)
    bomba_fulano_lista.append(slika)
for i in range(1,10):
    rupa = pygame.image.load(os.path.join("igranje", f"rupa{i}.png")).convert_alpha()
    bomba_fulano_lista.append(rupa)
for i in range(1,7):
    pogodenosapozadinom = pygame.image.load(os.path.join("igranje", f"bomba_pogodeno{i}.png")).convert_alpha()
    pogodenobezpoz = pygame.image.load(os.path.join("igranje", f"pogodeno_vlastito{i}.png")).convert_alpha()
    pogodeno_lista.append(pogodenosapozadinom)
    vlastito_pogodeno_lista.append(pogodenobezpoz)
for i in range(1,9):
    fulan = pygame.image.load(os.path.join("igranje", f"fulano_animacija{i}.png")).convert_alpha()
    fulano_lista.append(fulan)


#Sound effecti
POSTAVLJANJE_BRODA_ZVUK = pygame.mixer.Sound(os.path.join("potapanje brodova", "postavljanje_broda_zvuk.ogg"))
VRATI_NAZAD_ZVUK = pygame.mixer.Sound(os.path.join("potapanje brodova", "vrati_nazad_zvuk.ogg"))
EXIT_GUMB_ZVUK = pygame.mixer.Sound(os.path.join("potapanje brodova", "exit_gumb_zvuk.ogg"))
TUPI_GUMB_ZVUK = pygame.mixer.Sound(os.path.join("potapanje brodova", "tupi_gumb_zvuk.ogg"))
KLIK_GUMB_ZVUK = pygame.mixer.Sound(os.path.join("potapanje brodova", "klik_gumb_zvuk.ogg"))

#Hoveri brodova
HOVER_CARRIER = pygame.image.load(os.path.join("potapanje brodova", "hover_carrier.png" )).convert_alpha()
HOVER_BATTLESHIP = pygame.image.load(os.path.join("potapanje brodova", "hover_battleship.png" )).convert_alpha()
HOVER_DESTROYER = pygame.image.load(os.path.join("potapanje brodova", "hover_destroyer.png" )).convert_alpha()
HOVER_SUBMARINE = pygame.image.load(os.path.join("potapanje brodova", "hover_submarine.png" )).convert_alpha()
HOVER_PATROL = pygame.image.load(os.path.join("potapanje brodova", "hover_patrol.png" )).convert_alpha()

ZELENI_KVADRAT_2 = pygame.image.load(os.path.join("potapanje brodova", "zeleni_kvad2.png" )).convert_alpha()
ZELENI_KVADRAT_3 = pygame.image.load(os.path.join("potapanje brodova", "zeleni_kvad3.png" )).convert_alpha()
ZELENI_KVADRAT_4 = pygame.image.load(os.path.join("potapanje brodova", "zeleni_kvad4.png" )).convert_alpha()
ZELENI_KVADRAT_5 = pygame.image.load(os.path.join("potapanje brodova", "zeleni_kvad5.png" )).convert_alpha()

CRVENI_KVADRAT_2 = pygame.image.load(os.path.join("potapanje brodova", "crveni_kvad2.png" )).convert_alpha()
CRVENI_KVADRAT_3 = pygame.image.load(os.path.join("potapanje brodova", "crveni_kvad3.png" )).convert_alpha()
CRVENI_KVADRAT_4 = pygame.image.load(os.path.join("potapanje brodova", "crveni_kvad4.png" )).convert_alpha()
CRVENI_KVADRAT_5 = pygame.image.load(os.path.join("potapanje brodova", "crveni_kvad5.png" )).convert_alpha()

#Background postavljanje
BG_POSTAVLJANJE = pygame.image.load(os.path.join("postavljanje", "background_postavljanje.png" )).convert_alpha()
BG_POSTAVALJANJE_RECT = BG_POSTAVLJANJE.get_rect(topleft=(0,0))
GRID_VODA = pygame.image.load(os.path.join("postavljanje", "plavi_ekran.png" )).convert_alpha()
GRID_VODA_RECT = GRID_VODA.get_rect(topleft = (0,0))#rect vode, ovo omogućuje da se slika zapravo miče

SUM_POSTAVLJANJE = pygame.image.load(os.path.join("postavljanje", "samsung_ekran.png" )).convert_alpha()


SUM_POSTAVLJANJE_RECT = SUM_POSTAVLJANJE.get_rect(topleft=(672,128)) 


OBRUB_CARRIER = pygame.image.load(os.path.join("postavljanje", "obrub_carrier.png" )).convert_alpha() 
OBRUB_BATTLESHIP = pygame.image.load(os.path.join("postavljanje", "obrub_battleship.png" )).convert_alpha() 
OBRUB_DESTROYER = pygame.image.load(os.path.join("postavljanje", "obrub_destroyer.png" )).convert_alpha() 
OBRUB_SUBMARINE = pygame.image.load(os.path.join("postavljanje", "obrub_submarine.png" )).convert_alpha() 
OBRUB_PATROL = pygame.image.load(os.path.join("postavljanje", "obrub_patrol.png" )).convert_alpha()
 
OBRUB_CARRIER_RECT = OBRUB_CARRIER.get_rect(topleft=(672,128))
OBRUB_BATTLESHIP_RECT = OBRUB_BATTLESHIP.get_rect(topleft=(672,128))
OBRUB_DESTROYER_RECT = OBRUB_DESTROYER.get_rect(topleft=(672,128))
OBRUB_SUBMARINE_RECT = OBRUB_SUBMARINE.get_rect(topleft=(672,128))
OBRUB_PATROL_RECT = OBRUB_PATROL.get_rect(topleft=(672,128))
OBRUBI_BRODOVI_RECT = [OBRUB_CARRIER_RECT,OBRUB_BATTLESHIP_RECT,OBRUB_DESTROYER_RECT,OBRUB_SUBMARINE_RECT,OBRUB_PATROL_RECT]

OBRUBI_BRODOVI_CRTANJE = [[OBRUB_CARRIER,OBRUB_CARRIER_RECT],[OBRUB_BATTLESHIP,OBRUB_BATTLESHIP_RECT],[OBRUB_DESTROYER,OBRUB_DESTROYER_RECT],
[OBRUB_SUBMARINE,OBRUB_SUBMARINE_RECT],[OBRUB_PATROL,OBRUB_PATROL_RECT]]

rotate1 = pygame.image.load(os.path.join("postavljanje", "rotate_frame1.png" )).convert_alpha()
rotate2 = pygame.image.load(os.path.join("postavljanje", "rotate_frame2.png" )).convert_alpha()
rotate3 = pygame.image.load(os.path.join("postavljanje", "rotate_frame3.png" )).convert_alpha()
rotate_key_index = 0
rotate_lista = [rotate1,rotate2,rotate3]

#Background igranje
BG_IGRANJE = pygame.image.load(os.path.join("igranje", "background_igranje.png" )).convert_alpha()
BG_IGRANJE_RECT = BG_IGRANJE.get_rect(topleft=(0,0))
VODA_IGRANJE = pygame.image.load(os.path.join("igranje", "plavi_ekrani.png" )).convert_alpha()
VODA_IGRANJE_RECT = VODA_IGRANJE.get_rect(topleft=(0,0))

play_run = True

#Main menu grafika
lista_bomba_animacija = []
bomba_index = 0
for i in range(1,27):
    bomba = pygame.image.load(os.path.join("main_menu\omba_animacija", f'bomba_frame{i}.png' )).convert_alpha()
    lista_bomba_animacija.append(bomba)
lista_brod_animacija = []
brod_index = 0
for i in range(1,28):
    brod = pygame.image.load(os.path.join("main_menu\od_animacija", f'brod_frame{i}.png' )).convert_alpha()
    lista_brod_animacija.append(brod)
lista_more_animacija = []
more_index = 0
for i in range(1,5):
    more = pygame.image.load(os.path.join("main_menu\more_animacija", f'more{i}.png' )).convert_alpha()
    lista_more_animacija.append(more)

#Sve za Brod spriteove i provjere postavljanja
Kvadrat_x, Kvadrat_y = 0, 0
brod = None
brod_velkiX = None

lista_rect_kvadrata_A = []
lista_imena_kvadrata_A = []
lista_imena_kvadrata_B = []
lista_rect_kvadrata_B = []

#Služi da se određeni programi izvrše samo jednom
PROVJERA = True
izrada_liste_A = True
izrada_liste_B = True
zapis_rezultata_jednom = True

#Sve za profile i biranje
PLAYERI_SELEKTIRANI = {}
PLAYERI_IMENA = {}
PLAYERI_LISTA_GUMBOVA = []

selektirani_profili = []
with open("potapanje brodova\profili.txt",encoding="utf-8") as datoteka:
        profili = datoteka.readlines()
with open("potapanje brodova\score.txt",encoding="utf-8") as datoteka:
    score = datoteka.readlines()


imenovanje_profila_bool = True
biranje_profila_bool = True

def LOADING_SCREEN():
    PROZOR.fill('White')
    PROZOR.blit(LOGO,(150,0))
    pygame.mixer.Sound.play(INTRO).set_volume(0.75)
    pygame.display.update()
    time.sleep(3.3)                
    PROZOR.fill('White')
LOADING_SCREEN()

class Button:
    def __init__(self, text_input, text_size, text_color, rect_width, rect_height, rect_color, hoveringRect_color, pos):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.poz = (pos[0],pos[1])
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
            pygame.mixer.Sound.play(KLIK_GUMB_ZVUK)
            zapis(igrac)
            run_pA = False
            run_pB = False

class CrtanjeBrod():
    def __init__(self, picture_path):
        self.image = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(672,128))
        self.mask = pygame.mask.from_surface(self.image)

    def mask_collide(self,play_mouse_pos):
        poz_u_rectu = play_mouse_pos[0] - self.rect.x, play_mouse_pos[1] - self.rect.y 
        lista_valuea = list(SUM_POSTAVLJANJE_BRODOVI_CRTAJ.values())
        lista_valuea_obrubi = []
        for član in lista_valuea:
            lista_valuea_obrubi.append(član[1])
            
        try:  
            if True not in lista_valuea_obrubi: # Ako ništa nije selektirano
                provjera_klika_sum_broda(poz_u_rectu) 
            else: # Ako je druga varijabla False
                SUM_POSTAVLJANJE_BRODOVI_CRTAJ.update({SUM_POSTAVLJANJE_BRODOVI_LISTA[lista_valuea_obrubi.index(True)]:[lista_valuea[lista_valuea_obrubi.index(True)[0]],False]})
                
                provjera_klika_sum_broda(poz_u_rectu) 
        except:
            pass
    
    def update(self):
        self.mask = pygame.mask.from_surface(self.image)
                
                
                
def provjera_klika_sum_broda(poz_u_rectu):
    global brod_collidean
    global duljina_broda
    global brod_izabran
    if SUM_POSTAVLJANJE_BRODOVI_LISTA[0].mask.get_at(poz_u_rectu) and not (SUM_POSTAVLJANJE_BRODOVI_LISTA[1].mask.get_at(poz_u_rectu) or SUM_POSTAVLJANJE_BRODOVI_LISTA[2].mask.get_at(poz_u_rectu) or SUM_POSTAVLJANJE_BRODOVI_LISTA[3].mask.get_at(poz_u_rectu) or SUM_POSTAVLJANJE_BRODOVI_LISTA[4].mask.get_at(poz_u_rectu)):
        SUM_POSTAVLJANJE_BRODOVI_CRTAJ.update({SUM_POSTAVLJANJE_BRODOVI_LISTA[0]:[True,True]})
        duljina_broda = 5
        brod_izabran = True
        brod_collidean = SUM_BRODOVI_VEZA_SPRITE_BRODOVI.get(SUM_POSTAVLJANJE_BRODOVI_LISTA[0]) 
                        
                        
    elif SUM_POSTAVLJANJE_BRODOVI_LISTA[1].mask.get_at(poz_u_rectu) and not (SUM_POSTAVLJANJE_BRODOVI_LISTA[2].mask.get_at(poz_u_rectu) or SUM_POSTAVLJANJE_BRODOVI_LISTA[3].mask.get_at(poz_u_rectu) or SUM_POSTAVLJANJE_BRODOVI_LISTA[4].mask.get_at(poz_u_rectu)):
        SUM_POSTAVLJANJE_BRODOVI_CRTAJ.update({SUM_POSTAVLJANJE_BRODOVI_LISTA[1]:[True,True]})
        duljina_broda = 4
        brod_izabran = True
        brod_collidean = SUM_BRODOVI_VEZA_SPRITE_BRODOVI.get(SUM_POSTAVLJANJE_BRODOVI_LISTA[1]) 
                
                        
    elif SUM_POSTAVLJANJE_BRODOVI_LISTA[2].mask.get_at(poz_u_rectu) and not (SUM_POSTAVLJANJE_BRODOVI_LISTA[3].mask.get_at(poz_u_rectu) or SUM_POSTAVLJANJE_BRODOVI_LISTA[4].mask.get_at(poz_u_rectu)): 
        SUM_POSTAVLJANJE_BRODOVI_CRTAJ.update({SUM_POSTAVLJANJE_BRODOVI_LISTA[2]:[True,True]})
        duljina_broda = 3
        brod_izabran = True
        brod_collidean = SUM_BRODOVI_VEZA_SPRITE_BRODOVI.get(SUM_POSTAVLJANJE_BRODOVI_LISTA[2]) 
                        
                            
    elif SUM_POSTAVLJANJE_BRODOVI_LISTA[3].mask.get_at(poz_u_rectu) and not SUM_POSTAVLJANJE_BRODOVI_LISTA[4].mask.get_at(poz_u_rectu): 
        SUM_POSTAVLJANJE_BRODOVI_CRTAJ.update({SUM_POSTAVLJANJE_BRODOVI_LISTA[3]:[True,True]})
        duljina_broda = 3
        brod_izabran = True
        brod_collidean = SUM_BRODOVI_VEZA_SPRITE_BRODOVI.get(SUM_POSTAVLJANJE_BRODOVI_LISTA[3]) 
                        
                            
    elif SUM_POSTAVLJANJE_BRODOVI_LISTA[4].mask.get_at(poz_u_rectu): 
        SUM_POSTAVLJANJE_BRODOVI_CRTAJ.update({SUM_POSTAVLJANJE_BRODOVI_LISTA[4]:[True,True]})
        duljina_broda = 2
        brod_izabran = True
        brod_collidean = SUM_BRODOVI_VEZA_SPRITE_BRODOVI.get(SUM_POSTAVLJANJE_BRODOVI_LISTA[4])

                    
 #rotiranje brodova          
             
class Brod(pygame.sprite.Sprite):
    def __init__(self,picture_path,poz_x,poz_y):
        super().__init__()
        #rectangle
        self.pozx = poz_x
        self.pozy = poz_y
        self.image = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft =(poz_x, poz_y)
       
    
    def rotacija_poz_90(self,brod_velkiX,poz_broda_x,poz_broda_y,Hover_brod,Zeleni_brod,Crveni_brod):    
        brod_velkiX.image = pygame.transform.rotate(brod_velkiX.image, 90)
        brod_velkiX.rect = brod_velkiX.image.get_rect()
        brod_velkiX.rect.topleft =(poz_broda_x+640, poz_broda_y)
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.topleft =(poz_broda_x, poz_broda_y)
        Hover_brod = pygame.transform.rotate(Hover_brod, 90)
        Zeleni_brod = pygame.transform.rotate(Zeleni_brod, 90)
        Crveni_brod = pygame.transform.rotate(Crveni_brod, 90)
        HOVER_BRODOVA.update({self:Hover_brod})
        ZELENI_KVADRATI.update({self:Zeleni_brod})
        CRVENI_KVADRATI.update({self:Crveni_brod})
        

    def rotacija_neg_90(self,brod_velkiX,poz_broda_x,poz_broda_y,Hover_brod,Zeleni_brod,Crveni_brod):
        brod_velkiX.image = pygame.transform.rotate(brod_velkiX.image, -90)
        brod_velkiX.rect = brod_velkiX.image.get_rect()
        brod_velkiX.rect.topleft =(poz_broda_x+640, poz_broda_y)
        self.image = pygame.transform.rotate(self.image, -90)
        self.rect = self.image.get_rect()
        self.rect.topleft =(poz_broda_x, poz_broda_y)
        Hover_brod = pygame.transform.rotate(Hover_brod, -90)
        Zeleni_brod = pygame.transform.rotate(Zeleni_brod, -90)
        Crveni_brod = pygame.transform.rotate(Crveni_brod, -90)
        HOVER_BRODOVA.update({self:Hover_brod})
        ZELENI_KVADRATI.update({self:Zeleni_brod})
        CRVENI_KVADRATI.update({self:Crveni_brod})


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
    
    def vrati_nazad(self,brod_velkiX,brodovi_rotacija,brodovi_pozicije,Hover_brod,Zeleni_brod,Crveni_brod):#Vraća brodove na prvobitne pozicije brodova 
        global vrati_nazad_provjera
        global trenutni_sum_brod
        vrati_nazad_provjera = True
        poz_x = self.pozx
        poz_y = self.pozy
        if brodovi_rotacija.get(self) == 1:
            self.image = pygame.transform.rotate(self.image, -90)
            self.rect = self.image.get_rect()
            self.rect.topleft =(self.pozx, self.pozy)
            brod_velkiX.image = pygame.transform.rotate(brod_velkiX.image, -90)
            brod_velkiX.rect = brod_velkiX.image.get_rect()
            brod_velkiX.rect.topleft =(self.pozx+640, self.pozy)
            brodovi_rotacija.update({self:0})
            Hover_brod = pygame.transform.rotate(Hover_brod, -90)
            Zeleni_brod = pygame.transform.rotate(Zeleni_brod, -90)
            Crveni_brod = pygame.transform.rotate(Crveni_brod, -90)
            HOVER_BRODOVA.update({self:Hover_brod})
            ZELENI_KVADRATI.update({self:Zeleni_brod})
            CRVENI_KVADRATI.update({self:Crveni_brod})  
        brod_velkiX.rect.topleft = poz_x + 640, poz_y
        self.rect.topleft = poz_x, poz_y
        brodovi_pozicije.update({self:(poz_x, poz_y)})
        trenutni_sum_brod = list(SUM_BRODOVI_VEZA_SPRITE_BRODOVI.keys())[list(SUM_BRODOVI_VEZA_SPRITE_BRODOVI.values()).index(self)]
        SUM_POSTAVLJANJE_BRODOVI_CRTAJ.update({trenutni_sum_brod:[True,False]})
        trenutni_sum_brod.update()
         

class Veliki_Xevi(pygame.sprite.Sprite):
     def __init__(self,picture_path,poz_x,poz_y):
        super().__init__()
        self.pozx = poz_x
        self.pozy = poz_y
        self.image = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft =(poz_x, poz_y)
        
#exit screen

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

        CANCEL_GUMB = Button('Ne', 30, 'Black', 70, 40, '#475F77', '#D74B4B', (490, 410))
        CONFIRM_GUMB = Button('Da', 30, 'Black', 70, 40, '#475F77', '#77dd77', (790, 410))

        for gumb in [CANCEL_GUMB, CONFIRM_GUMB]:
            gumb.changeColor(ESC_MOUSE_POS)
            gumb.update(screen)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if CONFIRM_GUMB.checkForInput(ESC_MOUSE_POS):
                    pygame.mixer.Sound.play(KLIK_GUMB_ZVUK)
                    zmaj = True
                    run = False
                if CANCEL_GUMB.checkForInput(ESC_MOUSE_POS):
                    pygame.mixer.Sound.play(KLIK_GUMB_ZVUK)
                    run = False
        pygame.display.update()
        clock.tick(FPS)
#mreža prvog igrača        
def gridA(pozicija):
    global izrada_liste_A
    global lista_rect_kvadrata_A
    y = 80
    if pozicija == 'lijevo':
        #crtanje grida
        for i in range(10):
            y += 48
            x = 48
            for j in range (10):
                x += 48
                KVADRAT_RECT = KVADRAT.get_rect(topleft = (x,y))
                if izrada_liste_A == True:
                    lista_rect_kvadrata_A.append(KVADRAT_RECT)
                PROZOR.blit(KVADRAT,KVADRAT_RECT)
        OKOLNI_GRID_RECT = OKOLNI_GRID.get_rect(topleft = (96,128))
        PROZOR.blit(OKOLNI_GRID, OKOLNI_GRID_RECT)
        izrada_liste_A = False

        #brojevi
        broj_x = 80
        broj_y = 143
        for i in range(1,11):
            broj = FONT_BROJ_SLOVO.render(str(i),1,'Black')
            if i == 10:
                broj_x -= 10
            broj_rect = broj.get_rect(topleft = (broj_x, broj_y))
            PROZOR.blit(broj, broj_rect)
            broj_y += 48

        #slova
        slovo_x = 113
        slovo_y = 108
        for i in range(0,10):
            slovo = FONT_BROJ_SLOVO.render(str(chr(ord("A")+i)),1,'Black')
            slovo_rect = slovo.get_rect(topleft = (slovo_x, slovo_y))
            PROZOR.blit(slovo, slovo_rect)
            slovo_x += 48

    elif pozicija == 'desno':
        #crtanje grida
        for i in range(10):
            y += 48
            x = 688
            for j in range (10):
                x += 48
                KVADRAT_RECT = KVADRAT.get_rect(topleft = (x,y))
                if izrada_liste_A == True:
                    lista_rect_kvadrata_A.append(KVADRAT_RECT)
                PROZOR.blit(KVADRAT,KVADRAT_RECT)
        OKOLNI_GRID_RECT = OKOLNI_GRID.get_rect(topleft = (736,128))
        PROZOR.blit(OKOLNI_GRID, OKOLNI_GRID_RECT)
        izrada_liste_A = False

        #brojevi
        broj_x = 720
        broj_y = 143
        for i in range(1,11):
            broj = FONT_BROJ_SLOVO.render(str(i),1,'Black')
            if i == 10:
                broj_x -= 10
            broj_rect = broj.get_rect(topleft = (broj_x, broj_y))
            PROZOR.blit(broj, broj_rect)
            broj_y += 48

        #slova
        slovo_x = 753
        slovo_y = 108
        for i in range(0,10):
            slovo = FONT_BROJ_SLOVO.render(str(chr(ord("A")+i)),1,'Black')
            slovo_rect = slovo.get_rect(topleft = (slovo_x, slovo_y))
            PROZOR.blit(slovo, slovo_rect)
            slovo_x += 48
#mreža drugog igrača
def gridB(pozicija):
    global izrada_liste_B
    global lista_rect_kvadrata_B
    y = 80
    if pozicija == 'lijevo':
        #crtanje grida
        for i in range(10):
            y += 48
            x = 48
            for j in range (10):
                x += 48
                KVADRAT_RECT = KVADRAT.get_rect(topleft = (x,y))
                if izrada_liste_B == True:
                    lista_rect_kvadrata_B.append(KVADRAT_RECT)
                PROZOR.blit(KVADRAT,KVADRAT_RECT)
        OKOLNI_GRID_RECT = OKOLNI_GRID.get_rect(topleft = (96,128))
        PROZOR.blit(OKOLNI_GRID, OKOLNI_GRID_RECT)
        izrada_liste_B = False

        #brojevi
        broj_x = 80
        broj_y = 143
        for i in range(1,11):
            broj = FONT_BROJ_SLOVO.render(str(i),1,'Black')
            if i == 10:
                broj_x -= 10
            broj_rect = broj.get_rect(topleft = (broj_x, broj_y))
            PROZOR.blit(broj, broj_rect)
            broj_y += 48

        #slova
        slovo_x = 113
        slovo_y = 108
        for i in range(0,10):
            slovo = FONT_BROJ_SLOVO.render(str(chr(ord("A")+i)),1,'Black')
            slovo_rect = slovo.get_rect(topleft = (slovo_x, slovo_y))
            PROZOR.blit(slovo, slovo_rect)
            slovo_x += 48

    else:
        #crtanje grida
        for i in range(10):
            y += 48
            x = 688
            for j in range (10):
                x += 48
                KVADRAT_RECT = KVADRAT.get_rect(topleft = (x,y))
                if izrada_liste_B == True:
                    lista_rect_kvadrata_B.append(KVADRAT_RECT)
                PROZOR.blit(KVADRAT,KVADRAT_RECT)
        OKOLNI_GRID_RECT = OKOLNI_GRID.get_rect(topleft = (736,128))
        PROZOR.blit(OKOLNI_GRID, OKOLNI_GRID_RECT)
        izrada_liste_B = False

        #brojevi
        broj_x = 720
        broj_y = 143
        for i in range(1,11):
            broj = FONT_BROJ_SLOVO.render(str(i),1,'Black')
            if i == 10:
                broj_x -= 10
            broj_rect = broj.get_rect(topleft = (broj_x, broj_y))
            PROZOR.blit(broj, broj_rect)
            broj_y += 48

        #slova
        slovo_x = 753
        slovo_y = 108
        for i in range(0,10):
            slovo = FONT_BROJ_SLOVO.render(str(chr(ord("A")+i)),1,'Black')
            slovo_rect = slovo.get_rect(topleft = (slovo_x, slovo_y))
            PROZOR.blit(slovo, slovo_rect)
            slovo_x += 48     
#obrub
def crtanje_obruba_hover(play_mouse_pos):
    for i in range(5):
        poz_u_rectu = play_mouse_pos[0] - SUM_POSTAVLJANJE_BRODOVI_LISTA[i].rect.x, play_mouse_pos[1] - SUM_POSTAVLJANJE_BRODOVI_LISTA[i].rect.y #Postavlja 0,0 koordinate za poziciju miša u rect.topleft, a povećava se kretanjem unutar tog recta
        if SUM_POSTAVLJANJE_BRODOVI_LISTA[i].rect.collidepoint(play_mouse_pos) and SUM_POSTAVLJANJE_BRODOVI_LISTA[i].mask.get_at(poz_u_rectu): #Gleda da smo u rectu, a onda i u maski (ne moze gledati samo drugo jer dolazi do problema ako izademo iz recta)

            if SUM_POSTAVLJANJE_BRODOVI_LISTA[0].mask.get_at(poz_u_rectu) and not (SUM_POSTAVLJANJE_BRODOVI_LISTA[1].mask.get_at(poz_u_rectu) or SUM_POSTAVLJANJE_BRODOVI_LISTA[2].mask.get_at(poz_u_rectu) or SUM_POSTAVLJANJE_BRODOVI_LISTA[3].mask.get_at(poz_u_rectu) or SUM_POSTAVLJANJE_BRODOVI_LISTA[4].mask.get_at(poz_u_rectu)): #Ako C i ne B onda crtaj C
                if SUM_POSTAVLJANJE_BRODOVI_CRTAJ.get(SUM_POSTAVLJANJE_BRODOVI_LISTA[0])[0] == True:
                    PROZOR.blit(OBRUBI_BRODOVI_CRTANJE[0][0],OBRUBI_BRODOVI_CRTANJE[0][1])
                    for k in range(1,5):
                        if SUM_POSTAVLJANJE_BRODOVI_CRTAJ.get(SUM_POSTAVLJANJE_BRODOVI_LISTA[k])[0] == True:
                            PROZOR.blit(SUM_POSTAVLJANJE_BRODOVI_LISTA[k].image,SUM_POSTAVLJANJE_BRODOVI_LISTA[k].rect)
                    break

            elif SUM_POSTAVLJANJE_BRODOVI_LISTA[1].mask.get_at(poz_u_rectu) and not (SUM_POSTAVLJANJE_BRODOVI_LISTA[2].mask.get_at(poz_u_rectu) or SUM_POSTAVLJANJE_BRODOVI_LISTA[3].mask.get_at(poz_u_rectu) or SUM_POSTAVLJANJE_BRODOVI_LISTA[4].mask.get_at(poz_u_rectu)): #Ako B i ne D onda crtaj B
                if SUM_POSTAVLJANJE_BRODOVI_CRTAJ.get(SUM_POSTAVLJANJE_BRODOVI_LISTA[1])[0] == True:
                    PROZOR.blit(OBRUBI_BRODOVI_CRTANJE[1][0],OBRUBI_BRODOVI_CRTANJE[1][1])
                    for k in range(2,5):
                        if SUM_POSTAVLJANJE_BRODOVI_CRTAJ.get(SUM_POSTAVLJANJE_BRODOVI_LISTA[k])[0] == True:
                            PROZOR.blit(SUM_POSTAVLJANJE_BRODOVI_LISTA[k].image,SUM_POSTAVLJANJE_BRODOVI_LISTA[k].rect)
                    break
                
            elif SUM_POSTAVLJANJE_BRODOVI_LISTA[2].mask.get_at(poz_u_rectu) and not (SUM_POSTAVLJANJE_BRODOVI_LISTA[3].mask.get_at(poz_u_rectu) or SUM_POSTAVLJANJE_BRODOVI_LISTA[4].mask.get_at(poz_u_rectu)): #Ako D i ne S ili P onda crtaj D
                if SUM_POSTAVLJANJE_BRODOVI_CRTAJ.get(SUM_POSTAVLJANJE_BRODOVI_LISTA[2])[0] == True:
                    PROZOR.blit(OBRUBI_BRODOVI_CRTANJE[2][0],OBRUBI_BRODOVI_CRTANJE[2][1])
                    for k in range(3,5):
                        if SUM_POSTAVLJANJE_BRODOVI_CRTAJ.get(SUM_POSTAVLJANJE_BRODOVI_LISTA[k])[0] == True:
                            PROZOR.blit(SUM_POSTAVLJANJE_BRODOVI_LISTA[k].image,SUM_POSTAVLJANJE_BRODOVI_LISTA[k].rect)
                    break
                
            elif SUM_POSTAVLJANJE_BRODOVI_LISTA[3].mask.get_at(poz_u_rectu) and not SUM_POSTAVLJANJE_BRODOVI_LISTA[4].mask.get_at(poz_u_rectu): #Ako S i ne P onda crtaj S
                if SUM_POSTAVLJANJE_BRODOVI_CRTAJ.get(SUM_POSTAVLJANJE_BRODOVI_LISTA[3])[0] == True:
                    PROZOR.blit(OBRUBI_BRODOVI_CRTANJE[3][0],OBRUBI_BRODOVI_CRTANJE[4][1])
                    for k in range(4,5):
                        if SUM_POSTAVLJANJE_BRODOVI_CRTAJ.get(SUM_POSTAVLJANJE_BRODOVI_LISTA[k])[0] == True:
                            PROZOR.blit(SUM_POSTAVLJANJE_BRODOVI_LISTA[k].image,SUM_POSTAVLJANJE_BRODOVI_LISTA[k].rect)
                    break
            
            elif SUM_POSTAVLJANJE_BRODOVI_LISTA[4].mask.get_at(poz_u_rectu): #Ako P crtaj P
                if SUM_POSTAVLJANJE_BRODOVI_CRTAJ.get(SUM_POSTAVLJANJE_BRODOVI_LISTA[4])[0] == True:
                    PROZOR.blit(OBRUBI_BRODOVI_CRTANJE[4][0],OBRUBI_BRODOVI_CRTANJE[4][1])
                    break


def crtanje_pozadine(play_mouse_pos):
    PROZOR.blit(GRID_VODA,GRID_VODA_RECT)
    PROZOR.blit(BG_POSTAVLJANJE,BG_POSTAVALJANJE_RECT), PROZOR.blit(SUM_POSTAVLJANJE,SUM_POSTAVLJANJE_RECT)
    for i in range(len(SUM_POSTAVLJANJE_BRODOVI_CRTAJ)):
        if SUM_POSTAVLJANJE_BRODOVI_CRTAJ.get(SUM_POSTAVLJANJE_BRODOVI_LISTA[i])[0] == True:
            PROZOR.blit(SUM_POSTAVLJANJE_BRODOVI_LISTA[i].image,SUM_POSTAVLJANJE_BRODOVI_LISTA[i].rect)
            if SUM_POSTAVLJANJE_BRODOVI_CRTAJ.get(SUM_POSTAVLJANJE_BRODOVI_LISTA[i])[1] == True:
                PROZOR.blit(OBRUBI_BRODOVI_CRTANJE[i][0],OBRUBI_BRODOVI_CRTANJE[i][1])
    crtanje_obruba_hover(play_mouse_pos)
            
           

def provjera_hovera(brod,lista_rect_kvadrata,mouse_pos,brodovi_rotacija): #Crveni i zeleni hoveri
    for kvadrat in lista_rect_kvadrata:
            if kvadrat.collidepoint(mouse_pos):
                crveni_pravokutnik = CRVENI_KVADRATI.get(brod).get_rect(topleft = (kvadrat.topleft))
                zeleni_pravokutnik = ZELENI_KVADRATI.get(brod).get_rect(topleft = (kvadrat.topleft))  
                Kvadrat_hover_x, Kvadrat_hover_y = kvadrat.x, kvadrat.y
                j = (Kvadrat_hover_x-64)/48 - 1
                i = (Kvadrat_hover_y-96)/48 - 1  
                for brodek in LISTA_BRODOVA:
                    if brod != brodek:
                        if pygame.sprite.collide_rect(brod,brodek) == True:
                            if pygame.Rect.colliderect(crveni_pravokutnik,brodek.rect) == True:
                                PROZOR.blit(CRVENI_KVADRATI.get(brod),crveni_pravokutnik)
                                break
                        elif brodovi_rotacija.get(brod) == 0:
                            if j + duljina_broda > 10:
                                PROZOR.blit(CRVENI_KVADRATI.get(brod),crveni_pravokutnik)
                                break
                            else:    
                                PROZOR.blit(ZELENI_KVADRATI.get(brod), zeleni_pravokutnik)
                        elif brodovi_rotacija.get(brod) == 1:
                            if i + duljina_broda > 10:
                                PROZOR.blit(CRVENI_KVADRATI.get(brod),crveni_pravokutnik)
                                break
                            else:    
                                PROZOR.blit(ZELENI_KVADRATI.get(brod), zeleni_pravokutnik)

def rotate_key_animacija(pozicija_misa):
    global rotate_key_index
    rotate_key_index += 0.03
    if rotate_key_index >= len(rotate_lista):
        rotate_key_index = 0
    rotate_surf = rotate_lista[int(rotate_key_index)]
    rotate_rect = rotate_surf.get_rect(bottomright=(pozicija_misa))
    PROZOR.blit(rotate_surf, rotate_rect)

def čekanje_za_odabir(brod,brod_r,brod_velkiX,brodovi_rotacija,Brodovi_single_grupa,lista_rect_kvadrata,brodovi_pozicije,crtanje_imena,igrač):
    global idi
    global Kvadrat_x, Kvadrat_y
    global HOVER_BRODOVA
    idi = True
    while idi:
        čekanje_mouse_poz = pygame.mouse.get_pos()
        PROZOR.fill("White")
        crtanje_pozadine(čekanje_mouse_poz)
        if igrač == 'A':
            gridA('lijevo')
        elif igrač == 'B':
            gridB('lijevo')
        
        poz_broda_x, poz_broda_y = čekanje_mouse_poz
        brod.rect.topleft = (poz_broda_x-24, poz_broda_y-24) #brod prati cursor

        for brodic in SUM_POSTAVLJANJE_BRODOVI_LISTA:
            if SUM_POSTAVLJANJE_BRODOVI_CRTAJ.get(brodic) == [False,False]: 
                Brodovi_single_grupa.get(SUM_BRODOVI_VEZA_SPRITE_BRODOVI.get(brodic)).draw(PROZOR)
        Brodovi_single_grupa.get(brod).draw(PROZOR) 

        #Crveni i zeleni hoveri
        provjera_hovera(brod,lista_rect_kvadrata,čekanje_mouse_poz,brodovi_rotacija)
        hoverani_brod_rect = HOVER_BRODOVA.get(brod).get_rect(topleft = (brod.rect.topleft))
        PROZOR.blit(HOVER_BRODOVA.get(brod), hoverani_brod_rect)
        PROZOR.blit(crtanje_imena[0],crtanje_imena[1])
        rotate_key_animacija(čekanje_mouse_poz)
        if len(postavljeni_brodovi) < 5:
            CONFIRM_GUMB_PLAY = Button('Potvrdi', 30, 'Black', 175, 34, 'Grey', 'Grey', (1157,70))
            CONFIRM_GUMB_PLAY.update(PROZOR)
        else:
            CONFIRM_GUMB_PLAY = Button('Potvrdi', 30, 'Black', 175, 34, '#3EC9E9', '#77dd77', (1157,70))
            CONFIRM_GUMB_PLAY.changeColor(play_mouse_pos)
            CONFIRM_GUMB_PLAY.update(PROZOR)
        
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN and event.key == K_r:
                if brod_r == 0:
                    brod.rotacija_poz_90(brod_velkiX,poz_broda_x,poz_broda_y,HOVER_BRODOVA.get(brod),ZELENI_KVADRATI.get(brod),CRVENI_KVADRATI.get(brod))
                    brodovi_rotacija.update({brod:1})
                    brod_r = 1
                   
                elif brod_r == 1: 
                    brod.rotacija_neg_90(brod_velkiX,poz_broda_x,poz_broda_y,HOVER_BRODOVA.get(brod),ZELENI_KVADRATI.get(brod),CRVENI_KVADRATI.get(brod))
                    brodovi_rotacija.update({brod:0})
                    brod_r = 0
                    
                
            if event.type == MOUSEBUTTONDOWN:
                collide_kvadrat(brod_velkiX,brodovi_rotacija,lista_rect_kvadrata,brodovi_pozicije,brod,HOVER_BRODOVA.get(brod),ZELENI_KVADRATI.get(brod),CRVENI_KVADRATI.get(brod))
                
        pygame.display.update()
                
def collide_kvadrat(brod_velkiX,brodovi_rotacija,lista_rect_kvadrata,brodovi_pozicije,brod,Hover_brod,Zeleni_brod,Crveni_brod):
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
                    brod_velkiX.rect.topleft = (Kvadrat_x + 640, Kvadrat_y)
                    while PROVJERA:
                        provjera(Kvadrat_x, Kvadrat_y, duljina_broda,brod,brod_velkiX,brodovi_rotacija,brodovi_pozicije,Hover_brod,Zeleni_brod,Crveni_brod)
                    idi = False
    PROVJERA= True    
 
def provjera(x,y,duljinabroda,brod,brod_velkiX,brodovi_rotacija,brodovi_pozicije,Hover_brod,Zeleni_brod,Crveni_brod): #Provjerava stanu li brodovi u polje i preklapaju li se
    
    j = (y-100)/48 - 1
    i = (x-50)/48 - 1
    global PROVJERA
    if brodovi_rotacija.get(brod) == 1:
        if j + duljinabroda > 10:
            brod.vrati_nazad(brod_velkiX,brodovi_rotacija,brodovi_pozicije,Hover_brod,Zeleni_brod,Crveni_brod)
        else:
            for brodek in LISTA_BRODOVA:
                if brod != brodek:
                    if pygame.sprite.collide_rect(brodek,brod) == True:
                        brod.vrati_nazad(brod_velkiX,brodovi_rotacija,brodovi_pozicije,Hover_brod,Zeleni_brod,Crveni_brod)
    if brodovi_rotacija.get(brod) == 0:
        if i + duljinabroda > 10:
            brod.vrati_nazad(brod_velkiX,brodovi_rotacija,brodovi_pozicije,Hover_brod,Zeleni_brod,Crveni_brod)
        else:
            for brodek in LISTA_BRODOVA:
                if brod != brodek:
                    if pygame.sprite.collide_rect(brodek,brod) == True:
                        brod.vrati_nazad(brod_velkiX,brodovi_rotacija,brodovi_pozicije,Hover_brod,Zeleni_brod,Crveni_brod)
                        
    if vrati_nazad_provjera == False:
        pygame.mixer.Sound.play(POSTAVLJANJE_BRODA_ZVUK)
        
        SUM_POSTAVLJANJE_BRODOVI_CRTAJ.update({list(SUM_BRODOVI_VEZA_SPRITE_BRODOVI.keys())[list(SUM_BRODOVI_VEZA_SPRITE_BRODOVI.values()).index(brod)]:[False,False]})
        list(SUM_BRODOVI_VEZA_SPRITE_BRODOVI.keys())[list(SUM_BRODOVI_VEZA_SPRITE_BRODOVI.values()).index(brod)].mask.clear()
    
    elif vrati_nazad_provjera == True:
        pygame.mixer.Sound.play(VRATI_NAZAD_ZVUK)

    PROVJERA = False
    
def zapis(igrac): #zapisuje pozicije brodova u listu
    global lista_imena_kvadrata_A
    global lista_imena_kvadrata_B
    global LISTA_BRODOVA
    index = 0
    if igrac == 'A':
        lista_imena_kvadrata_A = []
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
        lista_imena_kvadrata_B = []
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
    global HOVER_BRODOVA
    global ZELENI_KVADRATI, CRVENI_KVADRATI
    global SUM_POSTAVLJANJE_BRODOVI_LISTA
    global SUM_POSTAVLJANJE_BRODOVI_CRTAJ
    global SUM_BRODOVI_VEZA_SPRITE_BRODOVI
    global SUM_POSTAVLJANJE_IMENA
    global lista_rect_kvadrata_A
    global player_A
    global player_A_render
    global player_A_rect
    global PLAYERI_FONT

    zmaj = False

    player_A = selektirani_profili[0]
    postavljeni_brodovi = []
    LISTA_BRODOVA = []
    vrati_nazad_provjera = False
    brod_izabran = False
    
    PLAYERI_FONT = pygame.font.Font(None, 28)
    player_A_render = PLAYERI_FONT.render(player_A,1,'Black')
    player_A_rect = player_A_render.get_rect(center = (482, 82))
    
    crtanje_imena_lista_A = [player_A_render,player_A_rect]

    
    SUM_CARRIER = CrtanjeBrod(os.path.join("postavljanje", "carrier_samsung.png" ))
    SUM_BATTLESHIP = CrtanjeBrod(os.path.join("postavljanje", "battleship_samsung.png" ))
    SUM_DESTROYER = CrtanjeBrod(os.path.join("postavljanje", "destroyer_samsung.png" ))
    SUM_SUBMARINE = CrtanjeBrod(os.path.join("postavljanje", "submarine_samsung.png" ))
    SUM_PATROL = CrtanjeBrod(os.path.join("postavljanje", "patrol_samsung.png" ))

    SUM_POSTAVLJANJE_BRODOVI_LISTA = [SUM_CARRIER, SUM_BATTLESHIP, 
    SUM_DESTROYER,SUM_SUBMARINE,SUM_PATROL]

    SUM_POSTAVLJANJE_BRODOVI_CRTAJ = {SUM_CARRIER:[True,False], SUM_BATTLESHIP:[True,False], SUM_DESTROYER:[True,False], 
    SUM_SUBMARINE:[True,False], SUM_PATROL:[True,False]}

    SUM_POSTAVLJANJE_IMENA = {SUM_CARRIER:"carrier", SUM_BATTLESHIP:"battleship", SUM_DESTROYER:"destroyer", 
    SUM_SUBMARINE:"submarine", SUM_PATROL:"patrol"}

    
#uploada slike Spriteova
    CARRIER = Brod(os.path.join("potapanje brodova", "carrier5.png"), 0, 0)
    BATTLESHIP = Brod(os.path.join("potapanje brodova", "battleship4.png"), 0, 0)
    DESTROYER = Brod(os.path.join("potapanje brodova", "destroyer3.png"), 0, 0)
    SUBMARINE = Brod(os.path.join("potapanje brodova", "submarine3.png"), 0, 0)
    PATROL = Brod(os.path.join("potapanje brodova", "patrol2.png"), 0, 0)

    CARRIER_GRUPA = pygame.sprite.GroupSingle(CARRIER)
    BATTLESHIP_GRUPA = pygame.sprite.GroupSingle(BATTLESHIP)
    DESTROYER_GRUPA = pygame.sprite.GroupSingle(DESTROYER)
    SUBMARINE_GRUPA = pygame.sprite.GroupSingle(SUBMARINE)
    PATROL_GRUPA = pygame.sprite.GroupSingle(PATROL)

    BRODOVI_SINGLE_GRUPE_A = {CARRIER:CARRIER_GRUPA, BATTLESHIP:BATTLESHIP_GRUPA, 
    DESTROYER:DESTROYER_GRUPA, SUBMARINE:SUBMARINE_GRUPA, PATROL:PATROL_GRUPA}

    
    BRODOVI_GRUPA_A = pygame.sprite.Group()
    BRODOVI_GRUPA_A.add(CARRIER,BATTLESHIP,DESTROYER,SUBMARINE,PATROL)
    LISTA_BRODOVA = BRODOVI_GRUPA_A.sprites()
    
    SUM_BRODOVI_VEZA_SPRITE_BRODOVI = {SUM_CARRIER:CARRIER, SUM_BATTLESHIP:BATTLESHIP, SUM_DESTROYER:DESTROYER, 
    SUM_SUBMARINE:SUBMARINE, SUM_PATROL:PATROL}
    
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
    
    HOVER_BRODOVA = {CARRIER:HOVER_CARRIER, BATTLESHIP:HOVER_BATTLESHIP, DESTROYER:HOVER_DESTROYER, SUBMARINE:HOVER_SUBMARINE, PATROL:HOVER_PATROL}
    ZELENI_KVADRATI = {CARRIER:ZELENI_KVADRAT_5, BATTLESHIP:ZELENI_KVADRAT_4, DESTROYER:ZELENI_KVADRAT_3, SUBMARINE:ZELENI_KVADRAT_3, PATROL:ZELENI_KVADRAT_2}
    CRVENI_KVADRATI = {CARRIER:CRVENI_KVADRAT_5, BATTLESHIP:CRVENI_KVADRAT_4, DESTROYER:CRVENI_KVADRAT_3, SUBMARINE:CRVENI_KVADRAT_3, PATROL:CRVENI_KVADRAT_2}
    #za igranje
    run_pA = True
    brodovi_pozicije_A = {CARRIER: (CARRIER.pozx, CARRIER.pozy), BATTLESHIP: (BATTLESHIP.pozx, BATTLESHIP.pozy), DESTROYER: (DESTROYER.pozx, DESTROYER.pozy), SUBMARINE: (SUBMARINE.pozx, SUBMARINE.pozy), PATROL: (PATROL.pozx, PATROL.pozy)}
    brodovi_rotacija_A = {CARRIER: 0, BATTLESHIP: 0, DESTROYER: 0, SUBMARINE: 0, PATROL: 0}
    while run_pA == True:
        play_mouse_pos = pygame.mouse.get_pos()
        zmaj = False
        PROZOR.fill("White")
        crtanje_pozadine(play_mouse_pos)
        gridA('lijevo')
        PROZOR.blit(crtanje_imena_lista_A[0],crtanje_imena_lista_A[1])
        for brodic in SUM_POSTAVLJANJE_BRODOVI_LISTA:
            if SUM_POSTAVLJANJE_BRODOVI_CRTAJ.get(brodic) == [False,False]: 
                BRODOVI_SINGLE_GRUPE_A.get(SUM_BRODOVI_VEZA_SPRITE_BRODOVI.get(brodic)).draw(PROZOR)
        if len(postavljeni_brodovi) < 5:
            CONFIRM_GUMB_PLAY = Button('Potvrdi', 30, 'Black', 175, 34, 'Grey', 'Grey', (1157,70))
            CONFIRM_GUMB_PLAY.update(PROZOR)
        else:
            CONFIRM_GUMB_PLAY = Button('Potvrdi', 30, 'Black', 175, 34, '#3EC9E9', '#77dd77', (1157,70))
            CONFIRM_GUMB_PLAY.changeColor(play_mouse_pos)
            CONFIRM_GUMB_PLAY.update(PROZOR)
            
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    esc_screen('Želiš li izaći iz igre?', PROZOR)
                    if zmaj == True:
                        run_pA = False
                    else: pass
            if event.type == MOUSEBUTTONDOWN:
                for SUM_BROD in SUM_POSTAVLJANJE_BRODOVI_LISTA:
                    SUM_BROD.mask_collide(play_mouse_pos)
                    if SUM_POSTAVLJANJE_BRODOVI_CRTAJ.get(SUM_BROD) == [False,False]:
                        SUM_BRODOVI_VEZA_SPRITE_BRODOVI.get(SUM_BROD).collide()
                if len(postavljeni_brodovi) == 5:
                    CONFIRM_GUMB_PLAY.checkForClick('A')

            if run_pA == True:
                if brod_izabran == True:
                    for kvadrat in lista_rect_kvadrata_A:
                        if kvadrat.collidepoint(play_mouse_pos):
                            if brod_collidean == CARRIER:
                                čekanje_za_odabir(CARRIER,brodovi_rotacija_A.get(CARRIER),CARRIER_X,brodovi_rotacija_A,BRODOVI_SINGLE_GRUPE_A,lista_rect_kvadrata_A,brodovi_pozicije_A,crtanje_imena_lista_A,'A')
                                if "C" not in postavljeni_brodovi and vrati_nazad_provjera == False:
                                    postavljeni_brodovi.append("C")
                                elif vrati_nazad_provjera == True:
                                    vrati_nazad_provjera = False
                                    if "C" in postavljeni_brodovi:
                                        postavljeni_brodovi.remove("C")
                                brod_izabran = False
                
                            elif brod_collidean == BATTLESHIP:
                                čekanje_za_odabir(BATTLESHIP,brodovi_rotacija_A.get(BATTLESHIP),BATTLESHIP_X,brodovi_rotacija_A,BRODOVI_SINGLE_GRUPE_A,lista_rect_kvadrata_A,brodovi_pozicije_A,crtanje_imena_lista_A,'A')
                                if "B" not in postavljeni_brodovi and vrati_nazad_provjera == False:
                                    postavljeni_brodovi.append("B")
                                elif vrati_nazad_provjera == True:
                                    vrati_nazad_provjera = False
                                    if "B" in postavljeni_brodovi:
                                        postavljeni_brodovi.remove("B")
                                brod_izabran = False

                            elif brod_collidean == SUBMARINE:
                                čekanje_za_odabir(SUBMARINE,brodovi_rotacija_A.get(SUBMARINE),SUBMARINE_X,brodovi_rotacija_A,BRODOVI_SINGLE_GRUPE_A,lista_rect_kvadrata_A,brodovi_pozicije_A,crtanje_imena_lista_A,'A')
                                if "S" not in postavljeni_brodovi and vrati_nazad_provjera == False:
                                    postavljeni_brodovi.append("S")
                                elif vrati_nazad_provjera == True:
                                    vrati_nazad_provjera = False
                                    if "S" in postavljeni_brodovi:
                                        postavljeni_brodovi.remove("S")
                                brod_izabran = False
                                                        
                            elif brod_collidean == DESTROYER:
                                čekanje_za_odabir(DESTROYER,brodovi_rotacija_A.get(DESTROYER),DESTROYER_X,brodovi_rotacija_A,BRODOVI_SINGLE_GRUPE_A,lista_rect_kvadrata_A,brodovi_pozicije_A,crtanje_imena_lista_A,'A')
                                if "D" not in postavljeni_brodovi and vrati_nazad_provjera == False:
                                    postavljeni_brodovi.append("D")
                                elif vrati_nazad_provjera == True:
                                    vrati_nazad_provjera = False
                                    if "D" in postavljeni_brodovi:
                                        postavljeni_brodovi.remove("D")
                                brod_izabran = False

                            elif brod_collidean == PATROL:
                                čekanje_za_odabir(PATROL,brodovi_rotacija_A.get(PATROL),PATROL_X,brodovi_rotacija_A,BRODOVI_SINGLE_GRUPE_A,lista_rect_kvadrata_A,brodovi_pozicije_A,crtanje_imena_lista_A,'A')
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
    global HOVER_BRODOVA
    global ZELENI_KVADRATI,CRVENI_KVADRATI
    global SUM_POSTAVLJANJE_BRODOVI_LISTA
    global SUM_POSTAVLJANJE_BRODOVI_CRTAJ
    global SUM_BRODOVI_VEZA_SPRITE_BRODOVI
    global SUM_POSTAVLJANJE_IMENA
    global lista_rect_kvadrata_B
    global player_B
    global player_B_render
    global player_B_rect
    
    player_B = selektirani_profili[1]
    postavljeni_brodovi = []
    LISTA_BRODOVA = []
    vrati_nazad_provjera = False
    brod_izabran = False
    zmaj = False
    
    player_B_render = PLAYERI_FONT.render(player_B,1,'Black')
    player_B_rect = player_B_render.get_rect(center = (482, 82))
    
    crtanje_imena_lista_B = [player_B_render,player_B_rect]

    SUM_CARRIER = CrtanjeBrod(os.path.join("postavljanje", "carrier_samsung.png" ))
    SUM_BATTLESHIP = CrtanjeBrod(os.path.join("postavljanje", "battleship_samsung.png" ))
    SUM_DESTROYER = CrtanjeBrod(os.path.join("postavljanje", "destroyer_samsung.png" ))
    SUM_SUBMARINE = CrtanjeBrod(os.path.join("postavljanje", "submarine_samsung.png" ))
    SUM_PATROL = CrtanjeBrod(os.path.join("postavljanje", "patrol_samsung.png" ))

    SUM_POSTAVLJANJE_BRODOVI_LISTA = [SUM_CARRIER, SUM_BATTLESHIP, 
    SUM_DESTROYER,SUM_SUBMARINE,SUM_PATROL]

    SUM_POSTAVLJANJE_BRODOVI_CRTAJ = {SUM_CARRIER:[True,False], SUM_BATTLESHIP:[True,False], SUM_DESTROYER:[True,False], 
    SUM_SUBMARINE:[True,False], SUM_PATROL:[True,False]}

    SUM_POSTAVLJANJE_IMENA = {SUM_CARRIER:"carrier", SUM_BATTLESHIP:"battleship", SUM_DESTROYER:"destroyer", 
    SUM_SUBMARINE:"submarine", SUM_PATROL:"patrol"}

    
    CARRIER = Brod(os.path.join("potapanje brodova", "carrier5.png"), 0, 0)
    BATTLESHIP = Brod(os.path.join("potapanje brodova", "battleship4.png"), 0, 0)
    DESTROYER = Brod(os.path.join("potapanje brodova", "destroyer3.png"), 0, 0)
    SUBMARINE = Brod(os.path.join("potapanje brodova", "submarine3.png"), 0, 0)
    PATROL = Brod(os.path.join("potapanje brodova", "patrol2.png"), 0, 0)

    CARRIER_GRUPA = pygame.sprite.GroupSingle(CARRIER)
    BATTLESHIP_GRUPA = pygame.sprite.GroupSingle(BATTLESHIP)
    DESTROYER_GRUPA = pygame.sprite.GroupSingle(DESTROYER)
    SUBMARINE_GRUPA = pygame.sprite.GroupSingle(SUBMARINE)
    PATROL_GRUPA = pygame.sprite.GroupSingle(PATROL)

    BRODOVI_SINGLE_GRUPE_B = {CARRIER:CARRIER_GRUPA, BATTLESHIP:BATTLESHIP_GRUPA, 
    DESTROYER:DESTROYER_GRUPA, SUBMARINE:SUBMARINE_GRUPA, PATROL:PATROL_GRUPA}
    
    BRODOVI_GRUPA_B = pygame.sprite.Group()
    BRODOVI_GRUPA_B.add(CARRIER,BATTLESHIP,DESTROYER,SUBMARINE,PATROL)
    LISTA_BRODOVA = BRODOVI_GRUPA_B.sprites()
    
    SUM_BRODOVI_VEZA_SPRITE_BRODOVI = {SUM_CARRIER:CARRIER, SUM_BATTLESHIP:BATTLESHIP, SUM_DESTROYER:DESTROYER, 
    SUM_SUBMARINE:SUBMARINE, SUM_PATROL:PATROL}

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
    
    HOVER_BRODOVA = {CARRIER:HOVER_CARRIER, BATTLESHIP:HOVER_BATTLESHIP, DESTROYER:HOVER_DESTROYER, SUBMARINE:HOVER_SUBMARINE, PATROL:HOVER_PATROL}
    ZELENI_KVADRATI = {CARRIER:ZELENI_KVADRAT_5, BATTLESHIP:ZELENI_KVADRAT_4, DESTROYER:ZELENI_KVADRAT_3, SUBMARINE:ZELENI_KVADRAT_3, PATROL:ZELENI_KVADRAT_2}
    CRVENI_KVADRATI = {CARRIER:CRVENI_KVADRAT_5, BATTLESHIP:CRVENI_KVADRAT_4, DESTROYER:CRVENI_KVADRAT_3, SUBMARINE:CRVENI_KVADRAT_3, PATROL:CRVENI_KVADRAT_2}
    
    run_pB = True
    brodovi_pozicije_B = {CARRIER: (CARRIER.pozx, CARRIER.pozy), BATTLESHIP: (BATTLESHIP.pozx, BATTLESHIP.pozy), DESTROYER: (DESTROYER.pozx, DESTROYER.pozy), SUBMARINE: (SUBMARINE.pozx, SUBMARINE.pozy), PATROL: (PATROL.pozx, PATROL.pozy)}
    brodovi_rotacija_B = {CARRIER: 0, BATTLESHIP: 0, DESTROYER: 0, SUBMARINE: 0, PATROL: 0}
    while run_pB == True:
        play_mouse_pos = pygame.mouse.get_pos()
        zmaj = False
        PROZOR.fill("White")
        crtanje_pozadine(play_mouse_pos)
        gridB('lijevo')
        PROZOR.blit(crtanje_imena_lista_B[0],crtanje_imena_lista_B[1])
        for brodic in SUM_POSTAVLJANJE_BRODOVI_LISTA:
            if SUM_POSTAVLJANJE_BRODOVI_CRTAJ.get(brodic) == [False,False]: 
                BRODOVI_SINGLE_GRUPE_B.get(SUM_BRODOVI_VEZA_SPRITE_BRODOVI.get(brodic)).draw(PROZOR)
        
        if len(postavljeni_brodovi) < 5:
            CONFIRM_GUMB_PLAY = Button('Potvrdi', 30, 'Black', 175, 34, 'Grey', 'Grey', (1157,70))
            CONFIRM_GUMB_PLAY.update(PROZOR)
        else:
            CONFIRM_GUMB_PLAY = Button('Potvrdi', 30, 'Black', 175, 34, '#3EC9E9', '#77dd77', (1157,70))
            CONFIRM_GUMB_PLAY.changeColor(play_mouse_pos)
            CONFIRM_GUMB_PLAY.update(PROZOR)
            
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    esc_screen('Želiš li izaći iz igre?', PROZOR)
                    if zmaj == True:
                        run_pB = False
                    else: pass
            if event.type == MOUSEBUTTONDOWN:
                for SUM_BROD in SUM_POSTAVLJANJE_BRODOVI_LISTA:
                    SUM_BROD.mask_collide(play_mouse_pos)
                    if SUM_POSTAVLJANJE_BRODOVI_CRTAJ.get(SUM_BROD) == [False,False]:
                        SUM_BRODOVI_VEZA_SPRITE_BRODOVI.get(SUM_BROD).collide()
                if len(postavljeni_brodovi) == 5:
                    CONFIRM_GUMB_PLAY.checkForClick('B')
            if run_pB == True:
                if brod_izabran == True:
                    for kvadrat in lista_rect_kvadrata_B:
                        if kvadrat.collidepoint(play_mouse_pos):
                            if brod_collidean == CARRIER:
                                čekanje_za_odabir(CARRIER,brodovi_rotacija_B.get(CARRIER),CARRIER_X,brodovi_rotacija_B,BRODOVI_SINGLE_GRUPE_B,lista_rect_kvadrata_B,brodovi_pozicije_B,crtanje_imena_lista_B,'B')
                                if "C" not in postavljeni_brodovi and vrati_nazad_provjera == False:
                                    postavljeni_brodovi.append("C")
                                elif vrati_nazad_provjera == True:
                                    vrati_nazad_provjera = False
                                    if "C" in postavljeni_brodovi:
                                        postavljeni_brodovi.remove("C")
                                brod_izabran = False
                
                            elif brod_collidean == BATTLESHIP:
                                čekanje_za_odabir(BATTLESHIP,brodovi_rotacija_B.get(BATTLESHIP),BATTLESHIP_X,brodovi_rotacija_B,BRODOVI_SINGLE_GRUPE_B,lista_rect_kvadrata_B,brodovi_pozicije_B,crtanje_imena_lista_B,'B')
                                if "B" not in postavljeni_brodovi and vrati_nazad_provjera == False:
                                    postavljeni_brodovi.append("B")
                                elif vrati_nazad_provjera == True:
                                    vrati_nazad_provjera = False
                                    if "B" in postavljeni_brodovi:
                                        postavljeni_brodovi.remove("B")
                                brod_izabran = False

                            elif brod_collidean == SUBMARINE:
                                čekanje_za_odabir(SUBMARINE,brodovi_rotacija_B.get(SUBMARINE),SUBMARINE_X,brodovi_rotacija_B,BRODOVI_SINGLE_GRUPE_B,lista_rect_kvadrata_B,brodovi_pozicije_B,crtanje_imena_lista_B,'B')
                                if "S" not in postavljeni_brodovi and vrati_nazad_provjera == False:
                                    postavljeni_brodovi.append("S")
                                elif vrati_nazad_provjera == True:
                                    vrati_nazad_provjera = False
                                    if "S" in postavljeni_brodovi:
                                        postavljeni_brodovi.remove("S")
                                brod_izabran = False
                                                        
                            elif brod_collidean == DESTROYER:
                                čekanje_za_odabir(DESTROYER,brodovi_rotacija_B.get(DESTROYER),DESTROYER_X,brodovi_rotacija_B,BRODOVI_SINGLE_GRUPE_B,lista_rect_kvadrata_B,brodovi_pozicije_B,crtanje_imena_lista_B,'B')
                                if "D" not in postavljeni_brodovi and vrati_nazad_provjera == False:
                                    postavljeni_brodovi.append("D")
                                elif vrati_nazad_provjera == True:
                                    vrati_nazad_provjera = False
                                    if "D" in postavljeni_brodovi:
                                        postavljeni_brodovi.remove("D")
                                brod_izabran = False

                            elif brod_collidean == PATROL:
                                čekanje_za_odabir(PATROL,brodovi_rotacija_B.get(PATROL),PATROL_X,brodovi_rotacija_B,BRODOVI_SINGLE_GRUPE_B,lista_rect_kvadrata_B,brodovi_pozicije_B,crtanje_imena_lista_B,'B')
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
    global vatra_index, vatra_surf
    vatra_index += 0.1
    if vatra_index >= len(vatra_lista):
        vatra_index = 0
    vatra_surf = vatra_lista[int(vatra_index)]
    if igrac == 'A':
        for i in range(0,100):
            recA = lista_rect_kvadrata_A[i]
            if len(lista_imena_kvadrata_A[i]) == 3:
                if lista_imena_kvadrata_A[i][2] == 'x':
                    pogoden_rectA = vatra_surf.get_rect(topleft = (recA.topleft))
                    PROZOR.blit(vatra_surf, pogoden_rectA)
    elif igrac == 'B':   
        for i in range(0,100):
            recB = lista_rect_kvadrata_B[i]
            if len(lista_imena_kvadrata_B[i]) == 3:
                if lista_imena_kvadrata_B[i][2] == 'x':
                    pogoden_rectB = vatra_surf.get_rect(topleft = (recB.topleft))
                    PROZOR.blit(vatra_surf, pogoden_rectB)                 

def hoveranje_animacija(igrac, mis_poz):  # Funkcija provjerava nalazi li se mis iznad kvadratica, ako da onda nacrta poseban kvadratic da to oznaci
    HOVERANI_KVADRAT = pygame.image.load(os.path.join("potapanje brodova", "hoverani_kvadrat.png")).convert_alpha()
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

def animacija_pogodenog(pozicija):
    global pog_index
    runpog = True
    pog_index = 0
    while runpog == True:
        reset = pygame.Surface((1280,720))
        reset.fill('Black')
        reset.set_alpha(0)
        PROZOR.blit(reset,(0,0))
        pog_index += 0.15
        if pog_index > len(pogodeno_lista):
            pog_index = 0
            runpog = False
            time.sleep(1)
            return
        pogodeno_surf = pogodeno_lista[int(pog_index)]
        pogodeno_rect = pogodeno_surf.get_rect(topleft = pozicija)
        PROZOR.blit(pogodeno_surf, pogodeno_rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(FPS)

def animacija_fulanog(pozicija):
    global bomb_ful_index
    runful = True
    bomb_ful_index = 0
    while runful == True:
        reset = pygame.Surface((1280,720))
        reset.fill('Black')
        reset.set_alpha(0)
        PROZOR.blit(reset,(0,0))
        bomb_ful_index += 0.15
        if bomb_ful_index > len(bomba_fulano_lista):
            bomb_ful_index = 0
            runful = False
            time.sleep(1)
            return
        fulano_surf = bomba_fulano_lista[int(bomb_ful_index)]
        fulano_rect = fulano_surf.get_rect(topleft = pozicija)
        PROZOR.blit(fulano_surf, fulano_rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(FPS)

def gadanje(igrac):  # Funkcija u listi imena kvadrata upisuje x i updejta rezultat
    global rezultat_A_igrac, rezultat_B_igrac, provjera_gadanja, pogodeno
    provjera_gadanja = False
    pogodeno = False
    if igrac == 'A':
        if postavljen_kvadratA:
            for i in range(0,100):
                rect = lista_rect_kvadrata_B[i]
                if rect.collidepoint((odabrani_kvadrat_rectA.topleft)):
                    lista_imena_kvadrata_B[i].append('x')
                    provjera_gadanja = True
                    if lista_imena_kvadrata_B[i][1] != 'x':
                        rezultat_B_igrac -= 1
                        pogodeno = True
            if pogodeno == True:
                animacija_pogodenog((odabrani_kvadrat_rectA.topleft))
            else:
                animacija_fulanog((odabrani_kvadrat_rectA.topleft))
    if igrac == 'B':
        if postavljen_kvadratB:
            for i in range(0,100):
                rect = lista_rect_kvadrata_A[i]
                if rect.collidepoint((odabrani_kvadrat_rectB.topleft)):
                    lista_imena_kvadrata_A[i].append('x')
                    provjera_gadanja = True
                    if lista_imena_kvadrata_A[i][1] != 'x':
                        rezultat_A_igrac -= 1
                        pogodeno = True
            if pogodeno == True:
                animacija_pogodenog((odabrani_kvadrat_rectB.topleft))
            else:
                animacija_fulanog((odabrani_kvadrat_rectB.topleft))                      

def crtanje_ekrana_igranje():
    PROZOR.blit(VODA_IGRANJE, VODA_IGRANJE_RECT)
    PROZOR.blit(BG_IGRANJE,BG_IGRANJE_RECT)

def igranje_A_ekran():
    global zmaj, provjera_gadanja
    zmaj = False
    run = True
    provjera_gadanja = False
    while run == True:
        PROZOR.fill('White')
        crtanje_ekrana_igranje()
        gridA('lijevo')
        gridB('desno')
        PROZOR.blit(player_A_render,player_A_rect)
        BRODOVI_GRUPA_A.draw(PROZOR)
        crtanje_fulanih_podrucja()
        #animacija_gadanja()
        zbrajanje_pogodenih_dijelova_brodova()
        crtanje_xeva('A')
        crtanje_pogodenih_vlastitih('A')
        mouse_pos = pygame.mouse.get_pos()
        hoveranje_animacija('A', mouse_pos)
        GUMB_SHOOT = Button(text_input = "Pucaj", text_size = 30, text_color = 'Black', rect_width = 175, rect_height = 34, rect_color = '#3EC9E9', hoveringRect_color = '#D74B4B', pos = (1172,37))
        GUMB_SHOOT.changeColor(mouse_pos)
        GUMB_SHOOT.update(PROZOR)
        crtanje_odabranog_kvadrata('A')

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    esc_screen('Želiš li izaći iz igre?', PROZOR)
                    if zmaj == True:
                        run = False
                    else: pass
            if event.type == MOUSEBUTTONDOWN:
                if GUMB_SHOOT.checkForInput(mouse_pos):
                    gadanje('A')
                    if provjera_gadanja == True:
                        pygame.mixer.Sound.play(KLIK_GUMB_ZVUK)
                        run = False
                promjena_poz_odabranog_kvadrata('A', mouse_pos)
                pass
        pygame.display.update()
        clock.tick(FPS)

def igranje_B_ekran():
    global zmaj, provjera_gadanja
    zmaj = False
    run = True
    provjera_gadanja = False
    while run == True:
        PROZOR.fill('White')
        crtanje_ekrana_igranje()
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
        GUMB_SHOOT = Button(text_input = "Pucaj", text_size = 30, text_color = 'Black', rect_width = 175, rect_height = 34, rect_color = '#3EC9E9', hoveringRect_color = '#D74B4B', pos = (1172,37))
        GUMB_SHOOT.changeColor(mouse_pos)
        GUMB_SHOOT.update(PROZOR)
        crtanje_odabranog_kvadrata('B')

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    esc_screen('Želiš li izaći iz igre?', PROZOR)
                    if zmaj == True:
                        run = False
                    else: pass
            if event.type == MOUSEBUTTONDOWN:
                if GUMB_SHOOT.checkForInput(mouse_pos):
                    gadanje('B')
                    if provjera_gadanja == True:
                        pygame.mixer.Sound.play(KLIK_GUMB_ZVUK)
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
    global selektirani_profili
    global profili
    global zmaj
    zmaj = False
    PROZOR.fill('#143763')
    for i in range(8):
        score[i]= score[i].strip("\n")
    Miš_pozicija= pygame.mouse.get_pos()
    font = pygame.font.Font(None, 100)
    RESTART_BUTTON = Button('Restart', 30, 'Black', 200, 40, '#DADBDD', '#77dd77', (620,500))
    RESTART_BUTTON.update(PROZOR)
    RESTART_BUTTON.changeColor(Miš_pozicija)
    RESTART_BUTTON.update(PROZOR)
    MAIN_MENU_BUTTON = Button('Main menu', 30, 'Black', 200, 40, '#DADBDD', '#77dd77', (620,575))
    MAIN_MENU_BUTTON.update(PROZOR)
    MAIN_MENU_BUTTON.changeColor(Miš_pozicija)
    MAIN_MENU_BUTTON.update(PROZOR)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if RESTART_BUTTON.checkForInput(Miš_pozicija):
                pygame.mixer.Sound.play(KLIK_GUMB_ZVUK)
                restart = True
            if MAIN_MENU_BUTTON.checkForInput(Miš_pozicija):
                pygame.mixer.Sound.play(KLIK_GUMB_ZVUK)
                main()
        if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    esc_screen('Želiš li izaći iz igre?', PROZOR)
                    if zmaj == True:
                        restart = True
                        return
    pobjednik = ""
    if rezultat1 == 0:
        pobjednik = selektirani_profili[1]
    if rezultat2 == 0:
        pobjednik = selektirani_profili[0]
    while zapis_rezultata_jednom==True:
        score[profili.index(pobjednik+"\n")] = str(int(score[profili.index(pobjednik+"\n")]) + 1)#računanje scora
        if int(score[profili.index(selektirani_profili[1]+"\n")])>int(score[profili.index(selektirani_profili[0]+"\n")]):
            boja_lijevo =  "#FF0000"
            boja_desno =  "#32CD32" 
        elif int(score[profili.index(selektirani_profili[0]+"\n")])>int(score[profili.index(selektirani_profili[1]+"\n")]):
            boja_lijevo = "#32CD32"
            boja_desno = "#FF0000"  
        elif int(score[profili.index(selektirani_profili[0]+"\n")])== int(score[profili.index(selektirani_profili[1]+"\n")]):
            boja_desno= "#32CD32"
            boja_lijevo = boja_desno
        with open("potapanje brodova\score.txt", "wt",encoding="utf-8") as datoteka:
            for i in range (8):
                score[i] = score[i] + "\n"
            datoteka.writelines(score)
            
            rezultat_lijevo = font.render(selektirani_profili[0] +" "+score[profili.index(selektirani_profili[0]+"\n")][:-1],True,boja_lijevo)
            rezultat_desno = font.render(score[profili.index(selektirani_profili[1]+"\n")][:-1]+ " " +selektirani_profili[1],True,boja_desno)
            
        zapis_rezultata_jednom = False
    
    winner = font.render(pobjednik+" Victory Royale",True,"#3EC9E9",)
    dvotocka = font.render(":",True,"#000000")
    winner_rect = winner.get_rect(midtop = (640,210))
    PROZOR.blit(winner,(winner_rect))
    PROZOR.blit(rezultat_lijevo,(550-len(selektirani_profili[0])*40,310))
    PROZOR.blit(rezultat_desno,(650,310))
    PROZOR.blit(dvotocka,(605,305))
    
    pygame.display.update()


def linija_playscore_animacija(i):
    global linija_key_index, linija_playscore_surf, trenutno_ime_upis
    linija_key_index += 0.01   
    if linija_key_index >= len(linija_playscore_animacija_lista):
        linija_key_index = 0
    linija_playscore_surf = linija_playscore_animacija_lista[int(linija_key_index)]
    if trenutno_ime_upis != "":
        kraj_imena_x, kraj_imena_y = PLAYERI_LISTA_GUMBOVA[i-1].text_rect.midright
        linija_playscore_rect = linija_playscore_surf.get_rect(midright = (kraj_imena_x+5, kraj_imena_y))
    else:
        linija_playscore_rect = linija_playscore_surf.get_rect(center = (PLAYERI_LISTA_GUMBOVA[i-1].main_rect.center))
    PROZOR.blit(linija_playscore_surf, linija_playscore_rect)

def imenovanje_profila(): #upisivanje imena igrača/profila za pamćenje rezultata
    global score
    global profili
    global PLAYERI_IMENA
    global PLAYERI_SELEKTIRANI
    global PLAYERI_LISTA_GUMBOVA
    global play_run
    global biranje_profila_bool
    global imenovanje_profila_bool
    global trenutno_ime_upis
    global zmaj
    imenovanje_profila_bool = True
    font = pygame.font.Font(None, 60)
    trenutno_ime_upis = ""
    for i in range(1,9):
        PLAYERI_SELEKTIRANI.update({f"player_{i}":False})
        PLAYERI_IMENA.update({f"player{i}": profili[i-1][:-1]})
    zmaj = False
    
    while imenovanje_profila_bool == True:
        PROZOR.fill('#143763')
        Create_profile = font.render("Napravi profile",1,'Black')
        Create_profile_rect = Create_profile.get_rect(center=(630,45))
        PROZOR.blit(Create_profile,Create_profile_rect)
        score_mouse_pos = pygame.mouse.get_pos()
        

        PLAYER_BUTTON1 = Button(PLAYERI_IMENA.get("player1"), 75, 'Black', 411, 91, '#DADBDD', '#77dd77', (307, 162))
        PLAYER_BUTTON2 = Button(PLAYERI_IMENA.get("player2"), 75, 'Black', 411, 91, '#DADBDD', '#77dd77', (307, 162+134))
        PLAYER_BUTTON3 = Button(PLAYERI_IMENA.get("player3"), 75, 'Black', 411, 91, '#DADBDD', '#77dd77', (307, 162+134*2))
        PLAYER_BUTTON4 = Button(PLAYERI_IMENA.get("player4"), 75, 'Black', 411, 91, '#DADBDD', '#77dd77', (307, 162+134*3))
        
        
        PLAYER_BUTTON5 = Button(PLAYERI_IMENA.get("player5"), 75, 'Black', 411, 91, '#DADBDD', '#77dd77', (962, 162)) 
        PLAYER_BUTTON6 = Button(PLAYERI_IMENA.get("player6"), 75, 'Black', 411, 91, '#DADBDD', '#77dd77', (962, 1*134+162))        
        PLAYER_BUTTON7 = Button(PLAYERI_IMENA.get("player7"), 75, 'Black', 411, 91, '#DADBDD', '#77dd77', (962, 2*134+162))
        PLAYER_BUTTON8 = Button(PLAYERI_IMENA.get("player8"), 75, 'Black', 411, 91, '#DADBDD', '#77dd77', (962, 3*134+162)) 
        
        

        PLAYERI_LISTA_GUMBOVA = [PLAYER_BUTTON1,PLAYER_BUTTON2,PLAYER_BUTTON3,PLAYER_BUTTON4,PLAYER_BUTTON5,PLAYER_BUTTON6,PLAYER_BUTTON7,PLAYER_BUTTON8]
        
        
        BACK1 = Button("NAZAD", 45, "Black", 119,55,'#DADBDD','#77dd77', (84,54))
        BACK1.update(PROZOR)
        BACK1.changeColor(score_mouse_pos)
        BACK1.update(PROZOR)
        for player_gumb in PLAYERI_LISTA_GUMBOVA:
            player_gumb.update(PROZOR)
            player_gumb.changeColor(score_mouse_pos)
            player_gumb.update(PROZOR)                    
        CHOOSE_PROFILE = Button("Potvrdi", 30, 'Black', 119,55, '#DADBDD', '#77dd77', (1137,651))
        CHOOSE_PROFILE.update(PROZOR)
        CHOOSE_PROFILE.changeColor(score_mouse_pos)
        CHOOSE_PROFILE.update(PROZOR)
        
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            
                
            if event.type == MOUSEBUTTONDOWN:
                for i in range (8):
                    PLAYERI_SELEKTIRANI.update({f"player_{i+1}":False})
                    if PLAYERI_IMENA.get(f"player{i+1}") == "":
                        PLAYERI_IMENA.update({f"player{i+1}":"Napravi profil"})
                    if PLAYERI_IMENA.get(f"player{i+1}") + "\n" == profili[i]:
                        pass
                    else:
                        score[i] = "0\n"

                if BACK1.checkForInput(score_mouse_pos):
                    pygame.mixer.Sound.play(KLIK_GUMB_ZVUK)
                    imenovanje_profila_bool = False
                    zmaj = True
                    break
                #Sound effect
                if CHOOSE_PROFILE.checkForInput(score_mouse_pos):
                        pygame.mixer.Sound.play(KLIK_GUMB_ZVUK)
                    
                for i in range(8):
                    
                    if PLAYERI_LISTA_GUMBOVA[i].checkForInput(score_mouse_pos):
                        pygame.mixer.Sound.play(KLIK_GUMB_ZVUK)
                        
                        for k in range (8):
                            if PLAYERI_IMENA.get(f"player{k+1}") == "" and PLAYERI_SELEKTIRANI.get(f"player{k+1}") == False:
                                PLAYERI_IMENA.update({f"player{k+1}":"Napravi profil"})
                            PLAYERI_SELEKTIRANI.update({f"player_{k+1}":False})

                        
                        PLAYERI_SELEKTIRANI.update({f"player_{i+1}":True})
                        trenutno_ime_upis = ""                    
                        PLAYERI_IMENA.update({f"player{i+1}":""})
                    if CHOOSE_PROFILE.checkForInput(score_mouse_pos):
                        if PLAYERI_IMENA.get(f"player{i+1}")+"\n"== profili[i]:
                            pass
                        else:
                            score[i] = "0\n"
                        
                        with open("potapanje brodova\profili.txt", encoding="utf-8") as datoteka:
                            profili = []
                            profili = datoteka.readlines()
                            for z in range (8):
                                profili[z] = PLAYERI_IMENA.get(f"player{z+1}") + "\n"
                        with open("potapanje brodova\profili.txt","wt",encoding="utf-8",) as datoteka:
                            datoteka.writelines(profili) 
                        with open("potapanje brodova\score.txt","wt",encoding="utf-8",) as datoteka:
                            datoteka.writelines(score)         
                        imenovanje_profila_bool = False
                        
                        
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    esc_screen('Želiš li izaći iz igre?', PROZOR)
                    if zmaj == True:
                        imenovanje_profila_bool = False
                    else: pass
                for i in range(8):
                    if PLAYERI_SELEKTIRANI.get(f"player_{i+1}") == True:
                        
                        
                        if event.key == pygame.K_BACKSPACE:
                            trenutno_ime_upis = PLAYERI_IMENA.get(f"player{i+1}")
                            trenutno_ime_upis = trenutno_ime_upis[:-1]
                            PLAYERI_IMENA.update({f"player{i+1}": trenutno_ime_upis})
                            
                        
                        elif event.key == pygame.K_RETURN:
                            PLAYERI_SELEKTIRANI.update({f"player_{i+1}":False})
                            if PLAYERI_IMENA.get(f"player{i+1}") == "" :
                                PLAYERI_IMENA.update({f"player{i+1}":"Napravi profil"})
                            trenutno_ime_upis = ""
                        else:
                            if len(trenutno_ime_upis) < 8:
                                trenutno_ime_upis = PLAYERI_IMENA.get(f"player{i+1}")
                                trenutno_ime_upis += event.unicode
                                if trenutno_ime_upis not in list(PLAYERI_IMENA.values()):
                                    PLAYERI_IMENA.update({f"player{i+1}": trenutno_ime_upis})
                                else:
                                    pygame.mixer.Sound.play(VRATI_NAZAD_ZVUK)

        for i in range(1,9):
            if PLAYERI_SELEKTIRANI.get(f"player_{i}") == True:
                linija_playscore_animacija(i)
        pygame.display.update()
        clock.tick(FPS)
        
        
def biranje_profila(): #biranje igrača koji će igrati
    global selektirani_profili
    global play_run
    global PLAYERI_IMENA
    global PLAYERI_SELEKTIRANI
    global PLAYERI_LISTA_GUMBOVA
    global zmaj
    biranje_profila_bool = True
    PROZOR.fill('#143763')
    PLAYER_BUTTON1 = Button(PLAYERI_IMENA.get("player1"), 75, 'Black', 411, 91, '#DADBDD', '#77dd77', (307, 162))
    PLAYER_BUTTON2 = Button(PLAYERI_IMENA.get("player2"), 75, 'Black', 411, 91, '#DADBDD', '#77dd77', (307, 162+134))
    PLAYER_BUTTON3 = Button(PLAYERI_IMENA.get("player3"), 75, 'Black', 411, 91, '#DADBDD', '#77dd77', (307, 162+134*2))
    PLAYER_BUTTON4 = Button(PLAYERI_IMENA.get("player4"), 75, 'Black', 411, 91, '#DADBDD', '#77dd77', (307, 162+134*3))
        
        
    PLAYER_BUTTON5 = Button(PLAYERI_IMENA.get("player5"), 75, 'Black', 411, 91, '#DADBDD', '#77dd77', (962, 162)) 
    PLAYER_BUTTON6 = Button(PLAYERI_IMENA.get("player6"), 75, 'Black', 411, 91, '#DADBDD', '#77dd77', (962, 1*134+162))        
    PLAYER_BUTTON7 = Button(PLAYERI_IMENA.get("player7"), 75, 'Black', 411, 91, '#DADBDD', '#77dd77', (962, 2*134+162))
    PLAYER_BUTTON8 = Button(PLAYERI_IMENA.get("player8"), 75, 'Black', 411, 91, '#DADBDD', '#77dd77', (962, 3*134+162)) 
        
    font = pygame.font.Font(None, 60)
    
    GUMBOVI_POZICIJE = [(307, 162),(307, 162+134),(307, 162+134*2),((307, 162+134*3)),((962, 162)),(962, 1*134+162),(962, 2*134+162),(962, 3*134+162)]
    PLAYERI_LISTA_GUMBOVA=[PLAYER_BUTTON1,PLAYER_BUTTON2,PLAYER_BUTTON3,PLAYER_BUTTON4,PLAYER_BUTTON5,PLAYER_BUTTON6,PLAYER_BUTTON7,PLAYER_BUTTON8]
    GUMBOVI_METAMORFOZA = {PLAYER_BUTTON1:0, PLAYER_BUTTON2:0, PLAYER_BUTTON3:0, PLAYER_BUTTON4:0 ,PLAYER_BUTTON5:0 ,PLAYER_BUTTON6:0 ,PLAYER_BUTTON7:0 ,PLAYER_BUTTON8:0}
    PROZOR.fill('#143763')
    zmaj = False

    while biranje_profila_bool == True:

        biranje_mouse_poz = pygame.mouse.get_pos()
        Choose_profile = font.render("Izaberi profile",1,'Black')
        Choose_profile_rect = Choose_profile.get_rect(center=(630,45))
        PROZOR.blit(Choose_profile,Choose_profile_rect)
        for player_gumb in PLAYERI_LISTA_GUMBOVA:
            if GUMBOVI_METAMORFOZA.get(player_gumb) == 0:
                if PLAYERI_IMENA.get(f"player{PLAYERI_LISTA_GUMBOVA.index(player_gumb)+1}") == "Napravi profil":
                    player_gumb = Button("N/A", 75, 'Black', 411,91, '#475F77', '#77dd77',GUMBOVI_POZICIJE[PLAYERI_LISTA_GUMBOVA.index(player_gumb)])
                    player_gumb.update(PROZOR)
                    pass             
                else:
                    player_gumb = Button(PLAYERI_IMENA.get(f"player{PLAYERI_LISTA_GUMBOVA.index(player_gumb)+1}"), 75, 'Black', 411,91, '#DADBDD', '#77dd77',GUMBOVI_POZICIJE[PLAYERI_LISTA_GUMBOVA.index(player_gumb)])
                    player_gumb.update(PROZOR)
                    player_gumb.changeColor(biranje_mouse_poz)
                    player_gumb.update(PROZOR)

        BACK = Button("NAZAD", 45, "Black", 119,55,'#DADBDD','#77dd77', (84,54))
        BACK.update(PROZOR)
        BACK.changeColor(biranje_mouse_poz)
        BACK.update(PROZOR)
        CONFIRM_SELECTED =  Button(("Potvrdi"), 30, 'Black', 119,55, '#DADBDD', '#77dd77', ((1137,651)))        
        CONFIRM_SELECTED.update(PROZOR)
        CONFIRM_SELECTED.changeColor(biranje_mouse_poz)
        CONFIRM_SELECTED.update(PROZOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()   
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    esc_screen('Želiš li izaći iz igre?', PROZOR)
                    if zmaj == True:
                        biranje_profila_bool = False
                    else: pass
            if event.type == MOUSEBUTTONDOWN:
                if CONFIRM_SELECTED.checkForInput(biranje_mouse_poz):
                    if len(selektirani_profili) == 2:
                        pygame.mixer.Sound.play(KLIK_GUMB_ZVUK)
                        biranje_profila_bool = False
                if BACK.checkForInput(biranje_mouse_poz):
                    pygame.mixer.Sound.play(KLIK_GUMB_ZVUK)
                    biranje_profila_bool = False
                    zmaj = True
                    break
                if len(selektirani_profili) <= 2:
                    for i in range(8):
                        if PLAYERI_LISTA_GUMBOVA[i].checkForInput(biranje_mouse_poz):
                            pygame.mixer.Sound.play(KLIK_GUMB_ZVUK)
                            if PLAYERI_IMENA.get(f"player{i+1}") == "Napravi profil":
                                pygame.mixer.Sound.play(VRATI_NAZAD_ZVUK)
                                pass
                            else:
                                if len(selektirani_profili)<2:
                                    PLAYERI_LISTA_GUMBOVA[i] = Button(PLAYERI_IMENA.get(f"player{i+1}"), 75, 'Black', 411, 91, '#D74B4B', '#77dd77',GUMBOVI_POZICIJE[i])
                                    PLAYERI_LISTA_GUMBOVA[i].update(PROZOR)
                                    GUMBOVI_METAMORFOZA.update({PLAYERI_LISTA_GUMBOVA[i]:1})
                                if PLAYERI_IMENA.get(f"player{i+1}") in selektirani_profili:
                                    selektirani_profili.remove(PLAYERI_IMENA.get(f"player{i+1}")) 
                                    PLAYERI_LISTA_GUMBOVA[i] = Button(PLAYERI_IMENA.get(f"player{i+1}"), 30, 'Black', 411, 91, '#475F77', '#77dd77',GUMBOVI_POZICIJE[i])
                                    PLAYERI_LISTA_GUMBOVA[i].update(PROZOR)
                                    GUMBOVI_METAMORFOZA.update({PLAYERI_LISTA_GUMBOVA[i]:0})
                                elif PLAYERI_IMENA.get(f"player{i+1}") not in selektirani_profili:
                                    selektirani_profili.append(PLAYERI_IMENA.get(f"player{i+1}"))
                                if len(selektirani_profili) == 3:
                                    selektirani_profili.remove(selektirani_profili[2])
                    
                
                            
        pygame.display.update()

def score_screen():
    global profili
    global score
    global zmaj
    score_bool = True
    print (score)
    PROZOR.fill('#143763')
    font = pygame.font.Font(None, 60)
    zmaj = False
    def po_scoreu(x):  
        return int(x[0])
    score_i_profili = [] 
    for i in range (8):
        score[i] = score[i].strip("\n")
        score_i_profili.append([score[i],profili[i]])
    score_i_profili.sort(key = po_scoreu, reverse = True) 

    while score_bool == True:
        PROZOR.fill('#143763')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if BACK3.checkForInput(score_mouse_poz) == True:
                    pygame.mixer.Sound.play(KLIK_GUMB_ZVUK)
                    score_bool = False
                    break
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    esc_screen('Želiš li izaći iz igre?', PROZOR)
                    if zmaj == True:
                        score_bool = False
                        break
            
        score_mouse_poz=pygame.mouse.get_pos()
        BACK3 = Button("NAZAD", 45, "Black", 119,55,'#DADBDD','#77dd77', (84,54))
        BACK3.update(PROZOR)
        BACK3.changeColor(score_mouse_poz)
        BACK3.update(PROZOR)
        for i in range (8):
            if score_i_profili[i][1]== "Napravi profil\n":
                pass
            else:
                tablica = font.render(str(i+1)+". "+ score_i_profili[i][1][:-1]+": "+score_i_profili[i][0],1,"Black")
                tablica_rect = tablica.get_rect(center=(630,100+i*60))
                PROZOR.blit(tablica,tablica_rect)
        pygame.display.update()
        clock.tick(FPS)
    for i in range (8):
        score[i] = score[i]+"\n"
        print (score)

def resetiranje_prije_igre(): # Resetira listu rectangleova prije svakog igranja
    global lista_rect_kvadrata_A, lista_rect_kvadrata_B, izrada_liste_A, izrada_liste_B, postavljen_kvadratA, postavljen_kvadratB, zapis_rezultata_jednom
    postavljen_kvadratA = False
    postavljen_kvadratB = False
    lista_rect_kvadrata_A = []
    lista_rect_kvadrata_B = []
    izrada_liste_A = True
    izrada_liste_B = True
    zapis_rezultata_jednom = True

def pauza_prije_promjene_igraca():  # Napravi pauzu od 3 sek između igrača
    TAJMER3 = pygame.image.load(os.path.join("potapanje brodova", "tajmer_3sec.png")).convert_alpha()
    TAJMER2 = pygame.image.load(os.path.join("potapanje brodova", "tajmer_2sec.png")).convert_alpha()
    TAJMER1 = pygame.image.load(os.path.join("potapanje brodova", "tajmer_1sec.png")).convert_alpha()
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
    global biranje_profila_bool
    global imenovanje_profila_bool
    global selektirani_profili
    zmaj = False
    resetiranje_prije_igre()
    selektirani_profili = [] 
    resetiranje_prije_igre()
    imenovanje_profila()
    if zmaj == True:
        return
    biranje_profila()
    if zmaj == True:
        return
    pp_run = True
    while pp_run == True:
        postavljanje_igracaA()
        if zmaj == True:
            pp_run == False
            break
        pauza_prije_promjene_igraca()
        resetiranje_prije_igre()
        postavljanje_igracaB()
        if zmaj == True:
            pp_run == False
            break
        rezultat_A_igrac = 17
        rezultat_B_igrac = 17
        run = True
        while run == True:
            pauza_prije_promjene_igraca()
            resetiranje_prije_igre()
            igranje_A_ekran()
            if zmaj == True:
                pp_run == False
                run = False
                break
            if rezultat_A_igrac == 0 or rezultat_B_igrac == 0:
                run = False
                break    
            pauza_prije_promjene_igraca()
            resetiranje_prije_igre()
            igranje_B_ekran()
            if zmaj == True:
                pp_run == False
                run = False
                break
            if rezultat_A_igrac == 0 or rezultat_B_igrac == 0:
                run = False
        if zmaj == True:
            pp_run = False
            break
        restart = False
        while restart == False:
            end_screen(rezultat_A_igrac,rezultat_B_igrac)
            if zmaj == True:
                pp_run == False
                run = False
                break
        lista_imena_kvadrata_A= []   
        lista_imena_kvadrata_B = [] 
        resetiranje_prije_igre()

def animacija_bombi():
    global bomba_index
    bomba_index += 0.12
    if bomba_index >= len(lista_bomba_animacija):
        bomba_index = 0
    bomba_surf = lista_bomba_animacija[int(bomba_index)]
    bomba_rect = bomba_surf.get_rect(topleft=(0,0))
    PROZOR.blit(bomba_surf, bomba_rect)

def animacija_broda():
    global brod_index
    brod_index += 0.09
    if brod_index >= len(lista_brod_animacija):
        brod_index = 0
    brod_surf = lista_brod_animacija[int(brod_index)]
    brod_rect = brod_surf.get_rect(topleft=(0,0))
    PROZOR.blit(brod_surf, brod_rect)

def animacija_more():
    global more_index
    more_index += 0.02
    if more_index >= len(lista_more_animacija):
        more_index = 0
    more_surf = lista_more_animacija[int(more_index)]
    more_rect = more_surf.get_rect(topleft=(0,0))
    PROZOR.blit(more_surf, more_rect)

def main():
    global zmaj
    tupi_zvuk = 1
    gumboslav = None
    PANORAMA = pygame.image.load(os.path.join("main_menu", "background.png" )).convert_alpha()
    PANORAMA_RECT = PANORAMA.get_rect(topleft=(0,0))
    NASLOV = pygame.image.load(os.path.join("main_menu", "naslov.png" )).convert_alpha()
    NASLOV_RECT = NASLOV.get_rect(topleft=(224,32))
    while True:
        zmaj = False
        PROZOR.fill('White')
        PROZOR.blit(PANORAMA, PANORAMA_RECT)
        animacija_bombi()
        PROZOR.blit(NASLOV, NASLOV_RECT)
        animacija_broda()
        animacija_more()
        PROZOR.blit(NASLOV, NASLOV_RECT)
        menu_mouse_poz = pygame.mouse.get_pos()
        GUMB_PLAY = Button(text_input = "Igraj", text_size = 30, text_color = 'Black', rect_width = 120, rect_height = 40, rect_color = '#DADBDD', hoveringRect_color = '#77dd77', pos = (640,250))
        GUMB_SCORE = Button(text_input = "Rezultati", text_size = 30, text_color = 'Black', rect_width = 120, rect_height = 40, rect_color = '#DADBDD', hoveringRect_color = '#77dd77', pos = (640,350))
        GUMB_EXIT = Button(text_input = "Izađi", text_size = 30, text_color = 'Black', rect_width = 80, rect_height = 40, rect_color = '#DADBDD', hoveringRect_color = '#D74B4B', pos = (640,450))
        MAIN_GUMBOVI_LISTA = {GUMB_PLAY: "GUMB_PLAY", GUMB_SCORE: "GUMB_SCORE", GUMB_EXIT: "GUMB_EXIT"}
        
        for gumb in [GUMB_PLAY, GUMB_SCORE, GUMB_EXIT]:
            gumb.changeColor(menu_mouse_poz)
            gumb.update(PROZOR)
            
            #Zvuk
            
            if gumb.checkForInput(menu_mouse_poz) == True and tupi_zvuk == 1:
                pygame.mixer.Sound.play(TUPI_GUMB_ZVUK)
                gumboslav = MAIN_GUMBOVI_LISTA.get(gumb)
                tupi_zvuk = 0
            elif MAIN_GUMBOVI_LISTA.get(gumb) == gumboslav and gumb.checkForInput(menu_mouse_poz) == False:
                tupi_zvuk = 1
                
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    esc_screen('Želiš li izaći iz igre?', PROZOR)
                    if zmaj == True:
                        pygame.mixer.Sound.play(EXIT_GUMB_ZVUK)
                        time.sleep(1.2)
                        pygame.quit()
                        sys.exit()
                    else: pass
            if event.type == MOUSEBUTTONDOWN:
                if GUMB_PLAY.checkForInput(menu_mouse_poz):
                    pygame.mixer.Sound.play(KLIK_GUMB_ZVUK)
                    play()
                if GUMB_SCORE.checkForInput(menu_mouse_poz):
                    pygame.mixer.Sound.play(KLIK_GUMB_ZVUK)
                    score_screen()
                if GUMB_EXIT.checkForInput(menu_mouse_poz):
                    esc_screen('Želiš li izaći iz igre?', PROZOR)
                    if zmaj == True:
                        pygame.mixer.Sound.play(EXIT_GUMB_ZVUK)
                        time.sleep(1.2)
                        pygame.quit()
                        sys.exit()
                    else: pass
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
