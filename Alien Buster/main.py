import pygame
import random
import math
from button import Button
from os import path

music_path = path.join(path.dirname(__file__), 'Assets', 'Audio', 'Music')
soundfx_path = path.join(path.dirname(__file__), 'Assets', 'Audio', 'SoundEffects')
aliens_path = path.join(path.dirname(__file__), 'Assets', 'Images', 'Aliens')
astronauts_path = path.join(path.dirname(__file__), 'Assets', 'Images', 'Astronauts')
backgrounds_path = path.join(path.dirname(__file__), 'Assets', 'Images', 'Backgrounds')
gfx_path = path.join(path.dirname(__file__), 'Assets', 'Images', 'MiscGfx')
print(gfx_path)

### Initializing Game ###
pygame.init()

screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("Alien Buster")
icon = pygame.image.load(path.join(gfx_path, 'icon.png'))
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

background = pygame.image.load(path.join(backgrounds_path, 'background.jpg'))
background2_inside = pygame.image.load(path.join(backgrounds_path, 'background2_inside.png'))
background2_outside = pygame.image.load(path.join(backgrounds_path, 'background2_outside.png'))
background_menu = pygame.image.load(path.join(backgrounds_path, 'background_menu.png'))
background_menu_play = pygame.image.load(path.join(backgrounds_path, 'background_menu_play.png'))
pygame.mixer.music.load(path.join(music_path, 'main_menu.wav') )
pygame.mixer.music.play(-1) #loops background music

### Global Variables ###
player_score = 0
ai_one_score = 0
ai_two_score = 0
iteration_count = 0
start_time = 0
time_left = 6000
ammo = 25
playing_game = False
doing_countdown = False
end_game = False
is_reloading = False
is_shooting = False

class Alien():
    point_values = [-50, 10, 20, 30, 40, 50]
    skins = [
    path.join(aliens_path, 'pig.png'), path.join(aliens_path,'alien_1.png'), 
    path.join(aliens_path,'alien_2.png'), path.join(aliens_path,'alien_3.png'), 
    path.join(aliens_path,'alien_4.png'), path.join(aliens_path,'alien_5.png')
    ]
    hit_marker_skins = [
    path.join(gfx_path, 'crosshair.png'), 
    path.join(gfx_path, 'crosshair1.png'), 
    path.join(gfx_path, 'crosshair2.png')
    ]
    points_font = pygame.font.Font('freesansbold.ttf', 32)
    hit_sound = pygame.mixer.Sound(path.join(soundfx_path, 'hit_sound.wav'))
    pig_hit = pygame.mixer.Sound(path.join(soundfx_path, 'pig_hit.wav'))

    def __init__(self, alien_id):
        self.value = Alien.point_values[alien_id]
        self.skin = pygame.image.load(Alien.skins[alien_id])
        self.hit_marker_skin = pygame.image.load(Alien.hit_marker_skins[0])
        self.y_position = 0
        self.dead_wait = 0
        self.is_hit = False
        self.hit_by = 0
        self.points_tag = Alien.points_font.render(f"{self.value}", True, (0, 0, 255))
        self.r_l = 0
        self.x_position = 0
        self.x_change = 0

    def appear(self):
        screen.blit(self.skin, (self.x_position, self.y_position))
        if self.is_hit == True:
            screen.blit(self.points_tag, (self.x_position + 12, self.y_position - 20))
            screen.blit(self.hit_marker_skin, (self.x_position, self.y_position))
    
    def randomize(self):
        alien_id = random.randint(0,5)
        self.value = Alien.point_values[alien_id]
        self.skin = pygame.image.load(Alien.skins[alien_id])
        self.y_position = random.randint(360, 650)
        self.is_hit = False
        self.dead_wait = 0
        self.r_l = random.randint(0,1)
        if self.r_l == 0:
            self.x_position = 1130
            self.x_change = random.uniform(-4.5,-1.5)
        else:
            self.x_position = -50
            self.x_change = random.uniform(1.5,4.5)
        
    def player_hit(self):
        if self.is_hit == False:
            self.is_hit = True
            Alien.hit_sound.play()
            self.x_change = 0
            self.hit_by = 0
            self.hit_marker_skin = pygame.image.load(path.join(gfx_path, 'hitmarker.png'))
            self.points_tag = Alien.points_font.render(f"{self.value}", True, (0, 0, 255))
            if self.value == -50:
                Alien.pig_hit.play()
            global player_score
            if player_score + self.value > 0:
                player_score += self.value
            else:
                player_score = 0

    def ai_check(self):
        if self.is_hit == False:
            steal_point = random.randint(0, 150) #230
            if steal_point == 69:
                ai_picker = random.randint(1,2)
                if self.value == -50:
                    ai_picker = random.randint(1,8) # Less likely to shoot a pig
                if ai_picker == 1:
                    self.is_hit = True
                    self.x_change = 0
                    self.hit_by = 1
                    self.hit_marker_skin = pygame.image.load(Alien.hit_marker_skins[self.hit_by])
                    self.points_tag = Alien.points_font.render(f"{self.value}", True, (255, 0, 0))
                    global ai_one_score
                    if ai_one_score + self.value > 0:
                        ai_one_score += self.value
                    else:
                        ai_one_score = 0
                elif ai_picker == 2:
                    self.is_hit = True
                    self.x_change = 0
                    self.hit_by = 2
                    self.hit_marker_skin = pygame.image.load(Alien.hit_marker_skins[self.hit_by])
                    self.points_tag = Alien.points_font.render(f"{self.value}", True, (0, 255, 0))
                    global ai_two_score
                    if ai_two_score + self.value > 0:
                        ai_two_score += self.value
                    else:
                        ai_two_score = 0

