import pygame #imports pygame module
import random#imports random 
from pygame.locals import * #imports all of pygame.locals

screenWidth = 1200
screenLength = 700

class Player(pygame.sprite.Sprite):#class is the "blueprint" for creating objects, this one is the player sprite
    def __init__(self):#init is the constructor for class. 'self' is used to access variables that belongs to the class
        super(Player, self).__init__()#This is to invokes the parent constructor 
        self.image = pygame.image.load('person.png').convert()#The player/self image is an image called person and is converted to a different pixel format
        self.image.set_colorkey((255, 255, 255), RLEACCEL)#This sets the hue/color of the image
        self.rect = self.image.get_rect()#This is to return the rect that will tell you the dimensions of the surface
    
    def update(self, pressed_keys):#keypress codes
        if pressed_keys[K_UP]:#if player presses the up arrow button
            self.rect.move_ip(0, -1.8)#allows it so the player will move in place and no copies of it will be produced.The numbers are the speed of the frames
        if pressed_keys[K_DOWN]:#if player presses the down arrow button
            self.rect.move_ip(0, 1.8)#allows it so the player will move in place and no copies of it will be produced.The numbers are the speed of the frames
        if pressed_keys[K_LEFT]:#if player presses the left arrow button
            self.rect.move_ip(-1.8, 0)#allows it so the player will move in place and no copies of it will be produced.The numbers are the speed of the frames
        if pressed_keys[K_RIGHT]:#if player presses the right arrow button
            self.rect.move_ip(1.8, 0)#allows it so the player will move in place and no copies of it will be produced.The numbers are the speed of the frames

  ##The code below restricts/stops the players when are moving so it prevents them from moving off the screen and disappearing
        if self.rect.left < 0: #The boundary for left side
            self.rect.left = 0#The boundary for left side
        elif self.rect.right > screenWidth:#The boundary for right side
            self.rect.right = screenWidth#The boundary for right side
        if self.rect.top <= 0:#The boundary for top side
            self.rect.top = 0#The boundary for top side
        elif self.rect.bottom >= screenLength:#The boundary for bottom side
            self.rect.bottom = screenLength#The boundary for bottom side
            
class Enemy(pygame.sprite.Sprite):#class is the "blueprint" for creating objects, this one is the enemy sprite
    def __init__(self):#init is the constructor for class. 'self' is used to access variables that belongs to the class
        super(Enemy, self).__init__()#This is to invokes the parent constructor 
        self.image = pygame.image.load('robotstroll1.png')#The enemy/self image is an image called robotstroll1 and is converted to a different pixel format
        self.image.set_colorkey((255, 255, 255), RLEACCEL)#This sets the hue/color of the image
        self.rect = self.image.get_rect(
            center=(random.randint(screenWidth, screenWidth+500), random.randint(0,screenLength))#This means that incoming enemies will start on the right side of the screen, and generate at random places
        )
        self.speed = random.randint(2, 20)#random speed that the enemies will spawn
        
    def update(self):#creates a def/ function for called update that uses the variable self
        self.rect.move_ip(-1, 0)#the enemies will move in place and at the speed of the numbers which is in frames
        if self.rect.right < 0:#if the enemies reaches the end of the screen 
            self.kill()#the enemy will destroy itself
def textob(text, font):#This is to create a function for text objects and the variables used are text and font
    textSurface = font.render(text, True, black)#This means that the font of textSurface will be black, the antialias is on and the text is what ever text is equal to.
    return textSurface, textSurface.get_rect()#This means that it will return text Surface, and the rectangle area to the caller

def button(msg,x,y,w,h,ic,ac, action=None):#a function for buttons that includes their placements, text, font, and there action/command)
    mouse = pygame.mouse.get_pos()#this make mouse variable = the position of the mouse
    click = pygame.mouse.get_pressed()#This makes click variable = when the mouse is pressed
    if x+w > mouse[0] > x and y+h > mouse[1] > y:#This is if the mouse is positioned over button 
        pygame.draw.rect(screen, ac,(x,y,w,h))#then it will draw the button/rectangle and position it at what the x,y,w,h variables are
        if click[0] == 1 and action != None:#This is for if  when the button is clicked and if action does not = none
            action()#It will run the action function  
    else:#If the mouse is not positioned over the button
        pygame.draw.rect(screen, ic,(x,y,w,h))#This rectangle will be drawned and positioned at what the x,y,w,h variables are

    tinyText = pygame.font.Font("freesansbold.ttf",20)#This is for the font of the text that is on the button =tinyText
    textSurf, textRect = textob(msg, tinyText)#This is for creating the text and the msg= to what is on the text and font is = tinyText
    textRect.center = ( (x+(w/2)), (y+(h/2)) )#This is to place and position the text
    screen.blit(textSurf, textRect)#This is to blit the text on the screen(draw text onto the screen) 

