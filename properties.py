import pygame
from drawing_functions import *
from constants import *
pygame.init()


class Property():                                                                

    def __init__(self,name,color,id,locx,locy,cost,x1,y1,x2,y2, rent, monopolyRent, buildCost, mortgage, set):           
        self.name = name
        self.color = color
        self.id = id
        self.type = PROPERTY

        self.locx = locx
        self.locy = locy

        self.cost = cost
        self.monopolyRent = monopolyRent
        self.buildCost = buildCost
        self.rent = rent  

        self.mortgage = mortgage
        self.isMortgaged = False
        self.set = set

        self.houses = 0
        self.owned = False
        self.owner = None

        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2


        self.row = "bottom"

        self.left = 0
        self.top = 0
        self.width = 0
        self.height = 0

        self.boxLeft = 0
        self.boxTop = 0
        self.boxWidth = 0
        self.boxHeight = 0

        self.houseCircles = [(), (), (), (), ()]
        self.circleRadius = 8

        self.textLength = 0
        self.textX = 0
        self.textY = 0
        self.textWidth = 0
        self.textHeight = 0

        # left column
        if self.locx == card_length/2:
            self.row = "left"

            self.boxLeft = 0.7*card_length
            self.boxTop = self.locy-card_breadth/2
            self.boxWidth = 0.3*card_length
            self.boxHeight = card_breadth

            self.left = 0
            self.top = self.locy-card_breadth/2
            self.width = card_length
            self.height = card_breadth

            self.houseCircles[0] = (self.boxLeft + self.boxWidth/2,self.boxTop + self.circleRadius + 2)
            self.houseCircles[1] = (self.boxLeft + self.boxWidth/2,self.boxTop + 3*self.circleRadius + 2)
            self.houseCircles[2] = (self.boxLeft + self.boxWidth/2,self.boxTop + 5*self.circleRadius + 2)
            self.houseCircles[3] = (self.boxLeft + self.boxWidth/2,self.boxTop + 7*self.circleRadius + 2)
            self.houseCircles[4] = (self.boxLeft + self.boxWidth/2 + 2, self.boxTop + self.boxHeight/2)
            self.textLength = 12
            self.textX = self.left
            self.textY = self.top
            self.textWidth = self.width - self.boxWidth
            self.textHeight = self.height

        # right column
        elif self.locx == display_height -  card_length/2:
            self.row = "right"

            self.boxLeft = display_height -  card_length
            self.boxTop = self.locy-card_breadth/2
            self.boxWidth = 0.3*card_length
            self.boxHeight = card_breadth

            self.left = display_height -  card_length
            self.top = self.locy-card_breadth/2
            self.width = card_length
            self.height = card_breadth

            self.houseCircles[0] = (self.boxLeft + self.boxWidth/2,self.boxTop + self.circleRadius + 2)
            self.houseCircles[1] = (self.boxLeft + self.boxWidth/2,self.boxTop + 3*self.circleRadius + 2)
            self.houseCircles[2] = (self.boxLeft + self.boxWidth/2,self.boxTop + 5*self.circleRadius + 2)
            self.houseCircles[3] = (self.boxLeft + self.boxWidth/2,self.boxTop + 7*self.circleRadius + 2)
            self.houseCircles[4] = (self.boxLeft + self.boxWidth/2 + 2, self.boxTop + self.boxHeight/2)
            self.textLength = 12
            self.textX = self.left + self.boxWidth
            self.textY = self.top
            self.textWidth = self.width - self.boxWidth
            self.textHeight = self.height

        # top row
        elif self.locy == card_length/2:
            self.row = "top"

            self.boxLeft = self.locx-card_breadth/2
            self.boxTop = 0.7*card_length
            self.boxWidth = card_breadth
            self.boxHeight = 0.3*card_length

            self.left = self.locx-card_breadth/2
            self.top = 0
            self.width = card_breadth
            self.height = card_length

            self.houseCircles[0] = (self.boxLeft + self.circleRadius + 2,self.boxTop + self.boxHeight/2)
            self.houseCircles[1] = (self.boxLeft + 3*self.circleRadius + 2,self.boxTop + self.boxHeight/2)
            self.houseCircles[2] = (self.boxLeft + 5*self.circleRadius + 2,self.boxTop + self.boxHeight/2)
            self.houseCircles[3] = (self.boxLeft + 7*self.circleRadius + 2,self.boxTop + self.boxHeight/2)
            self.houseCircles[4] = (self.boxLeft + self.boxWidth/2, self.boxTop + self.boxHeight/2 + 2)
            self.textLength = 12
            self.textX = self.left 
            self.textY = self.top
            self.textWidth = self.width
            self.textHeight = self.height - self.boxHeight

        # bottom row
        elif self.locy ==  display_height -  card_length/2:
            self.row = "top"

            self.boxLeft = self.locx-card_breadth/2
            self.boxTop = display_height -  card_length
            self.boxWidth = card_breadth
            self.boxHeight = 0.3*card_length

            self.left = self.locx-card_breadth/2
            self.top = display_height -  card_length
            self.width = card_breadth
            self.height = card_length

            self.houseCircles[0] = (self.boxLeft + self.circleRadius + 2,self.boxTop + self.boxHeight/2)
            self.houseCircles[1] = (self.boxLeft + 3*self.circleRadius + 2,self.boxTop + self.boxHeight/2)
            self.houseCircles[2] = (self.boxLeft + 5*self.circleRadius + 2,self.boxTop + self.boxHeight/2)
            self.houseCircles[3] = (self.boxLeft + 7*self.circleRadius + 2,self.boxTop + self.boxHeight/2)
            self.houseCircles[4] = (self.boxLeft + self.boxWidth/2, self.boxTop + self.boxHeight/2 + 2)
            self.textLength = 12
            self.textX = self.left 
            self.textY = self.top + self.boxHeight
            self.textWidth = self.width
            self.textHeight = self.height - self.boxHeight

    
    def onEnter(self, player, owner):        
        if owner is not None:
            # charge rent
            if player.id is not owner.id and not self.isMortgaged:
                owed = 0
                # does owner have all 3
                if all(x in owner.owned_properties for x in self.set):
                    # houses = 0 if no houses. rent[0] = base rent
                    # but for 3 properties, 2*base rent
                    # houses = 5 == hotel
                    if self.houses == 0:
                        owed = 2*self.rent[0]
                    else:
                        owed = self.rent[self.houses]
                else:
                    owed = self.rent[0]
                return {"type": PAYRENT, "amount": owed, "payto": owner.id}
            else:
                return {"type": NONE}
        else:
            if self.canBuy(player.money):
                return {"type": CANBUY, "value": True}
            else:
                return {"type": CANBUY, "value": False}

    def canBuy(self, money):
        if not self.owned:
            if money >= self.cost:
                return True
        return False
                        
    def draw(self, surface, name, owned, ownedSet, borderCol, mortgaged):                                      
        lfont = pygame.font.Font('freesansbold.ttf',10)

        surface.fill(self.color, rect = [self.boxLeft, self.boxTop, self.boxWidth, self.boxHeight])
        pygame.draw.rect(surface, black, [self.left, self.top, self.width, self.height], 1)
        if owned:
            pygame.draw.rect(surface, borderCol, [self.left, self.top, self.width, self.height], 3 if not ownedSet else 5)
        if mortgaged:
            pygame.draw.line(surface, (140, 0, 0), (self.left, self.top), (self.left + self.width, self.top + self.height), 3)
            pygame.draw.line(surface, (140, 0, 0), (self.left, self.top + self.height), (self.left + self.width, self.top), 3)

        chanceTextSplit(surface, name, self.textLength, 10, lfont, black, self.textX, self.textY, self.textWidth, self.textHeight)

        
    def drawHouses(self, surface, houses):
        if houses < 5:
            for i in range(houses):
                pygame.draw.circle(surface, green, self.houseCircles[i], self.circleRadius)
                pygame.draw.circle(surface, black, self.houseCircles[i], self.circleRadius, 1)
        if houses == 5:
            pygame.draw.circle(surface, red, self.houseCircles[4], 2*self.circleRadius)
            pygame.draw.circle(surface, black, self.houseCircles[4], 2*self.circleRadius, 1)

        

        
    def mortgageProperty(self, player):
        player.money += self.mortgage
        self.isMortgaged = True

    def unMortgageProperty(self, player):
        player.money -= int(1.1*self.mortgage) 
        self.isMortgaged = False

    def buildHouse(self, player, totalHouses, totalHotels):
        if self.houses <= 5:
            if self.houses == 4:
                if totalHotels > 0:
                    player.numHotels += 1
                    player.numHouses -= 4
                    player.money -= self.buildCost
                    self.houses += 1
                    return("hotel")
            else:
                if totalHouses > 0:
                    self.houses += 1
                    player.money -= self.buildCost
                    player.numHouses += 1
                    return("house")
        return(NONE)

    def mortgageHouse(self, player, totalHouses):
        if self.houses > 0:

            if self.houses == 5 and totalHouses >= 4:
                player.numHotels -= 1
                player.numHouses += 4
                self.houses -= 1
                player.money += int(self.buildCost/2)
                return("hotel")
            elif self.houses < 5:
                self.houses -= 1
                player.numHouses -= 1
                player.money += int(self.buildCost/2)
                return("house")

