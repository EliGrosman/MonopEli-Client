import pygame
import os,sys
from property_info import properties
from drawing_functions import drawPlayerStuff, drawActions, drawButtons, textInPos
from constants import *

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("./assets")

    return os.path.join(base_path, relative_path)

class Grid:
    def __init__(self):
        self.properties = properties

    def draw(self, surface, players, properties_server, actions, turn, canEnd, myId, houseData, totalHouses, totalHotels, mortgageData):
        lfont = pygame.font.Font(resource_path("font.ttf"), 20)

        # draw each property
        for property in self.properties:
            if len(properties_server) == 0:
                propName = ""
            else:
                propName = properties_server[property.id]["name"]
            owned = False
            ownedSet = False
            borderCol = (0, 0, 0)
            if actions["turn"] > 0:
                for player in players:
                    player_properties = player["owned_properties"]     
                    if property.id in player_properties:
                        owned = True
                        borderCol = player["color"]
                    if all(x in player_properties for x in property.set):
                        ownedSet = True
            property.draw(surface, propName, owned, ownedSet, borderCol, property.id in mortgageData)
        # draw houses on each property
        for housedata in houseData:
            property = self.properties[housedata["id"]]
            if property.type == PROPERTY:
                property.drawHouses(surface, housedata["houses"])
        # draw player stuff on right side
        for player in players:
            pygame.draw.circle(surface, player['color'],[(int)(player['locx']) + (player['player']-1) * 10,(int)(player['locy'])],10)
            if len(properties_server) > 0:
                jailname = properties_server[40]['name']
            else:
                jailname = ""
            drawPlayerStuff(surface, player, myId, mortgageData, jailname)
        # draw actions
        if actions["roll1"] != 0:
            drawActions(surface, actions["turn"], actions["player"], actions["roll1"], actions["roll2"], actions["landedon"], actions["lines"])

        # draw amount of house/hotesl left
        textInPos(surface, "Houses left: " + str(totalHouses), lfont, black, 2*card_breadth , card_length + 5)
        textInPos(surface, "Hotels left: " + str(totalHotels), lfont, black, 2*card_breadth , card_length + 25)
        # draw roll/end turn buttons
  
        drawButtons(surface, turn, canEnd)
            