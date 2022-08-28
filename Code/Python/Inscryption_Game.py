import pygame
from pyautogui import size
from os import listdir
from sys import exit
from serial import Serial
from threading import Thread
from PIL import Image
from random import uniform
from math import floor

#Main game variables.
Current_CardsPos = []
Current_CardsNum = []
Cards = ["", "", "", "", "", "", "", "", "", ""]
onPlayer2 = False
PlayersHealth = [0, 0]
PlayersBattery = [1, 1]
PlayersBones = [0, 0]
Circuits = ([], [-1, -1, -1, -1])
turn = 0
selectedCard = [-1, -1]
#Green, Orange, Blue
PlayersGems = ([False, False, False], [False, False, False])

#Classes
class Card:
    def __init__(self, Pos, Name, Power, Health, Cost, *Sigils):
        self.Pos = Pos
        self.Name = Name
        self.Power = Power
        self.Health = Health
        self.Cost = Cost
        if len(Sigils) > 0:
            self.Sigils = Sigils[0]
        else:
            self.Sigils = []
        self.Air = False
        self.Airblock = False
        self.Quills = False
        self.Nano = False
        self.Swapper = False
        self.Right = onPlayer2
        self.VesselPrinter = False
        self.Annoyed = False
        self.Conduit = False
        self.Guardian = False #
        self.AttackUp = False
        self.Buffed = False
        self.Powered = False
        self.BuffWhenPowered = False
        self.TriWhenPowered = False
        self.Tri = False
        self.Bi = False
        self.Sentry = False
        self.Clinger = False
        self.Sniper = False
        self.checkSigils()
    def checkSigils(self):
        for sigil in self.Sigils:
            if sigil == 3:
                self.Airblock = True
            elif sigil == 5:
                self.Air = True
            elif sigil == 12 or sigil == 19 or sigil == 26:
                self.Conduit = True
            elif sigil == 13:
                self.VesselPrinter = True
            elif sigil == 20:
                self.Sentry = True
            elif sigil == 21:
                self.Quills = True
            elif sigil == 22:
                self.Sniper = True    
            elif sigil == 25:
                self.Clinger = True
            elif sigil == 29:
                self.Nano = True
            elif sigil == 31:
                self.TriWhenPowered = True
            elif sigil == 32:
                self.Swapper = True
            elif sigil == 33:
                self.BuffWhenPowered = True
            elif sigil == 34:
                self.Tri = True
    def checkPoweredSigils(self):
        if self.BuffWhenPowered:
            if inCircuit(self.Pos):
                self.Buffed = True
            else:
                self.Buffed = False
        elif self.TriWhenPowered:
            if inCircuit(self.Pos):
                self.Tri = True
            else:
                self.Tri = False
    def getDamage(self):
        self.checkPoweredSigils()
        return self.Power + int(self.Annoyed) + int(self.AttackUp) + 2*int(self.Buffed)
    def Attack(self, snipe = -1):
        if snipe != -1:
            self.Strike(snipe)
            return
        damagePositions = [0]
        if self.Tri or self.Bi:
            if self.Tri:
                damagePositions = [-1, 0, 1]
            elif self.Bi:
                damagePositions = [-1, 1]
            if -1 in damagePositions and (self.Pos - 1) % 5 == 4:
                damagePositions.remove(-1)
            elif 1 in damagePositions and (self.Pos + 1) % 5 == 0:
                damagePositions.remove(1)
        for position in damagePositions:
            enemyPos = (self.Pos + 5 + position) % 10
            self.Strike(enemyPos)
    def Strike(self, pos):
        damage = self.getDamage()
        if isinstance(Cards[pos], Card):
            if not self.Air or Cards[pos].Airblock:
                Cards[pos].Damage(damage)
            else:
                PlayersHealth[int(self.Pos < 5)] -= damage
        else:
            PlayersHealth[int(self.Pos < 5)] -= damage
    def Damage(self, DamageDone):
        if self.Nano:
            self.Nano = False
            return
        if self.VesselPrinter:
            displayMessage(f"Player {int(self.Pos > 4) + 1} draw a vessel.")
        if self.Swapper:
            oldPow = self.Power
            self.Power = self.Health
            self.Health = oldPow
        self.Health -= DamageDone
        if self.Quills and isinstance(Cards[(self.Pos + 5) % 10]):
            Cards[(self.Pos + 5) % 10].Damage(1)
        if self.Health <= 0:
            KillCard(self.Pos)  
    def Move(self, direction):
        if (not isinstance(Cards[(self.Pos + direction) % 10], Card)) and (self.Pos % 5 + direction >= 0) and (self.Pos % 5 + direction <= 4):
            Current_CardsPos[Current_CardsPos.index(self.Pos)] = self.Pos + direction
            Cards[self.Pos + direction] = self
            Cards[self.Pos] = ""
            self.Pos = self.Pos + direction
            self.Right = direction > 0
            self.Annoyed = False
            if isinstance(Cards[(self.Pos + 5) % 10], Card):
                if Cards[(self.Pos + 5) % 10].Sentry:
                    self.Damage(1)
    def AddSigil(self, Sigil):
        if not isinstance(Sigil, list):
            Sigil = [Sigil]
        for sig in Sigil:
            self.Sigils.append(sig)
        self.checkSigils()

