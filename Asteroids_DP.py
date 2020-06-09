
#########################################
# Programmer: David P.
# Date: 1/23/2018
# File Name: Final_Asteroids_DP.py
# Description: Mutliplayer Asteroids Game
#########################################
import pygame
import math
import random
import sys

pygame.init()
HEIGHT = 600
WIDTH  = 800
screen=pygame.display.set_mode((WIDTH,HEIGHT))

#Fonts
small_Font = pygame.font.SysFont("Ariel Black",30)
regular_Font = pygame.font.SysFont("Ariel Black",40)
big_Font = pygame.font.SysFont("Ariel Black",75)

#Colours
BLACK = (  0,  0,  0)
WHITE = (255,255,255)
RED   = (255,  0,  0)
YELLOW= (255,255,  0)

#Angle Increment
STEP = 10

#Images
timeAndScore = pygame.image.load("timeScore.png")
gameOverScreen = pygame.image.load("screens/gameOver.jpg")
twoPlayerButton = pygame.image.load("2-player.png")
threePlayerButton = pygame.image.load("3-player.png")
startScreen = pygame.image.load("screens/startScreen.jpg")
health5 = pygame.image.load("lives/health5.png")
health4 = pygame.image.load("lives/health4.png")
health3 = pygame.image.load("lives/health3.png")
health2 = pygame.image.load("lives/health2.png")
health1 = pygame.image.load("lives/health1.png")
life3 = pygame.image.load("lives/life3.png")
life2 = pygame.image.load("lives/life2.png")
life1 = pygame.image.load("lives/life1.png")
twoRules = pygame.image.load("screens/twoRules.jpg")
threeRules = pygame.image.load("screens/threeRules.jpg")

#Background
galaxy1 = pygame.image.load("screens/galaxyBG.jpg")
galaxy2 = pygame.image.load("screens/galaxyBG2.jpg")


#Other
numOfCollision=0
score=0
level=1
lives=3
health=5
time=0
timeCap=0
clock=pygame.time.Clock()
FPS=60
spawn=True

#Booleans determining if the game is running a two, or three-player game
twoPlayer=False
threePlayer=False

#Sound effects
explosion=pygame.mixer.Sound('sounds/explosion.wav')
miniExplosion=pygame.mixer.Sound('sounds/drop.wav')
startGameOver=pygame.mixer.Sound('sounds/startGameOver.wav')

#Songs
backgroundMusic=pygame.mixer.music.load("sounds/backgroundMusic.wav")

#Explosion Sprites
e1=pygame.image.load('explosion/e1.png')
e2=pygame.image.load('explosion/e2.png')
e3=pygame.image.load('explosion/e3.png')
e4=pygame.image.load('explosion/e4.png')
e5=pygame.image.load('explosion/e5.png')
e6=pygame.image.load('explosion/e6.png')
e7=pygame.image.load('explosion/e7.png')
e8=pygame.image.load('explosion/e8.png')
e9=pygame.image.load('explosion/e9.png')

#Gif starters
eCurrentImage=0                                                                      # Used for the sprites of the explosion  
eCurrentImage2=0                                                                     # For Suicide ship 1,Suicide ship 2,
eCurrentImage3=0                                                                     # and ship collision gif

#Instructions
rulesCounter=1
twoPlayerRules=False
threePlayerRules=False

                                                        #---------------------------------------#
                                                        #                Classes                #
                                                        #---------------------------------------#
