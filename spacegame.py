import pygame
import math 
import random
from pygame import mixer 
import sys

FPS = 60
BLACK = (0, 0, 0)
IMG_WIDTH = 50
IMG_HEIGHT = 80
green = (0, 255, 0)
mixer.init() 
pygame.init()
GAME_FONT = pygame.font.Font('Silkscreen-Bold.ttf', 45)

background_image = pygame.image.load('assets/spacebg.png')
background_size = background_image.get_size()

screen = pygame.display.set_mode(background_size)
pygame.display.set_caption('Space Eaters')

class getSprite:
    def __init__(self,image):
        self.sheet = pygame.image.load(image).convert()
    def get_sprite(self, x, y, width, height):
        sprite = pygame.surface.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite


spaceshipimage = getSprite('assets/gamesprite.png').get_sprite(0, 0, 8, 16)
spaceshipimage_left = getSprite('assets/gamesprite.png').get_sprite(8, 0, 8, 16)
spaceshipimage_right = getSprite('assets/gamesprite.png').get_sprite(16, 0, 8, 16)
life_heart_img = getSprite('assets/gamesprite.png').get_sprite(32,55,8,18)
laser_img = getSprite('assets/gamesprite.png').get_sprite(0,17,8,7)
asteriod_img = getSprite('assets/gamesprite.png').get_sprite(88,0,15,15)
scaled_asteriod = pygame.transform.scale(asteriod_img,(IMG_HEIGHT,IMG_HEIGHT))
scaled_asteriod.set_colorkey(BLACK)
alien_img = getSprite('assets/gamesprite.png').get_sprite(70,18,18,15)
scaled_alien = pygame.transform.scale(alien_img,(IMG_HEIGHT,IMG_HEIGHT))
scaled_alien.set_colorkey(BLACK)
scaled_image_laser = pygame.transform.scale(laser_img, (IMG_WIDTH,IMG_WIDTH))
scaled_image_laser.set_colorkey(BLACK)
scaled_image_heart = pygame.transform.scale(life_heart_img, (IMG_WIDTH,IMG_HEIGHT))
scaled_image_heart.set_colorkey(BLACK)
scaled_image = pygame.transform.scale(spaceshipimage, (IMG_WIDTH, IMG_HEIGHT))
scaled_image.set_colorkey(BLACK)
scaled_image_l = pygame.transform.scale(spaceshipimage_left, (IMG_WIDTH, IMG_HEIGHT))
scaled_image_l.set_colorkey(BLACK)
scaled_image_r = pygame.transform.scale(spaceshipimage_right, (IMG_WIDTH, IMG_HEIGHT))
scaled_image_r.set_colorkey(BLACK)
spaceship_x = 360
spaceship_y = 650
alien_x = random.randrange(0,720)
alien_y = random.randrange(80,200) 
alien_speed = -10
asteriod_x = random.randrange(0,720)
asteriod_y = 80
laser_x = 360
laser_y = 600
player_lives = 3
player_score = 0
check_space = False
game_over = False
running = True
game_clock = pygame.time.Clock()

def bulletaliencollision():
    dist = math.sqrt(math.pow(laser_x - alien_x,2) + math.pow(laser_y - alien_y,2))
    if dist < 30:
        return True

def spaceshipasteriodcollision():
    dist = math.sqrt(math.pow(spaceship_x - asteriod_x,2) + math.pow(spaceship_y - asteriod_y,2))
    if dist < 75:
        return True

def laserasteriodcollision():
    dist = math.sqrt(math.pow(laser_x - asteriod_x,2) + math.pow(laser_y - asteriod_y,2))
    if dist < 30:
        return True


