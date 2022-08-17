import pygame
import sys
sys.path.append("../Scrum-Dog-Millionaires")
import gameSettings as gs
from ChunkGenerator import generateChunk
import playerHandler as ph
import Camera as cam


class MinePy:
    def __init__(self):
        pygame.init()
        #self.screen = pygame.display.set_mode((gs.width, gs.height))
        self.screen = pygame.Surface((gs.width, gs.height))
        self.clock = pygame.time.Clock()
        self.game_speed = 60
        #self.mode = 0
        self.player = ph.Player((gs.width/2 - gs.blockSize * 4, - gs.blockSize*2), gs.blockSize)
        self.camera = cam.Camera(self.player)
        self.worldBlocks = pygame.sprite.Group()
        self.collisionblocks = self.worldBlocks 
        gs.generatedChunks[0] = generateChunk(0, self.worldBlocks)

        
        
    def action(self, action):
        if action == 0:
            self.player.jump()
        elif action in [1, 2]:
            self.player.MoveOnX({}, action)
     

        self.player.update(self.clock.tick(), self.worldBlocks)  #may need to change to collison blocks later
        print(self.player.getPlayerPos())

    def evaluate(self):
        #if player die return -69 else yes
        return 0    

    def is_done(self):
        return False
    
    def observe(self):
        #RGB array?? --> views
        return self.player.getPlayerPos()

    #Should be RGB array in future? 
    def view(self):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                quit()

        #DO drawing 
        bg = pygame.Rect(0, 0, gs.width, gs.height)
        pygame.draw.rect(self.screen, (0, 0, 0), bg)
        self.collisionblocks = self.camera.draw(self.screen, self.worldBlocks)
        #pygame.display.update()
        pygame.display.flip()
        self.clock.tick(self.game_speed)                    

    