class HitMarker():
    skins = [
    path.join(gfx_path, 'crosshair.png'), 
    path.join(gfx_path, 'crosshair1.png'), 
    path.join(gfx_path, 'crosshair2.png')
    ]

    def __init__(self, id):
        self.skin = pygame.image.load(HitMarker.skins[id])
        self.x_position = 0
        self.y_position = 0
        self.can_hit = True

    def appear(self):
        screen.blit(self.skin, (self.x_position - 32, self.y_position - 32))

class Astronaut():
    skins = [
    path.join(astronauts_path, 'player_char.png'), path.join(astronauts_path, 'ai_1_char.png'), 
    path.join(astronauts_path, 'ai_2_char.png'), path.join(astronauts_path, 'player_eject.png'), 
    path.join(astronauts_path, 'ai_1_eject.png'), path.join(astronauts_path, 'ai_2_eject.png')
    ]
    coordinates = [[400, 500], [200, 500], [0, 200]]

    def __init__(self, id):
        self.skin = pygame.image.load(Astronaut.skins[id])
        self.skin_eject = pygame.image.load(Astronaut.skins[id + 3])
        self.crown = pygame.image.load(path.join(astronauts_path, 'winner_crown.png'))
        self.x_position = 0
        self.y_position = 0
        self.place = 0
    
    def appear(self):
        if self.place == 2:
            screen.blit(self.skin_eject, (self.x_position, self.y_position))
        else:
            screen.blit(self.skin, (self.x_position, self.y_position))
            if self.place == 0:
                screen.blit(self.crown, (self.x_position - 10, self.y_position - 80))

### Game Objects ###
score_font = pygame.font.Font('freesansbold.ttf', 24)
start_font = pygame.font.Font('freesansbold.ttf', 256)
play_button = Button((255,255,255), 253, 360, 230, 80, 60, 'Play')
help_button = Button((255,255,255), 595, 360, 230, 80, 60, 'Help')
play_again_button = Button((255,255,255), 718, 507, 115, 30, 30, 'Play Again')
main_menu_button = Button((255,255,255), 840, 507, 115, 30, 30, 'Main Menu')
ammo_button = Button((255, 255, 255), 900, 30, 160, 50, 32, f"AMMO: {ammo}")
player_click = HitMarker(0)
ai_one_click = HitMarker(1)
ai_two_click = HitMarker(2)
hit_markers = [player_click, ai_one_click, ai_two_click]
start_text = ["3", "2", "1", "GO!"]
countdown = pygame.mixer.Sound(path.join(soundfx_path, 'countdown.wav'))
reload_sound = pygame.mixer.Sound(path.join(soundfx_path, 'reload.wav'))
astronauts = []
for i in range(3):
    astronaut = Astronaut(i)
    astronauts.append(astronaut)
sorted_astronauts = astronauts[:]
aliens = []
for i in range(5):
    alien = Alien(0)
    aliens.append(alien)
    alien.randomize()

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
    if playing_game == True:
        screen.blit(p_score, (10, 10))
        screen.blit(a1_score, (10, 40))
        screen.blit(a2_score, (10, 70))
    elif end_game == True:
        screen.blit(p_score, (715, 400))
        screen.blit(a1_score, (715, 435))
        screen.blit(a2_score, (715, 470))

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
    distance = math.sqrt(((alien_x - (player_x - 32)) ** 2) + ((alien_y - player_y) ** 2))
    if distance < 45:
        return True
    return False

def reset_game():
    global time_left
    global start_time
    global player_score
    global ai_one_score
    global ai_two_score
    global ammo
    pygame.mouse.set_visible(False)
    time_left = 6000
    start_time = 0
    player_score = 0
    ai_one_score = 0
    ai_two_score = 0
    ammo = 25
    for alien in aliens:
        alien.randomize()

