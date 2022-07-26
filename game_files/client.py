import  pygame
import os,sys
from gui import Grid
from client_login import login_gui
import socket
import threading
import json
from drawing_functions import drawBankruptcyWindow, drawCard, drawBuyWindow, drawChanceCommunity, drawGameOver, drawBuildMortgage, drawOwedWindow, drawJailWindow, drawTradeWindow, drawCantEndText, drawTradeWindowThirdParty, mouseInBox, textInPos
from constants import *
from string import ascii_letters, digits
from property_info import properties 
import time

HOST=''
PORT=9009

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("./assets")

    return os.path.join(base_path, relative_path)




pygame.init()
clock = pygame.time.Clock()

def create_thread(target):
    thread=threading.Thread(target=target)
    thread.daemon=True
    thread.start()

connection_established=False
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)


surface=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('MonopEli - Client')
icon = pygame.image.load(resource_path("icon.ico"))
pygame.display.set_icon(icon)

player_id = 0
players = []
grid=Grid()
login = login_gui()
running=False
turn=False

position = 0
actions = {"turn": 0, "player": 0, "roll1": 0, "roll2": 0, "landedon": "NA", "lines": []}
buydata = {"propname": None, "id": None, "cost": None}
canEnd = False
rolled = False
finishedBuy = True
myId = 0
declaringBankruptcy = False
trading = False
tradeData = {"player1": None, "player2": None, "properties1": [], "properties2": [], "selectedProperties1": [], "selectedProperties2": [], "money1": None, "money2": None}
game_over = False
winner = None
countDoubles = 0
buildingMortgage = None
canBuyMortgage = False

propertyData = []

tempPropID = 0
tempHouses = 0
tempType = NONE
tempIsMortgaged = False
tempBuildPrice = 0
tempMortVal = 0
tempCanBuild = False
houseData = []

chanceData = {'cardType': None, 'chanceText': None, 'chancePlayer': 0}
acknowledgedChance = True
acknowledgedOwed = True

totalHouses = 0
totalHotels = 0

totalOwed = 0
mortgageData = []
jail = False

password = ""
simualting = False

drawProp = None
tempRename = None
tempRenameId = None

if not os.path.exists('./savedInfo/'):
    os.makedirs('./savedInfo')

if os.path.exists('./savedInfo/pastIP.txt'):
    with open('./savedInfo/pastIP.txt', 'r') as f:
        HOST = f.read()

if os.path.exists('./savedInfo/pastName.txt'):
    with open('./savedInfo/pastName.txt', 'r') as f:
        password = f.read()