class special_cards():                        

    def __init__(self,name,id,cost,locx,locy,x1,y1,x2,y2, rent, mortgage, type, set):
        self.name = name
        self.id = id
        self.cost = cost
        self.rent = rent
        self.mortgage = mortgage
        self.type = type
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.locx = locx
        self.locy = locy

        self.houses = 0
        self.isMortgaged = False

        self.owner = None
        self.owned = False
        self.set = set
        self.textLength = 0
        self.textX = 0
        self.textY = 0
        self.textWidth = 0
        self.textHeight = 0
        self.buildCost = 0

        # left column
        if self.locx == card_length/2:
            self.row = "left"

            self.boxLeft = 0.7*card_length
            self.boxTop = self.locy-card_breadth/2
            self.boxWidth = 0.3*card_length
            self.boxHeight = card_breadth

            self.left = 0
            self.top = self.locy-card_breadth/2
            self.width = card_length
            self.height = card_breadth

            self.textLength = 12
            self.textX = self.left
            self.textY = self.top
            self.textWidth = self.width - self.boxWidth
            self.textHeight = self.height

        # right column
        elif self.locx == display_height -  card_length/2:
            self.row = "right"

            self.boxLeft = display_height -  card_length
            self.boxTop = self.locy-card_breadth/2
            self.boxWidth = 0.3*card_length
            self.boxHeight = card_breadth

            self.left = display_height -  card_length
            self.top = self.locy-card_breadth/2
            self.width = card_length
            self.height = card_breadth
            self.textLength = 12
            self.textX = self.left + self.boxWidth
            self.textY = self.top
            self.textWidth = self.width - self.boxWidth
            self.textHeight = self.height

        # top row
        elif self.locy == card_length/2:
            self.row = "top"

            self.boxLeft = self.locx-card_breadth/2
            self.boxTop = 0.7*card_length
            self.boxWidth = card_breadth
            self.boxHeight = 0.3*card_length

            self.left = self.locx-card_breadth/2
            self.top = 0
            self.width = card_breadth
            self.height = card_length

            self.textLength = 12
            self.textX = self.left 
            self.textY = self.top
            self.textWidth = self.width
            self.textHeight = self.height - self.boxHeight

        # bottom row
        elif self.locy ==  display_height -  card_length/2:
            self.row = "top"

            self.boxLeft = self.locx-card_breadth/2
            self.boxTop = display_height -  card_length
            self.boxWidth = card_breadth
            self.boxHeight = 0.3*card_length

            self.left = self.locx-card_breadth/2
            self.top = display_height -  card_length
            self.width = card_breadth
            self.height = card_length

            self.textLength = 12
            self.textX = self.left 
            self.textY = self.top + self.boxHeight
            self.textWidth = self.width
            self.textHeight = self.height - self.boxHeight

    def mortgageProperty(self, player):
        player.money += self.mortgage
        self.isMortgaged = True

    def unMortgageProperty(self, player):
        player.money -= int(1.1*self.mortgage) 
        self.isMortgaged = False

    def onEnter(self, player, owner, roll):        
        if owner is not None:
            # charge rent
            if player.id is not owner.id and not self.isMortgaged:
                owed = 0
                # does owner have in set
                if self.type == RAIL:
                    numRRs = sum(i in owner.owned_properties for i in self.set)
                    owed = self.rent[numRRs - 1]
                elif self.type == UTILITY:
                    if all(i in owner.owned_properties for i in self.set):
                        owed = 10 * roll
                    else:
                        owed = 4 * roll
                else:
                    owed = 0
                    
                return {"type": PAYRENT, "amount": owed, "payto": owner.id}
            else:
                return {"type": NONE}
        else:
            if self.canBuy(player.money):
                return {"type": CANBUY, "value": True}
            else:
                return {"type": CANBUY, "value": False}

    def canBuy(self, money):
        if not self.owned:
            if money >= self.cost:
                return True
        return False
        
    def draw(self, surface, name,  owned, ownedSet, borderCol, mortgaged):                                    
        lfont = pygame.font.Font('freesansbold.ttf',10)
    
        surface.fill(black, rect = [self.boxLeft, self.boxTop, self.boxWidth, self.boxHeight])
        pygame.draw.rect(surface, black, [self.left, self.top, self.width, self.height], 1)
        if owned:
            pygame.draw.rect(surface, borderCol, [self.left, self.top, self.width, self.height], 3 if not ownedSet else 5)
        if mortgaged:
            pygame.draw.line(surface, (140, 0, 0), (self.left, self.top), (self.left + self.width, self.top + self.height), 3)
            pygame.draw.line(surface, (140, 0, 0), (self.left, self.top + self.height), (self.left + self.width, self.top), 3)
        chanceTextSplit(surface, name, self.textLength, 10, lfont, black, self.textX, self.textY, self.textWidth, self.textHeight)
        