class Ship():                                                                       #######
    def __init__(self,shipX,shipY,angle,ship_image):                                      #
        self.x=shipX                                                                      # Initiating the
        self.y=shipY                                                                      # ship attributes
        self.angle=angle                                                                  #
        self.ship_image=ship_image                                                        #
        self.thrust=6                                                               #######
        
    def rotate(self,ship_image,angle):                                                  #Finds the size of the image
        ORIGINALrect = self.ship_image.get_rect()                                       #Rotates the image corresonding to the angle
        rot_image = pygame.transform.rotate(self.ship_image,angle)                      #Copies the image
        rot_rect = ORIGINALrect.copy()                                                  #Rotates it on the center of the image
        rot_rect.center = rot_image.get_rect().center                                   #Sets the copied image for the image
        rot_image = rot_image.subsurface(rot_rect).copy()                               #Rotates the image
        return rot_image
        
    def move_forward(self):                                                              #########
        if (self.angle%360>=0 and self.angle%360<=90):                                           #
            self.x -= int(round(self.thrust*math.sin(self.angle*math.pi/180)))                   #
            self.y -= int(round(self.thrust*math.cos(self.angle*math.pi/180)))                   #
        elif self.angle%360>=90 and self.angle%360<=180:                                         # An angle is passed through when the user rotates
            self.x += int(round(self.thrust*math.cos(((-self.angle)-90)*math.pi/180)))           # with their keys. The formula uses the four quadrants
            self.y += int(round(self.thrust*math.sin(((-self.angle)-90)*math.pi/180)))           # for their own formulas. The ship then moves the direction
        elif self.angle%360>=180 and self.angle%360<=270:                                        # of the angle. 
            self.x+= int(round(self.thrust*math.sin((self.angle-180)*math.pi/180)))              # 
            self.y += int(round(self.thrust*math.cos((self.angle-180)*math.pi/180)))             # **Thrust - The speed of the ship**
        else:                                                                                    #
            self.x += int(round(self.thrust*math.cos((self.angle-270)*math.pi/180)))             #
            self.y -= int(round(self.thrust*math.sin((self.angle-270)*math.pi/180)))     #########
            
    def draw(self):
        screen.blit(self.ship_image, (self.x-shipW/2,self.y-shipW/2))
        pygame.display.update()

        
class Suicide(Ship):                                                                    ########
    def __init__(self,shipX,shipY,angle,ship_image):                                           #
        self.x=shipX                                                                           #
        self.y=shipY                                                                           # Suicide ship class inherited from the
        self.angle=angle                                                                       # Ship class.
        self.ship_image=ship_image                                                             # Only thing that is changed is
        self.thrust=8                                                                          # the thrust.
                                                                                        ########
        
class Rock():                                                                           ########
    def __init__(self,rockX,rockY):                                                            #               
        self.image=pygame.image.load("meteor.png")                                             #                              
        self.w=42                                                                              # 
        self.x=rockX                                                                           #  
        self.y=rockY                                                                           #            | --- Moves --- Moves at a random rangle 
        self.velocity=7                                                                        #            |               Uses Sin for Y - linear graph
        self.angle=random.randrange(0,360)                                                     #            |               Uses Cos for X - linear graph
                                                                                               # Rock class |                
    def move(self):                                                                            #            |                        
        for j in range(len(rock.x)):                                                           #            |                                         
            self.x[j]+=int(round(self.velocity*math.cos(self.angle*math.pi/180)))              #            |--- Draws --- Takes the rock and centers                                                                                
            self.y[j]+=int(round(self.velocity*math.sin(self.angle*math.pi/180)))              #                            it according to the X coordinate                                                                      
                                                                                               #               
    def draw(self):                                                                            #                                    
        for j in range(len(rock.x)):                                                           #                                                     
            screen.blit(self.image, (self.x[j]-self.w/2,self.y[j]-self.w/2))                   #                                                                                             
            pygame.display.update()                                                            #                                                    
                                                                                        ########
                                                        #---------------------------------------#
                                                        #               Functions               #
                                                        #---------------------------------------#
def mainMenu():
    startGameOver.play()
    screen.blit(startScreen, (0,0))                                     # Draws the menu image
    screen.blit(twoPlayerButton, (201,350))                             # Draws the button
    screen.blit(threePlayerButton, (440,350))                           # Draws the button
    pygame.display.update()                                             # Updates the screen

def gameOver():
    startGameOver.play()                                                # Plays the gameover sound
    screen.blit(gameOverScreen, (0,0))                                  # Draws the gameover picture
    
    score_text = big_Font.render(str(int(score)), 1, (75,75,220))       ############
    screen.blit(score_text,(380,343))                                              # 
    level_text = big_Font.render(str(level), 1, (75,75,220))                       # Draws the text on the game over screen
    screen.blit(level_text,(380,390))                                   ############
    pygame.display.update()                                             # Updates the screen

