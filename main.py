import pygame
import random as r
from sys import exit
import math
from pygame.locals import *

#region init...
player_data_ = open("Player data.txt", "r+")
player_data = player_data_.readlines()
flags = FULLSCREEN | DOUBLEBUF | SRCALPHA
title = "title"
pygame.init()
pygame.display.set_caption(title)
clock = pygame.time.Clock()
arena_size = 1
screen = pygame.display.set_mode((1920, 1080), flags, 16)
menu = pygame.Surface(screen.get_size())
ui = pygame.Surface((screen.get_size()[0], screen.get_size()[1]), SRCALPHA)
buttonclick = pygame.mixer.Sound("sfx/destroy.mp3")
#endregion

#region functinos...

def reset():
    pass
    global shooting
    global shot_speed
    global bullet_damage
    global points
    global wave
    global dashing
    global level
    global sub_exp
    global level_points
    global dashed
    global dead
    global ui_update
    global recoil_reduction
    global vawe
    global menuon
    global player_colors
    global enemies
    global player
    global cursor
    global bullets
    global particles
    global level_bar

    shooting = False
    shot_speed = 2
    bullet_damage = 1
    points = 0
    wave = 0
    dashing = False
    level = 1
    sub_exp = 0
    level_points = 0
    dashed = False
    dead = False
    ui_update = 2
    recoil_reduction = 0
    vawe = 0
    menuon = False
    player_colors = {0: (237, 37, 78), 1: (255, 166, 48), 2: (71, 160, 37), 3: (215, 73, 50)}
    enemies = []
    player = Controller([render.get_width() / 2, render.get_height() / 2], "sprites/player{}.png".format(wave + 1))
    cursor = Mouse()
    bullets = []
    particles = []
    level_bar = Progressbar(1000)

def degrees_to_radians(degrees):
    radians = degrees * math.pi / 180
    return radians

def direction(v1, v2):
    dx = v2[0] - v1[0]
    dy = v2[1] - v1[1]
    mag = math.sqrt(dx**2 + dy**2)
    if mag == 0:
        return [0, 0]
    else:
        return [dx/mag, dy/mag]

def distance(pos1, pos2):
    x1 = pos1[0]
    y1 = pos1[1]
    x2 = pos2[0]
    y2 = pos2[1]
    return pow(pow(x2-x1, 2) + pow(y2-y1, 2), 0.5)

def look_at(target, pos):
    dx = target[0] - pos[0]
    dy = target[1] - pos[1]
    angle = math.atan2(dy, dx)
    return angle

def move_to(self, origin, target, speed):
    rotation = look_at(target, origin)
    x, y = vector_from_radians(rotation)
    self.velocity[0] += x * speed
    self.velocity[1] += y * speed

def vector_from_radians(radians):
    x = math.cos(radians)
    y = math.sin(radians)
    return [x, y]

def radians_to_degrees(angle_in_radians):
    angle_in_degrees = angle_in_radians * 180 / math.pi
    return angle_in_degrees

