import pygame
import time
from pygame.locals import *
import os
pygame.init()
pygame.mixer.init()
pygame.font.init()


LOGO = pygame.image.load(os.path.join("potapanje brodova", "MLKJR_LOGO.png" ))
INTRO = pygame.mixer.Sound(os.path.join("potapanje brodova", "INTRO.ogg"))
WHITE = (255, 255, 255)

screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sinking Ships")
FPS = 60

FONT=pygame.font.SysFont("Comic Sans MS", 50)
NASLOV = FONT.render("Sinking Ships", False,(0,0,0))

PLAY = FONT.render("Play", False,(0,0,0))
SCORE = FONT.render("Score", False,(0,0,0))

PLAYRECT = PLAY.get_rect(topleft =(880, 300))
SCORERECT = SCORE.get_rect(topleft = (860, 500))

#MOUSEPOSITION = pygame.mouse.get_pos

def LOADING_SCREEN():
    screen.fill(WHITE)
    screen.blit(LOGO,(250,0))
    pygame.mixer.Sound.play(INTRO)
    pygame.display.update()
    time.sleep(4)

def MENU():
    screen.fill(WHITE)
    #screen.blit(karlova slika brodića)
    screen.blit(NASLOV, (790, 100))
    screen.blit(PLAY, PLAYRECT)
    screen.blit(SCORE, SCORERECT)
    #pygame.mixer.Sound.play(neka background glazba
    pygame.display.update()





def main():
    clock = pygame.time.Clock()
    run = True
    LOADING_SCREEN()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            MENU()
            #if event.type == pygame.MOUSEBUTTONDOWN: in progress
            #    if event.button == 1: in progress
            #        if PLAYRECT.colliderect(MOUSEPOSITION)== 1: in progress
            #               run = False in progress

               
               
    pygame.quit

if __name__ == "__main__":
    main()