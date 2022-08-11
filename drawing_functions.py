from constants import *
import pygame
import json

text_height = .15*card_length
box_width = 3*card_breadth

# draw text in the middle of a box given by x, y, length, and height of box
def text_in_box(surface, text, font,tc,x,y,l,h):             
    textSurface = font.render(text, True, tc)
    textRect = textSurface.get_rect()
    textRect.center = (x+l/2,y+h/2)
    surface.blit(textSurface, textRect)

# draw text at x, y 
def textInPos(surface, text, font, col, x, y):
    textSurface = font.render(text, True, col)
    textRect = textSurface.get_rect()
    textRect.left = x
    textRect.top = y
    surface.blit(textSurface, textRect)

def mouseInBox(mouse, left, top, width, height):
    if mouse[0] >= left and mouse[0] <= left + width and mouse[1] >= top and mouse[1] <= top + height:
        return True
    return False

# fits long text into a box. Used for chance/chest window and also drawing property names on the board
def chanceTextSplit(surface, text, maxLineLength, sep, font, tc, x, y, l, h):
    splitLines = text.split(' ')
    # print(splitLines)
    lines = []

    if len(splitLines) == 1:
        lines.append(splitLines[0])
    
    cur = splitLines[0]
    del splitLines[0]

    while len(splitLines) > 0:
        next = splitLines[0]
        del splitLines[0]
        if len(splitLines) == 0:
            if len(cur + " " + next) < maxLineLength:
                lines.append(cur + " " + next)
            else:
                lines.append(cur)
                lines.append(next)
            
        elif len(cur + " " + next) < maxLineLength:
            cur = cur + " " + next
        else:
            lines.append(cur)
            cur = next   
    y -= (len(lines)*sep)/4 
    for i in range(len(lines)):
        line = lines[i]

        text_in_box(surface, line, font,tc,x,y+i*sep,l,h)
# darw card in the top right
def drawCard(surface, property, chanceText):
    lfont = pygame.font.Font('freesansbold.ttf',10)
    

    if(property.type == PROPERTY):
        surface.fill(property.color, rect = [13*card_breadth, 0, box_width, .25*card_length])
        pygame.draw.rect(surface, black, [13*card_breadth, 0, box_width, 2*card_length], 2)
        text_in_box(surface, property.name, lfont, black, 13*card_breadth, 0, box_width, .25*card_length)
        text_in_box(surface, f"Cost: ${property.cost}", lfont, black, 13*card_breadth, .3*card_length, box_width, text_height)
        text_in_box(surface, f"Rent: ${property.rent[0]}", lfont, black, 13*card_breadth, .3*card_length+20, box_width, text_height)
        text_in_box(surface, f"Rent with color set: ${property.monopolyRent}", lfont, black, 13*card_breadth, .4*card_length+20, box_width, text_height)

        text_in_box(surface, f"With 1 house: {' '*(21-len(str(property.rent[1])))}${property.rent[1]}", lfont, black, 13*card_breadth, .6*card_length+20, box_width, text_height)
        text_in_box(surface, f"With 2 houses: {' '*(19-len(str(property.rent[2])))}${property.rent[2]}", lfont, black, 13*card_breadth, .7*card_length+20, box_width, text_height)
        text_in_box(surface, f"With 3 houses: {' '*(19-len(str(property.rent[3])))}${property.rent[3]}", lfont, black, 13*card_breadth, .8*card_length+20, box_width, text_height)
        text_in_box(surface, f"With 1 hotel: {' '*(23-len(str(property.rent[4])))}${property.rent[4]}", lfont, black, 13*card_breadth, .9*card_length+20, box_width, text_height)
        text_in_box(surface, f"Mortgage value: ${property.mortgage}", lfont, black, 13*card_breadth, 1.3*card_length+20, box_width, text_height)
        text_in_box(surface, f"Houses cost: ${property.buildCost} each", lfont, black, 13*card_breadth, 1.5*card_length+20, box_width, text_height)
        text_in_box(surface, f"Hotels, ${property.buildCost} plus 4 houses", lfont, black, 13*card_breadth, 1.7*card_length+20, box_width, text_height)
    if(property.type == RAIL):
        surface.fill(black, rect = [13*card_breadth, 0, box_width, .25*card_length])
        pygame.draw.rect(surface, black, [13*card_breadth, 0, box_width, 2*card_length], 2)
        text_in_box(surface, property.name, lfont, (255, 255, 255), 13*card_breadth, 0, box_width, .25*card_length)
        text_in_box(surface, f"Cost: ${property.cost}", lfont, black, 13*card_breadth, .3*card_length, box_width, text_height)
        text_in_box(surface, f"Rent: {' '*(43-len(str(property.rent[0])))}${property.rent[0]}", lfont, black, 13*card_breadth, .3*card_length+20, box_width, text_height)
        text_in_box(surface, f"If 2 R.R's are owned: {' '*(18-len(str(property.rent[1])))}${property.rent[1]}", lfont, black, 13*card_breadth, .5*card_length+20, box_width, text_height)
        text_in_box(surface, f"If 3 R.R's are owned: {' '*(18-len(str(property.rent[2])))}${property.rent[2]}", lfont, black, 13*card_breadth, .7*card_length+20, box_width, text_height)
        text_in_box(surface, f"If 4 R.R's are owned: {' '*(18-len(str(property.rent[3])))}${property.rent[3]}", lfont, black, 13*card_breadth, .9*card_length+20, box_width, text_height)
        text_in_box(surface, f"Mortgage value: ${property.mortgage}", lfont, black, 13*card_breadth, 1.3*card_length+20, box_width, text_height)
    if(property.type == UTILITY):
        surface.fill(black, rect = [13*card_breadth, 0, box_width, .25*card_length])
        pygame.draw.rect(surface, black, [13*card_breadth, 0, box_width, 2*card_length], 2)
        text_in_box(surface, property.name, lfont, (255, 255, 255), 13*card_breadth, 0, box_width, .25*card_length)
        text_in_box(surface, f"Cost: ${property.cost}", lfont, black, 13*card_breadth, .3*card_length, box_width, text_height)
        text_in_box(surface, f"If one 'Utility' is owned, rent is", lfont, black, 13*card_breadth, .3*card_length+20, box_width, text_height)
        text_in_box(surface, f"4 times ammount shown on dice", lfont, black, 13*card_breadth, .4*card_length+20, box_width, text_height)
        
        text_in_box(surface, f"If both 'Utilities' are owned, rent", lfont, black, 13*card_breadth, .7*card_length+20, box_width, text_height)
        text_in_box(surface, f"is 10 times amount shown on dice", lfont, black, 13*card_breadth, .8*card_length+20, box_width, text_height)

        text_in_box(surface, f"Mortgage value: ${property.mortgage}", lfont, black, 13*card_breadth, 1.3*card_length+20, box_width, text_height)     