def display_text(text, surface, position, size, color=(255, 255, 255)):
    font = pygame.font.SysFont("Arial", size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

def open_menu(a=0):
    global arena_size
    on = True
    mouse = False
    arena = 0
    button1 = Button([585, 270], [750, 150], (0, 0, 0), 50)
    button2 = Button([585, 570], [750, 150], (0, 0, 0), 50)
    button3 = Button([585, 870], [750, 150], (0, 0, 0), 50)
    increase = True
    while on:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                on = False
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse = False

        if wave == 0:
            menu.fill((70, 83, 98))
        elif wave == 1:
            menu.fill((97, 28, 53))
        elif wave == 2:
            menu.fill((36, 16, 35))
        else:
            menu.fill((0, 0, 0))

        button1.call(mouse)
        button2.call(mouse)
        button3.call(mouse)
        if button1.hover:
            button1.color = (255, 255, 255)
        else:
            button1.color = player_colors[wave]
        button1.call(mouse)
        if button2.hover:
            button2.color = (255, 255, 255)
        else:
            button2.color = player_colors[wave]
        button1.call(mouse)
        if button3.hover:
            button3.color = (255, 255, 255)
        else:
            button3.color = player_colors[wave]
        if button1.pressed:
            buttonclick.play()
            on = False
        if button2.pressed and increase and a == 1:
            buttonclick.play()
            arena += 1
            arena_size = (arena % 4)+1
            increase = False
        if button2.pressed and a == 0:
            buttonclick.play()
            reset()
            on = False
        if not button2.pressed:
            increase = True

        if button3.pressed:
            buttonclick.play()
            quit()

        #region draw...

        button1.draw()
        button2.draw()
        button3.draw()
        display_text(f"Highest level: {int(max_round)}", menu, (ui.get_width() / 2 - 270, 100), 75)
        display_text("Start" if a==1 else "Reusme", menu, (845+30*a, 300), 75, player_colors[wave] if button1.hover else (255, 255, 255))
        display_text("Restart" if a==0 else f"arena size: {arena_size}", menu, (830-75*a, 600), 75, player_colors[wave] if button2.hover else (255, 255, 255))
        display_text("Quit", menu, (880, 900), 75, player_colors[wave] if button3.hover else (255, 255, 255))
        screen.blit(menu, (0, 0))
        pygame.display.update()
        clock.tick(20)

        #endregion

#endregion

#region classes...

class Button:
    def __init__(self, position, size, color, rounding=0):
        self.position = position
        self.size = size
        self.state = False
        self.pressed = False
        self.hover = False
        self.color = color
        self.rounding = rounding

    def call(self, mouse):
        self.pressed = False
        self.hover = False
        self.state = mouse
        if self.position[0] < pygame.mouse.get_pos()[0] < self.position[0] + self.size[0]:
            if self.position[1] < pygame.mouse.get_pos()[1] < self.position[1] + self.size[1]:
                self.hover = True
                if self.state:
                    self.pressed = True

    def draw(self):
        pygame.draw.rect(menu, self.color, (self.position[0], self.position[1], self.size[0], self.size[1]), 0, self.rounding)

class Progressbar:
    def __init__(self, lenght):
        self.position = [(screen.get_width()/2)-lenght/2, screen.get_height()-100]
        self.lenght = lenght
        self.value = 0
        self.progress = 0

    def call(self):
        self.progress = self.lenght * self.value/100

class Rigidbody:
    def __init__(self):
        self.velocity = [0, 0]
        self.friction = 1
        self.position = [0, 0]

    def call(self):
        self.velocity[0] -= self.friction * 0.01 * self.velocity[0]
        self.velocity[1] -= self.friction * 0.01 * self.velocity[1]
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

class Particle:
    def __init__(self, position, speed, rotation, size, lifetime, color):
        if color != player_colors[wave]:
            self.color = [int(color[0]*3), int(color[1]*3), int(color[2]*3)]
            for col in range(3):
                self.color[col] = min(int(color[col] * 3), 255)
        else:
            self.color = color
        self.position = [position[0]+50, position[1]+50]
        self.speed = speed
        self.size = size
        self.rotation = rotation
        self.diein = pygame.time.get_ticks() + lifetime*1000
        self.initsize = size

    def call(self):
        x, y = vector_from_radians(self.rotation)
        self.position[0] += x * self.speed
        self.position[1] += y * self.speed
        self.size = self.initsize * (self.diein - pygame.time.get_ticks()) / 200

class Enemy(Rigidbody):
    def __init__(self, position, speed, health, display, friction=0.5):
        super().__init__()
        self.friction = friction*health
        self.health = health
        self.value = health
        self.position = position
        self.display = pygame.image.load(display).convert_alpha()
        self.display = pygame.transform.scale(self.display, (int(75+health*5), int(75+health*5)))
        self.display = pygame.transform.rotate(self.display, -90)
        self.image = self.display
        self.display.set_alpha(100)
        self.speed = speed/10*health
        self.collider = False
        self.spawntime = pygame.time.get_ticks()
        self.angle = 0

    def call(self):
        super().call()
        if self.spawntime + 2000 < pygame.time.get_ticks():
            self.collider = True
            move_to(self, self.position, player.position, self.speed)
            self.display.set_alpha(255)
            self.angle = look_at([self.velocity[0] + self.position[0], self.velocity[1] + self.position[1]], self.position)
            self.display = pygame.transform.rotate(self.image, -math.degrees(self.angle))

        if self.position[0] > render.get_width()-10:
            self.velocity[0] = min(self.velocity[0], 0)
        if self.position[0] < 10:
            self.velocity[0] = max(self.velocity[0], 0)
        if self.position[1] > render.get_height()-10:
            self.velocity[1] = min(self.velocity[1], 0)
        if self.position[1] < 10:
            self.velocity[1] = max(self.velocity[1], 0)

class Projectile:
    def __init__(self, position, rotation, display, damage, spread):
        self.image = pygame.image.load(display).convert_alpha()
        self.rotation = rotation + degrees_to_radians(r.randint(-10, 10)/20*spread)
        self.spread = spread
        self.damage = damage
        self.diein = pygame.time.get_ticks() + 5 * 1000
        self.position = position
        self.display = pygame.transform.scale(self.image, (int((15 * damage/2)+30), int((25 * damage/2)+50)))
        self.display = pygame.transform.rotate(self.display, -radians_to_degrees(self.rotation)-90)
        self.speed = 10

    def reset(self, position, rotation, damage, spread):
        self.rotation = rotation + degrees_to_radians(r.randint(-10, 10)/10*spread)
        self.spread = spread
        self.damage = damage
        self.diein = pygame.time.get_ticks() + 5 * 1000
        self.position = position
        self.display = pygame.transform.scale(self.image, (int((15 * damage/2)+30), int((25 * damage/2)+50)))
        self.display = pygame.transform.rotate(self.display, -radians_to_degrees(self.rotation) - 90)
        self.speed = 10

    def update(self):
        self.display = pygame.transform.scale(self.image, (int((15 * self.damage / 2) + 30), int((25 * self.damage / 2) + 50)))
        self.display = pygame.transform.rotate(self.display, -radians_to_degrees(self.rotation) - 90)

    def recolor(self, display):
        self.image = pygame.image.load(display).convert_alpha()

    def call(self):
        x, y = vector_from_radians(self.rotation)
        self.position[0] += x * self.speed
        self.position[1] += y * self.speed

class Controller(Rigidbody):
    def __init__(self, position, display, friction=7):
        super().__init__()
        self.shield = 0
        self.dashstart = 0
        self.friction = friction
        self.position = position
        self.display = pygame.image.load(display).convert_alpha()
        self.display = pygame.transform.rotate(self.display, -90)
        self.display = pygame.transform.scale(self.display, (int(100), int(100)))
        self.image = self.display
        self.angle = 0
        self.speed = 10

    def call(self):
        super().call()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and self.position[0] < render.get_width():
            self.velocity[0] += self.speed/100
        if keys[pygame.K_a] and self.position[0] > 0:
            self.velocity[0] -= self.speed/100
        if keys[pygame.K_s] and self.position[1] < render.get_height():
            self.velocity[1] += self.speed/100
        if keys[pygame.K_w] and self.position[1] > 0:
            self.velocity[1] -= self.speed/100

        if self.position[0] > render.get_width()-10:
            self.velocity[0] = -1
        if self.position[0] < 10:
            self.velocity[0] = 1
        if self.position[1] > render.get_height()-10:
            self.velocity[1] = -1
        if self.position[1] < 10:
            self.velocity[1] = 1

        if dashing:
            target = [self.position[0] + self.velocity[0], self.position[1] + self.velocity[1]]
        else:
            target = cursor.position
        dx = target[0] - self.position[0]
        dy = target[1] - self.position[1]
        self.angle = math.atan2(dy, dx)
        self.display = pygame.transform.rotate(self.image, -math.degrees(self.angle))
        if dashing:
            self.speed = 110
        else:
            self.speed = 10

    def recolor(self, display):
        self.display = pygame.image.load(display).convert_alpha()
        self.display = pygame.transform.rotate(self.display, -90)
        self.display = pygame.transform.scale(self.display, (int(100), int(100)))
        self.image = self.display

    def get_rotation(self):
        return self.angle

    def shot(self, damage, reduction):
        red = reduction + 1
        direc = direction(self.position, cursor.position)
        self.velocity[0] = self.velocity[0] - direc[0] * max(damage/red, 0)
        self.velocity[1] = self.velocity[1] - direc[1] * max(damage/red, 0)

class Mouse:
    def __init__(self):
        self.position = [0, 0]

    def call(self):
        self.position = (pygame.mouse.get_pos()[0] - cam_pos[0], pygame.mouse.get_pos()[1] - cam_pos[1])

#endregion

#region variables...
max_round = player_data[0]
shooting = False
shot_speed = 2
bullet_damage = 1
points = 0
wave = 0
dashing = False
level = 1
sub_exp = 0
level_points = 0
dashed = False
dead = False
ui_update = 2
recoil_reduction = 0
vawe = 0
menuon = False
player_colors = {0:(237, 37, 78), 1:(255, 166, 48), 2:(71, 160, 37), 3:(215, 73, 50)}

#endregion

open_menu(1)
arena_factor = (arena_size-1)/arena_size
render = pygame.Surface((int(screen.get_size()[0]*arena_size), int(screen.get_size()[1]*arena_size)))

#region objects...
enemies = []
player = Controller([render.get_width()/2, render.get_height()/2], "sprites/player{}.png".format(wave+1))
cursor = Mouse()
bullets = []
particles = []
level_bar = Progressbar(1000)
#endregion

#region timers...

last_enemy_spawn = pygame.time.get_ticks()
last_enemy2_spawn = pygame.time.get_ticks()
last_enemy3_spawn = pygame.time.get_ticks()
last_shot = pygame.time.get_ticks()

#endregion

#region sounds...
pygame.mixer.music.load(f"music/Music{arena_size}.wav")
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)
shoot1 = pygame.mixer.Sound("sfx/shoot1.mp3")
shoot2 = pygame.mixer.Sound("sfx/shoot2.mp3")
shoot3 = pygame.mixer.Sound("sfx/shoot3.mp3")
hit = pygame.mixer.Sound("sfx/impactMining_000.ogg")
hit.set_volume(0.7)
destroy = pygame.mixer.Sound("sfx/impactMetal_003.ogg")
destroy.set_volume(0.7)
shield = pygame.mixer.Sound("sfx/forceField_003.ogg")
shield.set_volume(0.2)
bdamage = pygame.mixer.Sound("sfx/phaserUp5.mp3")
bdamage.set_volume(0.7)
frate = pygame.mixer.Sound("sfx/phaseJump3.mp3")
frate.set_volume(0.7)
recoilrez = pygame.mixer.Sound("sfx/lowDown.mp3")
shieldown = pygame.mixer.Sound("sfx/pepSound4.ogg")
shieldown.set_volume(0.2)
deaths = pygame.mixer.Sound("sfx/explosionCrunch_003.ogg")
deaths.set_volume(0.2)

