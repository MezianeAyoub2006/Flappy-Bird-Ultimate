"""
We handle everything related to text on this file
In FlappyBird it's mainly score label rendering.
"""

def render_digit(game, digit, position):
    #Just a simple digit rendering function to abstract a little bit the code
    game.screen.blit(game.numbers[int(digit)], position)

def render_number(game, number, position):    
    offset = 0
    for digit in str(number):        
        #We render each digit one by one to render the full number
        render_digit(game, digit, (position[0]+offset, position[1]))
        #The "1" caracter has a different width than the others so we must offset based on that
        offset += 17*1.25 if digit == "1" else 25*1.25
  
def number_lenght(number):
    #This function is used to compute the number width in term of pixels on the screen
    number_string = str(number)
    one_count = number_string.count("1")
    return one_count*17*1.25 + (len(number_string) - one_count)*25*1.25