def game():#creates a funtion called game     
    enemies = pygame.sprite.Group()#handles multiple sprite objects
    all_sprites = pygame.sprite.Group()#creates all the characters using the pygame method
    all_sprites.add(player)#adds player to the screen
    
    exit=False#variable exit=false(will help with main loop)
    while not exit: #the loop(while not false(basically while True)
        for event in pygame.event.get():#gets the event/ what is going on in pygame
            if event.type == pygame.QUIT:#if the event is the quit or x button(if pressed) 
                pygame.quit()#pygame will quit
            elif(event.type == ADDENEMY):#if the event is 'ADDENEMY' the code below will run
                new_enemy=Enemy()#make the new_enemy variable equal Enemy' function/class 
                enemies.add(new_enemy)#new enemy is added
                all_sprites.add(new_enemy)#creates new enemy sprite group
        screen.blit(background, (0, 0))#it will blit(draw the image to the screen at the given position) the background every time the player moves 
        pressed_keys = pygame.key.get_pressed()#returns a dictionary with all the keypress event in the queue,and will assist in getting keys at every frame
        player.update(pressed_keys)#updates the pressed_keys
        enemies.update()#updates the enemies
        for entity in all_sprites:#all objects in the 'all_sprites' group will be render
            screen.blit(entity.image, entity.rect)#it will blit(draw the image to the screen at the given position)everytime the enemies move.
        if pygame.sprite.spritecollideany(player, enemies):#if the player collides with any enemies the code below will run 
            player.kill()#kills the player when it hits an enemy
            enemies.remove()#This removes the enemies
            end()#This is to run the end function
       

        pygame.display.update()#updates the screen with everything that has been drawn from blit 


def end():#creates a funtion called end
    largeTexty = pygame.font.Font('freesansbold.ttf',100)#Font of of a text = largeTexty
    Texty, Textplace = textob("Game over", largeTexty)#the text and font of the text using textob funtion
    Textplace.center = ((screenWidth/2.1),(screenLength/2.3))#where the text is placed
    screen.blit(Texty, Textplace)#it will blit(draw the image to the screen at the given position) the text
    
    over=True#keeps the main loop running

    while over:#the loop
        for event in pygame.event.get():#gets the event/ what is going on in pygame
            if event.type == pygame.QUIT:#if the event is the quit or x button(if pressed)
                pygame.quit()#pygame will quit
        

        button("Play Again",screenWidth/2 - 200,400,150,50,green,lightgreen,game)#This creates the button and make the text Play again, and places it and make it appear green and become brighter green when hover over it and when clicked it will run the function game
        button("Quit",screenWidth/2 + 50,400,150,50,red,lightred,pygame.quit)#This creates the button and make the text Quit, and places it and make it appear red and become brighter red when hover over it and when clicked it will quit the game

            
        pygame.display.update()#updates the screen with everything that has been drawn from blit
        clock.tick(15)#updates clock to will not run at more than 15 frames per seconds
    
    

def intro():#creates a funtion called intro
    
    running=True#keeps the main loop running

    while running:#the loop
        for event in pygame.event.get():#gets the event/ what is going on in pygame
            if event.type == pygame.QUIT:#if the event is the quit or x button(if pressed)
                pygame.quit()#pygame will quit

        screen.fill(white)#makes the screen/backgroung white
        largeText = pygame.font.Font('freesansbold.ttf',80)#Font of of a text = largeText
        smallText = pygame.font.Font('freesansbold.ttf',17)#Font of of a text = smallText
        Title, Place = textob("Robots Are Coming", largeText)#the text and font of the text using textob funtion
        Intruction, Placement= textob("Press the up, down, left, or right arrow key to move. You are the person, avoid the robots. Click the x button at the top of the screen to exit", smallText)#the text and font of the text using textob funtion
        Placement.center=((screenWidth/2), (screenLength/3+50))#where the text is placed
        Place.center = ((screenWidth/2),(screenLength/4))#where the text is placed
        screen.blit(Title, Place)#it will blit(draw the image to the screen at the given position) the Title
        screen.blit(Intruction, Placement)#it will blit(draw the image to the screen at the given position) the Insturction.

        button("Start",screenWidth/2 - 200,screenLength/2,150,50,green,lightgreen,game)#This creates the button and make the text Start, and places it and make it appear green and become brighter green when hover over it and when clicked it will run the function game
        button("Quit",screenWidth/2 + 50,screenLength/2,150,50,red,lightred,pygame.quit)#This creates the button and make the text Quit, and places it and make it appear red and become brighter red when hover over it and when clicked it will quit the game
            
        pygame.display.update()#updates the screen with everything that has been drawn from blit
        clock.tick(15)#updates clock to will not run at more than 15 frames per seconds


pygame.init()# initialize all pygame modules

black = (0,0,0)#make the variable black = the hue (0,0,0) = black
white = (255,255,255)#make the variable white= the hue (255,255,255) = white
red = (200,0,0)#make the variable red = the hue (150,0,0) = dark red
green = (0,200,0)#make the variable green = the hue (0,0,0) = dark green
lightred = (255,0,0)#make the variable lightred = the hue (255,0,0) = bright red
lightgreen = (0,250,0)#make the variable lightgreen = the hue (0,200,0) = bright green

screen=pygame.display.set_mode((screenWidth,screenLength))#creates a screen for the game
pygame.display.set_caption('Avoid the Robots')#This will be the title of the window display
clock = pygame.time.Clock()#make the pygame.time.Clock function = clock(variable)

ADDENEMY = pygame.USEREVENT + 1#a custom event for new enemies to spawn
pygame.time.set_timer(ADDENEMY, 65)#a timer which will create enemies over the course of the game. Enemies will fire every 65 milliseconds

player = Player()#creates the 'player', make player variable = Player class
background = pygame.image.load("eyenice.png").convert()#makes the background the image (eyenice) and converts it's pixel format


intro()#runs the intro