#Functions
def returnKeyNum(key):
    if key == pygame.K_0:
        return 0
    elif key == pygame.K_1:
        return 1
    elif key == pygame.K_2:
        return 2
    elif key == pygame.K_3:
        return 3
    elif key == pygame.K_4:
        return 4
    elif key == pygame.K_5:
        return 5
    elif key == pygame.K_6:
        return 6
    elif key == pygame.K_7:
        return 7
    elif key == pygame.K_8:
        return 8
    elif key == pygame.K_9:
        return 9
    elif key == pygame.K_a:
        if not selecting:
            attackPhase()
    elif key == pygame.K_RETURN:
        return -1
    elif key == pygame.K_l:
        pygame.quit() 
        exit(0)

def listsToString():
    newList = []
    Numi = 0
    Posi = 0
    for i in range(len(Current_CardsNum) + len(Current_CardsPos)):
        if i % 2 == 0:
            newList.append(Current_CardsPos[Posi])
            Posi += 1
        else:
            newList.append(Current_CardsNum[Numi])
            Numi += 1
    return ', '.join(map(str, newList))

def connect():
    arduino = Serial()
    arduino.port = 'COM15'
    arduino.baudrate = 9600
    arduino.open()
    return arduino

def readArduino():
    while 1:
        data = arduino.readline()
        cardID = str(data[2:len(data)-2])
        pos = str(data[0])
        pos = int(pos) - 48 #Man idk. Probably hex shenanigans
        print(data)
        print(pos, cardID)
        if updating:
            continue
        try:   
            cardID = CardIds[cardID]
            updateCards(pos, cardID)
        except:
            print("Read failed.")

