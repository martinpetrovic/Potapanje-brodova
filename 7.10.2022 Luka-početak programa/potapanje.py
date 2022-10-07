from ast import main
import pygame, sys
import os

pygame.init()

 
ŠIRINA, VISINA = 1280, 720
PROZOR = pygame.display.set_mode((ŠIRINA, VISINA))
pygame.display.set_caption("Potapanje brodova")
PROZOR.fill('White')

FONT = pygame.font.Font(None, 30)
FPS = 30


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
                #if self.name == 'Play':
                if self.name == 'Exit game':
                    #Možemo dodat da iskoči prozor i pita 'Are you sure you want to exit the game?'
                    pygame.quit()
                
                
                
              


def main():
    
    clock = pygame.time.Clock()
    run = True
    GUMB_PLAY = Button('Play',200,40,(ŠIRINA/2 - 100,200))
    GUMB_EXIT = Button('Exit game',200,40,(ŠIRINA/2 - 100,350))
    GUMB_SCORE = Button('View score',200,40,(ŠIRINA/2 - 100,275))
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        GUMB_PLAY.CrtajGumb()
        GUMB_SCORE.CrtajGumb()
        GUMB_EXIT.CrtajGumb()
        GUMB_EXIT.provjeri_klik()
        
    

    pygame.quit()



if __name__ == "__main__":
    main()

