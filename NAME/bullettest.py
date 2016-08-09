
import pygame
import time
import random
import math
x= pygame.init()

#Softcoded variables
display_width = 1000
display_height = 600
FPS= 15

#colors
white = (255, 255, 255)
black = (0, 0 ,0)

red =   (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 200)
yellow= (255, 200, 0)

l_red =   (255, 0, 0)
l_green = (0, 255, 0)
l_blue = (0, 0, 255)
l_yellow= (255, 255, 0)

d_blue = (0, 0, 125)
ll_blue = (155, 155, 255)

##img= pygame.image.load('snake_head.png')
##apple= pygame.image.load("myapple2.png")
smallfont = pygame.font.Font("Helvetica-Condensed-Light.otf", 25)    #create a font object with size= 25
medfont = pygame.font.Font("Helvetica-Condensed-Light.otf", 50)
largefont = pygame.font.Font("Helvetica-Condensed-Light.otf", 75)
clock = pygame.time.Clock()     #Make a Clock object


tankWidth = 40
tankHeight = 20
turretWidth = 3
wheelWidth = 5
turretLength = 25
ground_height = 35



enemyTankX = display_width* 0.1
enemyTankY = display_height* 0.9
enemy_turretAngle= -240
enemy_gunX= 0
enemy_gunY= 0


screen= gameDisplay = pygame.display.set_mode((display_width, display_height))   #The surface for displaying with size specified in a tuple of width and height
pygame.display.set_caption('Tanks')               #Adding the title aka caption for the game
#icon = pygame.image.load('myapple2.png')
#pygame.display.set_icon(icon)


#Pause
def pause():
    paused = True

    message_to_screen("Paused", black, -100, size= "large")
    message_to_screen("Press 'C' to continue or 'Q' to quit", black, 25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        clock.tick(5)

#Controls
def game_controls():
    gcont = True

    while gcont:

        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        
        gameDisplay.fill(white)
        message_to_screen("Controls",
                         green,
                         -125,
                         "large")
        message_to_screen("Fire: Spacebar",
                          black,
                          -25)
        message_to_screen("Move Turret: Up and Down arrows",
                          black,
                          -0)           
        message_to_screen("Move Tank: Left and Right arrows",
                          black,
                          25)
        message_to_screen("Pause: P",
                              black,
                              50,
                              size= "small")

        button("play", 300+60, 300+100, 80, 50, green, l_green, action = "play")
        #button("menu", 160, 300, 80, 50, yellow, l_yellow,action= "menu")
        button("quit", 300+260, 300+100, 80, 50, red, l_red, action= "quit")
        pygame.display.update()
        clock.tick(15)

#Score
def score(score):
     text = smallfont.render("Score: "+ str(score), True, black)
     gameDisplay.blit(text, [0, 0])
     
def text_objects(text, color, size):
    if size == "small":
        textSurface= smallfont.render(text, True, color)        #render msg, Antialiasing = True, color
    elif size == "medium":
        textSurface= medfont.render(text, True, color)
    elif size == "large":
        textSurface= largefont.render(text, True, color)        
    return textSurface, textSurface.get_rect()

def text_to_button(msg, color, buttonX, buttonY, buttonWidth, buttonHeight, size= "small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center=  buttonX+buttonWidth/2, buttonY+buttonHeight/2
    gameDisplay.blit(textSurf, textRect)

#Message function
def message_to_screen(msg, color, y_displace=0, size = "small" ):
    textSurf, textRect= text_objects(msg, color, size)
    textRect.center= (display_width/2), (display_height/2)+y_displace
    gameDisplay.blit(textSurf, textRect)
    
#Button function
def button(text, x, y, width, height, inactive_color, active_color, action= None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)

    if x < cur[0]< x+width and y < cur[1] < y+height:
        pygame.draw.rect(gameDisplay, active_color, (x, y, width, height))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()
            if action == "controls":
                game_controls()
            if action == "play":
                gameLoop()
            if action == "menu":
                pass
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, width, height))
    text_to_button(text, black, x, y, width, height)