class extra_card():
    def __init__(self,name,id,type,locx,locy,x1,y1,x2,y2):
        self.name = name
        self.id = id
        self.type = type
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.locx = locx
        self.locy = locy
        self.owned = False
        self.owner = None
        self.set = []

        self.textLength = 0
        self.textX = 0
        self.textY = 0
        self.textWidth = 0
        self.textHeight = 0
        self.buildCost = 0

        # left column
        if self.locx == card_length/2:
            self.row = "left"

            self.boxLeft = 0.7*card_length
            self.boxTop = self.locy-card_breadth/2
            self.boxWidth = 0.3*card_length
            self.boxHeight = card_breadth

            self.left = 0
            self.top = self.locy-card_breadth/2
            self.width = card_length
            self.height = card_breadth

            self.textLength = 12
            self.textX = self.left
            self.textY = self.top
            self.textWidth = self.width - self.boxWidth
            self.textHeight = self.height

        # right column
        elif self.locx == display_height -  card_length/2:
            self.row = "right"

            self.boxLeft = display_height -  card_length
            self.boxTop = self.locy-card_breadth/2
            self.boxWidth = 0.3*card_length
            self.boxHeight = card_breadth

            self.left = display_height -  card_length
            self.top = self.locy-card_breadth/2
            self.width = card_length
            self.height = card_breadth
            self.textLength = 12
            self.textX = self.left + self.boxWidth
            self.textY = self.top
            self.textWidth = self.width - self.boxWidth
            self.textHeight = self.height

        # top row
        elif self.locy == card_length/2:
            self.row = "top"

            self.boxLeft = self.locx-card_breadth/2
            self.boxTop = 0.7*card_length
            self.boxWidth = card_breadth
            self.boxHeight = 0.3*card_length

            self.left = self.locx-card_breadth/2
            self.top = 0
            self.width = card_breadth
            self.height = card_length

            self.textLength = 12
            self.textX = self.left 
            self.textY = self.top
            self.textWidth = self.width
            self.textHeight = self.height - self.boxHeight

        # bottom row
        elif self.locy ==  display_height -  card_length/2:
            self.row = "top"

            self.boxLeft = self.locx-card_breadth/2
            self.boxTop = display_height -  card_length
            self.boxWidth = card_breadth
            self.boxHeight = 0.3*card_length

            self.left = self.locx-card_breadth/2
            self.top = display_height -  card_length
            self.width = card_breadth
            self.height = card_length

            self.textLength = 12
            self.textX = self.left 
            self.textY = self.top + self.boxHeight
            self.textWidth = self.width
            self.textHeight = self.height - self.boxHeight

        if self.id == 0:
            self.width = card_length
            self.height = card_length
            self.textWidth = card_length
        if self.id == 10:
            self.left = 0
            self.width = card_length
            self.height = card_length
            self.textX = 0
            self.textWidth = card_length
            self.locx -= self.width/4
            self.locy += self.height/6
        if self.id == 20:
            self.top = 0
            self.width = card_length
            self.height = card_length
            self.textWidth = card_length
        if self.id == 30:
            self.width = card_length
            self.height = card_length
            #self.textX = self.left
            self.textWidth = card_length

        if self.id == 40:
            self.height = self.height / 2
            self.textY = self.top
            self.textHeight = self.textHeight / 2
            self.locy -= self.height /4


    def onEnter(self, player, owner):
        return {"type": self.type}

    def canBuy(self, money):
        return False
        
    def draw(self, surface, name, owned, ownedSet, borderCol, mortgaged):
        lfont = pygame.font.Font('freesansbold.ttf',10)
    
        pygame.draw.rect(surface, black, [self.left, self.top, self.width, self.height], 1)
        chanceTextSplit(surface, name, self.textLength, 10, lfont, black, self.textX, self.textY, self.textWidth, self.textHeight)

