import pygame
import random
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
background2_inside = pygame.image.load('background2_inside.png')
background2_outside = pygame.image.load('background2_outside.png')

### Global Variables ###
alien_values = [-50, 10, 20, 30, 40, 50]
alien_images = ['pig.png', 'a1.png', 'a2.png', 'a3.png', 'a4.png', 'a5.png']
hit_marker_skins = ['crosshair.png', 'crosshair1.png', 'crosshair2.png']
astronaut_skins = ['playerchar.png', 'ai1char.png', 'ai2char.png', 'player_eject.png', 'ai1_eject.png', 'ai2_eject.png']
astronaut_coordinates = [[200, 500], [400, 500], [0, 125]]
player_score = 0
ai_one_score = 0
ai_two_score = 0
iteration_count = 0
current_time = 0
start_time = 0
first_place = 0
second_place = 1
third_place = 2
time_left = 6000
ammo = 25
playing_game = False
doing_countdown = False
end_game = False
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
                if ai_picker == 1:
                    self.is_hit = True
                    self.x_change = 0
                    self.points_tag = Alien.points_font.render(f"{self.value}", True, (255, 0, 0))
                    ai_one_click.x_position = self.x_position + 32
                    ai_one_click.y_position = self.y_position + 32
                    self.hit_by = 1
                    global ai_one_score
                    ai_one_score += self.value
                elif ai_picker == 2:
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

class Astronaut():
    def __init__(self, id):
        self.skin = pygame.image.load(astronaut_skins[id])
        self.skin_eject = pygame.image.load(astronaut_skins[id + 3])
        self.x_position = 0
        self.y_position = 0
        self.last_place = False
    
    def appear(self):
        if self.last_place == True:
            screen.blit(self.skin_eject, (self.x_position, self.y_position))
        else:
            screen.blit(self.skin, (self.x_position, self.y_position))

### Game Objects ###
score_font = pygame.font.Font('freesansbold.ttf', 24)
start_font = pygame.font.Font('freesansbold.ttf', 256)
play_button = Button((255,255,255), 200, 200, 150, 100, 60, 'hi')
ammo_button = Button((255, 255, 255), 900, 30, 160, 50, 32, f"AMMO: {ammo}")
player_click = HitMarker(0)
ai_one_click = HitMarker(1)
ai_two_click = HitMarker(2)
hit_markers = [player_click, ai_one_click, ai_two_click]
start_text = ["3", "2", "1", "GO!"]
astronauts = []
for i in range(3):
    astronaut = Astronaut(i)
    astronauts.append(astronaut)
aliens = []
for i in range(5):
    alien = Alien(0)
    aliens.append(alien)


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
    screen.blit(time_left_display, (500, 10))

def show_countdown():
    converted_time = start_time // 100
    start_countdown = start_font.render(start_text[converted_time], True, (255, 255, 255))
    if converted_time < 3:
        screen.blit(start_countdown, (500, 250))
    else:
        screen.blit(start_countdown, (350, 250))

def is_shot(alien_x, alien_y, player_x, player_y):
    distance = math.sqrt(((alien_x - player_x) ** 2) + ((alien_y - player_y) ** 2))
    if distance < 40:
        return True
    return False

def reset_game():
    global time_left
    global start_time
    global player_score
    global ai_one_score
    global ai_two_score
    global ammo
    time_left = 6000
    start_time = 0
    player_score = 0
    ai_one_score = 0
    ai_two_score = 0
    ammo = 25
    for alien in aliens:
        alien.randomize()

def determine_placements():
    global first_place
    global second_place
    global third_place
    if player_score > ai_one_score:
        if player_score > ai_two_score: # 0 > 1
            first_place = 0
            second_place = 1
            third_place = 2
        else: # 2 > 0 > 1
            first_place = 2
            second_place = 0
            third_place = 1
    elif player_score > ai_two_score: # 1 > 0
        if ai_one_score > ai_two_score: # 1 > 0 > 2
            first_place = 1
            second_place = 0
            third_place = 2
        else: 
            first_place = 2
            second_place = 1
            third_place = 0
    else:
        if ai_one_score > ai_two_score:
            first_place = 1
            second_place = 2
            third_place = 0
        else:
            first_place = 2
            second_place = 1
            third_place = 0

def set_astronaut_values():
    astronauts[first_place].x_position = astronaut_coordinates[0][0]
    astronauts[first_place].y_position = astronaut_coordinates[0][1]
    astronauts[second_place].x_position = astronaut_coordinates[1][0]
    astronauts[second_place].y_position = astronaut_coordinates[1][1]
    astronauts[third_place].x_position = astronaut_coordinates[2][0]
    astronauts[third_place].y_position = astronaut_coordinates[2][1]
    astronauts[third_place].last_place = True

running = True
while running:
    pos = pygame.mouse.get_pos()
    screen.fill((0, 0, 0))
    if doing_countdown == True:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if start_time <= 390:
            show_countdown()
        else:
            reset_game()
            doing_countdown = False
            playing_game = True
        start_time += 1
    elif playing_game == True:
        screen.blit(background, (0, 0))
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
            determine_placements()
            set_astronaut_values()
            playing_game = False
            end_game = True
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
    elif end_game == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(background2_outside, (0, 0))
        astronauts[third_place].appear()
        screen.blit(background2_inside, (0, 0))
        astronauts[first_place].appear()
        astronauts[second_place].appear()
        show_scores()
        astronauts[third_place].x_position += 1.4
    else:
        screen.blit(background2_inside, (0, 0))
        screen.blit(background2_outside, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_over(pos):
                    start_time = 0
                    doing_countdown = True
        play_button.draw(screen)
    pygame.display.update()
    clock.tick(100)