#Barrier
def barrier(xlocation, randomHeight, barrier_width):

    pygame.draw.rect(gameDisplay, black, [xlocation, display_height-randomHeight, barrier_width, randomHeight])

    
#Tank
def tank(x, y, angle):
    x = int(x)
    y = int(y)

    angle = 3.14159/180*angle  
    
    pygame.draw.circle(gameDisplay, black, (x, y), int(tankHeight/2))
    pygame.draw.rect(gameDisplay, black, (x-int(tankWidth/2), y, tankWidth, tankHeight))

    pygame.draw.line(gameDisplay, black, (x, y), (x+math.sin(angle)*turretLength, y+math.cos(angle)*turretLength), turretWidth)

    startX = int(tankWidth/2-wheelWidth)
    for i in range(7):
        pygame.draw.circle(gameDisplay, black, (x-startX, y+int(tankHeight)), wheelWidth)
        startX -= 5
    return (int(x+math.sin(angle)*turretLength), int(y+math.cos(angle)*turretLength))


#Enemy Tank
def enemy_tank(x, y, angle, color):
    x = int(x)
    y = int(y)

    angle = 3.14159/180*angle  
    
    pygame.draw.circle(gameDisplay, color, (x, y), int(tankHeight/2))
    pygame.draw.rect(gameDisplay, color, (x-int(tankWidth/2), y, tankWidth, tankHeight))

    pygame.draw.line(gameDisplay, color, (x, y), (x+math.sin(angle)*turretLength, y+math.cos(angle)*turretLength), turretWidth)

    startX = int(tankWidth/2-wheelWidth)
    for i in range(7):
        pygame.draw.circle(gameDisplay, color, (x-startX, y+int(tankHeight)), wheelWidth)
        startX -= 5
    return (int(x+math.sin(angle)*turretLength), int(y+math.cos(angle)*turretLength))


#Enemy Turret Rotate
def enemy_turret_rotate(theta):

    global enemyTankX
    global enemyTankY
    global enemy_turretAngle
    global enemy_gunX
    global enemy_gunY

    angle = enemy_turretAngle
    
    radAngle= 3.14159/180*angle
    x= int(enemyTankX)
    y= int(enemyTankY)
    

    while  int(theta)!= int(angle):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.draw.circle(gameDisplay, white, (x, y), int(tankHeight/2))
        pygame.draw.line(gameDisplay, white, (x, y), (x+math.sin(radAngle)*turretLength, y+math.cos(radAngle)*turretLength), turretWidth)
        
        if angle < theta:
            angle+= 1
        else:
            angle-= 1

        radAngle= 3.14159/180*angle
        pygame.draw.circle(gameDisplay, black, (x, y), int(tankHeight/2))
        pygame.draw.line(gameDisplay, black, (x, y), (x+math.sin(radAngle)*turretLength, y+math.cos(radAngle)*turretLength), turretWidth)
        
        pygame.display.update()
        clock.tick(15)
    enemy_turretAngle= angle
    enemy_gunX= int(x+math.sin(radAngle)*turretLength)
    enemy_gunY= int(y+math.cos(radAngle)*turretLength)
        
