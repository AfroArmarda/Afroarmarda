import pygame
import random
import time
import playerClass
import Highscores
from tkinter import *

#SETTING UP SCREEN 
#initialising pygame
pygame.init()
direction = 0

easterEgg = 0
#setting screen dimensions
displayWidth = 900
displayHeight = 575

#setting screen and giving it a caption 
gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption("Afro Armada")

#loading in the background image
background = pygame.image.load("road_background.png")

#changing icon for window 
icon = pygame.image.load("character.png")
pygame.display.set_icon(icon)

#define colours (red green blue)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
yellow = (227,207,87)
blue = (0,0,255)
orange = (255,140,0)

#CHARACTER
#setting character dimensions for colision boundaries 
characterThickness = 40
characterHeight = 83

#character health bar length
HealthLength = 400
HealthHeight = 20
HealthLengthR = 400

#player kills 
kills = 0

#Counts the number of round a player completes as the roundNum variable loops
#back round after 4 
roundCounter = 1 

#BULLET
#bullet variables
bulletLen = 5
bx = 0
by = 0

#FIRE
#fire variables and loading in the fire image 
character_f = pygame.image.load("character_fire.png")

##fire1 = pygame.image.load("fire1.png")
##fire2 = pygame.image.load("fire2.png")
##fire3 = pygame.image.load("fire3.png")
##
##fireX = 500
##fireY = 400

#CLOCK SPEED
#defining FPS
clock = pygame.time.Clock()
FPS = 20

#setting variable for the round timer 
countDown = -1
timer = "60"

#round number
roundNum = 1
#setting false to make loop for the game to loop through the events 
gameExit = False

class bullet:
    def __init__(self, flip, bulletX, bulletY):
        
        self.flip = flip
        self.direction = direction
        self.bulletX = bulletX
        self.bulletY = bulletY


    def Move(self):
        #finding out what direction the character is facing to see what direction the bullet needs to go
        if self.flip == True:
            self.direction = -40
        else:
            self.direction = 40
    
        self.bulletX += self.direction
        
        return self.bulletX

    def getBulletX(self):
        return self.bulletX

    def getBulletY(self):
        return self.bulletY
        
class enemy:
    def __init__(self, load_x, load_y, E_load_x, E_load_y, Ehealthlength):
        self.load_x = load_x
        self.load_y = load_y
        self.E_load_y = E_load_y
        self.E_load_x = E_load_x
        self.Ehealthlength = Ehealthlength

    def Zmove(self, load_x, load_y):

        #sets the move to 0 so it doesn't infinately accellerate 
        EmoveX = 0
        EmoveY = 0

        #checks if the x and y are bigger or smaller than its position
        if self.E_load_x > self.load_x:
            EmoveX -= 2.5 

        if self.E_load_x < self.load_x:
            EmoveX += 2.5

        if self.E_load_y > self.load_y:
            EmoveY -= 2.5

        if self.E_load_y < self.load_y:
            EmoveY += 2.5

        #updates them so they're closer to the character position
        self.E_load_x += EmoveX
        self.E_load_y += EmoveY

        #flipping the enemy image so that it can face the right way  
        enemy_R = pygame.image.load("enemy.png")
        enemy_L = pygame.transform.flip(enemy_R, True, False)

        enemy_R_W = pygame.image.load("enemy_walk.png")
        enemy_L_W = pygame.transform.flip(enemy_R_W, True, False)

        #checks if the move variable is positive or negative so it knows which way the character needs to face 
        if EmoveX >= 0:

            #devides the current position so that it will display a different image depending on the result to make a walk animation   
            if self.E_load_x % 2 == 0:
                enemyDirection = enemy_R = pygame.image.load("enemy.png")

            if self.E_load_x % 2 != 0:
                enemyDirection = enemy_R_W = pygame.image.load("enemy_walk.png")

        if EmoveX < 0:

            if self.E_load_x % 2 == 0:
                enemyDirection = enemy_L = pygame.transform.flip(enemy_R, True, False)

            if self.E_load_x % 2 != 0:
                enemyDirection = enemy_L_W = pygame.transform.flip(enemy_R_W, True, False)

        return enemyDirection

    def enemyX(self):
        return self.E_load_x

    def enemyY(self):
        return self.E_load_y

    def Ehealthlength(self):
        return self.Ehealthlength

    def setXY(self, load_x, load_y):
        #to update the character x and y so the enemy knows where the character is 
        self.load_x = load_x
        self.load_y = load_y

    def Ehealthloss(self, damage):
        self.Ehealthlength -= damage