def livesAndHealthDraw():
    if health==5:screen.blit(health5, (0,0))                            #If the health is 5, draw the given image | declared at the top
    if health==4:screen.blit(health4, (0,0))                            #If the health is 4, draw the given image | declared at the top
    if health==3:screen.blit(health3, (0,0))                            #If the health is 3, draw the given image | declared at the top
    if health==2:screen.blit(health2, (0,0))                            #If the health is 2, draw the given image | declared at the top
    if health==1:screen.blit(health1, (0,0))                            #If the health is 1, draw the given image | declared at the top
    if lives==3:screen.blit(life3, (0,0))                               #If the lives are 3, draw the given image | declared at the top
    if lives==2:screen.blit(life2, (0,0))                               #If the lives are 2, draw the given image | declared at the top
    if lives==1:screen.blit(life1, (0,0))                               #If the life is 1, draw the given image | declared at the top
            

def redraw_screen():                                                                            ########
    if twoPlayer==True:                                                                                # The background of the game changes by
        screen.blit(galaxy1, (0,0))                                                                    # levels for the sole reason of letting
    elif threePlayer==True:                                                                            # the user know that they move onto the next level.
        screen.blit(galaxy2, (0,0))                                                             ######## Odd level - orange background, Even level - purble background
    
    screen.blit(timeAndScore,(0,0))                                                             ########
    fps_text = small_Font.render(str(int(FPS)), 1, YELLOW)                                             #               
    screen.blit(fps_text,(WIDTH-30,5))                                                                 #
    time_text = regular_Font.render(str(int(time)), 1, (20,50,220))                                    # Text on the 
    screen.blit(time_text,(40,42))                                                                     # game screen
    score_text = regular_Font.render(str(score), 1, (75,75,220))                                       # [FPS, Time, Score, Level
    screen.blit(score_text,(40,76))                                                                    # and number of asteroids]
    level_text = regular_Font.render(str(level), 1, (75,75,220))                                       # 
    screen.blit(level_text,(40,108))                                                                   #
    asteroid_text = regular_Font.render(str(len(rock.x)), 1, (20,50,220))                              #
    screen.blit(asteroid_text,(40,140))                                                         ########
    
    livesAndHealthDraw()                                    # Calling the health and lives function
    spaceShip.draw()                                        # Drawing the ship
    if twoPlayer==True or threePlayer==True:                # If the user clicked 2 player [Main menu]
        suicideShip.draw()                                  # Drawing the suicide ship 1
    if threePlayer==True:                                   # If the user clicked 3 player [Main menu]
        suicideShip2.draw()                                 # Drawing the suicide ship 2
    rock.move()                                             # Moving the rock
    rock.draw()                                             # Drawing the rock
    pygame.display.update()
                                                        #---------------------------------------#
                                                        #            Main program               #
                                                        #---------------------------------------#

#Ship
ORIGINALship = pygame.image.load("ship.png")
ship_image = ORIGINALship.copy()                     # keep the original image intact, so it does not get distorted 
shipX = WIDTH/2
shipY = HEIGHT/2
shipW=50
sAngle = 0

#Ship 2
ORIGINALship2 = pygame.image.load("suicide.png")
ship_image2 = ORIGINALship2.copy()                   # keep the original image intact, so it does not get distorted 
shipX2 = WIDTH/2-50
shipY2 = HEIGHT/2
shipW2=20
sAngle2 = 0

#Ship 3
ORIGINALship3 = pygame.image.load("suicide2.png")
ship_image3 = ORIGINALship3.copy()                   # keep the original image intact, so it does not get distorted 
shipX3 = WIDTH/2+70
shipY3 = HEIGHT/2
shipW3=20
sAngle3 = 0

#Asteroids
rockX=[]
rockY=[]
rock=Rock(rockX,rockY)

spaceShip=Ship(shipX,shipY,sAngle,ship_image)               ####### 
suicideShip=Suicide(shipX2,shipY2,sAngle2,ship_image2)            # All the objects
suicideShip2=Suicide(shipX3,shipY3,sAngle3,ship_image3)           # 
rock=Rock(rockX,rockY)                                      ####### 

#------------------------------------------------------------------------------------------------------------#

inPlay = False
while mainMenu:                                                             # While true
    startGameOver.stop()
    mainMenu()                                                              # Menu function / image
    for event in pygame.event.get():                                        # For every event loop
        if event.type==pygame.MOUSEBUTTONDOWN:                              # If clicked on the button
            if event.type == pygame.QUIT:
                inPlay=False 
            mx,my=pygame.mouse.get_pos()                                 
            if mx>=201 and mx<=201+159 and my>=350 and my<=350+70:
                twoPlayerRules=True
                mainMenu= False
            if mx>=440 and mx<=440+159 and my>=350 and my<=350+70:
                threePlayerRules=True
                mainMenu= False    
                