# draw chance/chest card the player landed on in the middle
def drawChanceCommunity(surface, cardType, chanceText, playerId, chancePlayer):
    lfont = pygame.font.Font('freesansbold.ttf',10)

    pygame.draw.rect(surface, (255, 255, 255), [buttonWindowLeft, buttonWindowTop + buttonWindowLength+ 1.5*card_length, buttonWindowWidth, buttonWindowLength])
    pygame.draw.rect(surface, black, [buttonWindowLeft, buttonWindowTop  +buttonWindowLength+1.5*card_length, buttonWindowWidth, buttonWindowLength], 2)

    if playerId == chancePlayer:
        text_in_box(surface, "You drew a " + cardType + " card", lfont, black, buttonWindowLeft, buttonWindowTop + buttonWindowLength + 1.5*card_length - 50, buttonWindowWidth, buttonWindowLength)

        pygame.draw.rect(surface, black, [buttonWindowLeft + 15, buttonWindowTop +buttonWindowLength+ 2.18*card_length, buttonWindowWidth - 30, buttonHeight/3], 2)
        text_in_box(surface, "Accept", lfont, black, buttonWindowLeft + 15, buttonWindowTop +buttonWindowLength+ 2.18*card_length, buttonWindowWidth - 30, buttonHeight/3)
    else:
        text_in_box(surface, "Player " + str(chancePlayer) + " drew a " + cardType + " card", lfont, black, buttonWindowLeft, buttonWindowTop +buttonWindowLength+ 1.5*card_length - 50, buttonWindowWidth, buttonWindowLength)
    
    chanceTextSplit(surface, chanceText, 45, 10, lfont, black, buttonWindowLeft, buttonWindowTop + buttonWindowLength + 1.5*card_length - 20, buttonWindowWidth, buttonWindowLength)

# draw how much the player owes
def drawOwedWindow(surface, totalOwed):
    lfont = pygame.font.Font('freesansbold.ttf',10)

    pygame.draw.rect(surface, (255, 255, 255), [buttonWindowLeft, buttonWindowTop + buttonWindowLength+ 1.5*card_length, buttonWindowWidth, buttonWindowLength])
    pygame.draw.rect(surface, black, [buttonWindowLeft, buttonWindowTop  +buttonWindowLength+1.5*card_length, buttonWindowWidth, buttonWindowLength], 2)

    text_in_box(surface, "You owe " + str(totalOwed), lfont, black, buttonWindowLeft, buttonWindowTop + buttonWindowLength + 1.5*card_length - 50, buttonWindowWidth, buttonWindowLength)

    pygame.draw.rect(surface, black, [buttonWindowLeft + 15, buttonWindowTop +buttonWindowLength+ 2.18*card_length, buttonWindowWidth - 30, buttonHeight/3], 2)
    text_in_box(surface, "Accept", lfont, black, buttonWindowLeft + 15, buttonWindowTop +buttonWindowLength+ 2.18*card_length, buttonWindowWidth - 30, buttonHeight/3)