def enemy_thinking(mainTankX, mainTankY, xlocation, barrierWidth, randomHeight):

    global enemyTankX
    global enemyTankY
    global enemy_turretAngle
    global enemy_gunX
    global enemy_gunY
    enemy_gun= enemy_gunX, enemy_gunY

    thinking= True

    power = 80
    v= 10 + 10*power/100
    targetX = mainTankX- enemyTankX
    gravity= 0.5
    theta= 0

    while thinking:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        targetX = mainTankX-tankHeight/2- enemyTankX
        enemy_gun= enemy_gunX, enemy_gunY

        #Adjustments
        try:
            if targetX>0.87*display_width:
                print("Over Over")
                Log_display("Over Over", targetX)
                theta= math.asin(gravity*targetX/v/v)/2.3*180/3.14159
            elif targetX>0.85*display_width:
                print("Over")
                Log_display("Over", targetX)
                theta= math.asin(gravity*targetX/v/v)/2.2*180/3.14159
            elif targetX>0.78*display_width:
                print("Over Mid")
                Log_display("Over Mid", targetX)
                theta= math.asin(gravity*targetX/v/v)/2.1*180/3.14159
            elif targetX>0.60*display_width:
                print("Mid")
                Log_display("Mid", targetX)
                theta= math.asin(gravity*targetX/v/v)/2.05*180/3.14159
            elif targetX>0.30*display_width:
                print("Under Mid")
                Log_display("Under Mid", targetX)
                theta= math.asin(gravity*targetX/v/v)/2*180/3.14159
            else:
                print("Under")
                Log_display("Under Under", targetX)
                theta= math.asin(gravity*targetX/v/v)/1.8*180/3.14159

            thinking = False
            print(theta)
            enemy_turret_rotate(-270+90-theta)
            enemy_fireShell(mainTankX, mainTankY, enemyTankX, enemyTankY, -270+90-theta, power, xlocation, barrierWidth, randomHeight)
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")
            enemy_tank(enemyTankX, enemyTankY, enemy_turretAngle, white)
            enemyTankX+=1
            enemy_gunX, enemy_gunY= enemy_tank(enemyTankX, enemyTankY, enemy_turretAngle, black)
            pygame.display.update()
            

        
    
        

        
def enemy_explosion(x, y, size=50):
    explode= True

    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        startPoint= x, y
        colorChoices = [ll_blue, d_blue, blue, l_blue]
        magnitude = 1

        while magnitude < size:
            exploding_bit_x  = x #+ random.randrange(-1*magnitude, magnitude)
            exploding_bit_y  = y #+ random.randrange(-1*magnitude, magnitude)
            pygame.draw.circle(gameDisplay, colorChoices[random.randrange(0, 4)], (exploding_bit_x, exploding_bit_y), 2)#random.randrange(1, 5))
            magnitude += 1
            pygame.display.update()
            clock.tick(100)
        explode = False

 
def enemy_fireShell(mainTankX, mainTankY, tankX, tankY, turretAngle, TurretPower, xlocation, barrierWidth, randomHeight):

    global enemyTankX
    global enemyTankY
    global enemy_turretAngle
    global enemy_gunX
    global enemy_gunY

    tankX= enemyTankX
    tankY= enemyTankY
    turretAngle= enemy_turretAngle
    xy = (enemy_gunX, enemy_gunY)


    gravity = 0.5
    TurretVelocity= 10 + 10* TurretPower/100
    turretAngle -= 90 
    angle = 3.14159/180*turretAngle
    velocityX= TurretVelocity*math.cos(angle)
    velocityY= TurretVelocity*math.sin(angle)


    fire = True

    shell = list(xy)
    print("FIRE!", xy, turretAngle)

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print(int(shell[0]), int(shell[1]))
        pygame.draw.circle(gameDisplay, l_blue, (int(shell[0]), int(shell[1])), 2)

        shell[0] += velocityX
        shell[1] -= velocityY
        velocityY-= gravity


        

        #Ground Collision
        if shell[1]>= display_height-ground_height:
            print("Ground:", shell[0], shell[1])
            #hit_x = int((shell[0]*display_height-ground_height)/shell[1])
            hit_x = int((shell[0]))
            hit_y = int(shell[1])
            print("Impact:", hit_x, hit_y)
            enemy_explosion(hit_x, hit_y)
            fire = False
            continue



        #Player tank HEAD Collision
        check_x_1 = shell[0] <= mainTankX+int(tankHeight/2)
        check_x_2 = shell[0] >= mainTankX-int(tankHeight/2)

        check_y_1 = shell[1] <= mainTankY+int(tankHeight/2)
        check_y_2 = shell[1] >= mainTankY-int(tankHeight/2)

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            print("Player Tank HEAD SHOT!!:", shell[0], shell[1])
            hit_x = int(shell[0])
            hit_y = int(shell[1])
            print("Impact:", hit_x, hit_y)
            enemy_explosion(hit_x, hit_y)
            fire = False
            continue



        #Player tank BODY Collision
        check_x_1 = shell[0] <= mainTankX+int(tankWidth/2)
        check_x_2 = shell[0] >= mainTankX-int(tankWidth/2)

        check_y_1 = shell[1] <= mainTankY+tankHeight
        check_y_2 = shell[1] >= mainTankY

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            print("Player Tank Body hit!!:", shell[0], shell[1])
            hit_x = int(shell[0])
            hit_y = int(shell[1])
            print("Impact:", hit_x, hit_y)
            enemy_explosion(hit_x, hit_y)
            fire = False
            continue




        #Barrier Collision
        check_x_1 = shell[0] <= xlocation + barrierWidth
        check_x_2 = shell[0] >= xlocation

        check_y_1 = shell[1] <= display_height-ground_height
        check_y_2 = shell[1] >= display_height-randomHeight

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            print("Last shell:", shell[0], shell[1])
            hit_x = int(shell[0])
            hit_y = int(shell[1])
            print("Impact:", hit_x, hit_y)
            enemy_explosion(hit_x, hit_y)
            fire = False
        
        pygame.display.update()
        clock.tick(60)