while twoPlayerRules==True:                                         ######
    pygame.time.delay(40)                                                #
    rulesCounter+=8                                                      #
    screen.blit(threeRules,[0,0])                                        # Displays the two player rules on the screen
    pygame.draw.rect(screen, YELLOW, (10,HEIGHT-20,rulesCounter,10), 0)  # with the buffering loading bar on
    if rulesCounter>=WIDTH-10:                                           # the bottom of the screen. 
       twoPlayerRules=False                                              #
       inPlay=True                                                       #
       twoPlayer=True                                                    #
    pygame.display.update()                                         ######   

while threePlayerRules==True:                                       ######
    pygame.time.delay(40)                                                #
    rulesCounter+=8                                                      #
    screen.blit(twoRules,[0,0])                                          #
    pygame.draw.rect(screen, YELLOW, (10,HEIGHT-20,rulesCounter,10), 0)  # Displays the three player rules on the screen
    if rulesCounter>=WIDTH-10:                                           # with the buffering loading bar on
        threePlayerRules=False                                           # the bottom of the screen. 
        inPlay=True                                                      #
        threePlayer=True                                                 #
    pygame.display.update()                                         ######   

        
pygame.mixer.music.play(loops=-1)                                  #Plays the main background music
while inPlay:                                                       #While the main game is happening
    startGameOver.stop()                                            #Stops the main menu music   
    pygame.event.get()           
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():        
        if event.type == pygame.QUIT:
            inPlay=False   

    if keys[pygame.K_ESCAPE]:
        sys.exit()
                                                                    #---------------------------------------#
                                                                    #   Keys used for player movement       # ---> Using steps to change the angle. Changing the angles in the ships
                                                                    #---------------------------------------#    > and then updating the image in the class method: Rotate
    #Keys player 1 [UP,LEFT,RIGHT]
    if keys[pygame.K_LEFT]:
        sAngle += STEP
        sAngle = sAngle%360
        spaceShip.angle=sAngle
        spaceShip.ship_image=ship_image
        spaceShip.ship_image=spaceShip.rotate(ship_image,sAngle)
        
    if keys[pygame.K_RIGHT]:
        sAngle -= STEP
        sAngle = sAngle%360
        spaceShip.angle=sAngle
        spaceShip.ship_image=ship_image
        spaceShip.ship_image=spaceShip.rotate(ship_image,sAngle)
        
    if keys[pygame.K_UP]:
        spaceShip.move_forward()

    #Keys player 2 [W,A,D]
    if twoPlayer==True or threePlayer==True: 
        if keys[pygame.K_a]:
            sAngle2 += STEP
            sAngle2 = sAngle2%360
            suicideShip.angle=sAngle2
            suicideShip.ship_image=ship_image2
            suicideShip.ship_image=suicideShip.rotate(ship_image2,sAngle2)
            
        if keys[pygame.K_d]:
            sAngle2 -= STEP
            sAngle2 = sAngle2%360
            suicideShip.angle=sAngle2
            suicideShip.ship_image=ship_image2
            suicideShip.ship_image=suicideShip.rotate(ship_image2,sAngle2)
            
        if keys[pygame.K_w]:
            suicideShip.move_forward()
            
    #Keys player 3 [I,J,L]
    if threePlayer==True:
        if keys[pygame.K_j]:
            sAngle3 += STEP
            sAngle3 = sAngle3%360
            suicideShip2.angle=sAngle3
            suicideShip2.ship_image=ship_image3
            suicideShip2.ship_image=suicideShip2.rotate(ship_image3,sAngle3)
            
        if keys[pygame.K_l]:
            sAngle3 -= STEP
            sAngle3 = sAngle3%360
            suicideShip2.angle=sAngle3
            suicideShip2.ship_image=ship_image3
            suicideShip2.ship_image=suicideShip2.rotate(ship_image3,sAngle3)
            
        if keys[pygame.K_i]:
            suicideShip2.move_forward()

                                                                    #---------------------------------------#
                                                                    #        Border - Shop Collision        #
                                                                    #---------------------------------------#
    if spaceShip.x<0:
        spaceShip.x=WIDTH
    elif spaceShip.x>WIDTH:
        spaceShip.x=0

    if spaceShip.y<0:
        spaceShip.y=HEIGHT
    elif spaceShip.y>HEIGHT:
        spaceShip.y=0


    if twoPlayer==True or threePlayer==True:            ####### 
        if suicideShip.x<0:                                   # 
            suicideShip.x=WIDTH                               # 
        elif suicideShip.x>WIDTH:                             # If the user clicked on either two player
            suicideShip.x=0                                   # or three player in the main menu, if both suicide ships 
                                                              # are out of the boundries, the ship will be
        if suicideShip.y<0:                                   # teleported to the other side
            suicideShip.y=HEIGHT                              # 
        elif suicideShip.y>HEIGHT:                            # 
            suicideShip.y=0                             ####### 
            
    if threePlayer==True:                               #######
        if suicideShip2.x<0:                                  #
            suicideShip2.x=WIDTH                              #
        elif suicideShip2.x>WIDTH:                            # If the user clicked on the three player setting in                                                                 
            suicideShip2.x=0                                  # the main menu, if both suicide ships
                                                              # are out of the boundries, the ship will be
        if suicideShip2.y<0:                                  # teleported to the other side
            suicideShip2.y=HEIGHT                             #
        elif suicideShip2.y>HEIGHT:                           #
            suicideShip2.y=0                            #######                                 
        
                                                                    #---------------------------------------#
                                                                    #      Ship Collision With Asteroid     #
                                                                    #---------------------------------------#
    if twoPlayer==True:                                                                                                                                           #[If two player setting was clicked]#
        for j in reversed(range(len(rock.x))):
            if suicideShip.x<=rock.x[j]+rock.w and suicideShip.x>=rock.x[j]-rock.w and suicideShip.y<=rock.y[j]+rock.w and suicideShip.y>=rock.y[j]-rock.w:
                rock.x.pop(j)
                rock.y.pop(j)
                score+=100
                miniExplosion.play()                                                                                                                        # Suicide ship collision with asteroid
                eCurrentImage=1
                
            elif spaceShip.x<=rock.x[j]+rock.w and spaceShip.x>=rock.x[j]-rock.w and spaceShip.y<=rock.y[j]+rock.w and spaceShip.y>=rock.y[j]-rock.w:
                rock.x.pop(j)
                rock.y.pop(j)
                spaceShip.x=WIDTH/2
                spaceShip.y=HEIGHT/2
                health-=1                                                                                                                                   # Main ship collision with asteroid
                explosion.play()
                eCurrentImage3=1
                
    if threePlayer==True:                                                                                                                                           #[If three player setting was clicked]#
        for j in reversed(range(len(rock.x))):
            if suicideShip.x<=rock.x[j]+rock.w and suicideShip.x>=rock.x[j]-rock.w and suicideShip.y<=rock.y[j]+rock.w and suicideShip.y>=rock.y[j]-rock.w:
                rock.x.pop(j)
                rock.y.pop(j)                                                                                                                               # Suicide ship collision with asteroid
                score+=100
                miniExplosion.play()
                eCurrentImage=1
                
            elif suicideShip2.x<=rock.x[j]+rock.w and suicideShip2.x>=rock.x[j]-rock.w and suicideShip2.y<=rock.y[j]+rock.w and suicideShip2.y>=rock.y[j]-rock.w:
                rock.x.pop(j)
                rock.y.pop(j)
                score+=100                                                                                                                                  # Suicide ship 2 collision with asteroid
                miniExplosion.play()
                eCurrentImage2=1
                
            elif spaceShip.x<=rock.x[j]+rock.w and spaceShip.x>=rock.x[j]-rock.w and spaceShip.y<=rock.y[j]+rock.w and spaceShip.y>=rock.y[j]-rock.w:
                rock.x.pop(j)
                rock.y.pop(j)
                spaceShip.x=WIDTH/2
                spaceShip.y=HEIGHT/2                                                                                                                        # Main ship collision with asteroid
                health-=1
                explosion.play()
                eCurrentImage3=1                                                                                                                        
                                                                                                   ##############
    if eCurrentImage==1:                                                                                        #
        screen.blit(e1,(suicideShip.x-100,suicideShip.y-100))                                                   #
        pygame.display.update()                                                                                 #
        eCurrentImage+=1                                                                                        #
    elif eCurrentImage==2:                                                                                      #
        screen.blit(e2,(suicideShip.x-100,suicideShip.y-100))                                                   #
        eCurrentImage+=1                                                                                        #
        pygame.display.update()                                                                                 #                                                                                 
    elif eCurrentImage==3:                                                                                      #
        screen.blit(e3,(suicideShip.x-100,suicideShip.y-100))                                                   #
        pygame.display.update()                                                                                 #
        eCurrentImage+=1                                                                                        #
    elif eCurrentImage==4:                                                                                      #
        screen.blit(e4,(suicideShip.x-100,suicideShip.y-100))                                                   #
        pygame.display.update()                                                                                 #                                                                                 
        eCurrentImage+=1                                                                                        # 
    elif eCurrentImage==5:                                                                                      #-------# Updates each image to create the look of a gif [Suicide Ship 1]
        screen.blit(e5,(suicideShip.x-100,suicideShip.y-100))                                                   #
        pygame.display.update()                                                                                 #
        eCurrentImage+=1                                                                                        #
    elif eCurrentImage==6:                                                                                      #
        screen.blit(e6,(suicideShip.x-100,suicideShip.y-100))                                                   #
        pygame.display.update()                                                                                 #
        eCurrentImage+=1                                                                                        #                                                                                      
    elif eCurrentImage==7:                                                                                      #
        screen.blit(e7,(suicideShip.x-100,suicideShip.y-100))                                                   #
        pygame.display.update()                                                                                 #
        eCurrentImage+=1                                                                                        #
    elif eCurrentImage==8:                                                                                      #
        screen.blit(e8,(suicideShip.x-100,suicideShip.y-100))                                                   #
        pygame.display.update()                                                                                 #
        eCurrentImage+=1                                                                                        #
    elif eCurrentImage==9:                                                                                      #
        screen.blit(e9,(suicideShip.x-100,suicideShip.y-100))                                                   #
        pygame.display.update()                                                                                 #
        eCurrentImage=0                                                                             #############

                                                                    #Explosion Gif [Suicide ship 2]
    if eCurrentImage2==1:                                                                           #############
        screen.blit(e1,(suicideShip2.x-100,suicideShip2.y-100))                                                 #
        pygame.display.update()                                                                                 #
        eCurrentImage2+=1                                                                                       #
    elif eCurrentImage2==2:                                                                                     #
        screen.blit(e2,(suicideShip2.x-100,suicideShip2.y-100))                                                 #
        eCurrentImage2+=1                                                                                       #
        pygame.display.update()                                                                                 #
    elif eCurrentImage2==3:                                                                                     #
        screen.blit(e3,(suicideShip2.x-100,suicideShip2.y-100))                                                 #
        pygame.display.update()                                                                                 #
        eCurrentImage2+=1                                                                                       #
    elif eCurrentImage2==4:                                                                                     #
        screen.blit(e4,(suicideShip2.x-100,suicideShip2.y-100))                                                 #
        pygame.display.update()                                                                                 #
        eCurrentImage2+=1                                                                                       #
    elif eCurrentImage2==5:                                                                                     #-------# Updates each image to create the look of a gif [Suicide Ship 2]
        screen.blit(e5,(suicideShip2.x-100,suicideShip2.y-100))                                                 #
        eCurrentImage2+=1                                                                                       #
    elif eCurrentImage2==6:                                                                                     #
        screen.blit(e6,(suicideShip2.x-100,suicideShip2.y-100))                                                 #
        pygame.display.update()                                                                                 #
        eCurrentImage2+=1                                                                                       #
    elif eCurrentImage2==7:                                                                                     #                                                                                     
        screen.blit(e7,(suicideShip2.x-100,suicideShip2.y-100))                                                 #
        pygame.display.update()                                                                                 #
        eCurrentImage2+=1                                                                                       #
    elif eCurrentImage2==8:                                                                                     #
        screen.blit(e8,(suicideShip2.x-100,suicideShip2.y-100))                                                 #
        pygame.display.update()                                                                                 #
        eCurrentImage2+=1                                                                                       #
    elif eCurrentImage2==9:                                                                                     #
        screen.blit(e9,(suicideShip2.x-100,suicideShip2.y-100))                                                 #
        pygame.display.update()                                                                                 #
        eCurrentImage2=0                                                                            #############

                                                                    #Explosion Gif [Main ship]
    if eCurrentImage3==1:                                                                           #############
        screen.blit(e1,(spaceShip.x-100,spaceShip.y-100))                                                       #
        pygame.display.update()                                                                                 #
        eCurrentImage3+=1                                                                                       #
    elif eCurrentImage3==2:                                                                                     #
        screen.blit(e2,(spaceShip.x-100,spaceShip.y-100))                                                       #
        eCurrentImage3+=1                                                                                       #
        pygame.display.update()                                                                                 #
    elif eCurrentImage3==3:                                                                                     #
        screen.blit(e3,(spaceShip.x-100,spaceShip.y-100))                                                       #
        pygame.display.update()                                                                                 #
        eCurrentImage3+=1                                                                                       #
    elif eCurrentImage3==4:                                                                                     #
        screen.blit(e4,(spaceShip.x-100,spaceShip.y-100))                                                       #
        pygame.display.update()                                                                                 #
        eCurrentImage3+=1                                                                                       #
    elif eCurrentImage3==5:                                                                                     #
        screen.blit(e5,(spaceShip.x-100,spaceShip.y-100))                                                       #
        pygame.display.update()                                                                                 #
        eCurrentImage3+=1                                                                                       #-------# Updates each image to create the look of a gif [main spaceShip]
    elif eCurrentImage3==6:                                                                                     #
        screen.blit(e6,(spaceShip.x-100,spaceShip.y-100))                                                       #
        pygame.display.update()                                                                                 #
        eCurrentImage3+=1                                                                                       #
    elif eCurrentImage3==7:                                                                                     #
        screen.blit(e7,(spaceShip.x-100,spaceShip.y-100))                                                       #
        pygame.display.update()                                                                                 #
        eCurrentImage3+=1                                                                                       #
    elif eCurrentImage3==8:                                                                                     #
        screen.blit(e8,(spaceShip.x-100,spaceShip.y-100))                                                       #
        pygame.display.update()                                                                                 #
        eCurrentImage3+=1                                                                                       #
    elif eCurrentImage3==9:                                                                                     #
        screen.blit(e9,(spaceShip.x-100,spaceShip.y-100))                                                       #
        pygame.display.update()                                                                                 #
        eCurrentImage3=0                                                                            #############
            

                                                 ########
    for j in range(len(rock.x)):                        #
        if rock.x[j]<0:                                 #
            rock.x[j]=WIDTH                             #
        if rock.x[j]>WIDTH:                             # If the rock goes out of the border, it will get teleported
            rock.x[j]=0                                 # from the other side, like the ship.
                                                        #
        if rock.y[j]<0:                                 #
            rock.y[j]=HEIGHT                            #
        if rock.y[j]>HEIGHT:                            #
            rock.y[j]=0                          ########
    
    for i in range(10):
        if level ==i:
            if spawn==True:
                for i in range(level*2):
                    rock.x.append(random.randrange(rock.w,WIDTH-rock.w/2))      #Spawning new asteroids (X)
                    rock.y.append(random.randrange(rock.w,HEIGHT-rock.w/2))     #Spawning new asteroisd (Y)
                spawn=False

    if len(rock.x)==0:
        level+=1
        rock.velocity+=.5                           # Increasing the speed
        rock.angle=random.randrange(0,360)          # Change the angle of rocks moving
        spawn=True
                                                    # Health and lives. If the main ship collides with the asteroid,
    if health==0:                                   # health will be removed. If there are 0 lives, the game is over.
        lives-=1
        health=5
    if lives==0:
        break
    
    redraw_screen() 
    FPS=random.randrange(55,65)                     # FPS counter on the top right corner
    clock.tick(FPS)                                 # Ticking the FPS for the clock
    timeCap+=1                                      # TIme will increase by 1 everytime the timecap has a remainder of 0 - 35%
    if timeCap%35==0:
        time+=1
    pygame.time.delay(20)                           #Delay set to 20 to make the game non-laggy
#---------------------------------------#
gameOver()                                          # Sets the gameover function / image
pygame.time.delay(5000)                             # Set the delay to 5000 for the gameover function can last for 5 seconds
pygame.quit()