def updateCards(pos, num, overrideBattery = False):
    if onPlayer2 != (pos > 4):
        print("It is Player {0}'s turn.".format(int(onPlayer2) + 1))
        return
    try:
        statsGot = CardStats[num].split(",", 5)
    except:
        print("Could not find card", num)
        return
    statsGot[-1] = statsGot[-1].strip()
    if statsGot.count('') > 0:
        for i in range(statsGot.count('')):
            statsGot.remove('')
    print(statsGot, filenames[num])
    if PlayersBattery[int(pos > 4)] - int(statsGot[4]) < 0 and not overrideBattery:
        print("Not enought battery to play this card.")
        return
    elif not overrideBattery:
        PlayersBattery[int(pos > 4)] -= int(statsGot[4])
    updating = True
    if len(statsGot) < 6:
        name = statsGot[1]
        statsGot = list(map(int, statsGot[2:5]))
        statsGot.insert(0, name)
        statsGot.insert(0, pos)
        NewCard = Card(pos, statsGot[1], statsGot[2], statsGot[3], statsGot[4])
        Cards[pos] = NewCard
    else:
        sigilsGot = statsGot[5]
        name = statsGot[1]
        statsGot = list(map(int, statsGot[2:5]))
        statsGot.insert(0, name)
        statsGot.insert(0, pos)
        if sigilsGot.find(",") != -1:
            sigilsGot = sigilsGot[1:len(sigilsGot) - 1].split(",")
        if isinstance(sigilsGot, list):
            sigilsGot = list(map(int, sigilsGot))
        else:
            sigilsGot = [int(sigilsGot)]
        NewCard = Card(pos, name, statsGot[2], statsGot[3], statsGot[4], sigilsGot)
        Cards[pos] = NewCard
        for sigil in sigilsGot:
            if sigil == 2:
                #Amorphous
                rand = floor(uniform(0, 33))
                while rand == 1 or rand == 4:
                    rand = floor(uniform(0, 33))
                Cards[pos].Sigils = [rand]
                print("Got Sigil", rand)
    if pos in Current_CardsPos:
        del Current_CardsNum[Current_CardsPos.index(pos)]
        Current_CardsPos.remove(pos)
    Current_CardsPos.append(pos)
    Current_CardsNum.append(num)
    cardPlaced(pos)
    checkCircuits()
    placeStats()
    place_Card.play()
    updating = False

def cardPlaced(pos):
    enemyPos = (pos + 5) % 10
    #Sentry
    if isinstance(Cards[enemyPos], Card):
        if Cards[enemyPos].Sentry:
            Cards[pos].Damage(1)
    #Guardian
    for enemy in range(int(enemyPos > 4)*5, int(enemyPos > 4)*5 + 5):
        if isinstance(Cards[enemy], Card):
            if Cards[enemy].Guardian and not isinstance(Cards[enemyPos], Card) and enemy != enemyPos:
                updateCards(enemyPos, Current_CardsNum[Current_CardsPos.index(enemy)], True)
                deleteCard(enemy)
    #Clinger
    friendBool = int(pos > 4)*5
    for friend in range(friendBool, friendBool + 5):
        if friend == pos:
            continue
        if isinstance(Cards[friend], Card):
            if Cards[friend].Clinger:
                endPos = friend
                boolDifDir = int(friend > pos) - int(friend < pos)
                for clingPos in range(pos + boolDifDir, int(friend > pos)*4 + friendBool + boolDifDir, boolDifDir):
                    if not isinstance(Cards[clingPos], Card):
                        endPos = clingPos
                        break
                if friend != endPos:
                    updateCards(endPos, Current_CardsNum[Current_CardsPos.index(friend)], True)
                    deleteCard(friend)

def attackPhase():
    global onPlayer2
    global turn
    for i in range(5):
        if isinstance(Cards[i + int(onPlayer2)*5], Card) and not Cards[i + int(onPlayer2)*5].Sniper:
            Cards[i + int(onPlayer2)*5].Attack()
    for i in range(len(PlayersBattery)):
        if onPlayer2:
            if turn + 1 > 6:
                PlayersBattery[i] = 6
            else:
                PlayersBattery[i] = turn//2 + 2
    checkCircuits()
    sigilPhase()
    placeStats()
    turn += 1
    onPlayer2 = not onPlayer2

