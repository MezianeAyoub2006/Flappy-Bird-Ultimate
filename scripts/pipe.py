import pygame, random

def get_pipe_image(game, lenght):
    return game.assets["pipe"].subsurface(pygame.Rect(0, 0, 70, lenght))

class Pipe:
    def __init__(self, game, height, position, spacing=30):
        self.game = game
        self.spacing = spacing
        self.height = height
        self.position = position
        self.kill = False
        self.pipe_created = False
        self.end_score = False
    
    def get_rect(self):
        return [
            pygame.Rect(self.position, 0, 70, self.height), 
            pygame.Rect(self.position, self.height+self.spacing, 70, 700-self.height-self.spacing)
        ]
        
        

    def render(self):
        rect_0, rect_1 = self.get_rect()
        self.game.screen.blit(
            pygame.transform.flip(
                get_pipe_image(self.game, rect_0.height), 0, 1
            ), rect_0.topleft
        )
        self.game.screen.blit(
            get_pipe_image(self.game, rect_1.height), 
            rect_1.topleft
        )
    
    def update(self):
        self.position -= self.game.game_speed
        self.render()
        if self.position <= -100:
            self.on_death()
        self.handle_bird_collision()
        self.handle_pipes_creation()
        self.handle_score_increment()
          
    def handle_score_increment(self):
        if self.position >= self.game.bird.pos[0] + 35 and not self.end_score:
            if self.game.score_count > 0:
                self.game.score_count -= 1
            if self.game.score_count == 0 and not self.game.end:
                self.game.score += 1
                pygame.mixer.Channel(random.randint(99, 500)).play(self.game.assets["point"])
            self.end_score = True
    
    def handle_pipes_creation(self):
        if self.position <= 700 and not self.pipe_created:
            self.game.pipes.append(Pipe(self.game, random.randint(70, 400), 1000, self.game.difficulty_settings["gap"]))
            self.pipe_created = True
    
    def handle_bird_collision(self):
        for rect in self.get_rect():
            if rect.colliderect(self.game.bird.get_rect()) and self.game.end == False:
                pygame.mixer.Channel(2).play(self.game.assets["hit"])
                pygame.mixer.Channel(5).play(self.game.assets["die"])
                self.game.end = True
                self.game.bird.speed = 7

    def on_death(self):
        self.kill = True
        
        
