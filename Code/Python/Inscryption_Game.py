import pygame
import pyautogui
import os
import sys
import serial
from threading import Thread

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
        print(data)
        print(pos, cardID)
        updating = True
        try:   
            cardID = CardIds[cardID]
            pos = int(pos) - 48 #Man idk. Probably hex shenanigans
            if pos in Current_CardsPos:
                del Current_CardsNum[Current_CardsPos.index(pos)]
                Current_CardsPos.remove(pos)
            Current_CardsPos.append(pos)
            Current_CardsNum.append(cardID)
            place_Card.play()
        except:
            print("Read failed.")
        updating = False

pygame.init()
pygame.mixer.init()
arduino = connect()
width, height = pyautogui.size()
Card_Height = 233
Card_Width = 155
screen = pygame.display.set_mode((width, height))
Buffer_Width = Card_Width*3/2
Buffer_Height = Card_Height*2/5
Current_CardsPos = []
Current_CardsNum = []

t = Thread(target = readArduino)
t.daemon = True
t.start()

Card_names = []
base = "Code\\Python\\Resources\\Images\\"
for filename in os.listdir("Code\\Python\\Resources\\Images"):
    name = filename.replace(".png", "")
    Card_names.append(name)

#Loading Images
Card1 = pygame.image.load(base + Card_names[0] + ".png")
Card2 = pygame.image.load(base + Card_names[1] + ".png")
Card3 = pygame.image.load(base + Card_names[2] + ".png")
Card4 = pygame.image.load(base + Card_names[3] + ".png")
Card5 = pygame.image.load(base + Card_names[4] + ".png")
Card6 = pygame.image.load(base + Card_names[5] + ".png")
Card7 = pygame.image.load(base + Card_names[6] + ".png")
Card8 = pygame.image.load(base + Card_names[7] + ".png")
Card9 = pygame.image.load(base + Card_names[8] + ".png")
Card10 = pygame.image.load(base + Card_names[9] + ".png")
Cards = [Card1, Card2, Card3, Card4, Card5, Card6, Card7, Card8, Card9, Card10]
#Loading Sounds
place_Card = pygame.mixer.Sound("Code\\Python\\Resources\\Audio\\CardClick.wav")
select_Card = pygame.mixer.Sound("Code\\Python\\Resources\\Audio\\Select.ogg")
botopia = pygame.mixer.music.load("Code\\Python\\Resources\\Audio\\Botopia.mp3")
select_Card.set_volume(0.1)
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.7)

CardIds = {
    "b'30 B3 C5 24'": 0, #White
    "b'30 94 0F 22'": 1 #Blue
}

onNum = False
updating = False
while 1:
    #Clear screen
    screen.fill(0)
    for h in range(len(Cards)):   
        if h in Current_CardsPos and not updating:
            screen.blit(Cards[Current_CardsNum[Current_CardsPos.index(h)]], ((width/2 - 2*Buffer_Width - Card_Width/2) + (h%5)*Buffer_Width, Buffer_Height + int(h > len(Cards)//2 - 1)*(height - Card_Height - 2*Buffer_Height)))
        else:
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((width/2 - 2*Buffer_Width - Card_Width/2) + (h%5)*Buffer_Width, Buffer_Height + int(h > len(Cards)//2 - 1)*(height - Card_Height - 2*Buffer_Height), Card_Width, Card_Height), 3)
    if len(Current_CardsNum) != len(Current_CardsPos):    
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect((width/2 - 2*Buffer_Width - Card_Width/2 - Card_Width/10) + (Current_CardsPos[-1]%5)*Buffer_Width, Buffer_Height - Card_Height/14 + int(Current_CardsPos[-1] > len(Cards)//2 - 1)*(height - Card_Height - 2*Buffer_Height), Card_Width*6/5, Card_Height*8/7), 10)
    listString = listsToString()
    pygame.display.set_caption(listString)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit() 
            sys.exit(0) 
        if event.type == pygame.KEYDOWN:
            keyNum = returnKeyNum(event.key)
            if onNum:
                onNum = False
                Current_CardsNum.append(keyNum)
                place_Card.play()
                updating = False
            else:
                onNum = True
                updating = True
                if keyNum in Current_CardsPos:
                    del Current_CardsNum[Current_CardsPos.index(keyNum)]
                    Current_CardsPos.remove(keyNum)
                Current_CardsPos.append(keyNum)
                select_Card.play()