def explosion(x, y, size=50):
    explode= True

    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        startPoint= x, y
        colorChoices = [red, l_red, yellow, l_yellow]
        magnitude = 1

        while magnitude < size:
            exploding_bit_x  = x + random.randrange(-1*magnitude, magnitude)
            exploding_bit_y  = y + random.randrange(-1*magnitude, magnitude)
            pygame.draw.circle(gameDisplay, colorChoices[random.randrange(0, 4)], (exploding_bit_x, exploding_bit_y), random.randrange(1, 5))
            magnitude += 1
            pygame.display.update()
            clock.tick(100)
        explode = False


def fireShell(xy, tankX, tankY, turretAngle, TurretPower, xlocation, barrierWidth, randomHeight):
    gravity = 0.5
    TurretVelocity= 10 + 10* TurretPower/100
    turretAngle -= 90 
    angle = 3.14159/180*turretAngle
    velocityX= TurretVelocity*math.cos(angle)
    velocityY= TurretVelocity*math.sin(angle)


    fire = True

    shell = list(xy)
    print("FIRE!", xy, turretAngle)

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print(int(shell[0]), int(shell[1]))
        pygame.draw.circle(gameDisplay, l_red, (int(shell[0]), int(shell[1])), 2)

        shell[0] += velocityX
        shell[1] -= velocityY
        velocityY-= gravity


        #Ground Collision
        if shell[1]>= display_height-ground_height:
            print("Ground:", shell[0], shell[1])
            hit_x = int((shell[0]*display_height-ground_height)/shell[1])
            hit_y = int(display_height-ground_height)
            print("Impact:", hit_x, hit_y)
            explosion(hit_x, hit_y)
            fire = False
            continue



        #Enemy tank HEAD Collision
        check_x_1 = shell[0] <= enemyTankX+int(tankHeight/2)
        check_x_2 = shell[0] >= enemyTankX-int(tankHeight/2)

        check_y_1 = shell[1] <= enemyTankY+int(tankHeight/2)
        check_y_2 = shell[1] >= enemyTankY-int(tankHeight/2)

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            print("Enemy Tank HEAD SHOT!!:", shell[0], shell[1])
            hit_x = int(shell[0])
            hit_y = int(shell[1])
            print("Impact:", hit_x, hit_y)
            explosion(hit_x, hit_y)
            fire = False
            continue



        #Enemy tank BODY Collision
        check_x_1 = shell[0] <= enemyTankX+int(tankWidth/2)
        check_x_2 = shell[0] >= enemyTankX-int(tankWidth/2)

        check_y_1 = shell[1] <= enemyTankY+tankHeight
        check_y_2 = shell[1] >= enemyTankY

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            print("Enemy Tank Body hit!!:", shell[0], shell[1])
            hit_x = int(shell[0])
            hit_y = int(shell[1])
            print("Impact:", hit_x, hit_y)
            explosion(hit_x, hit_y)
            fire = False
            continue




        #Barrier Collision
        check_x_1 = shell[0] <= xlocation + barrierWidth
        check_x_2 = shell[0] >= xlocation

        check_y_1 = shell[1] <= display_height-ground_height
        check_y_2 = shell[1] >= display_height-randomHeight

        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            print("Barrier:", shell[0], shell[1])
            hit_x = int(shell[0])
            hit_y = int(shell[1])
            print("Impact:", hit_x, hit_y)
            explosion(hit_x, hit_y)
            fire = False
            continue 
            
            
        pygame.display.update()
        clock.tick(60)

