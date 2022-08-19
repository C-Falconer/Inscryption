import pygame
import pyautogui
import os
import sys
import serial
from threading import Thread
from PIL import Image

#Main game variables.
Current_CardsPos = []
Current_CardsNum = []
Cards = ["", "", "", "", "", "", "", "", "", ""]
onPlayer2 = False
PlayersHealth = [0, 0]
PlayersBattery = [1, 1]
turn = 0

#Classes
class Card:
    def __init__(self, Pos, Name, Power, Health, Cost, *Sigils):
        self.Pos = Pos
        self.Name = Name
        self.Power = Power
        self.Health = Health
        self.Cost = Cost
        self.Sigils = Sigils
    def Attack(self):
        if isinstance(Cards[(self.Pos + 5)%10], Card):
            Cards[(self.Pos + 5)%10].Damage(self.Power)
        else:
            PlayersHealth[int(self.Pos < 5)] -= self.Power
    def Damage(self, DamageDone):
        self.Health -= DamageDone
        if self.Health <= 0:
            KillCard(self.Pos)  

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
        attackPhase()
    else:
        return 7

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
    arduino = serial.Serial()
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

def updateCards(pos, num):
    if onPlayer2 != (pos > 4):
        print("It is Player {0}'s turn.".format(int(onPlayer2) + 1))
        return
    statsGot = CardStats[num].split(",", 5)
    statsGot[-1] = statsGot[-1].strip()
    print(statsGot)
    if PlayersBattery[int(pos > 4)] - int(statsGot[4]) < 0:
        print("Not enought battery to play this card.")
        return
    else:
        PlayersBattery[int(pos > 4)] -= int(statsGot[4])
    updating = True
    if len(statsGot) < 6:
        name = statsGot[1]
        statsGot = list(map(int, statsGot[2:5]))
        statsGot.insert(0, name)
        statsGot.insert(0, pos)
        NewCard = Card(pos, statsGot[1], statsGot[2], statsGot[3], statsGot[4])
    else:
        sigilsGot = statsGot[5]
        name = statsGot[1]
        statsGot = list(map(int, statsGot[2:5]))
        statsGot.insert(0, name)
        statsGot.insert(0, pos)
        if sigilsGot.find(",") != -1:
            sigilsGot = sigilsGot[1:len(sigilsGot) - 1].split(",")
        sigilsGot = list(map(int, sigilsGot))
        NewCard = Card(pos, statsGot[1], statsGot[2], statsGot[3], statsGot[4], sigilsGot)
    Cards[pos] = NewCard
    if pos in Current_CardsPos:
        del Current_CardsNum[Current_CardsPos.index(pos)]
        Current_CardsPos.remove(pos)
    Current_CardsPos.append(pos)
    Current_CardsNum.append(num)
    place_Card.play()
    updating = False

def attackPhase():
    global onPlayer2
    global turn
    for i in range(5):
        if isinstance(Cards[i + int(onPlayer2)*5], Card):
            Cards[i + int(onPlayer2)*5].Attack()
    turn += 1
    for i in range(len(PlayersBattery)):
        if(turn + 1 > 6):
            PlayersBattery[i] = 6
        else:
            PlayersBattery[i] = turn + 1
    onPlayer2 = not onPlayer2

def KillCard(pos):
    del Cards[pos]     
    Cards.insert(pos, "") 
    del Current_CardsNum[Current_CardsPos.index(pos)]
    Current_CardsPos.remove(pos)

#Setting up game
pygame.init()
pygame.mixer.init()
arduino = connect()
width, height = pyautogui.size()
Card_Height = 233
Card_Width = 155
screen = pygame.display.set_mode((width, height))
font = pygame.font.Font(pygame.font.get_default_font(), 32)
text = font.render("0  0 0", True, (255, 255, 255), (0, 0, 0))
text2 = font.render("0 0", True, (255, 255, 255), (0, 0, 0))
textLabel = text.get_rect()
textLabel2 = text2.get_rect()
textLabel.topleft = (0, 0)
textLabel2.topright = (width-31, 0)
Buffer_Width = Card_Width*3/2
Buffer_Height = Card_Height*2/5

#Beginning Thread
t = Thread(target = readArduino)
t.daemon = True
t.start()

#Loading Images
CardImages = []
base = "Code\\Python\\Resources\\Images\\"
for filename in os.listdir(base + "Cards"):
    CardImages.insert(len(CardImages), pygame.image.load(base + "Cards\\" + filename))
Background = pygame.image.load(base + "Background3.jpg")
Background = pygame.transform.scale(Background, (width, height))
CardSlot = pygame.image.load(base + "CardSlot.png")
CardSlot = pygame.transform.scale(CardSlot, (Card_Width, Card_Height))


#Loading Sounds and Setting Volumes
place_Card = pygame.mixer.Sound("Code\\Python\\Resources\\Audio\\CardClick.wav")
select_Card = pygame.mixer.Sound("Code\\Python\\Resources\\Audio\\Select.ogg")
botopia = pygame.mixer.music.load("Code\\Python\\Resources\\Audio\\Botopia.mp3")
select_Card.set_volume(0.1)
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
    if len(Current_CardsNum) != len(Current_CardsPos):    
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect((width/2 - 2*Buffer_Width - Card_Width/2 - Card_Width/10) + (Current_CardsPos[-1]%5)*Buffer_Width, Buffer_Height - Card_Height/14 + int(Current_CardsPos[-1] > 4)*(height - Card_Height - 2*Buffer_Height), 10 + Card_Width*6/5, Card_Height*8/7), 10)
    listString = listsToString()
    pygame.display.set_caption(listString)
    text2String = str(PlayersHealth[1]) + " " + str(PlayersBattery[1])
    textLabel2.topright = (width - 1 - 15*(len(text2String)-3), 0)
    text = font.render(str(turn) + "  " + str(PlayersHealth[0]) + " " + str(PlayersBattery[0]), True, (255, 255, 255), (0, 0, 0))    
    text2 = font.render(text2String, True, (255, 255, 255), (0, 0, 0))
    screen.blit(text, textLabel)
    screen.blit(text2, textLabel2)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit() 
            sys.exit(0) 
        if event.type == pygame.KEYDOWN:
            keyNum = returnKeyNum(event.key)
            if keyNum == None:
                continue
            if onNum:
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