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
        global is_spawning
        self.value = alien_values[alien_number]
        self.skin = pygame.image.load(alien_images[alien_number])
        self.x_position = random.randint(100, 900)
        self.y_position = random.randint(360, 650)
        self.is_hit = False

    def appear(self):
        screen.blit(self.skin, (self.x_position, self.y_position))
        
    def ai_check(self):
        time.sleep(random.uniform(0.1,0.7))
        ai_picker = random.randint(1,2)
        if self.value == -50:
            ai_picker = random.randint(1,6) # Less likely to shoot a pig
        points_font = pygame.font.Font('freesansbold.ttf', 32)
        if ai_picker is 1:
            self.is_hit = True
            points_tag = points_font.render(f"{self.value}", True, (255, 0, 0))
            global ai_one_score
            ai_one_score += self.value
            screen.blit(points_tag, (self.x_position + 12, self.y_position - 20))
            #print(f"ai one: {ai_one_score} (+ {self.value})")
        elif ai_picker is 2:
            self.is_hit = True
            points_tag = points_font.render(f"{self.value}", True, (0, 255, 0))
            global ai_two_score
            ai_two_score += self.value
            screen.blit(points_tag, (self.x_position + 12, self.y_position - 20))
            #print(f"ai two: {ai_two_score} (+ {self.value})")
        pygame.display.update()

alien_one = Alien(0)
alien_two = Alien(0)
alien_three = Alien(0)
alien_four = Alien(0)
alien_five = Alien(0)
aliens = [alien_one, alien_two, alien_three, alien_four, alien_five]


def alien_spawner():
    alien_gen = random.randint(1,4) # 1 = 1-2 aliens possibly spawning, 2 = 1-3 aliens ..., 4 = 1-5 aliens possibly spawning
    spawn_count = random.randint(1, alien_gen+1) # first - alien_gen or less will be generated and appear
    print(f"spawning {spawn_count}")
    for i in range(spawn_count):
        aliens[i] = Alien(random.randint(0,5))
        aliens[i].appear()
    pygame.display.update()
    for i in range(spawn_count):
        aliens[i].ai_check()
    time.sleep(1)

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    alien_spawner()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()