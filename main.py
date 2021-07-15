import pygame
import random
from pygame import mixer
import sys, os 
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# initialize the pygame library
pygame.init()

#create the screen
screen = pygame.display.set_mode((1390,720))

# background
background= pygame.image.load(resource_path('spaceBackground.jpg'))

#background sound
mixer.music.load(resource_path('background.wav'))
mixer.music.play(-1)
mixer.music.set_volume(0.015) 
#Title and icon
pygame.display.set_caption("Space invaders")
icon = pygame.image.load(resource_path('spaceship.png'))
pygame.display.set_icon(icon)

#alien
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
alien_rectangle=[]
numOfEnemies = 3
moveSpeedAlien = 0.3

alienPicture = pygame.image.load(resource_path("alien.png"))
alienPicture= pygame.transform.scale(alienPicture, (64, 64))
for i in range(numOfEnemies):
    alienImg.append(alienPicture)
    alienX.append(random.randint(0,(screen.get_width()-64)))
    alienY.append(random.randint(10,100))
    alienY_change.append(32)
    alienX_change.append(moveSpeedAlien) 
    alien_rectangle= [alienImg.get_rect() for alienImg in alienImg] 

#player
playerImg = pygame.image.load(resource_path('rocket.png'))
playerX = (screen.get_width() / 2) -64  
playerY = 480
playerX_change = 0
moveSpeed =0.5 
player_rectange= playerImg.get_rect()

#boss
bossImg = pygame.image.load(resource_path('boss.png'))
bossImg= pygame.transform.scale(bossImg, (128, 128))
bossX = (screen.get_width() / 2) -100
bossY = 20
bossX_change = 0.9
bossY_change = 0
bossMoveSpeed = 0.25
boss_rectangle= bossImg.get_rect()

#boss bullet
bossBulletImg= pygame.image.load(resource_path('bossBullet.png'))
bossBulletImg.convert()
bossBulletImg= pygame.transform.scale(bossBulletImg, (50, 50))
bossBulletY= 100
bossBulletX=0 
bossBulletMoveSpeed = 0.7
bossBulletY_change = bossBulletMoveSpeed
bossBulletX_change = 0 
bossBulletState = "ready"
bossBullet_rectangle = bossBulletImg.get_rect()

#bossLives text
bossLives = 100 
bossFont = pygame.font.Font('freesansbold.ttf',20)
bossTextY = 10
bossTextX =screen.get_width()-180

#score
scoreValue =0
font = pygame.font.Font('freesansbold.ttf',20)
textX = 10
textY = 10

#gameOverText
overFont = pygame.font.Font('freesansbold.ttf',80)

#GameOver win text
winFont= pygame.font.Font('freesansbold.ttf',80)

#gameOverText
bossLossFont= pygame.font.Font('freesansbold.ttf',60)

#bullet
bulletImg= pygame.image.load(resource_path('bullet.png'))
bulletImg.convert()
bulletImg= pygame.transform.scale(bulletImg, (32, 32))
bulletY= 480
bulletX=0 
bulletMoveSpeed = 3
bulletY_change = bulletMoveSpeed
bulletX_change = 0 
bulletState = "ready"
bullet_rectangle = bulletImg.get_rect()

def gameOverText():
    overText= overFont.render("Game Over!",True,(255,255,255)) 
    screen.blit(overText, (200, 250))

def victory():
    winText= winFont.render("You Win!!",True,(255,255,255)) 
    screen.blit(winText, (500, 250))

def bossLoss():
    bossLossText= bossLossFont.render("You lost",True,(255,255,255)) 
    screen.blit(bossLossText, (10, 250))

def showScore(x,y):
    score = font.render("Score: "+str(scoreValue),True,(255,255,255)) 
    screen.blit(score, (x, y))

def showBossLives(x,y):
    bossLivesScore= font.render("Boss lives: "+str(bossLives),True,(255,255,255)) 
    screen.blit(bossLivesScore, (x, y))

def player(x,y):
    screen.blit(playerImg, (x, y))

def alien(x,y,i):
    screen.blit(alienImg[i], (x, y))

def fireBullet(x,y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg,(x+16,y+10))

def fireBossBullet(x,y):
    global bossBulletState
    screen.blit(bossBulletImg,(x+16,y+10))

def boss(x,y):
    screen.blit(bossImg, (x,y))