def determine_placements():
    if player_score > ai_one_score:
        if player_score > ai_two_score: # 0 > 1
            astronauts[0].place = 0
            astronauts[1].place = 1
            astronauts[2].place = 2
        else: # 2 > 0 > 1
            astronauts[0].place = 1
            astronauts[1].place = 2
            astronauts[2].place = 0
    elif player_score > ai_two_score: # 1 > 0
        if ai_one_score > ai_two_score: # 1 > 0 > 2
            astronauts[0].place = 1
            astronauts[1].place = 0
            astronauts[2].place = 2
        else:
            astronauts[0].place = 2
            astronauts[1].place = 1
            astronauts[2].place = 0
    else:
        if ai_one_score > ai_two_score:
            astronauts[0].place = 2
            astronauts[1].place = 0
            astronauts[2].place = 1
        else:
            astronauts[0].place = 2
            astronauts[1].place = 1
            astronauts[2].place = 0

def prep_astronauts():
    for astronaut in astronauts:
        astronaut.x_position = Astronaut.coordinates[astronaut.place][0]
        astronaut.y_position = Astronaut.coordinates[astronaut.place][1]
        sorted_astronauts[astronaut.place] = astronaut


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
            countdown.stop()
            pygame.mixer.music.load(path.join(music_path, 'playing_game.wav'))
            pygame.mixer.music.play(-1)
            playing_game = True
        start_time += 1
    elif playing_game == True:
        screen.blit(background, (0, 0))
        show_ammo()
        show_scores()
        show_time_left()
        player_click.x_position = pos[0]
        player_click.y_position = pos[1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_shooting == False:
                    if ammo > 0 and is_reloading == False and not ammo_button.is_over(pos):
                        is_shooting = True
                        iteration_count = 0
                        """player_click.x_position = pos[0]
                        player_click.y_position = pos[1]"""
                        shoot_sound = pygame.mixer.Sound(path.join(soundfx_path, 'shoot.wav'))
                        shoot_sound.play()
                        ammo += -1
                if ammo_button.is_over(pos):
                    reload_sound.play()
                    is_reloading = True
                    iteration_count = 0
        if time_left <= 0:
            determine_placements()
            prep_astronauts()
            pygame.mouse.set_visible(True)
            playing_game = FalseS
            for alien in aliens:
                alien.randomize()
            pygame.mixer.music.load(path.join(music_path, 'end_game.wav'))
            pygame.mixer.music.play(-1)
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
                player_click.can_hit = True
                pass
                #hit_markers[alien.hit_by].appear()
            if alien.dead_wait > 50:
                alien.randomize()
            if alien.is_hit == True:
                alien.dead_wait += 1
            if is_shot(alien.x_position, alien.y_position, player_click.x_position, player_click.y_position):
                if is_shooting == True and player_click.can_hit == True:
                    player_click.can_hit = False
                    alien.player_hit()
            alien.ai_check()
        if iteration_count > 15:
            is_shooting = False
        if is_shooting == True:
            iteration_count += 1
        """elif is_shooting == False:
            player_click.x_position = 2000
            player_click.y_position = 2000"""
        if ammo == 25:
            reload_sound.stop()
            is_reloading = False
        if is_reloading:
            if ammo < 25 and iteration_count % 5 == 0:
                ammo += 1
            iteration_count += 1
        player_click.appear()
        time_left -= 1
    elif end_game == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                if play_again_button.is_over(pos):
                    play_again_button.color = (0, 255, 0)
                elif main_menu_button.is_over(pos):
                    main_menu_button.color = (192, 192, 192)
                else:
                    play_again_button.color = (255, 255, 255)
                    main_menu_button.color = (255, 255, 255)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.is_over(pos):
                    start_time = 0
                    end_game = False
                    pygame.mixer.music.stop()
                    countdown.play()
                    doing_countdown = True
                elif main_menu_button.is_over(pos):
                    pygame.mixer.music.load(path.join(music_path, 'main_menu.wav'))
                    pygame.mixer.music.play(-1)
                    end_game = False
        screen.blit(background2_outside, (0, 0))
        sorted_astronauts[2].appear()
        for alien in aliens:
            alien.x_position += alien.x_change
            alien.appear()
            if alien.r_l == 0:
                if alien.x_position <= -60:
                    alien.randomize()
            elif alien.r_l == 1:
                if alien.x_position >= 1200:
                    alien.randomize()
        screen.blit(background2_inside, (0, 0))
        sorted_astronauts[0].appear()
        sorted_astronauts[1].appear()
        show_scores()
        if sorted_astronauts[2].x_position < 1020:
            sorted_astronauts[2].x_position += 12
        else:
            play_again_button.draw(screen)
            main_menu_button.draw(screen)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_over(pos):
                    pygame.mixer.music.stop()
                    countdown.play()
                    doing_countdown = True
        if play_button.is_over(pos):
            screen.blit(background_menu_play, (0, 0))
        else:
            screen.blit(background_menu, (0, 0))
    pygame.display.update()
    clock.tick(100)