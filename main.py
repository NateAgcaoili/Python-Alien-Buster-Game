import pygame
import random
import time
import math
from button import Button


### Initializing Game ###
pygame.init()

screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("Alien Buster")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

background = pygame.image.load('background.jpg')

### Global Variables ###
alien_values = {0:-50, 1:10, 2:20, 3:30, 4:40, 5:50}
alien_images = {0:'pig.png', 1:'a1.png', 2:'a2.png', 3:'a3.png', 4:'a4.png', 5:'a5.png'}
hit_marker_skins = {0:'crosshair.png', 1:'crosshair1.png', 2:'crosshair2.png'}
player_score = 0
ai_one_score = 0
ai_two_score = 0
iteration_count = 0
current_time = 0
time_left = 6000
ammo = 25
playing_game = False
is_reloading = False
is_shooting = False

class Alien():
    points_font = pygame.font.Font('freesansbold.ttf', 32)
    def __init__(self, alien_id):
        self.value = alien_values[alien_id]
        self.skin = pygame.image.load(alien_images[alien_id])
        self.y_position = random.randint(360, 650)
        self.dead_wait = 0
        self.is_hit = False
        self.hit_by = 0
        self.points_tag = Alien.points_font.render(f"{self.value}", True, (0, 0, 255))
        self.r_l = random.randint(0,1)
        if self.r_l == 0:
            self.x_position = 1130
            self.x_change = random.uniform(-5,-2)
        else:
            self.x_position = -50
            self.x_change = random.uniform(2,5)

    def appear(self):
        screen.blit(self.skin, (self.x_position, self.y_position))
        if self.is_hit == True:
            screen.blit(self.points_tag, (self.x_position + 12, self.y_position - 20))
    
    def randomize(self):
        alien_id = random.randint(0,5)
        self.r_l = random.randint(0,1)
        self.value = alien_values[alien_id]
        self.skin = pygame.image.load(alien_images[alien_id])
        if self.r_l == 0:
            self.x_position = 1130
            self.x_change = random.uniform(-5,-2)
        else:
            self.x_position = -50
            self.x_change = random.uniform(2,5)
        self.y_position = random.randint(360, 650)
        self.is_hit = False
        self.dead_wait = 0
        
    def player_hit(self):
        if self.is_hit == False:
            self.is_hit = True
            self.x_change = 0
            self.hit_by = 0
            self.points_tag = Alien.points_font.render(f"{self.value}", True, (0, 0, 255))
            global player_score
            if player_score + self.value > 0:
                player_score += self.value
            else:
                player_score = 0

    def ai_check(self):
        if self.is_hit == False:
            steal_point = random.randint(0, 250)
            if steal_point == 69:
                ai_picker = random.randint(1,2)
                if self.value == -50:
                    ai_picker = random.randint(1,6) # Less likely to shoot a pig
                if ai_picker is 1:
                    self.is_hit = True
                    self.x_change = 0
                    self.points_tag = Alien.points_font.render(f"{self.value}", True, (255, 0, 0))
                    ai_one_click.x_position = self.x_position + 32
                    ai_one_click.y_position = self.y_position + 32
                    self.hit_by = 1
                    global ai_one_score
                    ai_one_score += self.value
                elif ai_picker is 2:
                    self.is_hit = True
                    self.x_change = 0
                    self.points_tag = Alien.points_font.render(f"{self.value}", True, (0, 255, 0))
                    ai_two_click.x_position = self.x_position + 32
                    ai_two_click.y_position = self.y_position + 32
                    self.hit_by = 2
                    global ai_two_score
                    ai_two_score += self.value

class HitMarker():
    def __init__(self, id):
        self.skin = pygame.image.load(hit_marker_skins[id])
        self.x_position = 0
        self.y_position = 0

    def appear(self):
        screen.blit(self.skin, (self.x_position - 32, self.y_position - 32))

### Game Objects ###
alien_one = Alien(random.randint(0,5))
alien_two = Alien(random.randint(0,5))
alien_three = Alien(random.randint(0,5))
alien_four = Alien(random.randint(0,5))
alien_five = Alien(random.randint(0,5))
aliens = [alien_one, alien_two, alien_three, alien_four, alien_five]
score_font = pygame.font.Font('freesansbold.ttf', 24)
play_button = Button((255,255,255), 200, 200, 150, 100, 60, 'hi')
ammo_button = Button((255, 255, 255), 900, 30, 160, 50, 32, f"AMMO: {ammo}")
player_click = HitMarker(0)
ai_one_click = HitMarker(1)
ai_two_click = HitMarker(2)
hit_markers = [player_click, ai_one_click, ai_two_click]


def show_ammo():
    red = abs(25 - ammo) * 10
    green = 255 - red
    ammo_button.color = (red, green, 0)
    if ammo == 0:
        ammo_button.text = "Click to Reload"
    else:
        ammo_button.text = f"AMMO: {ammo}"
    ammo_button.draw(screen, True)

def show_scores():
    p_score = score_font.render(f"Player Points: {player_score}", True, (0, 0, 255))
    a1_score = score_font.render(f"AI 1 Points: {ai_one_score}", True, (255, 0, 0))
    a2_score = score_font.render(f"AI 2 Points: {ai_two_score}", True, (0, 255, 0))
    screen.blit(p_score, (10, 10))
    screen.blit(a1_score, (10, 40))
    screen.blit(a2_score, (10, 70))

def show_time_left():
    converted_time = time_left // 100
    time_left_display = score_font.render(f"Time Left: {converted_time}", True, (255, 255, 255))
    screen.blit(time_left_display, (540, 10))

def is_shot(alien_x, alien_y, player_x, player_y):
    distance = math.sqrt(((alien_x - player_x) ** 2) + ((alien_y - player_y) ** 2))
    if distance < 40:
        return True
    return False

running = True
while running:
    pos = pygame.mouse.get_pos()
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    if playing_game == True:
        show_ammo()
        show_scores()
        show_time_left()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_shooting == False:
                    if ammo > 0 and is_reloading == False and not ammo_button.is_over(pos):
                        is_shooting = True
                        iteration_count = 0
                        player_click.x_position = pos[0]
                        player_click.y_position = pos[1]
                        ammo += -1
                if ammo_button.is_over(pos):
                    is_reloading = True
                    iteration_count = 0
        if time_left <= 0:
            playing_game = False
        for alien in aliens:
            alien.x_position += alien.x_change
            alien.appear()
            if alien.r_l == 0:
                if alien.x_position <= -60:
                    alien.randomize()
            elif alien.r_l == 1:
                if alien.x_position >= 1200:
                    alien.randomize()
            if alien.dead_wait > 25:
                hit_markers[alien.hit_by].appear()
            if alien.dead_wait > 50:
                alien.randomize()
            if alien.is_hit == True:
                alien.dead_wait += 1
            if is_shot(alien.x_position, alien.y_position, player_click.x_position, player_click.y_position):
                if is_shooting == True:
                    alien.player_hit()
            alien.ai_check()
        if iteration_count > 25:
            is_shooting = False
        if is_shooting == True:
            player_click.appear()
            iteration_count += 1
        if ammo == 25:
            is_reloading = False
        if is_reloading:
            if ammo < 25 and iteration_count % 5 == 0:
                ammo += 1
            iteration_count += 1
        time_left -= 1
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_over(pos):
                    playing_game = True
        play_button.draw(screen)
    pygame.display.update()
    clock.tick(100)