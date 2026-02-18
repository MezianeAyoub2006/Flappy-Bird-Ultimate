"""
We handle everything related to the background here.
"""

def render_background(game):
    game.screen.blit(game.assets["background"], (0, 0))
    """
    We take care of the timer to render the ground. 
    It's displayed two times so it can move while being fully rendered
    """
    game.screen.blit(game.assets["ground"], (game.background_timer, 700))
    game.screen.blit(game.assets["ground"], (game.background_timer+450, 700))
    game.background_timer -= game.game_speed