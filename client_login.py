import pygame
import os
from drawing_functions import text_in_box, textInPos
from constants import *

# client gui
class login_gui:
    def __init__(self):
        pass

    def draw(self, surface):
        lfont = pygame.font.Font('freesansbold.ttf',20)
        textInPos(surface, "Enter a password (remember this, it is used to reconnect if you get disconnected)", lfont, black, 100, 50)
        pygame.draw.rect(surface, black, [100, 100, 600, 100], 2)

        text_in_box(surface, "Connect", lfont, black, 100, 220, 100, 75)
        pygame.draw.rect(surface, black, [100, 220, 100, 75], 2)
            