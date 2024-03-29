import pygame

audio = True
try:
    pygame.mixer.init()
    grassSound = pygame.mixer.Sound("../../Sound Effects/grass6.ogg")
    stoneSound = pygame.mixer.Sound("../../Sound Effects/stone1.ogg")
    dirtSound  = pygame.mixer.Sound("../../Sound Effects/sand5.ogg")
    woodSound  = pygame.mixer.Sound("../../Sound Effects/wood1.ogg")
    leafSound  = pygame.mixer.Sound("../../Sound Effects/leaf.ogg")
    grassSound.set_volume(0.3)
    stoneSound.set_volume(0.3)
    dirtSound.set_volume(0.3)
    woodSound.set_volume(0.3)
    leafSound.set_volume(0.3)
    breakGrassSound = pygame.mixer.Sound("../../Sound Effects/breakgrass1.ogg")
    breakDirtSound  = pygame.mixer.Sound("../../Sound Effects/breakgravel1.ogg")
    breakWoodSound  = pygame.mixer.Sound("../../Sound Effects/breakwood1.ogg")
    breakStoneSound  = pygame.mixer.Sound("../../Sound Effects/breakstone3.ogg")
    breakLeafSound  = pygame.mixer.Sound("../../Sound Effects/breakleaf.ogg")
    breakGrassSound.set_volume(0.1)
    breakDirtSound.set_volume(0.1)
    breakWoodSound.set_volume(0.1)
    breakStoneSound.set_volume(0.1)
    breakLeafSound.set_volume(0.1)  
except:
    print("no audio device found")
    audio=False

def getGrassSound():
    return grassSound

def playMusic():
    # Loading and playing background music:

    pygame.mixer.music.load('MainGame/Assets/SelfExploration.wav')
    pygame.mixer.music.play(-1, 0.0) #-1 makes the track loop infintely, play from 0th second
    pygame.mixer.music.set_volume(0.5)

def stopMusic():
    pygame.mixer.music.stop()
    
def playSoundforID(id): #takes in block id from playerHandler and plays the appropriate sound
    if id==0 and audio:
        grassSound.play()
    
    elif id==1 and audio:
        dirtSound.play()
    elif (id==8 or id==5 or id==7) and audio:
        woodSound.play()
    elif id==6 and audio:
        leafSound.play()
    elif audio:
        stoneSound.play()
    
def playBreakSoundforID(id): #takes in id from breakPlaceHandler.py and plays the breaking sound for that block
    if id==0 and audio:
        breakGrassSound.play()
    if id==1 and audio:
        breakDirtSound.play()
    if (id==8 or id==5 or id==7) and audio:
        breakWoodSound.play()
    if id==6 and audio:
        breakLeafSound.play()
    elif audio:
        breakStoneSound.play() #covers blocks like diamon, iron etc
