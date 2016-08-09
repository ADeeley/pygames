import pygame
import time
import random
import math

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,180,0)
RED = (255,0,0)

#------Initialising the game----------------------------------------------------------
pygame.init()
size = (800,600)
gameDisplay = pygame.display.set_mode(size)
pygame.display.set_caption("Invasion Super-Nautica")

gameExit = False
Lazer = False

playerSize = 30
lazerSpeed = 20
lazerXnY = [size[0]/2, size[1]-playerSize]

fps = 30

angle = 150
angle = 10.0
turretLength = 50

clock = pygame.time.Clock()

#------------Game functions---------------------------------------------------------

def draw_player():
    '''Draws the player as a sprite, maybe a turret'''
    pass
    
def draw_enemy():
    '''Draws the enemy sprite in a random location in the top three quarters of the screen
    '''
    pass

def fire_lazer(lazerXnY, lazer_list):
    '''Prints a lazer to the screen. Includes physics for the lazer'''
    for element in lazer_list:
        yield pygame.draw.rect(gameDisplay, RED, [lazerXnY[0], lazerXnY[1], playerSize/2, playerSize/2])
    
def turret(angle):
    line_x = size[0]/2
    line_y = size[1]
    line_xa = size[0]/2
    line_ya = size[1]-50
    
    rotate = (int(line_xa+math.sin(angle)*turretLength), int(line_ya+math.cos(angle)*turretLength))
    
    pygame.draw.line(gameDisplay, BLACK, [line_x, line_y],[rotate[0], rotate[1]], 10)

    
def enemy_death():
    '''The death of an enemy. Flashes red and disappears'''
    pass
    
def player_death():
    '''The player has taken x amount of damage and dies. Breaks the loop and displays the
    final score'''
    pass
    
def score():
    '''keeps a track of and displays the score when called'''
    pass       
            
def player_health():
    '''keeps a track of the player health and calls player_death when 0'''
    pass
    
#------------Main program loop---------------------------------------------------------
def gameLoop(angle): 
        global Lazer
        gameExit = False
        gameOver = False
        lazer_list = []
        while not gameExit:
            
            while gameOver:
                gameDisplay.fill(WHITE)
                message_to_screen("Game Over", red, -50)
                message_to_screen("Press C to play again or Q to quit,", black, 50)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameExit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            gameExit = True
                            gameOver = False
                        if event.key == pygame.K_c:
                            gameLoop()
                
            for event in pygame.event.get(): # built in event handling
                if event.type == pygame.QUIT:
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        lazer_list.append(lazerXnY)
                        fire_lazer(lazerXnY,lazer_list).next()
                    if event.key == pygame.K_a:
                        angle-=0.2
                    if event.key == pygame.K_d:
                        angle+=0.2
            gameDisplay.fill(WHITE)
 #           if lazerXnY[1]<0:
 #               Lazer = False
            
   #         if Lazer == True:
   #             fire_lazer(lazerXnY)
    #            lazerXnY[1] -= 5
            print lazer_list

            for L in range(len(lazer_list)-1):
                lazerXnY[L] -=5
        #        fire_lazer(lazerXnY[L])
                
                
##            if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
##                gameOver = True

            pygame.draw.rect(gameDisplay, BLACK, [size[0]/2-playerSize/2, size[1]-playerSize, playerSize, playerSize])
      #      turret(angle)
            
            pygame.display.update()
            
            clock.tick(fps)    

        pygame.quit() # uninitialise pygame
        quit()
        
gameLoop(angle)