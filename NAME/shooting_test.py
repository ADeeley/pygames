
#  if space is a keydown event then append [x,y] to the lazer list

# ---loop--- for every elementin the list apply the speed change 
# blit a square to the game display with the coordinates of each square





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
pygame.display.set_caption("Bouncing_block")

gameExit = False
fps = 30
clock = pygame.time.Clock()


#------------Game functions---------------------------------------------------------
block_X_change = 10 # should be out of the loop, as they will constantly be redefined
block_Y_change = 5
   
#------------Main program loop---------------------------------------------------------
def gameLoop(block_X_change, block_Y_change): 
        gameExit = False
        gameOver = False
        block_x = 50
        block_y = 50
        blockSize = 50
        
        #define [x, y] as lazer start points 
        XnY = [600,400]
        # define speed as the rate of change
        speed = 1
        # list to store lazers
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
                            lazer_list.append(XnY)
            gameDisplay.fill(WHITE)
            

            for el in range(len(lazer_list)-1):
                try:
                    lazer_list[el][1] -= speed
                    if lazer_list[el][1] <= 0:
                        del lazer_list[el][1]
                except:
                    break



            block_x += block_X_change
            block_y += block_Y_change
            
            #box logic
#            if block_x > size[0]-blockSize or block_x < 0:
#                block_X_change = block_X_change*-1
#            if block_y> size[1]-blockSize or block_y < 0:
#                block_Y_change = block_Y_change*-1
                
            print lazer_list  
            print block_x, block_y, block_X_change, block_Y_change
            pygame.draw.rect(gameDisplay, BLACK, [block_x, block_y, blockSize, blockSize])


            pygame.display.update()
            
            clock.tick(fps)    

        pygame.quit() # uninitialise pygame
        quit()
        
gameLoop(block_Y_change, block_Y_change)