# draw jail window. Pay to get out, use jail card
def drawJailWindow(surface, jailCards):
    lfont = pygame.font.Font('freesansbold.ttf',10)

    pygame.draw.rect(surface, (255, 255, 255), [buttonWindowLeft, buttonWindowTop + buttonWindowLength+ 1.5*card_length, buttonWindowWidth, buttonWindowLength])
    pygame.draw.rect(surface, black, [buttonWindowLeft, buttonWindowTop  +buttonWindowLength+1.5*card_length, buttonWindowWidth, buttonWindowLength], 2)

    text_in_box(surface, "Pay $50 to get out of jail?", lfont, black, buttonWindowLeft, buttonWindowTop + buttonWindowLength + 1.5*card_length - 50, buttonWindowWidth, buttonWindowLength)

    pygame.draw.rect(surface, black, [buttonWindowLeft + 5, buttonWindowTop +buttonWindowLength+ 2.18*card_length, buttonWidth, buttonHeight/3], 2)
    text_in_box(surface, "Accept", lfont, black, buttonWindowLeft + 5, buttonWindowTop +buttonWindowLength+ 2.18*card_length, buttonWidth, buttonHeight/3)

    pygame.draw.rect(surface, black, [buttonWindowLeft + 5 + buttonWidth + 20, buttonWindowTop +buttonWindowLength+ 2.18*card_length, buttonWidth, buttonHeight/3], 2)
    text_in_box(surface, "Use get out of jail card" if jailCards > 0 else "No get out of jail cards", lfont, black, buttonWindowLeft + 5 + buttonWidth + 20, buttonWindowTop +buttonWindowLength+ 2.18*card_length, buttonWidth, buttonHeight/3)

# draw player name, money, jail cards, and properties on the right side of the screen
def drawPlayerStuff(surface, player, myId, mortgagedProperties):
    lfont = pygame.font.Font('freesansbold.ttf', 20)
    lfont_small = pygame.font.Font('freesansbold.ttf', 15)

    if(player["player"] == 1):
        left = 13*card_breadth
        top = 2*card_length + 15
        width = 4*card_breadth
        height = 1.8*card_length
    elif(player["player"] == 2):
        left = 13*card_breadth + 4*card_breadth + 15
        top = 2*card_length + 15
        width = 4*card_breadth
        height = 1.8*card_length
    elif(player["player"] == 3):
        left = 13*card_breadth
        top = 2*card_length + 1.8*card_length + 30
        width = 4*card_breadth
        height = 1.8*card_length
    elif(player["player"] == 4):
        left = 13*card_breadth + 4*card_breadth + 15
        top = 2*card_length + 1.8*card_length + 30
        width = 4*card_breadth
        height = 1.8*card_length
    
    pygame.draw.rect(surface, black, [left, top, width, height], 2)
    pygame.draw.circle(surface, player["color"], (left + 15, top + 15), 10)
    textInPos(surface, str(player["name"]), lfont, black, left + 25, top + 7.5)
    textInPos(surface, "Balance: " + str(player["money"]), lfont, black, left + 5, top + 25)
    textInPos(surface, "Get out of jail cards: " + str(player["jailCards"]), lfont_small, black, left + 5, top + 42)

    if player["player"] == myId:
        pygame.draw.rect(surface, black, [left + 5, top + 55, 1.3*buttonWidth, buttonHeight-10], 2)
        text_in_box(surface, "Declare Bankruptcy", lfont_small, black, left + 5, top + 55, 1.3*buttonWidth, buttonHeight-10)
    else:
        pygame.draw.rect(surface, black, [left + 5, top + 55, 1.3*buttonWidth, buttonHeight-10], 2)
        text_in_box(surface, "Trade", lfont, black, left + 5, top +55, 1.3*buttonWidth, buttonHeight-10)

    miniBoxWidth = 23

    if player["bankrupt"]:
        text_in_box(surface, "Bankrupt!", lfont, black, left + 5, top + 15 + buttonHeight + 10, width, buttonHeight)
    else:
        drawPlayerProperties(surface, player["owned_properties"], mortgagedProperties, left + 25, top + 2*card_length - 10, miniBoxWidth, [], [-1, -1])

def drawPlayerProperties(surface, playerProperties, mortgagedProperties, left, top, miniBoxWidth, selected, mouse):
    clicked = None
    d = [ [1, 3], [6, 8, 9], [11, 13, 14], [16, 18, 19], [21, 23, 24], [26, 27, 29], [31, 32, 34], [37, 39], [5, 15, 25, 35], [12, 28]]
    colors = [brown, lightblue, magenta, orange, red, yellow, green, blue, black, (166, 166, 166)]
    for x in range(len(d)):
        for y in range(len(d[x])):
            id = d[x][y]
            col = colors[x]
            if id in playerProperties:
                pygame.draw.rect(surface, col, [left + x*miniBoxWidth, top - (2+y)*miniBoxWidth, miniBoxWidth, miniBoxWidth])
                if id in mortgagedProperties:
                    pygame.draw.line(surface, (140, 0, 0), (left + x*miniBoxWidth, top - (2+y)*miniBoxWidth), (left + x*miniBoxWidth + miniBoxWidth, top - (2+y)*miniBoxWidth + miniBoxWidth), 2)
                    pygame.draw.line(surface, (140, 0, 0), (left + x*miniBoxWidth, top - (2+y)*miniBoxWidth + miniBoxWidth), (left + x*miniBoxWidth + miniBoxWidth, top - (2+y)*miniBoxWidth), 2)
            pygame.draw.rect(surface, black if id not in selected else red, [left + x*miniBoxWidth, top - (2+y)*miniBoxWidth, miniBoxWidth, miniBoxWidth], 1 if id not in selected else 2)
            if mouseInBox(mouse, left + x*miniBoxWidth, top - (2+y)*miniBoxWidth, miniBoxWidth, miniBoxWidth): clicked = id
    

    return clicked

