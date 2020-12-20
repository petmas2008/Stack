import pygame 
from pygame.locals import * 

winWidth=600
winHeight=480
color_CYAN=(0,255,255)

pygame.init()

caption="Image Test"
pygame.display.set_caption(caption)

Game_Window=pygame.display.set_mode((winWidth,winHeight))
Game_Window.fill(color_CYAN)

font1 = pygame.font.SysFont(None, 32)#normal font with size of 32;font design not specified.
text1=font1.render("Hello I am simple text", True,(255,0,0))#text color specified to red

while True:
    
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            exit()    
   
    Game_Window.blit(text1,(20,20))

    pygame.display.flip()