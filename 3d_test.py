import pygame
import time

pygame.init()

screen_width = 500
screen_height = 500

screen = pygame.display.set_mode([screen_width, screen_height])

def create_3D_rect(start_x, start_y, s_side, l_side, depth):
    #~ Draws the top of the rectangle
    px, py = start_x, start_y
    x, y = px+l_side, py-s_side
    pygame.draw.line(screen, (0, 0, 255), (px, py), (x, y))
    px, py = x, y
    x, y = px+s_side, py+s_side
    pygame.draw.line(screen, (0, 0, 255), (px, py), (x, y))
    px, py = (start_x+l_side)+s_side, (start_y-s_side)+s_side
    x, y = x-l_side, y+s_side
    pygame.draw.line(screen, (0, 0, 255), (px, py), (x, y))
    px, py = px-l_side, py+s_side
    x, y = start_x, start_y
    pygame.draw.line(screen, (0, 0, 255), (px, py), (x, y))
    #~ Draws the stems going down from the corners
    px, py = x, y
    x, y = px, py+depth
    pygame.draw.line(screen, (0, 0, 255), (px, py), (x, y))
    px, py = x, y
    x, y = px+s_side, py+s_side
    pygame.draw.line(screen, (0, 0, 255), (px, py), (x, y))
    px, py = x, y
    x, y = px+l_side, py-s_side
    pygame.draw.line(screen, (0, 0, 255), (px, py), (x, y))
    px, py = start_x+s_side+l_side, start_y+depth+s_side-s_side
    x, y = px, py-depth
    pygame.draw.line(screen, (0, 0, 255), (px, py), (x, y))
    px, py = x-l_side, y+s_side
    x, y = px, py+depth
    pygame.draw.line(screen, (0, 0, 255), (px, py), (x, y))
    
def adjust_pos(x, y, direction):
    if direction == "SW":
        return x-4, y+4
    return x+4, y+4
    
x, y = 200, 200
count = 4
running = True
directions = ["SE", "SW"]

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill([255, 255, 255])
    
    create_3D_rect(x, y, 40, 200, 40)
    x, y = adjust_pos(x, y, directions[0])
    time.sleep(.05)
    pygame.display.flip()