#class for other objects on the screen e.g. healthkits and fires
    
class extraObjects:
    def __init__(self,objX, objY):
    
        self.objX = objX
        self.objY = objY

    def fire(self, randomFire):
        
        if randomFire == 1:
            fireImage = fire1 = pygame.image.load("fire1.png")

        if randomFire == 2:
            fireImage = fire1 = pygame.image.load("fire2.png")
        
        if randomFire == 3:
            fireImage = fire1 = pygame.image.load("fire3.png")

        return fireImage

    def healthkit(self):
        
        healthkit = pygame.image.load("healthkit.png")
        return healthkit
        

    def objectX(self):      
        return self.objX        

    def objectY(self):
        return self.objY

#lists for classes 
blist = []
zlist = []
clist = []
firelist = []
healthlist = []


#putting message on screen function
def message(msg,colour,size,x,y):
    font = pygame.font.SysFont(None,size)
    screenText = font.render(msg,True, colour)
    gameDisplay.blit(screenText,[x,y])
    

##def enemy():
##    global E_load_x
##    global E_load_y
##    global HealthLength
##    global gameExit
##    global EhealthLength
##
##    #importing enemy image and flipping images based on direction 
##    enemy_R = pygame.image.load("enemy.png")
##    enemy_L = pygame.transform.flip(enemy_R, True, False)
##
##    enemy_R_W = pygame.image.load("enemy_walk.png")
##    enemy_L_W = pygame.transform.flip(enemy_R_W, True, False)
##
##    #how much enemy moves by
##    EmoveX = 0 
##    EmoveY = 0
##
##    #setting enemy dimensions
##    enemyThickness = 40
##    enemyHeight = 83
##    
##
##    #making enemy image move toward character        
##    if E_load_x > load_x:
##        EmoveX -= 3.5
##        
##    if E_load_x < load_x:
##        EmoveX += 3.5
##        
##    if E_load_y > load_y:
##        EmoveY -= 3.5
##
##    if E_load_y < load_y:
##        EmoveY += 3.5
##
##DO OUTSIDE OF CLASS
##    #making the enemy image stop moving if it touches the character and taking health off character 
##    if load_x > E_load_x and load_x < E_load_x + enemyThickness or load_x + characterThickness > E_load_x and load_x + characterThickness < E_load_x + enemyThickness:
##            if load_y > E_load_y and load_y < E_load_y + enemyThickness or load_y + characterThickness > E_load_y and load_y + characterThickness < E_load_y + enemyThickness:
##                EmoveX = 0
##                EmoveY = 0
##                HealthLength -= 10
##                if HealthLength < 0:
##                    HealthLength = 0
##                    gameExit = True
##
##    #enemy will move based on values given to variables
##    E_load_x += EmoveX
##    E_load_y += EmoveY
##
##    #loads flipped images depending on which way character is going
##    if EmoveX >= 0:
##
##        if E_load_x % 2 == 0:
##            gameDisplay.blit(enemy_R_W, (E_load_x, E_load_y ))
##
##        if E_load_x % 2 != 0:
##            gameDisplay.blit(enemy_R, (E_load_x, E_load_y ))
##
##    if EmoveX < 0:
##
##        if E_load_x % 2 == 0:
##            gameDisplay.blit(enemy_L_W, (E_load_x, E_load_y ))
##
##        if E_load_x % 2 != 0:
##            gameDisplay.blit(enemy_L, (E_load_x, E_load_y))
##
##    #enemy health bar
##    pygame.draw.rect(gameDisplay, black, [E_load_x - 16, E_load_y -30,85,20])
##    pygame.draw.rect(gameDisplay, green, [E_load_x - 11, E_load_y -26, EhealthLength,12])
##
##
####    if bulletX > E_load_x and bulletX < E_load_x + 47 or bulletX + bulletLen > E_load_x and bulletX + bulletLen < E_load_x + 47:
####        if bulletY > E_load_y and bulletY < E_load_y + 47 or bulletY + bulletLen > E_load_y and bulletY + bulletLen < E_load_y + 47:
####             EhealthLength -= 18
####             if EhealthLength < 0:
####                 EhealthLength = 0
                 
