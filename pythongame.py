import pygame
import random
import math

# Initializing the pygame

pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))  # 800-width 600-height

# Background
background = pygame.image.load('background1.png')
# Background Sound
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")  # sets the name of the game
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('gaming.png')
playerx = 370
playery = 480
playerx_change = 0

# enemy
enemyImg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('people.png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(4)
    enemyy_change.append(40)

# bullet
bulletImg = pygame.image.load('security.png')
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 10
bullet_state = "Ready"  # Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

# Scores:
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

testX = 10
testY = 10

# Game Over-Text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render(" GAME OVER ", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))  # blit:draw,screen:surface


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # blit:draw,screen:surface


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    if (distance < 27):
        return True
    else:
        return False


# awind=any action in the game
running = True
while running:
    screen.fill((161, 32, 32))  # rgb color->red  green blue

    # background Image
    screen.blit(background, (0, 0))  # since the image is heavy :.Iteration is slow

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False

        # if a keystroke is pressed check whether it's right or left

        if (event.type == pygame.KEYDOWN):
            # print("A keystroke is pressed")
            if event.key == pygame.K_LEFT:
                playerx_change = -5
            if event.key == pygame.K_RIGHT:
                playerx_change = 5
            if event.key == pygame.K_SPACE:
                # Get the current x-coordinate of the spaceship
                if bullet_state == "Ready":
                    bullet_sound = pygame.mixer.Sound("shoot.wav")
                    bullet_sound.play()
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)

        if (event.type == pygame.KEYUP):
            if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                playerx_change = 0
    # Checking for boundaries of spaceship so it doesn't go out of bounds
    playerx += playerx_change

    if (playerx <= 0):
        playerx = 0
    elif (playerx >= 736):
        playerx = 736

    # Enemy Movements
    for i in range(num_of_enemies):

        # Game-Over
        if (enemyy[i] > 440):
            for j in range(num_of_enemies):
                enemyy[j] = 2000
            game_over_text()
            break

        enemyx[i] += enemyx_change[i]

        if (enemyx[i] <= 0):
            enemyx_change[i] = 4
            enemyy[i] += enemyy_change[i]
        elif (enemyx[i] >= 736):
            enemyx_change[i] = -4
            enemyy[i] += enemyy_change[i]

        # collision
        collision = isCollision(enemyx[i], enemyy[i], bulletx, bullety)
        if (collision):
            explosion_sound = pygame.mixer.Sound("invaderkilled.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "Ready"
            score_value += 1
            print(score_value)
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 150)

        enemy(enemyx[i], enemyy[i], i)

    # Bullet Movement
    if (bullety <= 0):
        bullety = 480
        bullet_state = "Ready"

    if bullet_state == "Fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    player(playerx, playery)
    show_score(testX, testY)
    pygame.display.update()