#  draw turn/past actions in the top right
def drawActions(surface, turnNum, playerName, roll1, roll2, landedOn, lines):
    lfont = pygame.font.Font('freesansbold.ttf',20)
    lfont15 = pygame.font.Font('freesansbold.ttf', 15)
    left = 13*card_breadth + box_width + 15
    top = 0
    width = 5*card_breadth
    height = 2*card_length

    pygame.draw.rect(surface, black, [left, top, width, height], 2)
    textInPos(surface, "Turn: " + str(turnNum), lfont, black, left + 5, top + 5)
    textInPos(surface, str(playerName) + " rolls " + str(roll1) + ", " + str(roll2), lfont, black, left + 5, top + 25)

    pygame.draw.line(surface, black, (left, top + 50), (left + width - 2, top + 50))

    textInPos(surface, "Landed on " + landedOn, lfont15, black, left + 5, top + 55)

    for i in range(len(lines)):
        textInPos(surface, lines[i], lfont15, black, left + 5, top + 55 + 25*(i+1))

# draw game over and winner name
def drawGameOver(surface, winner):
    lfont = pygame.font.Font('freesansbold.ttf',50)
    pygame.draw.rect(surface, (255, 255, 255), [buttonWindowLeft, buttonWindowTop, buttonWindowWidth + 5, buttonWindowLength + 5])
    text_in_box(surface, "Game Over!", lfont, black, buttonWindowLeft, buttonWindowTop, buttonWindowWidth, buttonWindowLength)
    text_in_box(surface, "Winner: " + str(winner), lfont, black, buttonWindowLeft, buttonWindowTop + 45, buttonWindowWidth, buttonWindowLength)

# draw window for buying property they landed on
def drawBuyWindow(surface, propname, cost):
    if propname is not None:
        lfont = pygame.font.Font('freesansbold.ttf',25)
        pygame.draw.rect(surface, (255, 255, 255), [buttonWindowLeft, buttonWindowTop + 1.5*card_length, buttonWindowWidth, buttonWindowLength])
        pygame.draw.rect(surface, black, [buttonWindowLeft, buttonWindowTop + 1.5*card_length, buttonWindowWidth, buttonWindowLength], 2)
        text_in_box(surface, "Would you like to buy", lfont, black, buttonWindowLeft, buttonWindowTop + 1.5*card_length - 40, buttonWindowWidth, buttonWindowLength)
        text_in_box(surface, propname, lfont, black, buttonWindowLeft, buttonWindowTop + 1.5*card_length - 15, buttonWindowWidth, buttonWindowLength)
        text_in_box(surface, "For $" + str(cost) + "?", lfont, black, buttonWindowLeft, buttonWindowTop + 1.5*card_length + 10, buttonWindowWidth, buttonWindowLength)

        pygame.draw.rect(surface, black, [buttonWindowLeft + 5, buttonWindowTop + 2.18*card_length, buttonWidth, buttonHeight/3], 2)
        text_in_box(surface, "Yes", lfont, black, buttonWindowLeft + 5, buttonWindowTop + 2.18*card_length, buttonWidth, buttonHeight/3)

        pygame.draw.rect(surface, black, [buttonWindowLeft + 5 + buttonWidth + 20, buttonWindowTop + 2.18*card_length, buttonWidth, buttonHeight/3], 2)
        text_in_box(surface, "No", lfont, black, buttonWindowLeft + 5 + buttonWidth + 20, buttonWindowTop + 2.18*card_length, buttonWidth, buttonHeight/3)

# confirm declare bankruptcy
def drawBankruptcyWindow(surface):
    lfont = pygame.font.Font('freesansbold.ttf',23)
    pygame.draw.rect(surface, (255, 255, 255), [buttonWindowLeft, buttonWindowTop + 1.5*card_length, buttonWindowWidth, buttonWindowLength])
    pygame.draw.rect(surface, black, [buttonWindowLeft, buttonWindowTop + 1.5*card_length, buttonWindowWidth, buttonWindowLength], 2)
    text_in_box(surface, "Are you sure you want", lfont, black, buttonWindowLeft, buttonWindowTop + 1.5*card_length - 40, buttonWindowWidth, buttonWindowLength)
    text_in_box(surface, "To declare bankruptcy?", lfont, black, buttonWindowLeft, buttonWindowTop + 1.5*card_length - 15, buttonWindowWidth, buttonWindowLength)

    pygame.draw.rect(surface, black, [buttonWindowLeft + 5, buttonWindowTop + 2.18*card_length, buttonWidth, buttonHeight/3], 2)
    text_in_box(surface, "Yes", lfont, black, buttonWindowLeft + 5, buttonWindowTop + 2.18*card_length, buttonWidth, buttonHeight/3)

    pygame.draw.rect(surface, black, [buttonWindowLeft + 5 + buttonWidth + 20, buttonWindowTop + 2.18*card_length, buttonWidth, buttonHeight/3], 2)
    text_in_box(surface, "No", lfont, black, buttonWindowLeft + 5 + buttonWidth + 20, buttonWindowTop + 2.18*card_length, buttonWidth, buttonHeight/3)

