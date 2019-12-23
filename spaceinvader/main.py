import pygame as pg
import random as rd
import math
from pygame import mixer

# initialize
pg.init()

# create a screen
screen = pg.display.set_mode((800, 600))

# background
background = pg.image.load('background.png')

# background sound
mixer.music.load('zelda.mp3')
mixer.music.play(-1)

# title and icon
pg.display.set_caption('Space Invader')
icon = pg.image.load('ufo.png')
pg.display.set_icon(icon)

# player
playerimg = pg.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0
speed = 5

# enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10
for i in range(num_of_enemies):
    enemyimg.append(pg.image.load('enemy.png'))
    enemyX.append(rd.randint(0, 736))
    enemyY.append(rd.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# bullet
bulletimg = pg.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'

# score
score_value = 0
font = pg.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# game over text
over_font = pg.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render('Score:' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX - bulletX), 2) + math.pow((enemyY - bulletY), 2))
    if distance <= 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        # react to key stroke
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                playerX_change = -speed
            if event.key == pg.K_RIGHT:
                playerX_change = speed
            if event.key == pg.K_SPACE:
                if bullet_state == 'ready':
                    bulletX = playerX

                    fire_bullet(playerX, bulletY)
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    playerY += playerY_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):
        # game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision == True:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 10
            enemyX[i] = rd.randint(0, 736)
            enemyY[i] = rd.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Collision

    player(playerX, playerY)
    show_score(textX, textY)
    pg.display.update()
