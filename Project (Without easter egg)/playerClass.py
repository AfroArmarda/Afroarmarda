import pygame
gameDisplay = pygame.display.set_mode((0,0))

class player:
    def __init__(self, load_x, load_y, move_x, move_y, flip):
        
        self.load_x = load_x
        self.load_y = load_y
        self.move_x = move_x
        self.move_y = move_y
        self.flip = flip

    def playerUp(self):
        
        self.move_y = 0
        self.move_y -= 11

    def playerDown(self):

        self.move_y = 0
        self.move_y += 11

    def playerLeft(self, flip):

        #sets the flip so that the image can be flipped to face the right way
        self.flip = True 
        self.move_x = 0
        self.move_x -= 11
          
    def playerRight(self, flip):

        #sets the flip so that the image can be flipped to face the right way
        self.flip = False 
        self.move_x = 0
        self.move_x += 11

    def stop_x(self):
        #sets the character to stop for when a key is lifted 
        self.move_x = 0

    def stop_y(self):
        #sets the character to stop for when a key is lifted 
        self.move_y = 0
        
    def playerMove(self):
    
        if self.load_x + self.move_x + 40 > 900:
            self.move_x = 0

        if self.load_x + self.move_x + 10 < 0:
            self.move_x = 0
            
        if self.load_y + self.move_y < 0:
            self.move_y = 0

        if self.load_y + self.move_y + 77 > 575: 
            self.move_y = 0
        
        #adds the move variable to the current x and y coordinate of the player to make him move
        self.load_x += self.move_x
        self.load_y += self.move_y
            
        #flipping and impoting character images (for when character turns in opposite direction )       

        character_R = pygame.image.load("character.png")
        character_L = pygame.transform.flip(character_R,True, False)

        character_R_W = pygame.image.load("character_walk.png")
        character_L_W = pygame.transform.flip(character_R_W, True, False)

        #asks if its flipped or not to decide what image to display
        if self.flip == True:

            #devides the current position so that it will display a different image depending on the result to make a walk animation    
            if self.move_x == 0:
                gameDisplay.blit(character_L, (self.load_x, self.load_y))
            
            elif self.load_x % 2 == 0:
                gameDisplay.blit(character_L,(self.load_x,self.load_y))

                
            elif self.load_x % 2 != 0:
                gameDisplay.blit(character_L_W,(self.load_x, self.load_y))



        if self.flip == False:

            #devides the current position so that it will display a different image depending on the result to make a walk animation              
            if self.move_x == 0:
                gameDisplay.blit(character_R, (self.load_x, self.load_y))
            
            elif self.load_x % 2 == 0:
                gameDisplay.blit(character_R,(self.load_x, self.load_y))
                
            elif self.load_x % 2 != 0:
                gameDisplay.blit(character_R_W,(self.load_x, self.load_y))
                

            
    def playerX(self):
        return self.load_x

    def playerY(self):
        return self.load_y
