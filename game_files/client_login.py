import pygame
import os,sys
from drawing_functions import text_in_box, textInPos
from constants import *

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("./assets")

    return os.path.join(base_path, relative_path)

# client gui
class login_gui:
    def __init__(self):
        pass

    def draw(self, surface, failedConnect, changingName, changingIP):
        lfont = pygame.font.Font(resource_path("font.ttf"),20)

        textInPos(surface, "Enter your name (remember this, it is used to reconnect if you get disconnected)", lfont, black, 100, 50)
        pygame.draw.rect(surface, (255, 255, 255), [100, 100, 600, 100])
        pygame.draw.rect(surface, black, [100, 100, 600, 100], 2)
        if changingName:
            pygame.draw.rect(surface, blue, [105, 105, 590, 90], 2)

        textInPos(surface, "Enter IP of game host", lfont, black, 100, 220)
        pygame.draw.rect(surface, (255, 255, 255), [100, 250, 600, 100])
        pygame.draw.rect(surface, black, [100, 250, 600, 100], 2)
        if changingIP:
            pygame.draw.rect(surface, blue, [105, 255, 590, 90], 2)

        text_in_box(surface, "Connect", lfont, black, 100, 380, 100, 75)
        pygame.draw.rect(surface, black, [100, 380, 100, 75], 2)

        if failedConnect:
            textInPos(surface, "Failed to connect. Double check the IP.", lfont, red, 100, 355)
            