def KillCard(pos):
    CardSigils = Cards[pos].Sigils
    sigil12 = False
    for sigil in CardSigils:
        if sigil == 1:
            #Annoying
            if isinstance(Cards[(pos + 5) % 10], Card):
                #Probably redundant
                Cards[(pos + 5) % 10].Annoyed = False
        elif sigil == 6:
            #Green Mox
            PlayersGems[int(onPlayer2)][0] = False
        elif sigil == 7:
            #Orange Mox
            PlayersGems[int(onPlayer2)][1] = False
        elif sigil == 8:
            #Blue Mox
            PlayersGems[int(onPlayer2)][2] = False
        elif sigil == 11:
            #Detonate
            if isinstance(Cards[(pos + 1) % 10], Card) and pos % 5 != 4:
                deleteCard(pos + 1)
                PlayersBones[onPlayer2] += 1
            if isinstance(Cards[(pos - 1) % 10], Card) and pos % 5 != 0:
                deleteCard(pos - 1)
                PlayersBones[onPlayer2] += 1
            if isinstance(Cards[(pos + 5) % 10]):
                deleteCard((pos + 5) % 10)
                PlayersBones[not onPlayer2] += 1
        elif sigil == 12:
            sigil12 = True
        elif sigil == 16:
            displayMessage(f"Player {int(onPlayer2) + 1} was gifted a card")
        elif sigil == 24:
            if inCircuit(pos):
                displayMessage(f"Player {int(onPlayer2) + 1} was gifted a card")
            continue
        elif sigil == 10:
            #Bomb latch
            selectedCard[1] = 11
            selectionPhase()
        elif sigil == 28:
            #Shield Latch
            selectedCard[1] = 28
            selectionPhase()
        elif sigil == 30:
            #Brittle Latch
            selectedCard[1] = 4
            selectionPhase()
        elif sigil == 27:
            displayMessage(f"Player {int(onPlayer2) + 1}, put the {Cards[pos].Name} into your hand.")
    PlayersBones[onPlayer2] += 1
    deleteCard(pos)
    checkCircuits(sigil12)
    placeStats()
    #Check for annoying. Check for Gem. Check for Detonator. Check for Gift When Powered. Check for latch. Add bone.

def deleteCard(pos):
    del Cards[pos]     
    Cards.insert(pos, "") 
    del Current_CardsNum[Current_CardsPos.index(pos)]
    Current_CardsPos.remove(pos)

def sigilPhase():
    global sniping
    i = -1
    while i < 4:
        i += 1
        offset = i + int(onPlayer2)*5
        if isinstance(Cards[offset], Card):
            cardSigils = Cards[offset].Sigils
            if not isinstance(cardSigils, list):
                cardSigils = list(cardSigils)
            for sigil in cardSigils:
                if sigil == 0:
                    #Sprinter
                    if Cards[offset].Pos % 5 == 4:
                        Cards[offset].Right = False
                    elif Cards[offset].Pos % 5 == 0:
                        Cards[offset].Right = True
                    boolDifRight = int(Cards[offset].Right) - int(not Cards[offset].Right)
                    if (offset + boolDifRight < 10) and not isinstance(Cards[offset + boolDifRight], Card):
                        Cards[offset].Move(boolDifRight)
                        if i + 1 < 5 and (boolDifRight > 0):
                            i += 1
                    elif (offset - boolDifRight < 10) and not isinstance(Cards[offset - boolDifRight], Card):
                        Cards[offset].Move(-boolDifRight)
                        if i + 1 < 5 and (boolDifRight < 0):
                            i += 1                  
                elif sigil == 4:
                    #Brittle
                    KillCard(offset)
                elif sigil == 6:
                    #Green Mox
                    PlayersGems[int(onPlayer2)][0] = True
                elif sigil == 7:
                    #Orange Mox
                    PlayersGems[int(onPlayer2)][1] = True
                elif sigil == 8:
                    #Blue Mox
                    PlayersGems[int(onPlayer2)][2] = True
                elif sigil == 12:
                    #Attack Conduit
                    if isCircuit(offset):
                        for potentialCircuit in range(Circuits[1][int(onPlayer2)*2] + 1, Circuits[1][int(onPlayer2)*2 + 1]):
                            if isinstance(Cards[potentialCircuit], Card):
                                Cards[potentialCircuit].AttackUp = True
                elif sigil == 15:
                    #Battery Bearer
                    if PlayersBattery[int(onPlayer2)] <= 5:
                        PlayersBattery[int(onPlayer2)] += 1
                elif sigil == 17:
                    #Gem Detonator
                    PotentialGems = scanForGems()
                    for gemPos in PotentialGems:
                        Cards[gemPos].AddSigil(11)
                elif sigil == 18:
                    #Gem Guardian
                    PotentialGems = scanForGems()
                    for gemPos in PotentialGems:
                        Cards[gemPos].AddSigil(29)
                elif sigil == 19:
                    #Gem Spawn Conduit
                    if inCircuit(offset):
                        for gemSpot in range(Circuits[1][int(onPlayer2)*2] + 1, Circuits[1][int(onPlayer2)*2 + 1]):
                            if not isinstance(Cards[gemSpot], Card):
                                updateCards(gemSpot, 12, True)
                elif sigil == 22:
                    #Sniper
                    selectedCard[1] = offset
                    sniping = True
                    selectionPhase()
                elif sigil == 23:
                    #Transformer
                    Transform(offset)