def range_display(range):
    textSurf, textRect= text_objects("Range: "+str(range), black, "small")
    textRect.center= (display_width/2), 50
    if (range)<0:
        return
    gameDisplay.blit(textSurf, textRect)

def Log_display(string, value):
    textSurf, textRect= text_objects(string+": "+str(value), black, "small")
    textRect.center= (display_width/2), 60
    gameDisplay.blit(textSurf, textRect)

def power_display(level, angle):
    textSurf, textRect= text_objects("Power: "+str(level)+"%", black, "small")
    textSurf1, textRect1= text_objects("Angle: "+str(270-angle), black, "small")
    textRect.center= (display_width/2), 10
    textRect1.center= (display_width/2), 35
    gameDisplay.blit(textSurf, textRect)
    gameDisplay.blit(textSurf1, textRect1)

    
def game_intro():
    intro = True

    while intro:

        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro= False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        
        gameDisplay.fill(white)
        message_to_screen("Tanks",
                         green,
                         -125,
                         "large")
        message_to_screen("The objective is to shoot and destroy",
                          black,
                          -25)
        message_to_screen("the enemy tanks before they destroy you,",
                          black,
                          -0)           
        message_to_screen("also as they get more challenging with time",
                          black,
                          25)
##        message_to_screen("Press 'C' to play, 'P' to pause or 'Q' to quit",
##                              black,
##                              75,
##                              size= "small")

        button("play", 300+60, 300+100, 80, 50, green, l_green, action = "play")
        button("controls", 300+160, 300+100, 80, 50, yellow, l_yellow,action= "controls")
        button("quit", 300+260, 300+100, 80, 50, red, l_red, action= "quit")
        pygame.display.update()
        clock.tick(15)