#Function for game start menu and information
def game_pause():

        intro = True
        
        while intro == True:

            gameDisplay.fill(black)
            messages("Paused", red, 70, 370, 50)
            message("Press M to go back to menu", white, 60, 190, 190)
            message("Press I for information", white, 60, 245, 270 )
            message("Press R to resume", white, 60, 295,350)
            message("Press Q to quit", white, 60, 330,430)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        intro = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:

                        gameDisplay.fill(black)
                        message("Instructions and information",red, 50, 210, 20)
                        message("You will spawn  in the middle of the map with 1 minute to survive, zombies will", orange, 33, 30,170)
                        message("spawn. The further you get into the round, the more zombies will spawn and", orange, 33, 45,210)
                        message("the more rounds that you get through, the harder the game will get", orange, 33, 95,250)

                        message("Use the arrow keys to move and space to shoot", orange, 33, 210, 350)

                        message("Press B to go back to the menu", red, 40, 250,500)

                        pygame.display.update()
                        clock.tick(FPS)                   
                            
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    quit()

                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_b:
                                    break 

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        global kills
                        global roundNum
                        global roundCounter
                        global HealthLength
                        global timer
                        global background
                        
                        kills = 0
                        roundNum = 1
                        roundCounter = 1
                        HealthLength = 400
                        timer = "60"
                        zlist.clear()
                        clist.clear()
                        clist.append(playerClass.player(displayWidth/2, displayHeight/2, 0, 0, 0,easterEgg))
                        background = pygame.image.load("road_background.png")
                        game_intro()
                        print(kills, HealthLength)
                        intro = False
                        

    
def game_intro():

    intro = True

    while intro:
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    intro = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:

                    gameDisplay.blit(background, (0, 0))

                    message("Instructions and information",red, 50, 210, 20)
                    message("You will spawn  in the middle of the map with 1 minute to survive, zombies will", orange, 33, 30,170)
                    message("spawn. The further you get into the round, the more zombies will spawn and", orange, 33, 45,210)
                    message("the more rounds that you get through, the harder the game will get", orange, 33, 95,250)

                    message("Use the arrow keys to move and space to shoot", orange, 33, 210, 350)
                    message("Press P to pause the game", orange, 33, 310, 380)

                    message("Press B to go back to the menu", red, 40, 250,500)

                    pygame.display.update()
                    clock.tick(FPS)                   
                        
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_b:
                                break 
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

            gameDisplay.blit(background, (0,0))
            message("To start press S", orange, 50, 325, 400)

            message("For instuctions press I", orange, 50, 270, 200)

            message("To quit press Q", orange, 50, 325, 300)

            message("Welcome to Afro Armada", red, 100, 17, 50)



            pygame.display.update()
            clock.tick(FPS)

    
game_intro()
firelist.append(extraObjects(500,400))
firelist.append(extraObjects(50,200))
firelist.append(extraObjects(700,100))

#player list
clist.append(playerClass.player(displayWidth/2, displayHeight/2, 0, 0, 0,easterEgg))