def selectionPhase(contin = False):
    #Man idk, events or something.
    global updating
    global selecting
    global selectedCard
    global sniping
    if contin:
        if not sniping:
            if -1 not in selectedCard and isinstance(Cards[selectedCard[0]], Card):
                Cards[selectedCard[0]].AddSigil(selectedCard[1])
        else:
            if (selectedCard[0] > 4) != onPlayer2:
                print("You need to select one of your opponent's cards, Player " + str(int(onPlayer2) + 1) + ".")
                selectedCard[0] = -1
                return
            Cards[selectedCard[1]].Attack(selectedCard[0])
            sniping = False
        selectedCard = [-1, -1]
        selecting = False
    else:
        selecting = True
        if not sniping:
            displayMessage(f"Player {int(onPlayer2) + 1}, choose a card to place your sigil.")

def scanForGems():
    GemCardPos = []
    if PlayersGems[int(onPlayer2)][0] or PlayersGems[int(onPlayer2)][1] or PlayersGems[int(onPlayer2)][2]:
        for j in range(10):
            if isinstance(Cards[j], Card):
                PotentialGems = Cards[j].Sigils
                for sig in PotentialGems:
                    if sig == 6 or sig == 7 or sig == 8:
                        GemCardPos.append(j)
    return GemCardPos

def Transform(currentCard):
    name = Cards[currentCard].Name
    deleteCard(currentCard)
    if name == "GR1ZZ_T":
        updateCards(currentCard, 25, True)
    elif name == "GR1ZZ":
        updateCards(currentCard, 24, True)
    elif name == "QU177_T":
        updateCards(currentCard, 35, True)
    elif name == "QU177":
        updateCards(currentCard, 34, True)
    elif name == "SONIA_T":
        updateCards(currentCard, 44, True)
    elif name == "SONIA":
        updateCards(currentCard, 43, True)
    transform.play()

def displayMessage(message):
    global messageString
    messageString = str(message)

def selectionBox(pos):
    global width, height, Buffer_Width, Buffer_Height, Card_Width, Card_Height, screen
    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect((width/2 - 2*Buffer_Width - Card_Width/2 - Card_Width/10) + (pos%5)*Buffer_Width, Buffer_Height - Card_Height/14 + int(pos > 4)*(height - Card_Height - 2*Buffer_Height), 10 + Card_Width*6/5, Card_Height*8/7), 10)

def clearStatsImagePos():
    for j in range(4):
        cardStatsImagePos[int(j > 1)][j % 2].clear()

