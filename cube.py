import pygame
import constants as con

class Cube:
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=con.red):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
    
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
    
    def draw(self, frame, eyes=False):
        distance = self.w//self.rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(frame, self.color, 
        (i*distance+1, j*distance+1,
        distance-2, distance-2))
        if eyes:
            centre = distance//2
            radius = 3
            #центры глаз
            circleMiddle = (i*distance+centre-radius, j*distance+8)
            circleMiddle2 = (i*distance + distance - radius*2, j*distance+8)
            pygame.draw.circle(frame, con.black, circleMiddle, radius)
            pygame.draw.circle(frame, con.black, circleMiddle2, radius)