#loop for events to make character move
while not gameExit:

    #setting backgrounf
    gameDisplay.blit(background, (0, 0))
    
    #ENEMY
    #makes the medkit spawn in a random place 
    healthX = random.randint(30,870)
    healthY = random.randint(30,545)

    #generates random number so that it only spawns medkits when a random number is selected 
    randomMed = random.randint(1,100)
    if randomMed == 25:
        if len(healthlist) < 1:
            #adding healthkit to list
            healthlist.append(extraObjects(healthX, healthY))
        
    
    randomFire = random.randint(1,3)

    E_load_x = random.randint(20,850)
    E_load_y = random.randint(20,557)
        
    
    #count down for timer on the screen when countdown gets to 18 it is equal to a second 
    countDown += 1
    if countDown == 18:
        countDown = -1
        timer = int(timer)
        timer -= 1

    #spwaning enemies based on the time that the user has left, putting them into a long if statement so that there aren't loads of if statements 
    if timer == 58 or timer == 30 or timer == 20 or timer == 50 or timer == 49:
      
        zlist.append(enemy(clist[0].playerX(), clist[0].playerY(), E_load_x, E_load_y,75))
        
    #on the second and third round it adds extra zombies 
    if timer == 40 or timer == 10:
        if roundNum == 2 or roundNum == 3:
            zlist.append(enemy(clist[0].playerX(), clist[0].playerY(), E_load_x, E_load_y,75))

    #adding another zombie on the third round
    if timer == 45:
        if roundNum == 3:
            zlist.append(enemy(clist[0].playerX(), clist[0].playerY(), E_load_x, E_load_y,75))
        
    #changes the varibles such as the background depending on the round number         
            
    timer = str(timer)
    if timer == "0":
        timer = "60"
        HealthLength = 400
        roundCounter += 1

        #to make the rounds reset after 3 rounds so it carries on looping round 
        if roundNum == 3:
            roundNum = 1

        else:
            roundNum += 1

        #when timer gets to 0 zombies and fires all get cleared and only at 0 because otherwise they will keep getting cleared    
        #adding three fires to the list
        if roundNum == 1:
            
            #loading in background image
            background = pygame.image.load("road_background.png")
            zlist.clear()
            firelist.clear()            
            
            firelist.append(extraObjects(500,400))
            firelist.append(extraObjects(50,200))
            firelist.append(extraObjects(700,100))

        if roundNum == 2:
            
            background = pygame.image.load("background2.png")
            zlist.clear()
            firelist.clear()

            #adding in more fires in different locations 
            firelist.append(extraObjects(700,200))
            firelist.append(extraObjects(70,300))
            firelist.append(extraObjects(550,387))
            firelist.append(extraObjects(100,50))

        if roundNum == 3:

            background = pygame.image.load("background3.png")
            zlist.clear()
            firelist.clear()

            firelist.append(extraObjects(800,150))
            firelist.append(extraObjects(380,300))
            firelist.append(extraObjects(550,387))
            firelist.append(extraObjects(220,50))
            firelist.append(extraObjects(90,320))
    


       
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                for i in clist:
                    #method in player class to move left
                    i.playerLeft(True)


            if event.key == pygame.K_RIGHT:
                for i in clist:
                    #method in player class to move right
                    i.playerRight(False)


            if event.key == pygame.K_UP:
                for i in clist:
                    #method in player class to move up
                    i.playerUp()


            if event.key == pygame.K_DOWN:
                for i in clist:
                    #method in player class to move left
                    i.playerDown()

            if event.key == pygame.K_p:
                game_pause()
        


            if event.key == pygame.K_SPACE:
                #adds a bullet to the list to be filed 
                blist.append(bullet(flip,clist[0].playerX() + 40, clist[0].playerY() + 40))
                
            if event.key == pygame.K_j and easterEgg == 0:
                for i in clist:
                    i.EasterEgg()
                    easterEgg += 1
            if event.key == pygame.K_u and easterEgg == 1:
                for i in clist:
                    i.EasterEgg()
                    easterEgg += 1
            if event.key == pygame.K_l and easterEgg == 2:
                for i in clist:
                    i.EasterEgg()
                    easterEgg += 1
            if event.key == pygame.K_i and easterEgg == 3:
                for i in clist:
                    i.EasterEgg()
                    easterEgg += 1
            if event.key == pygame.K_e and easterEgg == 4:
                for i in clist:
                    i.EasterEggReset()
                    easterEgg = 0 
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                for i in clist:
                    #makes sure the chracter stops when the key is lifted
                    i.stop_x()

            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                for i in clist:
                    #makes sure the chracter stops when the key is lifted
                    i.stop_y()

    #displays the different fires on the screen
    for i in firelist:
        fireX = i.objectX()
        fireY = i.objectY()
        fireImage = i.fire(randomFire)

        gameDisplay.blit(fireImage,(fireX, fireY))

        #checks to see if the player is touching the fire 
        if clist[0].playerX() > fireX and clist[0].playerX() < fireX + 70 or clist[0].playerX() + characterThickness > fireX and clist[0].playerX() + characterThickness < fireX + 70:
            if clist[0].playerY() > fireY and clist[0].playerY() < fireY + 63 or clist[0].playerY() + characterThickness > fireY and clist[0].playerY() + characterThickness < fireY + 63:
                HealthLength -= 5

    #calls the method in the player class to make the player move
    for i in clist:
        i.playerMove()
        flip = i.flip
        #updates the x and y position of the character so the rest of the program can use them e.g. zombie and bullet
        for j in zlist:
            j.setXY(i.playerX(), i.playerY())

