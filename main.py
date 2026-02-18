import pygame, sys, random, asyncio, json
from scripts.text import *
from scripts.background import *
from scripts.bird import *
from scripts.pipe import *

import ctypes

try:
    ctypes.windll.user32.SetProcessDPIAware() 
except:
    pass

with open("data/json/difficulty.json", "r") as file:
    DIFFICULTY_SETTINGS = json.load(file)

def relative_scale(image, scaling):
    size_x, size_y = image.get_rect().w, image.get_rect().h
    return pygame.transform.scale(image, (size_x*scaling[0], size_y*scaling[1]))

class Game:
    def __init__(self, size):
        #Basic pygame initialisation
        pygame.init()
        pygame.mixer.init(channels=50)
        self.difficulty = "normal"
        self.screen = pygame.display.set_mode(size, pygame.SCALED, vsync=True)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Flappy Bird Ultimate")
        pygame.display.set_icon(
            pygame.image.load("yellowbird-upflap.png"),
        )
        self.properties()
        self.load_assets() 
        pygame.mixer.set_num_channels(1000)

    def properties(self):
        #We initialize all game properties
        self.pipes = [] 
        self.score = 0
        self.difficulty_settings = DIFFICULTY_SETTINGS[self.difficulty]
        self.game_speed = self.difficulty_settings["game_speed"]
        self.end = False
        self.begin = False
        self.mouse_pressed = False
        self.start_timer = 0
        self.background_timer = 0
        self.score_count = 4
        self.bird = Bird(self)
        self.first = True
        self.font = pygame.font.Font("FlappyBirdy.ttf", 100)

    def load_assets(self):
        #We load all the numbers to display the score
        self.numbers = [relative_scale(pygame.image.load("data/sprites/"+str(i)+".png"), (1.25, 1.25)).convert_alpha() for i in range(10)]

        #We load all other assets
        self.assets = {
            "background" : pygame.transform.scale(pygame.image.load("data/sprites/background-day.png"), (450, 720)).convert_alpha(),
            "ground" : pygame.transform.scale(pygame.image.load("data/sprites/base.png"), (450, 100)).convert_alpha(),
            "bird" : [
                pygame.transform.scale(
                    pygame.image.load(f"data/sprites/bluebird-{frame}flap.png"),
                    (51, 36)
                ).convert_alpha() for frame in ["down", "mid", "up"]
            ],

        } | {
            "pipe" : pygame.transform.scale(pygame.image.load("data/sprites/pipe-green.png"), (70, 800)),
            "wing" : pygame.mixer.Sound("data/audio/wing.ogg"),
            "point" : pygame.mixer.Sound("data/audio/point.ogg"),
            "hit" : pygame.mixer.Sound("data/audio/hit.ogg"),
            "swoosh" : pygame.mixer.Sound("data/audio/swoosh.ogg"),
            "die" : pygame.mixer.Sound("data/audio/die.ogg"),
            "menu" : pygame.mixer.Sound("data/audio/menu.wav"),   
        }


    def play(self, channel, sound):
        pygame.mixer.Channel(channel).play(self.assets[sound])

    def timers_logic(self):
        #We update every timers of the game
        if self.background_timer < -450:
            self.background_timer = 0
        if self.start_timer > 0:
            self.start_timer -= (1/60)
    
    def update_objects(self):
        for pipe in self.pipes: 
            pipe.update() 
        self.bird.update() 
        render_number(self, 
            self.score, 
            (450//2 - number_lenght(self.score), 10)
        )
        self.pipes = [pipe for pipe in self.pipes if not pipe.kill]
    
    def handle_game_speed(self):
        if self.end:
            self.game_speed *= 0.98
        else:
            self.game_speed = self.difficulty_settings["game_speed"]
                
    def select_difficulty(self):
        if not self.begin:
            image = self.font.render(self.difficulty, True, (0, 0, 0))
            rect = image.get_rect()
            rect.topleft = (130, 725)
            if rect.collidepoint(pygame.mouse.get_pos()):
                if self.mouse_pressed:
                    self.difficulty = {"easy" : "normal", "normal" : "hard", "hard" : "extreme", "extreme" : "unreal", "unreal" : "galactic", "galactic" : "easy"}[self.difficulty]
                    self.mouse_pressed = False
                    self.play(6, "menu")
                image = self.font.render(self.difficulty, True, (0, 0, 0), (180, 255, 255))
                pygame.mouse.set_cursor(pygame.cursors.broken_x)
            else:
                pygame.mouse.set_cursor(pygame.cursors.arrow)
    
            if self.start_timer < 0.5:
                image.set_alpha((255 - self.start_timer*255)*2)
            else:
                image.set_alpha(self.start_timer*255*2)
            self.screen.blit(image, rect.topleft)
    
    def handle_state_transition(self):
        if self.start_timer > 0:
            srf = pygame.Surface((450, 800))
            srf.fill((0, 0, 0))
            if self.start_timer > 0.5:
                srf.set_alpha((255 - self.start_timer*255)*2)
            else:
                srf.set_alpha(self.start_timer*255*2)
                if self.first:
                    self.properties()
                    self.start_timer = 0.5
                    self.first = False
            self.screen.blit(srf, (0, 0))
        else:
            self.start_timer = 0
    
    def handle_mouse_press(self):
        if self.mouse_pressed:
            self.on_press()
    
    def spawn_first_pipe(self):
        if self.pipes == []:
            self.pipes.append(Pipe(self, random.randint(70, 400), 1000, self.difficulty_settings["gap"]))

    def game_loop(self):
        self.difficulty_settings = DIFFICULTY_SETTINGS[self.difficulty]
        render_background(self)   # premier rendu
        self.timers_logic()
        self.update_objects()
        self.handle_game_speed()
        self.select_difficulty()
        self.handle_state_transition()
        self.handle_mouse_press()
    
    def on_press(self):
        self.begin = True
        if not self.end:
            self.bird.jump()
            self.play(0, "wing")
            self.spawn_first_pipe()
        if self.end and self.bird.pos[1] > 600 and self.start_timer == 0:
            self.play(4, "swoosh")
            self.start_timer = 1
            self.first = True
            self.easter_egg = " "

    async def run(self):
        #Basic pygame loop
        while True:
            self.keys = pygame.key.get_pressed()  
            self.mouse_pressed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self.keydown(event):
                        break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_pressed = True

            self.game_loop()

            pygame.display.flip()
            self.clock.tick(60)
            await asyncio.sleep(0)

    def keydown(self, event):
        if event.key == pygame.K_F11:
            pygame.display.toggle_fullscreen()
        else:
            self.on_press()
            return True
        return False

game = Game((450, 800))
asyncio.run(game.run())