#Main Game Loop
def gameLoop():
    
    gameExit = False
    gameOver = False
    FPS= 15

    mainTankX = display_width* 0.9
    mainTankY = display_height* 0.9
    tankMove= 0
    turretAngle= 240
    turretRotate = 0
    deltaAngle = 5
    rangeStart = 180
    rangeEnd = 270



    global enemyTankX
    enemyTankX = display_width* 0.025
    global enemyTankY
    global enemy_turretAngle
    global enemy_gunX
    global enemy_gunY
    

    fire_power = 100
    powerChange = 0
    
    xlocation =  (display_width/2) + random.randint(-0.2*display_width, +0.2*display_width)   
    randomHeight = random.randrange(display_height*0.1, display_height*0.6)
    barrierWidth = 50
    while not gameExit:                                 #Main game loop: Events must be processed in this main thread; Refer: http://www.pygame.org/docs/ref/event.html 
        
        #Game over
        if gameOver == True:
            message_to_screen("Game over",
                              red,
                              -50,
                              size= "large")
            
            message_to_screen("Press 'C' to play again or 'Q' to quit",
                              black,
                              20,
                              size= "small")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:       #When the window is closed
                    gameExit =True
                    gameOver =False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:         #If Q, exit
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:         #If C, restart Main loop
                        gameLoop()
        
        for event in pygame.event.get():                #iterate through all events from the event queue
            print(event)
            if event.type == pygame.QUIT:                #When the window is closed
                gameExit =True
            if event.type == pygame.KEYDOWN:             #When any key is pressed down
                if event.key == pygame.K_p:
                    pause()
                elif event.key == pygame.K_LEFT:           #Left arrow key
                    tankMove = -5
                    #mainTankX -= 5
                elif event.key == pygame.K_RIGHT:          #Right arrow
                    tankMove = 5
                    #mainTankX += 5
                elif event.key == pygame.K_UP and turretAngle>rangeStart:             #Up arrow
                    turretRotate = -deltaAngle
                elif event.key == pygame.K_DOWN and turretAngle<rangeEnd:           #Down arrow
                    turretRotate = deltaAngle
                elif event.key == pygame.K_SPACE:
                    tankMove = 0
                    turretRotate = 0
                    powerChange = 0
                    fireShell(gun, mainTankX, mainTankY, turretAngle, fire_power, xlocation, barrierWidth, randomHeight)
                    enemy_thinking(mainTankX, mainTankY, xlocation, barrierWidth, randomHeight)
                    #print("Returned angle: "+str(enemy_turretAngle))
                    #enemy_fireShell(enemy_gun, enemyTankX, enemyTankY, enemy_turretAngle, fire_power, xlocation, barrierWidth, randomHeight)
                elif event.key == pygame.K_d:
                    powerChange = 1
                elif event.key == pygame.K_a:
                    powerChange = -1
                                
            if event.type == pygame.KEYUP:              #Key released
                if event.key == pygame.K_LEFT and tankMove== -5:#Left arrow key
                    tankMove = 0
                elif event.key == pygame.K_RIGHT and tankMove== +5:       #Right arrow
                    tankMove = 0
                elif event.key == pygame.K_UP:             #Up arrow
                    turretRotate = 0
                elif event.key == pygame.K_DOWN:           #Down arrow
                    turretRotate = 0
                elif event.key == pygame.K_d and powerChange== 1:
                    powerChange = 0
                elif event.key == pygame.K_a and powerChange== -1:
                    powerChange = 0

        if turretRotate==-deltaAngle and turretAngle<=rangeStart:             #Up arrow
                    turretRotate = 0
                    turretAngle = rangeStart
        elif turretRotate==deltaAngle and turretAngle>=rangeEnd:             #Up arrow
                    turretRotate = 0
                    turretAngle = rangeEnd

        if powerChange==-1 and fire_power<=25:             #Up arrow
                    powerChange = 0
                    fire_power = 25
        elif powerChange==1 and fire_power>=110:             #Up arrow
                    powerChange = 0
                    fire_power = 110

        if mainTankX - tankWidth/2 < xlocation + barrierWidth:
            mainTankX += 5


        gameDisplay.fill(white)                         #Fills the entire background with a color, used to mostly clear the screen
        gun = tank(mainTankX, mainTankY, turretAngle)
        enemy_gunX, enemy_gunY = tank(enemyTankX, enemyTankY, enemy_turretAngle)
        fire_power += powerChange

        
        
        mainTankX += tankMove
        #enemyTankX = display_width-mainTankX
        turretAngle += turretRotate
        power_display(fire_power, turretAngle)
        barrier(xlocation, randomHeight, barrierWidth)

        #ground
        gameDisplay.fill(green, rect= [0, display_height-ground_height, display_width, ground_height])


        
        pygame.display.update()
        clock.tick(FPS)                #Define the FPS here, defined as 15FPS!!! This directly controls the amount of processing power required, so keep it low.



    pygame.quit()           #Quit pygame, i.e, uninitialize pygame
    quit()                  #Exit out of python

game_intro()
gameLoop()    