#adding medkit to the screen 
    for i in healthlist:
        medKit = i.healthkit()
        medX = i.objectX()
        medY = i.objectY()
        #displays on screen
        gameDisplay.blit(medKit,(medX, medY))

        #checks if the player is touching the med kit to give character health
        if medX > clist[0].playerX() and medX < clist[0].playerX() + characterThickness or medX + 31 > clist[0].playerX() and medX + 31 < clist[0].playerX() + characterThickness:
            if medY > clist[0].playerY() and medY < clist[0].playerY() + characterHeight or medY + 21 > clist[0].playerY() and medY + 21 < clist[0].playerY() + characterHeight:
                HealthLength += 70
                
                if HealthLength >= 400:
                    HealthLength = 400
                    
                healthlist.pop(0)

             
    if len(blist) > 0:
        for i in blist:
            #needs a variable for the counter so it can be used outside the loop
            #Bcounter = i 
            #calculates x and y for the bullet in the methods then draws the bullet based on that
            bx = (i.getBulletX())
            by = (i.getBulletY())
            pygame.draw.rect(gameDisplay, yellow, [bx, by, bulletLen, bulletLen])
            #changes the bulletX for next time the bullet is rendered 
            bx = i.Move()
            pygame.display.update()
            #delete bullet after it goes out of the bounds to avoid the screen flickering 
            if bx > 900 or bx < 0:
                blist.pop(0)


    if len(zlist) > 0:
        
        Zcounter = 0 
        for i in zlist:
            #displaying the enemy onto the screen with methods 
            gameDisplay.blit(zlist[Zcounter].Zmove(zlist[Zcounter].enemyX(), zlist[Zcounter].enemyY), (zlist[Zcounter].enemyX(),zlist[Zcounter].enemyY()))
            
            Ehealthlength = i.Ehealthlength

            #drawing enemy health bar 
            
            pygame.draw.rect(gameDisplay, black, [zlist[Zcounter].enemyX() - 16, zlist[Zcounter].enemyY() -30,85,20])
            pygame.draw.rect(gameDisplay, green, [zlist[Zcounter].enemyX() - 11, zlist[Zcounter].enemyY() -26, Ehealthlength,12])

            #if the bullet touches the enemy a method is called to take health from enemy             
            if bx > zlist[Zcounter].enemyX() and bx < zlist[Zcounter].enemyX() + characterThickness or bx + bulletLen > zlist[Zcounter].enemyX() and bx + bulletLen < zlist[Zcounter].enemyX() + characterThickness:
                if by > zlist[Zcounter].enemyY() and by < zlist[Zcounter].enemyY() + characterHeight or by + bulletLen > zlist[Zcounter].enemyY() and by + bulletLen < zlist[Zcounter].enemyY() + characterHeight:
                    i.Ehealthloss(15)
                 
                    
            #takes the enemy out of the list if its health is less than or equal to 0 so the enemy is deleted from the screen 
            if Ehealthlength <= 0:  
                Ehealthlength = 0
                kills += 1
                zlist.pop(Zcounter)
                zlist.append(enemy(clist[0].playerX(), clist[0].playerY(), E_load_x, E_load_y,75))

            #if statement for the enemy to hurt character 
            if clist[0].playerX() > zlist[Zcounter].enemyX() and clist[0].playerX() < zlist[Zcounter].enemyX() + characterThickness or clist[0].playerX() + characterThickness > zlist[Zcounter].enemyX() and clist[0].playerX() + characterThickness < zlist[Zcounter].enemyX() + characterThickness:
                if clist[0].playerY() > zlist[Zcounter].enemyY() and clist[0].playerY() < zlist[Zcounter].enemyY() + characterHeight or clist[0].playerY() + characterHeight > zlist[Zcounter].enemyY() and clist[0].playerY() + characterThickness < zlist[Zcounter].enemyY() + characterHeight:
                    HealthLength -= 10
                    
                    #stops the healthbar from going further down from 0
                    if HealthLength < 0:
                        HealthLength = 0
            #counter because the i in the for loop is not a number as it is looping through a list
            Zcounter += 1



    if HealthLength == 0:

        roundNum = 1
        timer = "60"
        zlist.clear()
        gameDisplay.fill(black)

        #Geting the highscores and names from a function in another file
        high1, high2 , high3, name1, name2, name3 = Highscores.GetHighScores()

        message("GAME OVER",red,50,350,50)
        message("Press R to restart or Q to quit", white, 50, 225, 435)
        message("Press M to go back to the menu ", white, 50, 212, 485)
        message("Press E to enter a high score", white , 50, 225, 535)
        message("High Scores", white, 50, 355, 110)

        #Puts the names and highscores to the screen
        message(name1, red, 60, 200, 210)
        message(name2, red, 60, 200, 290)
        message(name3, red, 60, 200, 370)
        message(high1, red, 60, 640, 210)
        message(high2, red, 60, 640, 290)
        message(high3, red, 60, 640, 370)

        #Puts the round number and name above the highscores
        message("Name", white, 30, 200, 170)
        message("Round number", white, 30, 590, 170)
        
        clist.clear()
        clist.append(playerClass.player(displayWidth/2, displayHeight/2, 0, 0, 0,easterEgg))
        
        pygame.display.update()
        
        while HealthLength <= 0:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        kills = 0
                        roundNum = 1
                        roundCounter = 1
                        HealthLength = 400
                        background = pygame.image.load("road_background.png")

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        name = ""
                        while name == "":
                            #Displays the window to enter name for highscore 
                            def display():
                                root.destroy()


                            root = Tk()
                            root.geometry("300x300")



                            v = StringVar()


                            e = Entry(root, textvariable = v)
                            e.place(x = 90, y=50)

                            l = Label(root, text = "Enter name for high score ")
                            l.place(x = 80,y =100)

                            b = Button(root, text = "OK", command = display)
                            b.place(x = 140, y = 150)
                            
                            root.mainloop()

                            #Takes the name that the user entered into this variable 
                            name = v.get()

                        #Counter is int so needs to be turned to str
                        roundCounter = str(roundCounter)

                        #Enters the name and highscore to the function to be written to the high score file 
                        Highscores.WriteHighScores(name,roundCounter)

                        #Turned back to int to prevent any potential issus 
                        roundCounter = int(roundCounter)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        #to go back to the menu after dying 
                        game_intro()
                        kills = 0
                        roundNum = 1
                        roundCounter = 1
                        HealthLength = 400
                        background = pygame.image.load("road_background.png")
                        
      