def placeStats():
    clearStatsImagePos()
    h = -1
    while h < len(Cards) - 1:
        h += 1
        if isinstance(Cards[h], Card):
            if isinstance(Cards[(h + 5) % 10], Card):
                if 1 in Cards[h].Sigils:
                    if not Cards[(h + 5) % 10].Annoyed:
                        Cards[(h + 5) % 10].Annoyed = True
                        h = -1
                        clearStatsImagePos()
                        continue
                elif Cards[(h + 5) % 10].Annoyed:
                    Cards[(h + 5) % 10].Annoyed = False
                    h = -1
                    clearStatsImagePos()
                    continue
            #Should probably make the surface of the stats the card.
            newcardStat = font2.render(str(Cards[h].getDamage()), True, (13, 230, 254))
            newcardStatLabel = newcardStat.get_rect()
            widthPos = (width/2 - 2*Buffer_Width - Card_Width/2) + (h%5)*Buffer_Width
            heightPos = Buffer_Height + int(h > 4)*(height - Card_Height - 2*Buffer_Height)
            wBuffers = [23, 113]
            hBuffer = 207
            xBuffers = ([0, 3, 25], [22, 19, 7])
            if(h <= 4):
                hBuffer = Card_Height - hBuffer
                wBuffers[0] = Card_Width - wBuffers[0]
                wBuffers[1] = Card_Width - wBuffers[1]
            newcardStatLabel.topright = (widthPos + wBuffers[0] + xBuffers[int(h > 4)][0], heightPos + hBuffer - xBuffers[int(h > 4)][2])
            newcardStat2 = font2.render(str(Cards[h].Health), True, (13, 230, 254))
            newcardStat2Label = newcardStat2.get_rect()
            newcardStat2Label.topright = (widthPos + wBuffers[1] + xBuffers[int(h > 4)][1], heightPos + hBuffer - xBuffers[int(h > 4)][2])
            if(h <= 4):
                newcardStat = pygame.transform.rotate(newcardStat, 180)
                newcardStat2 = pygame.transform.rotate(newcardStat2, 180)
            cardStatsImagePos[int(h > 4)][0].append((newcardStat, newcardStatLabel))
            cardStatsImagePos[int(h > 4)][1].append((newcardStat2, newcardStat2Label))

def checkCircuits(sigil12 = False):
    for i in range(len(Cards)):
        if isinstance(Cards[i], Card):
            if Cards[i].Conduit and i not in Circuits[0]:
                Circuits[0].append(i)
    Circuits[0].sort()
    if len(Circuits[0]) < 2:
        return
    bounds = [-1, -1, -1, -1]
    bounds[0] = min((i for i in Circuits[0] if i < 5), default= -1)
    bounds[1] = max((i for i in Circuits[0] if i < 5), default= -1)
    bounds[2] = min((i for i in Circuits[0] if i >= 5), default= -1)
    bounds[3] = max((i for i in Circuits[0] if i >= 5), default= -1)
    for j in range(2):
        if bounds[2*j] == bounds[2*j + 1]:
            bounds[2*j] = bounds[2*j + 1] = -1
    c = -1
    while c < len(Circuits[0]) - 1:
        c += 1
        if Circuits[0][c] >= bounds[0] and Circuits[0][c] <= bounds[1]:
            del Circuits[0][c]
            c = -1
        elif Circuits[0][c] >= bounds[2] and Circuits[0][c] <= bounds[3]:
            del Circuits[0][c]
            c = -1
    for b in range(len(bounds)):
        if bool(b % 2):
            if bounds[b] > Circuits[1][b]:
                Circuits[1][b] = bounds[b]
        else:
            if bounds[b] < Circuits[1][b]:
                Circuits[1][b] = bounds[b]
    checkPowered(sigil12)

def checkPowered(sigil12 = False):
    for pos in range(10):
        if isinstance(Cards[pos], Card):
            if inCircuit(pos):
                Cards[pos].Powered = True
            else:
                Cards[pos].Powered = False
                if sigil12:
                    Cards[pos].AttackUp = False

def inCircuit(pos):
    if pos > Circuits[1][int(pos > 4)*2] and pos < Circuits[1][int(pos > 4)*2 + 1]:
        return True
    return False

def isCircuit(pos):
    if Circuits[1][int(pos > 4)*2] == pos or Circuits[1][int(pos > 4)*2 + 1] == pos:
        return True
    return False