def drawTradeWindowThirdParty(surface, tradeData, p1Money, p2Money, mortgagedProperties):
    player1 = tradeData["p1name"]
    properties1 = tradeData["properties1"]
    selectedProperties1 = tradeData["selectedProperties1"]
    money1 = tradeData["money1"]

    player2 = tradeData["p2name"]
    properties2 = tradeData["properties2"]
    selectedProperties2 = tradeData["selectedProperties2"]
    money2 = tradeData["money2"]

    money = [str(money1), str(money2)]
    currentMoney = [p1Money, p2Money]

    lfont = pygame.font.Font('freesansbold.ttf',25)
    lfont2 = pygame.font.Font('freesansbold.ttf',18)
    pygame.draw.rect(surface, (255, 255, 255), [card_length + 20, buttonWindowTop + 1.5*card_length, 1.87*buttonWindowWidth, 2.8*buttonWindowLength])
    pygame.draw.rect(surface, black, [card_length + 20, buttonWindowTop + 1.5*card_length, 1.87*buttonWindowWidth, 2.8*buttonWindowLength], 2)
    miniBoxWidth = 23
    
    text_in_box(surface, str(player1) + " is trading with " + str(player2), lfont, black, card_length + 20, buttonWindowTop + 1.5*card_length, 1.87*buttonWindowWidth, 50)

    text_in_box(surface, str(player1), lfont, black, card_length + 30, buttonWindowTop + 2*card_length, miniBoxWidth*10, 50)
    textInPos(surface, "Money: ", lfont2, black, card_length + 30, buttonWindowTop + 2*card_length + 50)
    textInPos(surface, "$" + str(money1), lfont2, black, 1.75*card_length , buttonWindowTop + 2*card_length + 50)
    drawPlayerProperties(surface, properties1, mortgagedProperties, card_length + 30, buttonWindowTop + 3.5*card_length, miniBoxWidth, selectedProperties1, [-1, -1])

    text_in_box(surface, str(player2), lfont, black, card_length + 368, buttonWindowTop + 2*card_length, miniBoxWidth * 10, 50)
    textInPos(surface, "Money: ", lfont2, black, card_length + 368, buttonWindowTop + 2*card_length + 50)
    textInPos(surface, "$" + str(money2), lfont2, black, 1.5*card_length+ 370, buttonWindowTop + 2*card_length + 50)
    drawPlayerProperties(surface, properties2, mortgagedProperties, card_length + 368, buttonWindowTop + 3.5*card_length, miniBoxWidth, selectedProperties2, [-1, -1])

