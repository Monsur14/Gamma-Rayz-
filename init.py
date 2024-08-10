import pygame
import math
import random
from pygame import mixer 

pygame.init()

screen = pygame.display.set_mode((800,600))

background = pygame.image.load('pngtree-space-game-alien-exploration-background-picture-image_1592274.jpg')

mixer.music.load('mursic.wav')
mixer.music.play(-1)

pygame.display.set_caption("Gamma Rayz 👾")

playerImage = pygame.image.load('rifle3.png')
playerX = 370
playerY = 480
playerXChange = 0

enemyplayerImage = []
enemyplayerX = []
enemyplayerY = []
enemyplayerXChange = []
enemyplayerYChange = []
numofenemy = 6

for i in range(numofenemy):
    enemyplayerImage.append(pygame.image.load('ghost.png'))
    enemyplayerX.append(random.randint(0,735))
    enemyplayerY.append(random.randint(50, 150))
    enemyplayerXChange.append(4)
    enemyplayerYChange.append(40)

bulletImage = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletXChange = 0
bulletYChange = 10
bulletState = "ready"

score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

gamefont = pygame.font.Font('freesansbold.ttf', 64)

def showscore(x,y):
    scoreshow = font.render("Score: " + str(score),True, (0,255,255))
    screen.blit(scoreshow, (x,y))

def game_over_text(x,y):  
    over_text = gamefont.render("Game Over", True, (0,255,255))
    screen.blit(over_text,(200,250))

def player(x,y):
    screen.blit(playerImage,(x, y))

def enemy(x,y,i):
    screen.blit(enemyplayerImage[i],(x,y))

def bullet(x,y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImage, (x + 16, y + 10))

def collision(enemyplayerX,enemyplayerY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyplayerX - bulletX, 2)) + (math.pow(enemyplayerY - bulletY,2))
    if distance < 27:
        return True
    else:
        return False

run = True

while run:

    screen.fill((0,0,0))
    
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXChange = -5
            if event.key == pygame.K_RIGHT:
                playerXChange = 5
            if event.key == pygame.K_SPACE:
                if bulletState is "ready":
                    bulletSound = mixer.Sound('laser.wav')
                    bulletSound.play()
                    bulletX = playerX
                    bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXChange = 0


    playerX += playerXChange

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(numofenemy):

        if enemyplayerY[i] > 440:
            for j in range(numofenemy):
                enemyplayerY[j] = 2000
            game_over_text(playerX,playerY)
            break

        enemyplayerX[i] += enemyplayerXChange[i]

        if enemyplayerX[i] <= 0:
            enemyplayerXChange[i] = 4
            enemyplayerY[i] += enemyplayerYChange[i]

        elif enemyplayerX[i] >= 736:
            enemyplayerXChange[i] = -4
            enemyplayerY[i] += enemyplayerYChange[i]

        collisio = collision(enemyplayerX[i], enemyplayerY[i],bulletX,bulletY)
        if collisio:
            explosionSound = mixer.Sound('explosion.wav')
            explosionSound.play()
            bulletY = 480
            bulletState = "ready"
            score += 1 
            enemyplayerX[i] = random.randint(0,735)
            enemyplayerY[i] = random.randint(50, 150)

        enemy(enemyplayerX[i],enemyplayerY[i],i)

    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"

    if bulletState is "fire":
        bullet(bulletX, bulletY)
        bulletY -= bulletYChange

    
    
    player(playerX,playerY)
    showscore(textX, textY)
    pygame.display.update() 