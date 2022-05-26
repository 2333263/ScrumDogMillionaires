import pygame
pygame.mixer.init()
grassSound = pygame.mixer.Sound("Sound Effects\grass3.ogg")
stoneSound = pygame.mixer.Sound("Sound Effects\stone1.ogg")
def playMusic():
    
    #soundObj.play()
    # Loading and playing background music:

    pygame.mixer.music.load('SelfExploration.wav')
    pygame.mixer.music.play(-1, 0.0) #-1 makes the track loop infintely, play from 0th second

def stopSoundEffect():
    pygame.mixer.Sound.set_volume(0)

def playSoundforID(id): #takes in block id from playerHandler and plays the appropriate sound
    # 0 : "Grass",
    # 2 : "Stone"
    if id==0:
        pygame.mixer.Sound.set_volume(1)
        pygame.mixer.Sound.play(grassSound)
    elif id==2:
        pygame.mixer.Sound.set_volume(1)
        pygame.mixer.Sound.play(stoneSound)