mixer.music.load('assets/Game Music/opening theme.mp3')
mixer.music.play(-1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    screen.blit(background_image, (0, 0))  # Fill the screen with the background image
    highscoretext = GAME_FONT.render(f'SCORE: {player_score}', True, green )
    lifetext =  GAME_FONT.render(f'LIVES:', True, green)
    text_rect_l = lifetext.get_rect()
    text_rect_l.center = (450,50)
    text_rect = highscoretext.get_rect()
    text_rect.center = (180,50)
    screen.blit(highscoretext, text_rect)
    screen.blit(lifetext, text_rect_l)
    alien_x += alien_speed   
    asteriod_y += 2
    screen.blit(scaled_alien,(alien_x,alien_y))
    screen.blit(scaled_asteriod, (asteriod_x,asteriod_y))
    heart_size = 0
    for i in range(1,player_lives+1):
        screen.blit(scaled_image_heart, (550+heart_size,30))
        heart_size += 56
    if keys[pygame.K_LEFT]:
        spaceship_x -= 5
        screen.blit(scaled_image_l, (spaceship_x, spaceship_y))
    elif keys[pygame.K_RIGHT]:
        spaceship_x += 5
        screen.blit(scaled_image_r, (spaceship_x, spaceship_y)) 
    if keys[pygame.K_SPACE]:
        if not check_space:
            lasersound = mixer.Sound('assets/Game Music/laser sound.mp3')
            lasersound.play()
            check_space = True
            laser_x = spaceship_x
    else:
        screen.blit(scaled_image, (spaceship_x, spaceship_y))

    if check_space:
        screen.blit(scaled_image_laser, (laser_x,laser_y))
        laser_y -= 30
        screen.blit(scaled_image, (spaceship_x,spaceship_y))

    collision_occured = bulletaliencollision()
    asteriodhit = spaceshipasteriodcollision()
    laserasteriod = laserasteriodcollision()

    if laserasteriod:
        expsound = mixer.Sound('assets/Game Music/explosion sound.mp3')
        expsound.play()
        asteriod_x = random.randrange(0,720)
        asteriod_y = 80
        laser_y = 600
        check_space = False
    
    if asteriodhit:
        deathsound = mixer.Sound('assets/Game Music/death music.mp3')
        deathsound.play()
        player_lives -= 1 
        asteriod_x = random.randrange(0,720)
        asteriod_y = 80
        spaceship_x = 360
        spaceship_y = 650

    if collision_occured:
        expsound = mixer.Sound('assets/Game Music/explosion sound.mp3')
        expsound.play()
        player_score += 1 
        laser_y = 600
        check_space = False
        alien_x = random.randrange(0,720)
        alien_y = random.randrange(80,200)

    if(spaceship_x <= 0):
        spaceship_x = 0
    if(spaceship_x >= 720):
        spaceship_x = 720
    if(laser_y <= 0):
        laser_y = 600
        check_space = False
    if alien_x <= 0:
        alien_speed = 10
        alien_y += 50
    if alien_x >= 700:
        alien_speed = -10
        alien_y += 50
    if alien_y >= 600:
        deathsound = mixer.Sound('assets/Game Music/death music.mp3')
        deathsound.play()
        player_lives -= 1
        player_score -= 1 
        alien_x = random.randrange(0,720) 
        alien_y = random.randrange(8,200)
    if asteriod_y >= 600:
        asteriod_x = random.randrange(0,720)
        asteriod_y = 80 
    if player_score <= 0:
        player_score = 0

    if player_lives == 0:
        game_over = True 

    # Check for game restart
    if game_over:
        mixer.music.play()
        alien_y = 2000
        asteriod_y = 2000
        gameovertext = GAME_FONT.render('GAME OVER', True, green)
        text_rect_g = gameovertext.get_rect()
        text_rect_g.center = (300, 400)
        screen.blit(gameovertext, text_rect_g)
        restarttext = GAME_FONT.render('Press R to restart', True, green)
        text_rect_r = restarttext.get_rect()
        text_rect_r.center = (400, 500)
        screen.blit(restarttext, text_rect_r)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_over = False
            player_lives = 4
            player_score = 0
            spaceship_x = 360
            spaceship_y = 650

    pygame.display.update()
    game_clock.tick(FPS)