#Setting up game
pygame.init()
pygame.mixer.init()
arduino = connect()
width, height = size()
Card_Height = 233
Card_Width = 155
screen = pygame.display.set_mode((width, height))
messageString = ""
font = pygame.font.Font(pygame.font.get_default_font(), 32)
font2 = pygame.font.SysFont('bankgothic', 30)
text = font.render("0  0 0", True, (255, 255, 255), (0, 0, 0))
text2 = font.render("0 0", True, (255, 255, 255), (0, 0, 0))
textMessage = font.render(messageString, True, (255, 255, 255), (0, 0, 0))
#Player 1 or 2. Power or Health. Insert Box then Label as tuple. 
cardStatsImagePos = (([], []), ([], []))
textLabel = text.get_rect()
textLabel2 = text2.get_rect()
textMessageLabel = textMessage.get_rect()
textLabel.topleft = (0, 0)
textLabel2.topright = (width-31, 0)
textMessageLabel.topleft = (0, 0)
Buffer_Width = Card_Width*3/2
Buffer_Height = Card_Height*2/5

#Beginning Thread
t = Thread(target = readArduino)
t.daemon = True
t.start()

#Loading Images
CardImages = []
base = "Code\\Python\\Resources\\Images\\"
filenames = listdir(base + "Cards")
filenames.sort()
for filename in filenames:
    CardImage = pygame.image.load(base + "Cards\\" + filename)
    CardImage = pygame.transform.scale(CardImage, (Card_Width, Card_Height))
    CardImages.append(CardImage)
Background = pygame.image.load(base + "Background3.jpg")
Background = pygame.transform.scale(Background, (width, height))
CardSlot = pygame.image.load(base + "CardSlot.png")
CardSlot = pygame.transform.scale(CardSlot, (Card_Width, Card_Height))


#Loading Sounds and Setting Volumes
place_Card = pygame.mixer.Sound("Code\\Python\\Resources\\Audio\\CardClick.wav")
select_Card = pygame.mixer.Sound("Code\\Python\\Resources\\Audio\\Select.ogg")
transform = pygame.mixer.Sound("Code\\Python\\Resources\\Audio\\Transform.wav")
botopia = pygame.mixer.music.load("Code\\Python\\Resources\\Audio\\Botopia.mp3")
select_Card.set_volume(0.1)
transform.set_volume(0.2)
pygame.mixer.music.play(-1, 0.0) #Set as background music to loop infinitely
pygame.mixer.music.set_volume(0.7)

#Dictionary of RFID Tags and their associated ID.
CardIds = {
    "b'30 B3 C5 24'": 0, #White
    "b'93 60 22 AA'": 1, #White
    "b'D3 34 A0 A9'": 2, #White
    "b'B3 80 67 A9'": 3, #White
    "b'C3 B7 19 AA'": 4, #White
    "b'F3 D1 A2 A9'": 5, #White
    "b'83 C6 AD A9'": 6, #White
    "b'23 0A E1 A9'": 7, #White
    "b'93 39 0B AA'": 8, #White
    "b'93 B4 04 AA'": 9, #White
    "b'30 94 0F 22'": 10, #Blue
    "b'3A 00 FB B0'": 11, #Blue
    "b'BA CD FF B0'": 12, #Blue
    "b'DA 52 15 B1'": 13, #Blue
    "b'3A A0 13 B0'": 14, #Blue
    "b'2A 20 FE B0'": 15, #Blue
    "b'2A 6F 06 B0'": 16, #Blue
    "b'8A 3F 05 B1'": 17, #Blue
    "b'7A 62 03 B0'": 18, #Blue
    "b'AA 39 16 B1'": 19 #Blue
}

#Reading Stats
Stats = open("Code\\Python\\Resources\\CardStats.csv")
CardStats = Stats.readlines()[1:]