# recieve data sent by server
def receive_data():
    global turn,connection_established, player_id, players, position, actions, buydata, myId, canEnd, game_over, winner, rolled, propertyData, buildingMortgage, tempPropID, tempHouses, tempType, tempIsMortgaged, tempMortVal, houseData, acknowledgedChance, chanceData, totalOwed, acknowledgedOwed, totalHouses, totalHotels, tradeData, mortgageData, jail, finishedBuy, simulating
    while True:
        try:

            # get data 12288 is number of bits
            data_in = sock.recv(12288).decode('utf-8')

            # process multiple requests back to back
            datas = []
            if "}{" in data_in:
                datas = "}|||{".join(data_in.split("}{")).split('|||')
            else:
                datas = [data_in]
            for data_in in datas:
            
            # weird issue where json.loads would return strings so just keep loading until it works
                while(type(data_in) == type("a")):
                    data_in = json.loads(data_in)
                # when player connects
                if data_in["type"] == "close":
                    sock.close()
                    break
                if(data_in['type'] == "playerinfo"):
                    player_id = data_in['player']
                    myId = player_id
                # whenever game updates
                elif(data_in['type'] == "gamedata"):                 
                    players = data_in['players']
                    rolled = players[myId - 1]["rolled"]
                    propertyData = data_in['properties']
                    totalOwed = data_in['totalOwed']
                    mortgageData = data_in['mortgageData']
                    jail = players[myId - 1]['jail']

                    drawProp = None

                    if totalOwed > 0:
                        acknowledgedOwed = False
                    else:
                        acknowledgedOwed = True

                    totalHouses = data_in["totalHouses"]
                    totalHotels = data_in["totalHotels"]

                    if players[myId - 1]['turn']:
                        turn = True
                    else:
                        turn = False

                    
                    

                    if data_in['gameover']:
                        game_over = True
                        winner = data_in['winner']
                        turn = False
                        rolled = True
                        canEnd = False

                    if data_in['chanceData']['cardType'] is not None:
                        chanceData = data_in['chanceData']
                        acknowledgedChance = False
                    else:
                        acknowledgedChance = True

                    

                    position = players[player_id - 1]['current_space']

                    actions = data_in["actions"]
                    houseData = data_in["houseData"]

                    if data_in["doubles"] and players[myId - 1]['money'] >= 0:
                        rolled = False
                        canEnd = False
                    if data_in["simulating"]:
                        simulating = True
                        turn = False
                        rolled = True
                        canEnd = False
                        buydata = {"propname": None, "cost": None}  
                    else:
                        simulating = False
                        

                # when the player can buy the property they landed on. recieve this data
                elif(data_in['type'] == "buydata"):
                    buydata = data_in
                    finishedBuy = False
                
                # whenever player buys a house or mortgages property. updates that property's info
                elif(data_in['type'] == "buyMortUpdate"):
                    buildingMortgage = propertyData[data_in["id"]]["name"]

                    tempPropID = data_in["id"]
                    tempHouses = data_in["houses"]
                    tempType = data_in["proptype"]
                    tempIsMortgaged = data_in["isMortgaged"]
                    tempMortVal = data_in['mortgageVal']

                    found = False
                    for p in houseData:
                        if p["id"] == tempPropID:
                            found = True
                            p["houses"] = tempHouses
                    if not found:
                        houseData.append({"id": tempPropID, "houses": tempHouses})

                # whenever trade is updated
                elif(data_in['type'] == "tradeUpdate" or data_in['type'] == "tradeSend"):
                    tradeData = data_in
        except Exception as e:
            print(e)
            # print('Remote connection terminated')
            connection_established=False
            grid.game_over=True


# login
changingName = True
changingIP = False
failedConnect = False
while not running:
    
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            sock.close()
            pygame.display.quit()
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                try:
                    sock.connect((HOST,PORT))
                    connection_established=True
                    running = True
                    send_data = {'password': password}
                    send_data = json.dumps(send_data)
                    sock.sendall(bytes(send_data, encoding = "utf-8"))
                    with open('./savedInfo/pastIP.txt', 'w') as f:
                        f.write(HOST)
                    with open('./savedInfo/pastName.txt', 'w') as f:
                        f.write(password)
                    create_thread(receive_data)
                except :
                    failedConnect = True
            elif event.key == pygame.K_TAB:
                if changingName:
                    changingName = False
                    changingIP = True
                elif changingIP:
                    changingName = True
                    changingIP = False
            elif event.key == pygame.K_BACKSPACE:
                if changingName:
                    password = password[:-1]
                if changingIP:
                    HOST = HOST[:-1]
            else:
                char = event.unicode
                if (char in ascii_letters or char in digits) and len(password) <= 10 and changingName:
                    password += char
                if (char in digits or char == '.') and changingIP:
                    HOST += char

        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            mouse = pygame.mouse.get_pos()
            if mouseInBox(mouse, 100, 380, 100, 75) and len(password) > 0:
                try:
                    sock.connect((HOST,PORT))
                    connection_established=True
                    send_data = {'password': password}
                    send_data = json.dumps(send_data)
                    sock.sendall(bytes(send_data, encoding = "utf-8"))
                    running = True
                    with open('./savedInfo/pastIP.txt', 'w') as f:
                        f.write(HOST)
                    with open('./savedInfo/pastName.txt', 'w') as f:
                        f.write(password)
                    create_thread(receive_data)
                except :
                    failedConnect = True
            if mouseInBox(mouse, 100, 250, 600, 100):
                changingIP = True
                changingName = False
            if mouseInBox(mouse, 100, 100, 600, 100):
                changingIP = False
                changingName = True

    
    surface.fill((255,255,255))
    login.draw(surface, failedConnect, changingName, changingIP)

    lfont = pygame.font.Font(resource_path("font.ttf"), 20)
    textInPos(surface, password, lfont, black, 110, 140)
    textInPos(surface, HOST, lfont, black, 110, 290)
    pygame.display.flip()
    # run at 40 fps
    clock.tick(30)


