import pygame
import gameSettings as gs

#game menus

#information menu- pops up when user clicks the ? button on main menu
def infoMenu(screen, clock, infoPage):
    browsing= True #the user has paused the game
    while browsing:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: #if the user clicks escape, exit information menu
                    browsing=False
        screen.blit(infoPage,(220,100) ) #display the information screen
        pygame.display.update()
        clock.tick(60)


#pause menu - pops up when user clicks key "p"
def pauseMenu(screen, clock, pausePage):
    paused= True #the user has paused the game
    while paused:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c or event.key==pygame.K_ESCAPE: #if the user clicks c, resume game
                    paused=False
                elif event.key==pygame.K_q: #if the user clicks q, quit game
                    pygame.quit()
                    quit()
        screen.blit(pausePage,(0,0) ) #display the pause screen
        pygame.display.update()
        clock.tick(60)
def mouseOffPause( clock):
    paused= True #the user has paused the game
    while paused:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if (event.type == pygame.ACTIVEEVENT):
                if (event.gain == 1):
                    paused=False
        
        pygame.display.update()
        clock.tick(60)

#end menu - pops up when user enters the portal
def endMenu(screen, clock, endPage):
    completed= True #the user has paused the game
    while completed:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c or event.key==pygame.K_ESCAPE: #if the user clicks c, resume game
                    completed=False
                    gs.drawPortal = False
                    
                elif event.key==pygame.K_q: #if the user clicks q, quit game
                    pygame.quit()
                    quit()
            
        screen.blit(endPage,(0,0) ) #display the pause screen
        pygame.display.update()
        clock.tick(60)