#Main Loop
onNum = False
updating = False
selecting = False
sniping = False
inputKeys = []
while 1:
    #Clear screen
    screen.fill(0)
    screen.blit(Background, (0, 0))
    for h in range(10): 
        if h in Current_CardsPos and not updating:
            if h > 4:
                CurrentCard = CardImages[Current_CardsNum[Current_CardsPos.index(h)]]
            else:
                CurrentCard = pygame.transform.rotate(CardImages[Current_CardsNum[Current_CardsPos.index(h)]], 180)
            screen.blit(CurrentCard, ((width/2 - 2*Buffer_Width - Card_Width/2) + (h%5)*Buffer_Width, Buffer_Height + int(h > 4)*(height - Card_Height - 2*Buffer_Height)))
        else:
            if h > 4:
                CardSlotMod = CardSlot
            else:
                CardSlotMod = pygame.transform.rotate(CardSlot, 180)
            screen.blit(CardSlotMod, ((width/2 - 2*Buffer_Width - Card_Width/2) + (h%5)*Buffer_Width, Buffer_Height + int(h > 4)*(height - Card_Height - 2*Buffer_Height)))
            pygame.draw.rect(screen, (5,152,206), pygame.Rect((width/2 - 2*Buffer_Width - Card_Width/2) + (h%5)*Buffer_Width, Buffer_Height + int(h > 4)*(height - Card_Height - 2*Buffer_Height), Card_Width+10, Card_Height), 10) 
        if selecting:
            if pygame.Rect((width/2 - 2*Buffer_Width - Card_Width/2) + (h%5)*Buffer_Width, Buffer_Height + int(h > 4)*(height - Card_Height - 2*Buffer_Height), Card_Width+10, Card_Height).collidepoint(pygame.mouse.get_pos()):
                selectionBox(h)
    if len(Current_CardsNum) != len(Current_CardsPos):
        selectionBox(Current_CardsPos[-1])    
    for j in range(4):
        for statPic in cardStatsImagePos[int(j > 1)][j % 2]:
            if isinstance(statPic, tuple):
                screen.blit(statPic[0], statPic[1])
    listString = listsToString()
    pygame.display.set_caption(listString)
    text2String = str(PlayersHealth[1]) + " " + str(PlayersBattery[1])
    textLabel2.topright = (width - 1 - 15*(len(text2String)-3), 0)
    textMessageLabel.topleft = (width/2 - 1 - 15*len(messageString)/2, 0)
    text = font.render(str(turn) + "  " + str(PlayersHealth[0]) + " " + str(PlayersBattery[0]), True, (255, 255, 255), (0, 0, 0))    
    text2 = font.render(text2String, True, (255, 255, 255), (0, 0, 0))
    textMessage = font.render(messageString, True, (255, 255, 255), (0, 0, 0))
    screen.blit(text, textLabel)
    screen.blit(text2, textLabel2)
    screen.blit(textMessage, textMessageLabel)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit() 
            exit(0) 
        if event.type == pygame.KEYDOWN:
            keyNum = returnKeyNum(event.key)
            if keyNum == None:
                continue
            if onNum:
                if keyNum != -1:
                    inputKeys.append(keyNum)
                    continue
                keyNum = 0
                for k in range(len(inputKeys)):
                    keyNum += inputKeys[k]*10**(len(inputKeys) - k - 1)
                inputKeys.clear()
                onNum = False
                position = Current_CardsPos[-1]
                del Current_CardsPos[-1]
                updateCards(position, keyNum)
                updating = False
            else:
                if onPlayer2 != (keyNum > 4):
                    print("It is Player {0}'s turn.".format(int(onPlayer2) + 1))
                    continue
                onNum = True
                updating = True
                if keyNum in Current_CardsPos:
                    del Current_CardsNum[Current_CardsPos.index(keyNum)]
                    Current_CardsPos.remove(keyNum)
                Current_CardsPos.append(keyNum)
                select_Card.play()
        if event.type == pygame.MOUSEBUTTONDOWN:
            messageString = ""
            if selecting:
                mousePos = pygame.mouse.get_pos()
                for h in range(10):
                    if pygame.Rect((width/2 - 2*Buffer_Width - Card_Width/2) + (h%5)*Buffer_Width, Buffer_Height + int(h > 4)*(height - Card_Height - 2*Buffer_Height), Card_Width+10, Card_Height).collidepoint(mousePos):
                        selectedCard[0] = h
                        selectionPhase(True)
                        break