pressed = False
# main game loop
while running:
    # player money < 0 when they land on a space and can't afford to pay
    # this blocks them from ending the turn until they can afford
    if turn and rolled:
        if players[myId - 1]['money'] < 0:
            canEnd = False
        else:
            canEnd = True

    if tempRenameId is not None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE] and not pressed:
            tempRename = tempRename[:-1]
            time.sleep(0.15)
            keys2 = pygame.key.get_pressed()
            if keys2[pygame.K_BACKSPACE]:
                pressed = True
        elif keys[pygame.K_BACKSPACE] and pressed:
            tempRename = tempRename[:-1]
        else:
            pressed = False

    # get pygame events
    for event in pygame.event.get():
        # safely close game
        if event.type ==pygame.QUIT:
            sock.close()
            running=False
            pygame.display.quit()
            pygame.quit()
            sys.exit()

        # on mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if turn:
                    mouse = pygame.mouse.get_pos()

                    if tempRename is not None:
                        send_data = {'type': 'rename', 'propId': tempRenameId, "newname": tempRename}
                        send_data = json.dumps(send_data)
                        sock.sendall(bytes(send_data, encoding = "utf-8"))

                    # roll
                    if not rolled and acknowledgedChance and acknowledgedOwed and players[myId - 1]['money'] > 0 and not players[myId - 1]["jail"]:
                        if mouse[0] >= buttonWindowLeft + buttonMargin and mouse[0] <= buttonWindowLeft + buttonMargin + buttonWidth and mouse[1] >= buttonWindowTop + buttonMargin and mouse[1] <= buttonWindowTop + buttonMargin + buttonHeight: 
                            send_data = {'type': 'roll', 'id': player_id}
                            send_data = json.dumps(send_data)
                            sock.sendall(bytes(send_data, encoding = "utf-8"))
                            canEnd = True
                            rolled = True
                            drawProp = None
                            
                    # end turn
                    if canEnd and tradeData["player1"] is None:
                        if mouse[0] >= buttonWindowLeft + 2*buttonMargin + buttonWidth and mouse[0] <= buttonWindowLeft + 2*buttonMargin + 2*buttonWidth and mouse[1] >= buttonWindowTop + buttonMargin and mouse[1] <= buttonWindowTop + buttonMargin + buttonHeight: 
                            send_data = {'type': 'endturn', 'player': player_id}
                            send_data = json.dumps(send_data)
                            sock.sendall(bytes(send_data, encoding = "utf-8"))
                            turn=False
                            canEnd = False
                            rolled = False
                            buildingMortgage = None
                            tempRename = None
                            tempRenameId = None
                            canBuyMortgage = False
                            declaringBankruptcy = False
                            tempHouses = 0
                            tempType = NONE
                            tempPropID = 0
                            buydata = {"propname": None, "cost": None}  
                            chanceData = {"cardType": None, "chanceText": None, "chancePlayer": 0} 
                            tradeData = {"player1": None, "player2": None, "properties1": [], "properties2": [], "selectedProperties1": [], "selectedProperties2": [], "money1": None, "money2": None}
                            finishedBuy = True

                            send_data = {'type': 'acknowledgeChance'}
                            send_data = json.dumps(send_data)
                            sock.sendall(bytes(send_data, encoding = "utf-8"))

                            send_data = {'type': 'acknowledgeOwed'}
                            send_data = json.dumps(send_data)
                            sock.sendall(bytes(send_data, encoding = "utf-8"))
                    # buy window
                    if buydata["propname"] is not None and acknowledgedChance and acknowledgedOwed:
                        if mouse[0] >= buttonWindowLeft + 5 and mouse[0] <= buttonWindowLeft + 5 + buttonWidth and mouse[1] >= buttonWindowTop + 2.18*card_length and mouse[1] <= buttonWindowTop + 2.18*card_length + buttonHeight:
                            send_data = {'type': 'buy', 'propId': buydata['id'], 'id': player_id, 'value': True}
                            send_data = json.dumps(send_data)
                            sock.sendall(bytes(send_data, encoding = "utf-8"))
                            finishedBuy = True
                            canBuyMortgage = True
                            buydata = {"propname": None, "cost": None}    
                        if mouse[0] >= buttonWindowLeft + 5 + buttonWidth + 20 and mouse[0] <= buttonWindowLeft + 5 + buttonWidth + 20 + buttonWidth and mouse[1] >= buttonWindowTop + 2.18*card_length and mouse[1] <= buttonWindowTop + 2.18*card_length + buttonHeight:
                            finishedBuy = True
                            canBuyMortgage = True
                            buydata = {"propname": None, "cost": None}   
                    else:
                        canBuyMortgage = True

                    # bankruptcy
                    if declaringBankruptcy and acknowledgedChance and acknowledgedOwed:
                        if mouse[0] >= buttonWindowLeft + 5 and mouse[0] <= buttonWindowLeft + 5 + buttonWidth and mouse[1] >= buttonWindowTop + 2.18*card_length and mouse[1] <= buttonWindowTop + 2.18*card_length + buttonHeight:
                            send_data = {'type': 'bankruptcy', 'id': player_id, 'value': True}
                            send_data = json.dumps(send_data)
                            sock.sendall(bytes(send_data, encoding = "utf-8"))
                            turn=False
                            canEnd = False
                            rolled = True
                            declaringBankruptcy = False
                        if mouse[0] >= buttonWindowLeft + 5 + buttonWidth + 20 and mouse[0] <= buttonWindowLeft + 5 + buttonWidth + 20 + buttonWidth and mouse[1] >= buttonWindowTop + 2.18*card_length and mouse[1] <= buttonWindowTop + 2.18*card_length + buttonHeight:
                            declaringBankruptcy = False
                    
                    # build/mortgage window
                    if acknowledgedChance and acknowledgedOwed and rolled:
                        for propId in players[myId - 1]["owned_properties"]:
                            # for location info
                            prop = properties[propId]
                            if mouse[0] >= prop.left and mouse[0] <= prop.left + prop.width and mouse[1] >= prop.top and mouse[1] <= prop.top + prop.height:
                                if canBuyMortgage:
                                    tempCanBuild = True
                                    buildingMortgage = propertyData[prop.id]['name']
                                    tempRename = buildingMortgage
                                    tempRenameId = prop.id
                                    if prop.type == PROPERTY:
                                        tempHouses = propertyData[prop.id]['houses']
                                        tempBuildPrice = prop.buildCost
                                    else:
                                        tempHouses = 0
                                    tempType = prop.type
                                    tempPropID = prop.id

                                    tempMortVal = prop.mortgage
                                    tempIsMortgaged = prop.id in mortgageData

                                    if all(x in players[myId - 1]["owned_properties"] for x in prop.set):
                                        tempCanBuild = True
                                    else:
                                        tempCanBuild = False

                    # click build/mortgage window
                    if buildingMortgage is not None and acknowledgedChance and acknowledgedOwed and rolled:
                        # build button
                        if tempHouses < 5 and tempCanBuild:
                            if mouse[0] >= buttonWindowLeft + 5 and mouse[0] <= buttonWindowLeft + 10 + buttonWidth and mouse[1] >= buttonWindowTop + buttonWindowLength + 2.18*card_length and mouse[1] <= buttonWindowTop + buttonWindowLength + 2.18*card_length + buttonHeight / 3:
                                send_data = {'type': 'build', 'id': tempPropID, 'value': True}
                                send_data = json.dumps(send_data)
                                sock.sendall(bytes(send_data, encoding = "utf-8"))
                                print("buy")
                        # mortgage button
                        if mouse[0] >= buttonWindowLeft + 20 + buttonWidth and mouse[0] <= buttonWindowLeft + 20 + buttonWidth + buttonWidth + 5 and mouse[1] >= buttonWindowTop + buttonWindowLength + 2.18*card_length and mouse[1] <= buttonWindowTop + buttonWindowLength + 2.18*card_length + buttonHeight / 3:
                            if tempIsMortgaged:
                                send_data = {'type': 'unmortgage', 'id': tempPropID, 'value': True}
                                send_data = json.dumps(send_data)
                                sock.sendall(bytes(send_data, encoding = "utf-8"))
                                print("unmortgage")
                            else:
                                send_data = {'type': 'mortgage', 'id': tempPropID, 'value': True}
                                send_data = json.dumps(send_data)
                                sock.sendall(bytes(send_data, encoding = "utf-8"))
                                print("mortgage")

                    # acknowledge chance
                    if not acknowledgedChance:
                        if mouse[0] >= buttonWindowLeft + 15 and mouse[0] <= buttonWindowLeft + 15  + buttonWindowWidth - 30 and mouse[1] >= buttonWindowTop + buttonWindowLength + 2.18*card_length and mouse[1] <= buttonWindowTop + buttonWindowLength + 2.18*card_length + buttonHeight/3:
                            send_data = {'type': 'acknowledgeChance'}
                            send_data = json.dumps(send_data)
                            sock.sendall(bytes(send_data, encoding = "utf-8"))
                    # acknowledge amount owed
                    if acknowledgedChance and not acknowledgedOwed:
                        if mouse[0] >= buttonWindowLeft + 15 and mouse[0] <= buttonWindowLeft + 15  + buttonWindowWidth - 30 and mouse[1] >= buttonWindowTop + buttonWindowLength + 2.18*card_length and mouse[1] <= buttonWindowTop + buttonWindowLength + 2.18*card_length + buttonHeight/3:
                            send_data = {'type': 'acknowledgeOwed'}
                            send_data = json.dumps(send_data)
                            sock.sendall(bytes(send_data, encoding = "utf-8"))
                            
                    # jail window
                    if players[myId - 1]["jail"] and acknowledgedChance and acknowledgedOwed and players[myId - 1]["jailturns"] > 0:
                        # pay
                        if mouse[0] >= buttonWindowLeft + 5 and mouse[0] <= buttonWindowLeft + 5 + buttonWidth and mouse[1] >= buttonWindowTop + buttonWindowLength + 2.18*card_length and mouse[1] <= buttonWindowTop + buttonWindowLength + 2.18*card_length + buttonHeight/3:
                            send_data = {'type': 'getOutOfJail', 'id': myId, 'value': "pay"}
                            send_data = json.dumps(send_data)
                            sock.sendall(bytes(send_data, encoding = "utf-8"))

                        # use jail card
                        if mouse[0] >=buttonWindowLeft + 5 + buttonWidth + 20 and mouse[0] <= buttonWindowLeft + 5 + buttonWidth + 20 + buttonWidth and mouse[1] >= buttonWindowTop + buttonWindowLength + 2.18*card_length and mouse[1] <= buttonWindowTop + buttonWindowLength + 2.18*card_length + buttonHeight/3:
                            send_data = {'type': 'getOutOfJail', 'id': myId, 'value': "card"}
                            send_data = json.dumps(send_data)
                            sock.sendall(bytes(send_data, encoding = "utf-8"))

                    # click player windows (declare bankruptcy or trade)
                    lefts = [13*card_breadth, 13*card_breadth + 4*card_breadth + 15, 13*card_breadth, 13*card_breadth + 4*card_breadth + 15]
                    tops = [2*card_length + 15, 2*card_length + 15, 2*card_length + 1.8*card_length + 30, 2*card_length + 1.8*card_length + 30]
                    
                    if acknowledgedChance and turn and actions["turn"] > 0 and rolled:
                        for i in range(len(players)):
                            if mouse[0] >= lefts[i] + 5 and mouse[0] <= lefts[i] + 5 + 1.3*buttonWidth:
                                if mouse[1] >= tops[i] + 55 and mouse[1] <= tops[i] + 55 + buttonHeight-10:
                                    if myId == i + 1:
                                        # bankrupcy
                                        # print("bankrupcy " + str(i + 1))
                                        declaringBankruptcy = True
                                    else:
                                        # trade
                                        # print("trade " + str(i + 1))
                                        #trading = True
                                        # tradingWith = i + 1

                                        send_data = {'type': 'trade', 'player': myId - 1, 'with': i}
                                        send_data = json.dumps(send_data)
                                        sock.sendall(bytes(send_data, encoding = "utf-8"))

        if event.type == pygame.KEYDOWN and tempRenameId is not None:
            if event.key == pygame.K_RETURN:
                try:
                    send_data = {'type': 'rename', 'propId': tempRenameId, "newname": tempRename}
                    send_data = json.dumps(send_data)
                    sock.sendall(bytes(send_data, encoding = "utf-8"))
                    create_thread(receive_data)
                except :
                    pass
            elif event.key != pygame.K_BACKSPACE:
                char = event.unicode
                if (char in ascii_letters or char in digits or char == " ") and len(tempRename) <= 30:
                    tempRename += char

            

        # hover over prop
        mouse = pygame.mouse.get_pos()      
        if acknowledgedChance and acknowledgedOwed and finishedBuy:       
            for prop in properties:
                if mouseInBox(mouse, prop.left, prop.top, prop.width, prop.height):
                    drawProp = prop.id
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_ESCAPE:
                    running=False


    # draw white background
    surface.fill((255,255,255))
    # main draw function ()
    grid.draw(surface, players, propertyData, actions, (not rolled and turn), canEnd, myId, houseData, totalHouses, totalHotels, mortgageData)

    # draw card for landed on property in top right
    if len(propertyData) > 0:
        drawCard(surface, propertyData[position], chanceData["chanceText"])
    
    if drawProp and len(propertyData) > 0:
        drawCard(surface, propertyData[drawProp], "")

    # if player can buy a property, display the buy window
    if not finishedBuy and not game_over and acknowledgedChance and acknowledgedOwed and not jail and not simulating:
        drawBuyWindow(surface, buydata["propname"], buydata["cost"]) 
    
    # if player clicked declare bankruptcy, draw that window
    if declaringBankruptcy and not game_over and acknowledgedChance and acknowledgedOwed and finishedBuy and not simulating:
        drawBankruptcyWindow(surface)

    # if player clicked trade, draw trade window
    if tradeData["player1"] is not None and(rolled or players[myId - 1]['money'] < 0) and not game_over and acknowledgedChance and acknowledgedOwed and not jail and not simulating:
        if myId - 1 == tradeData["player1"] or myId - 1 == tradeData["player2"]:
            buildingMortgage = None
            drawTradeWindow(surface, tradeData, myId - 1, players[myId-1]["money"], players[tradeData["player2"]]["money"], sock, mortgageData)

    if tradeData["player1"] is not None and myId - 1 == tradeData["player2"]:
        drawTradeWindow(surface, tradeData, myId - 1, players[myId-1]["money"], players[tradeData["player2"]]["money"], sock, mortgageData)

    if tradeData["player1"] is not None and (myId - 1 != tradeData["player1"] and myId - 1 != tradeData["player2"]):
            drawTradeWindowThirdParty(surface, tradeData, players[tradeData["player1"]]["money"], players[tradeData["player2"]]["money"], mortgageData)

    # if game over
    if game_over:
        drawGameOver(surface, winner)

    # if they clicked a property to mortgage and rolled, show them the buy/mortgage window
    if (buildingMortgage is not None) and canBuyMortgage and rolled and tradeData["player1"] is None and not game_over and not jail and not simulating:
        buyType = "house"
        mortType = "Mortgage property"
        mortVal = tempMortVal
        if tempCanBuild and tempPropID not in mortgageData:
            if tempHouses > 0 and tempHouses <= 4:
                mortType = "Mortgage house"
                mortVal = tempBuildPrice * .5
            if tempHouses == 4:
                buyType = "hotel"
            if tempHouses == 5:
                buyType = None
                mortType = "Mortgage hotel"
                mortVal = tempBuildPrice * .5
        else:
            buyType = None

        if tempType == RAIL or tempType == UTILITY:
            buyType = None
        
        if tempIsMortgaged:
            mortType = "Unmortgage property"
            mortVal = int(-1.1*tempMortVal)
        
        drawBuildMortgage(surface, tempRename, buyType, mortType, tempHouses, tempBuildPrice, mortVal)
    
    # if landed on chance and didn't dismiss window, draw chance card
    if chanceData["chanceText"] is not None and not acknowledgedChance and not game_over and not simulating:
        drawChanceCommunity(surface, chanceData["cardType"], chanceData["chanceText"], myId, chanceData["chancePlayer"])
    
    # if they owe money and didn't dismiss window, draw owed window (runs after chance is acknowledged)
    if totalOwed > 0 and players[myId - 1]["turn"] and acknowledgedChance and not acknowledgedOwed and not game_over and not simulating:
        drawOwedWindow(surface, totalOwed)
    
    # if they're in jail, draw the jail window. (after chance and owed is acknowledged)
    if actions["turn"] > 0 and players[myId - 1]["turn"] and players[myId - 1]["jail"] and players[myId - 1]["jailturns"] > 0 and acknowledgedChance and acknowledgedOwed and not game_over and not simulating:
        drawJailWindow(surface, players[myId - 1]["jailCards"], propertyData[40]['name'])

    if turn and rolled:
        if players[myId - 1]['money'] < 0:
            drawCantEndText(surface)
    
    # idk
    pygame.display.flip()
    # run at 40 fps
    clock.tick(30)