##    if flip == True:
##
##        #if player touches fire 
##        if load_x > fireX and load_x < fireX + 70 or load_x + characterThickness > fireX and load_x + characterThickness < fireX + 70:
##            if load_y > fireY and load_y < fireY + 63 or load_y + characterThickness > fireY and load_y + characterThickness < fireY + 63:
##                print("hi")
##                gameDisplay.blit(character_f,(load_x, load_y))
##                HealthLength -= 10
##                if HealthLength < 0:
##                    HealthLength = 0
##                    break
##            
##        if moveX == 0:
##            gameDisplay.blit(character_L, (load_x, load_y))
##        
##        elif load_x % 2 == 0:
##            gameDisplay.blit(character_L,(load_x,load_y))
##            
##        elif load_x % 2 != 0:
##            gameDisplay.blit(character_L_W,(load_x, load_y))
##
##        for event in pygame.event.get():
##            if event.type == pygame.QUIT:
##                gameExit = True
##
##
##    if flip == False:
##
##        #if player touches fire 
##        if load_x > fireX and load_x < fireX + 70 or load_x + characterThickness > fireX and load_x + characterThickness < fireX + 70:
##            if load_y > fireY and load_y < fireY + 63 or load_y + characterThickness > fireY and load_y + characterThickness < fireY + 63:
##                gameDisplay.blit(character_f,(load_x, load_y))
##                HealthLength -= 10
##                if HealthLength < 0:
##                    HealthLength = 0
##                    break
##            
##        if moveX == 0:
##            gameDisplay.blit(character_R, (load_x, load_y))
##        
##        elif load_x % 2 == 0:
##            gameDisplay.blit(character_R,(load_x,load_y))
##            
##        elif load_x % 2 != 0:
##            gameDisplay.blit(character_R_W,(load_x, load_y))
##
##
##    #Making fire look like it moves
##            
##    fire = random.randint(1,3)
##    if fire == 1:
##        gameDisplay.blit(fire1,(fireX,fireY))
##    
##    if fire == 2:
##        gameDisplay.blit(fire2,(fireX,fireY))
##        
##    if fire == 3:
##        gameDisplay.blit(fire3,(fireX,fireY))


    #health bar 
    pygame.draw.rect(gameDisplay,black,[245,520,411,30])
    pygame.draw.rect(gameDisplay,red,[250,525,HealthLengthR,HealthHeight])
    pygame.draw.rect(gameDisplay,green,[250,525,HealthLength,HealthHeight])

            
    #red bar to go down slower than the green health to give a good effect and also goes back up if the player gets more health
    if HealthLengthR > HealthLength:
        HealthLengthR -= 5

    if HealthLengthR < HealthLength:
        HealthLengthR += 5

    #timer for how long the round has left 
    message(timer, black , 50, 850, 10 )


    #kill counter 
    kills = str(kills)
    message("kills: ", black, 50, 10, 10)
    message(kills, red, 50, 95, 12)
    kills = int(kills)

    #Roundcounter
    roundCounter = str(roundCounter)
    message("Round: ", black, 50, 389, 10)
    message(roundCounter, red, 50, 514, 10)
    roundCounter = int(roundCounter)
    
    #updating screen    
    pygame.display.update()

    clock.tick(FPS)

gameDisplay.fill(black)
message("GAME OVER",white,50,350,250)
pygame.display.update()
time.sleep(3)
pygame.quit()
quit()
    