# trade window
def drawTradeWindow(surface, tradeData, myId, p1Money, p2Money, sock, mortgagedProperties):
    p1id = tradeData["player1"]
    player1 = tradeData["p1name"]
    properties1 = tradeData["properties1"]
    selectedProperties1 = tradeData["selectedProperties1"]
    money1 = tradeData["money1"]

    p2id = tradeData["player2"]
    player2 = tradeData["p2name"]
    properties2 = tradeData["properties2"]
    selectedProperties2 = tradeData["selectedProperties2"]
    money2 = tradeData["money2"]

    money = [str(money1), str(money2)]
    currentMoney = [p1Money, p2Money]

    lfont = pygame.font.Font('freesansbold.ttf',25)
    lfont2 = pygame.font.Font('freesansbold.ttf',18)
    pygame.draw.rect(surface, (255, 255, 255), [card_length + 20, buttonWindowTop + 1.5*card_length, 1.87*buttonWindowWidth, 2.8*buttonWindowLength])
    pygame.draw.rect(surface, black, [card_length + 20, buttonWindowTop + 1.5*card_length, 1.87*buttonWindowWidth, 2.8*buttonWindowLength], 2)
    miniBoxWidth = 23

    if myId == p1id:
        done = False
        playerChanging = None
        
        text_in_box(surface, "Trading with " + str(player2), lfont, black, card_length + 20, buttonWindowTop + 1.5*card_length, 1.87*buttonWindowWidth, 50)

        text_in_box(surface, "You", lfont, black, card_length + 30, buttonWindowTop + 2*card_length, miniBoxWidth*10, 50)
        textInPos(surface, "Money: ", lfont2, black, card_length + 30, buttonWindowTop + 2*card_length + 50)

        pygame.draw.rect(surface, black, [1.75*card_length , buttonWindowTop + 2*card_length + 47.5, miniBoxWidth*3, miniBoxWidth], 1)
        textInPos(surface, "$" + money[0], lfont2, black, 1.75*card_length , buttonWindowTop + 2*card_length + 50)
        drawPlayerProperties(surface, properties1, mortgagedProperties, card_length + 30, buttonWindowTop + 3.5*card_length, miniBoxWidth, selectedProperties1, [-1, -1])

        text_in_box(surface, "Them", lfont, black, card_length + 368, buttonWindowTop + 2*card_length, miniBoxWidth * 10, 50)
        textInPos(surface, "Money: ", lfont2, black, card_length + 368, buttonWindowTop + 2*card_length + 50)

        pygame.draw.rect(surface, black, [1.5*card_length + 370 , buttonWindowTop + 2*card_length + 47.5, miniBoxWidth*3, miniBoxWidth], 1)
        textInPos(surface, "$" + money[1], lfont2, black, 1.5*card_length+ 370, buttonWindowTop + 2*card_length + 50)
        drawPlayerProperties(surface, properties2, mortgagedProperties, card_length + 368, buttonWindowTop + 3.5*card_length, miniBoxWidth, selectedProperties2, [-1, -1])

        if tradeData['type'] != "tradeSend":
            pygame.draw.rect(surface, black, [card_length + 30, buttonWindowTop + 3.5*card_length, 2*buttonWidth, buttonHeight/3], 2)
            text_in_box(surface, "Send offer", lfont, black, card_length + 30, buttonWindowTop + 3.5*card_length, 2*buttonWidth, buttonHeight/3)

            pygame.draw.rect(surface, black, [card_length + 30 + 2*buttonWidth + 10, buttonWindowTop + 3.5*card_length, 2*buttonWidth, buttonHeight/3], 2)
            text_in_box(surface, "Cancel", lfont, black, card_length + 30 + 2*buttonWidth + 10, buttonWindowTop + 3.5*card_length, 2*buttonWidth, buttonHeight/3)
        else:
            done = True

        while not done:
            mouse = [-1, -1]
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    mouse = pygame.mouse.get_pos()
                    # change player 1 money
                    if mouseInBox(mouse, 1.75*card_length, buttonWindowTop + 2*card_length + 47.5, miniBoxWidth*3, miniBoxWidth):
                        playerChanging = 0
                        money[playerChanging] = ""
                    # change player 2 money
                    elif mouseInBox(mouse, 1.5*card_length + 370, buttonWindowTop + 2*card_length + 47.5, miniBoxWidth*3, miniBoxWidth):
                        playerChanging = 1
                        money[playerChanging] = ""
                    # send offer
                    elif mouseInBox(mouse, card_length + 30, buttonWindowTop + 3.5*card_length, 2*buttonWidth, buttonHeight/3):
                        if playerChanging is not None and int(money[playerChanging]) > currentMoney[playerChanging]:
                            money[playerChanging] = str(currentMoney[playerChanging])
                        if playerChanging is not None and money[playerChanging] == "": money[playerChanging] = "0"
                        send_data = {'type': 'tradeSend', 'player1': p1id, 'player2': p2id, 'money1': money[0], 'money2': money[1], "selectedProperties1": selectedProperties1, "selectedProperties2": selectedProperties2}
                        send_data = json.dumps(send_data)
                        sock.sendall(bytes(send_data, encoding = "utf-8"))
                        done = True
                    # cancel trade
                    elif mouseInBox(mouse, card_length + 30 + 2*buttonWidth + 10, buttonWindowTop + 3.5*card_length, 2*buttonWidth, buttonHeight /3):
                        send_data = {'type': 'tradeCancel', 'player1': p1id, 'player2': p2id}
                        send_data = json.dumps(send_data)
                        sock.sendall(bytes(send_data, encoding = "utf-8"))
                        done = True
                    # unfocus money changing window
                    else:
                        if playerChanging is not None and int(money[playerChanging]) > currentMoney[playerChanging]:
                            money[playerChanging] = str(currentMoney[playerChanging])
                        if playerChanging is not None and money[playerChanging] == "": money[playerChanging] = "0"
                        playerChanging = None
                        send_data = {'type': 'tradeUpdate', 'player1': p1id, 'player2': p2id, 'money1': money[0], 'money2': money[1], "selectedProperties1": selectedProperties1, "selectedProperties2": selectedProperties2}
                        send_data = json.dumps(send_data)
                        sock.sendall(bytes(send_data, encoding = "utf-8"))

                if event.type == pygame.KEYDOWN and playerChanging is not None:
                    if event.key == pygame.K_RETURN:
                        if playerChanging is not None and int(money[playerChanging]) > currentMoney[playerChanging]:
                            money[playerChanging] = str(currentMoney[playerChanging])
                        if playerChanging is not None and money[playerChanging] == "": money[playerChanging] = "0"
                        send_data = {'type': 'tradeUpdate', 'player1': p1id, 'player2': p2id, 'money1': money[0], 'money2': money[1], "selectedProperties1": selectedProperties1, "selectedProperties2": selectedProperties2}
                        send_data = json.dumps(send_data)
                        sock.sendall(bytes(send_data, encoding = "utf-8"))
                    elif event.key == pygame.K_BACKSPACE:
                        money[playerChanging] = money[playerChanging][:-1]
                    else:
                        char = event.unicode
                        if char.isnumeric() and len(money[playerChanging]) < 5:
                            money[playerChanging] += char

                pygame.draw.rect(surface, (255, 255, 255), [1.75*card_length , buttonWindowTop + 2*card_length + 47.5, miniBoxWidth*3, miniBoxWidth])
                pygame.draw.rect(surface, black, [1.75*card_length , buttonWindowTop + 2*card_length + 47.5, miniBoxWidth*3, miniBoxWidth], 1)
                textInPos(surface, "$" + money[0], lfont2, black, 1.75*card_length , buttonWindowTop + 2*card_length + 50)
                r = drawPlayerProperties(surface, properties1, mortgagedProperties, card_length + 30, buttonWindowTop + 3.5*card_length, miniBoxWidth, selectedProperties1, mouse)
                if r is not None:
                    if r in selectedProperties1:
                        selectedProperties1.remove(r)
                    elif r in properties1:
                        selectedProperties1.append(r)
                    send_data = {'type': 'tradeUpdate', 'player1': p1id, 'player2': p2id, 'money1': money[0], 'money2': money[1], "selectedProperties1": list(set(selectedProperties1)), "selectedProperties2": list(set(selectedProperties2))}
                    send_data = json.dumps(send_data)
                    sock.sendall(bytes(send_data, encoding = "utf-8"))
                    done = True

                pygame.draw.rect(surface, (255, 255, 255), [1.5*card_length + 370 , buttonWindowTop + 2*card_length + 47.5, miniBoxWidth*3, miniBoxWidth])
                pygame.draw.rect(surface, black, [1.5*card_length + 370 , buttonWindowTop + 2*card_length + 47.5, miniBoxWidth*3, miniBoxWidth], 1)
                textInPos(surface, "$" + money[1], lfont2, black, 1.5*card_length+ 370, buttonWindowTop + 2*card_length + 50)
                r = drawPlayerProperties(surface, properties2, mortgagedProperties, card_length + 368, buttonWindowTop + 3.5*card_length, miniBoxWidth, selectedProperties2, mouse)
                if r is not None:
                    if r in selectedProperties2:
                        selectedProperties2.remove(r)
                    elif r in properties2:
                        selectedProperties2.append(r)
                    send_data = {'type': 'tradeUpdate', 'player1': p1id, 'player2': p2id, 'money1': money[0], 'money2': money[1], "selectedProperties1": list(set(selectedProperties1)), "selectedProperties2": list(set(selectedProperties2))}
                    send_data = json.dumps(send_data)
                    sock.sendall(bytes(send_data, encoding = "utf-8"))
                    done = True

            pygame.display.flip()
            pygame.time.Clock().tick(30)
    else:
        text_in_box(surface, str(player1) + " is trading with you", lfont, black, card_length + 20, buttonWindowTop + 1.5*card_length, 1.87*buttonWindowWidth, 50)

        text_in_box(surface, "You", lfont, black, card_length + 30, buttonWindowTop + 2*card_length, miniBoxWidth*10, 50)
        textInPos(surface, "Money: ", lfont2, black, card_length + 30, buttonWindowTop + 2*card_length + 50)
        textInPos(surface, "$" + str(money2), lfont2, black, 1.75*card_length , buttonWindowTop + 2*card_length + 50)
        drawPlayerProperties(surface, properties2, mortgagedProperties, card_length + 30, buttonWindowTop + 3.5*card_length, miniBoxWidth, selectedProperties2, [-1, -1])

        text_in_box(surface, "Them", lfont, black, card_length + 368, buttonWindowTop + 2*card_length, miniBoxWidth * 10, 50)
        textInPos(surface, "Money: ", lfont2, black, card_length + 368, buttonWindowTop + 2*card_length + 50)
        textInPos(surface, "$" + str(money1), lfont2, black, 1.5*card_length+ 370, buttonWindowTop + 2*card_length + 50)
        drawPlayerProperties(surface, properties1, mortgagedProperties, card_length + 368, buttonWindowTop + 3.5*card_length, miniBoxWidth, selectedProperties1, [-1, -1])

        if tradeData['type'] == "tradeSend":
            done = False

            pygame.draw.rect(surface, black, [card_length + 30, buttonWindowTop + 3.5*card_length, 2*buttonWidth, buttonHeight/3], 2)
            text_in_box(surface, "Accept offer", lfont, black, card_length + 30, buttonWindowTop + 3.5*card_length, 2*buttonWidth, buttonHeight/3)

            pygame.draw.rect(surface, black, [card_length + 30 + 2*buttonWidth + 10, buttonWindowTop + 3.5*card_length, 2*buttonWidth, buttonHeight/3], 2)
            text_in_box(surface, "Decline offer", lfont, black, card_length + 30 + 2*buttonWidth + 10, buttonWindowTop + 3.5*card_length, 2*buttonWidth, buttonHeight/3)

            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                        mouse = pygame.mouse.get_pos()
                        
                        # accept offer
                        if mouseInBox(mouse, card_length + 30,buttonWindowTop + 3.5*card_length, 2*buttonWidth, buttonHeight/3):
                            send_data = {'type': 'tradeAccept', 'player1': p1id, 'player2': p2id, 'money1': money[0], 'money2': money[1], "selectedProperties1": selectedProperties1, "selectedProperties2": selectedProperties2}
                            send_data = json.dumps(send_data)
                            sock.sendall(bytes(send_data, encoding = "utf-8"))
                            done = True
                        # decline offer
                        elif mouseInBox(mouse, card_length + 30 + 2*buttonWidth + 10, buttonWindowTop + 3.5*card_length,  2*buttonWidth, buttonHeight /3):
                            send_data = {'type': 'tradeCancel', 'player1': p1id, 'player2': p2id}
                            send_data = json.dumps(send_data)
                            sock.sendall(bytes(send_data, encoding = "utf-8"))
                            done = True
                pygame.display.flip()
                pygame.time.Clock().tick(30)


    