#Game loop
running = True
while running:

    screen.fill((0, 0, 0))
    #Constant background change
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check for the direction 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -moveSpeed 
            if event.key == pygame.K_RIGHT:
                playerX_change = moveSpeed 
            if event.key == pygame.K_SPACE:
                if bulletState == "ready":
                    bulletSound = mixer.Sound(resource_path('laser.wav'))
                    bulletSound.play()
                    bulletSound.set_volume(0.015)
                    bulletX = playerX
                    fireBullet(bulletX,bulletY)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    player_rectange.center = playerX, playerY

    ##########
    # player #
    ##########
    if playerX <=0:
        playerX=0

    if playerX >=screen.get_width()-64:
        playerX=screen.get_width()-64


    ##########
    # aliens #
    ##########
    for i in range(numOfEnemies):

        ############
        # gameOver #
        ############
        if alien_rectangle[i].colliderect(player_rectange):
            for j in range(numOfEnemies):
                alienY[j]=2000
            playerY = 2000
            gameOverSound= mixer.Sound(resource_path('gameOver.wav'))
            gameOverSound.play()
            gameOverSound.set_volume(0.015)
            gameOverSound.set_volume(0.015)
            gameOverText()
            break

        alienX[i] += alienX_change[i]

        if alienX[i] <=0:
            alienX_change[i]=0.3
            alienY[i]+= alienY_change[i]

        elif alienX[i] >=screen.get_width()-64:
            alienX_change[i]= 0.3 *(-1)
            alienY[i]+= alienY_change[i]
        alien_rectangle[i].center =  alienX[i], alienY[i]
        bullet_rectangle.center = bulletX,bulletY 
        alien(alienX[i],alienY[i], i)

    ################
    # bullet state #
    ################

    if bulletState == "fire":
        fireBullet(bulletX,bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bulletY=480
        bulletState = "ready"

    ############
    # colision #
    ############
    
    for i in range(numOfEnemies):
        alien_rectangle[i].center =  alienX[i], alienY[i]
        bullet_rectangle.center = bulletX,bulletY 
        
        if alien_rectangle[i].colliderect(bullet_rectangle):
            collisionSound = mixer.Sound(resource_path('explosion.wav'))
            collisionSound.play()
            collisionSound.set_volume(0.010)
            bulletY=480
            scoreValue +=1
            bulletState="ready"
            alienX[i] = random.randint(0,(screen.get_width()-64)) 
            alienY[i] = random.randint(0,100) 
            if scoreValue % 5 == 0:
                numOfEnemies+=1
                for i in range(numOfEnemies):
                    alienImg.append(alienPicture)
                    alienX.append(random.randint(0,(screen.get_width()-64)))
                    alienY.append(random.randint(10,100))
                    alienY_change.append(92)
                    alienX_change.append(0.3) 
                     #alien_rectangle[i] = alienImg[i].get_rect()  this doesnt work. I dont know why
                    alien_rectangle= [alienImg.get_rect() for alienImg in alienImg] #this works and I dont know why

            #################################
            #         _ ._  _ , _ ._        #
            #       (_ ' ( `  )_  .__)      #
            #     ( (  (    )   `)  ) _)    #
            #    (__ (_   (_ . _) _) ,__)   #
            #        `~~`\ ' . /`~~`        #
            #        ,::: ;   ; :::,        #
            #       ':::::::::::::::'       #
            #  _jgs______/_ __ \__________  #
            # |                           | #
            # |        boss level         | #
            # |___________________________| #
            #################################

    if scoreValue >100:
        numOfEnemies = 0
        for i in range(numOfEnemies):
            alienImg.append(pygame.image.load(resource_path('alien.png')))
            alienX.append(random.randint(0,(screen.get_width()-64)))
            alienY.append(random.randint(10,100))
            alienY_change.append(92)
            alienX_change.append(0.3) 
             #alien_rectangle[i] = alienImg[i].get_rect()  this doesnt work. I dont know why
            alien_rectangle= [alienImg.get_rect() for alienImg in alienImg] #this works and I dont know why
        #spawn boss
        moveSpeed = 0.7
        bulletMoveSpeed = 3
        boss(bossX, bossY)
        boss_rectangle.center = bossX,bossY
        bullet_rectangle.center = bulletX,bulletY 
        bossBullet_rectangle.center = bossBulletX,bossBulletY 
        showBossLives(bossTextX, bossTextY)
        if boss_rectangle.colliderect(bullet_rectangle):
            bossLives -=1
            collisionSound = mixer.Sound(resource_path('explosion.wav'))
            collisionSound.play()
            collisionSound.set_volume(0.010)
            bulletY=480
            bulletState="ready"
        bossX +=bossX_change

        if bossX <=0:
            bossX_change=0.1
            bossY+= bossY_change

        elif bossX >=screen.get_width()-100:
            bossX_change= 0.3 *(-1)
            bossY+= bossY_change
        boss_rectangle.center =  bossX, bossY
        bullet_rectangle.center = bulletX,bulletY 
        boss(bossX,bossY)

        if bossBulletState == "ready":
            bossBulletX =bossX 
            fireBossBullet(bossBulletX,bossBulletY)
            bossBulletY += bossBulletY_change
        if bossBulletY >= 600:
            bossBulletY=100
            bossBulletState = "ready"

        if bossLives< 1:
            bossY=3000
            playerY = 4000
            bulletY = 2000
            bossBulletState = "fire"
            bulletMoveSpeed ="fire"
            victory()
        
        if bossBullet_rectangle.colliderect(player_rectange):
            bossY=3000
            playerY = 4000
            bulletY = 5000
            bossBulletState = "fire"
            gameOverSound= mixer.Sound(resource_path('gameOver.wav'))
            gameOverSound.play()
            gameOverSound.set_volume(0.015)
            gameOverSound.set_volume(0.015)
            bossLoss()
       
    player(playerX,playerY)
    showScore(textX,textY)
    pygame.display.update()