shoot_channel1 = pygame.mixer.Channel(0)
shoot_channel2 = pygame.mixer.Channel(6)
shoot_channel3 = pygame.mixer.Channel(7)
hit_channel = pygame.mixer.Channel(1)
destroy_channel = pygame.mixer.Channel(2)
upgrade_channel = pygame.mixer.Channel(3)
phit_channel = pygame.mixer.Channel(4)
ui_channel = pygame.mixer.Channel(5)

#endregion

#gameloop
while True:

    if menuon:
        open_menu()
        menuon = False

    #region live variables...
    if int(max_round) < level:
        max_round = level
        player_data_.seek(0, 0)
        player_data_.write(str(level))
    enemy_health_multiplier = vawe + 1
    cam_pos = [int(-player.position[0]*arena_factor), int(-player.position[1]*arena_factor)]
    exp_needed = int(level * 2.5 * arena_size)
    exp = points - sub_exp
    level_bar.value = exp / exp_needed*100
    if exp >= exp_needed:
        sub_exp += exp_needed
        level += 1
        level_points += 1
        ui_update = 2

    #endregion

    #region enemy spawn...
    maxspeed = 0.75
    enemy_speed = 0.01 + pygame.time.get_ticks() * 0.00001
    if enemy_speed > maxspeed:
        enemy_speed = maxspeed

    if pygame.time.get_ticks() - last_enemy_spawn > 2000/(0.0001+pygame.time.get_ticks()*0.0001)+3000/arena_size:
        enemies.append(Enemy([r.randint(0, render.get_width()), r.randint(0, render.get_height())], enemy_speed, 1*enemy_health_multiplier,  "sprites/enemy{}.png".format(wave*3+1)))
        last_enemy_spawn = pygame.time.get_ticks()

    if level >= 5 and pygame.time.get_ticks() - last_enemy2_spawn > 8000/arena_size:
        enemies.append(Enemy([r.randint(0, 1920), r.randint(0, 1080)], enemy_speed/3, 5*enemy_health_multiplier, "sprites/enemy{}.png".format(wave*3+2)))
        last_enemy2_spawn = pygame.time.get_ticks()

    if level >= 10 and pygame.time.get_ticks() - last_enemy3_spawn > 25000/arena_size:
        enemies.append(Enemy([r.randint(0, 1920), r.randint(0, 1080)], enemy_speed/5, 15*enemy_health_multiplier, "sprites/enemy{}.png".format(wave*3+3)))
        last_enemy3_spawn = pygame.time.get_ticks()

    if level - 5*vawe >= 15:
        vawe += 1
        wave = vawe % 4
        player.recolor("sprites/player{}.png".format(wave + 1))
        for bullet in bullets:
            bullet.recolor("sprites/bullet{}.png".format(wave + 1))

    #endregion

    #region enemy destroy...
    for bullet in bullets:
        for enemy in list(enemies):
            if distance(enemy.position, bullet.position) < enemy.display.get_width()/2 and enemy.collider:
                if enemy.health > bullet.damage:
                    hit_channel.play(hit)
                    enemy.health -= bullet.damage
                    enemy.velocity[0] -= direction(enemy.position, bullet.position)[0]*bullet.damage
                    enemy.velocity[1] -= direction(enemy.position, bullet.position)[1]*bullet.damage
                    if bullet in bullets:
                        for i in range(10):
                            particles.append(Particle((enemy.position.copy()[0] - 50, enemy.position.copy()[1] - 50), r.randint(5, 10), look_at(enemy.position, player.position) + r.randint(-7, 7) / 10, r.randint(10, 25), r.randint(10, 20) / 100, pygame.transform.average_color(enemy.display)))
                        bullets.remove(bullet)

                else:
                    for i in range(20):
                        particles.append(Particle((enemy.position.copy()[0] - 50, enemy.position.copy()[1] - 50), r.randint(5, 10), look_at(enemy.position, player.position)+r.randint(-7, 7)/10, r.randint(10, 25), r.randint(30, 50)/100, pygame.transform.average_color(enemy.display)))
                    if enemy in enemies:
                        destroy_channel.play(destroy)
                        points += 1 * enemy.value
                        bullet.damage -= enemy.health
                        enemies.remove(enemy)
                        ui_update = 2
                        if bullet.damage <= 0:
                            bullets.remove(bullet)
                        bullet.update()

    #endregion

    #region player death...

    for enemy in enemies:
        if enemy.collider and distance(enemy.position, player.position) < enemy.display.get_width()/2-5:
            if player.shield <= 0:
                phit_channel.play(deaths)
                dead = True
            else:
                enemies.remove(enemy)
                phit_channel.play(shieldown)
                player.shield -= 1
                ui_update = 2
    if dead:
        reset()

    #endregion

    #region class function call...

    level_bar.call()

    for enemy in enemies:
        enemy.call()

    for particle in particles:
        particle.call()
        if particle.diein < pygame.time.get_ticks():
            particles.remove(particle)

    for bullet in bullets:
        bullet.call()

    for bullet in bullets:
        bullet.call()

    player.call()

    cursor.call()
    #endregion

    #region collision...
    for enemy in enemies:
        for i in enemies:
            if enemy is not i and distance(enemy.position, i.position) < enemy.display.get_width()/2 + i.display.get_width()/2 and enemy.collider and i.collider:
                enemy.velocity[0] -= direction(enemy.position, i.position)[0]
                enemy.velocity[1] -= direction(enemy.position, i.position)[1]

    #endregion

    #region events...
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            menuon = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            shooting = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            shooting = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                dashing = True
                dashed = True
                ui_update = 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                dashing = False
        if event.type == pygame.KEYDOWN and level_points > 0:
            if event.key == pygame.K_z:
                upgrade_channel.play(frate)
                level_points -= 1
                shot_speed += 0.5
                ui_update = 2
            if event.key == pygame.K_x:
                upgrade_channel.play(bdamage)
                level_points -= 1
                bullet_damage += 1
                ui_update = 2
            if event.key == pygame.K_c:
                upgrade_channel.play(recoilrez)
                level_points -= 1
                recoil_reduction += 1
                ui_update = 2
            if event.key == pygame.K_SPACE:
                upgrade_channel.play(shield)
                level_points -= 1
                player.shield += 1
                ui_update = 2
            if event.key == pygame.K_p:
                points += exp_needed
                ui_update = 2

    if dashing:
        particles.append(Particle((player.position.copy()[0] - 50 + r.randint(-15,15), player.position.copy()[1] - 50+ r.randint(-15,15)), r.randint(-5,5)/10, r.randint(-5,5)/10, r.randint(3,6)/3, r.randint(1,3)/3, player_colors[wave]))

    if shooting and pygame.time.get_ticks() - last_shot > 1000 / shot_speed and not dashing:
        bullet_updated = False
        match = r.randint(1,3)
        if match == 1:
            shoot_channel1.play(shoot1)
        elif match == 2:
            shoot_channel2.play(shoot2)
        elif match == 3:
            shoot_channel3.play(shoot3)
        for bullet in bullets:
            if bullet.diein < pygame.time.get_ticks():
                bullet.reset(player.position.copy(), player.get_rotation(), bullet_damage, shot_speed)
                bullet_updated = True
                player.shot(bullet_damage, recoil_reduction)
                break
        if not bullet_updated:
            bullets.append(Projectile(player.position.copy(), player.get_rotation(), "sprites/bullet{}.png".format(wave+1), bullet_damage, shot_speed))
            player.shot(bullet_damage, recoil_reduction)
        last_shot = pygame.time.get_ticks()

    #endregion

    #region camera...

    if wave == 0:
        render.fill((70, 83, 98))
    elif wave == 1:
        render.fill((97, 28, 53))
    elif wave == 2:
        render.fill((36, 16, 35))
    else:
        render.fill((0, 0, 0))

    if player.shield > 0:
        pygame.draw.circle(render, (player_colors[wave][0], player_colors[wave][1], player_colors[wave][2], 1), player.position, 75+5*player.shield, 5*player.shield)
    render.blit(player.display, (player.position[0] - int(player.display.get_width() / 2), player.position[1] - int(player.display.get_height() / 2)))
    for enemy in enemies:
        render.blit(enemy.display, (enemy.position[0] - int(enemy.display.get_width() / 2), enemy.position[1] - int(enemy.display.get_height() / 2)))
    for bullet in bullets:
        render.blit(bullet.display, (bullet.position[0] - int(bullet.display.get_width() / 2), bullet.position[1] - int(bullet.display.get_height() / 2)))
    for particle in particles:
        pygame.draw.rect(render, particle.color, (particle.position[0], particle.position[1], particle.size, particle.size))
    screen.blit(render, cam_pos)
    #region ui...
    if ui_update > 0:
        ui.fill((0, 0, 0, 0))
        ui_update -= 1
        if not dashed:
            display_text("hold shift to dash", ui, (ui.get_width() / 2 - 200, 300), 50)
        if level_points == 1:
            display_text("1 upgrade avaliable!", ui, (ui.get_width() / 2 - 250, 100), 50)
        elif level_points > 1:
            display_text(f"{level_points} upgrades avaliable!!", ui, (ui.get_width() / 2 - 250, 100), 50)
            display_text("press Z to increase fire rate", ui, (ui.get_width() / 2 - 190, 170), 30)
            display_text("press X to increase damage", ui, (ui.get_width() / 2 - 190, 220), 30)
            display_text("press C to lower gun recoil", ui, (ui.get_width() / 2 - 190, 270), 30)
            display_text("press SPACE to add a shield layer", ui, (ui.get_width() / 2 - 190, 320), 30)
        pygame.draw.rect(ui, (50, 50, 50, 100), (level_bar.position[0], level_bar.position[1], level_bar.lenght, 30), 5, 15)
        pygame.draw.rect(ui, player_colors[wave], (level_bar.position[0] + 5, level_bar.position[1] + 5, level_bar.progress, 20), 0, 10)
        display_text(f"{level}", ui, (ui.get_width() / 2, ui.get_height() - 200), 50)
    screen.blit(ui, (0, 0))
    #endregion
    pygame.display.update()
    clock.tick(60)

    #endregion