# draw message if player can't end because they don't have enough money
def drawCantEndText(surface):
    lfont = pygame.font.Font('freesansbold.ttf',20)
    chanceTextSplit(surface, "You cannot end your turn until you mortgage property or declare bankruptcy", 50, 15, lfont, black, buttonWindowLeft, buttonWindowTop + buttonWindowLength, buttonWindowWidth, buttonWindowLength)

# draw roll/end turn buttons
def drawButtons(surface, canRoll, canEnd):
    lfont = pygame.font.Font('freesansbold.ttf',20)
    lfont2 = pygame.font.Font('freesansbold.ttf',50)
    text_in_box(surface, "Your Turn!" if canRoll else "", lfont2, red, buttonWindowLeft, buttonWindowTop + card_length, buttonWindowWidth, buttonWindowLength)
    pygame.draw.rect(surface, black, [buttonWindowLeft, buttonWindowTop, buttonWindowWidth, buttonWindowLength], 2)

    # roll
    
    pygame.draw.rect(surface, (255, 255, 255) if canRoll else (166, 166, 166), [buttonWindowLeft + buttonMargin, buttonWindowTop + buttonMargin, buttonWidth, buttonHeight])
    pygame.draw.rect(surface, black, [buttonWindowLeft + buttonMargin, buttonWindowTop + buttonMargin, buttonWidth, buttonHeight], 2)
    text_in_box(surface, "Roll", lfont, black, buttonWindowLeft + buttonMargin, buttonWindowTop + buttonMargin, buttonWidth, buttonHeight)

    # end turn
    
    pygame.draw.rect(surface, (255, 255, 255) if canEnd else (166, 166, 166), [buttonWindowLeft + 2*buttonMargin + buttonWidth, buttonWindowTop + buttonMargin, buttonWidth, buttonHeight])
    pygame.draw.rect(surface, black, [buttonWindowLeft + 2*buttonMargin + buttonWidth, buttonWindowTop + buttonMargin, buttonWidth, buttonHeight], 2)
    text_in_box(surface, "End Turn", lfont, black, buttonWindowLeft + 2*buttonMargin + buttonWidth, buttonWindowTop + buttonMargin, buttonWidth, buttonHeight)

