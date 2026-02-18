import math, pygame

rotation_function = lambda x : max((42+2*x)/2 if x > -15 else -abs(x)**1.2, -80)

class Bird:
    def __init__(self, game):
        self.game = game
        self.play = False
        self.pos = [110, 720//2]
        self.speed = 0
        self.animation_timer = 0
        self.spining_timer = 0

    def update(self):
        self.spining_timer -= self.game.game_speed*3
        self.render()
        self.animation_logic()
        self.pos[1] -= self.speed
        if self.speed > -20:
            if self.game.begin:
                self.speed -= self.game.difficulty_settings["gravity"]
        self.do_touch_ground()
        self.do_touch_sky()
    
    def do_touch_ground(self):
        if self.pos[1] > 680:
            if self.game.end == False:
                pygame.mixer.Channel(2).play(self.game.assets["hit"])
            self.game.end = True
            self.pos[1] = 680
            self.speed = 0
    
    def do_touch_sky(self):
        if self.pos[1] <= 0 and self.game.end == False:
            pygame.mixer.Channel(5).play(self.game.assets["die"])
            pygame.mixer.Channel(2).play(self.game.assets["hit"])
            self.game.end = True

    def animation_logic(self):
        self.animation_timer += 1/7
        if self.animation_timer > 2.9:
            self.animation_timer = 0

    def jump(self):
        self.speed = self.game.difficulty_settings["jump"]

    def get_rect(self):
        return pygame.Rect(self.pos[0]-17, self.pos[1]-13, 40, 27)

    def render(self):
        rotation = self.spining_timer if self.game.end else (rotation_function(self.speed) if self.game.begin else 0)
        image = pygame.transform.rotate(self.game.assets["bird"][math.floor(self.animation_timer) if not self.game.end else 1], rotation)
        self.game.screen.blit(image, (self.pos[0] - image.get_width()/2, self.pos[1] - image.get_height()/2 + (8*math.sin(self.spining_timer/120) if not self.game.begin else 0)))

