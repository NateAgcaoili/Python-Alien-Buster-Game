import pygame
import random
import time

### Initializing Game ###
pygame.init()

screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("Alien Buster")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

background = pygame.image.load('background.jpg')

### Global Variables ###
alien_values = {0:-50, 1:10, 2:20, 3:30, 4:40, 5:50}
alien_images = {0:'pig.png', 1:'a1.png', 2:'a2.png', 3:'a3.png', 4:'a4.png', 5:'a5.png'}
player_score = 0
ai_one_score = 0
ai_two_score = 0

class Alien():
    def __init__(self, alien_number):
        self.value = alien_values[alien_number]
        self.skin = pygame.image.load(alien_images[alien_number])
        self.x_position = random.randint(0, 1010)
        self.y_position = random.randint(360, 650)
    def appear(self):
        screen.blit(self.skin, (self.x_position, self.y_position))

alien_one = Alien(0)
alien_two = Alien(0)
alien_three = Alien(0)
alien_four = Alien(0)
alien_five = Alien(0)
aliens = [alien_one, alien_two, alien_three, alien_four, alien_five]

def alien_spawner():
    random_num = random.randint(0,4)
    aliens[random_num] = Alien(random.randint(0,5))
    aliens[random_num].appear()
    time.sleep(4)

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    alien_spawner()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()