# draw building / mortgaging window if they click a property
def drawBuildMortgage(surface, propName, buyType, mortType, numHouses, buildCost, mortVal):   
    lfont = pygame.font.Font('freesansbold.ttf',13)

    pygame.draw.rect(surface, black, [buttonWindowLeft, buttonWindowTop + buttonWindowLength + 1.5*card_length, buttonWindowWidth, buttonWindowLength], 2)
    text_in_box(surface, propName, lfont, black, buttonWindowLeft, buttonWindowTop + buttonWindowLength + 1.25*card_length, buttonWindowWidth, buttonWindowLength)
    if (numHouses > 0 and numHouses < 5) or buyType is not None:
        text_in_box(surface, "Houses: " + str(numHouses) , lfont, black, buttonWindowLeft, buttonWindowTop + buttonWindowLength + 1.35*card_length, buttonWindowWidth, buttonWindowLength)
    if numHouses == 5:
        text_in_box(surface, "Hotels: 1", lfont, black, buttonWindowLeft, buttonWindowTop + buttonWindowLength + 1.35*card_length, buttonWindowWidth, buttonWindowLength)

    pygame.draw.rect(surface, black, [buttonWindowLeft + 5, buttonWindowTop + buttonWindowLength + 2.18*card_length, buttonWidth + 5, buttonHeight/3], 2)
    text_in_box(surface, ("Buy " + str(buyType) if buyType is not None else "Cannot buy"), lfont, black, buttonWindowLeft + 5, buttonWindowTop + buttonWindowLength + 2.18*card_length, buttonWidth + 5, buttonHeight/3)
    if buyType is not None:
        text_in_box(surface, "(-" + str(buildCost) + ")" , lfont, black, buttonWindowLeft + 5, buttonWindowTop + buttonWindowLength + 10 + 2.18*card_length, buttonWidth + 5, buttonHeight/3)

    pygame.draw.rect(surface, black, [buttonWindowLeft + buttonWidth + 20, buttonWindowTop + buttonWindowLength + 2.18*card_length, buttonWidth + 5, buttonHeight/3], 2)
    text_in_box(surface, mortType, lfont, black, buttonWindowLeft + buttonWidth + 20, buttonWindowTop + buttonWindowLength + 2.18*card_length, buttonWidth + 5, buttonHeight/3)
    text_in_box(surface, "(" + ("+" if mortVal > 0 else "") + str(int(mortVal)) + ")", lfont, black, buttonWindowLeft + buttonWidth + 20, buttonWindowTop + 10 + buttonWindowLength + 2.18*card_length, buttonWidth + 5, buttonHeight/3)