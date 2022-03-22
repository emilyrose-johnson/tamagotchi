import pygame
import pygame_menu
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'
selected = 45
current_img = None


def main():
    pygame.init()
    menu()

class Pet:
    def __init__(self, tamaName, tamaAge, tamaHunger, tamaSleep, tamaBrush, tamaPlay):
        self.name = tamaName
        self.age = tamaAge
        self.hunger = tamaHunger
        self.sleep = tamaSleep
        self.brush = tamaBrush
        self.play = tamaPlay


def run_game(tamaData):
    # flag to see if player exited
    crashed = False

    # create tama instance
    tama = Pet(tamaData[0], int(tamaData[1]), int(tamaData[2]), int(tamaData[3]), int(tamaData[4]), int(tamaData[5]))

    # setup for pet frame alternation every second
    current_img = tama_pet_small
    ALT = pygame.USEREVENT + 1
    pygame.time.set_timer(ALT, 1250)

    # while game not exited
    while not crashed:
        for event in pygame.event.get():
            # exit if x pressed
            if event.type == pygame.QUIT:
                crashed = True
            # alternate image, alpha sets transparency
            if event.type == ALT:
                carrot_small.set_alpha(0)
                current_img.set_alpha(0)
                if current_img == tama_pet_small:
                    current_img = tama_pet1_small
                    current_img.set_alpha(255)
                else:
                    current_img = tama_pet_small
                    current_img.set_alpha(255)
            # handles if button is clicked
            if event.type == pygame.MOUSEBUTTONUP:
                if 165 <= event.pos[0] <= 235 and 500 <= event.pos[1] <= 570:
                    shift_select('left')
                elif 365 <= event.pos[0] <= 435 and 500 <= event.pos[1] <= 570:
                    if selected == 45:
                        tama.hunger = 100
                        carrot_small.set_alpha(255)
                        current_img = tama_pet_eat_small
                        current_img.set_alpha(255)
                    elif selected == 245:
                        tama.sleep = 100
                        current_img = tama_pet_sleep_small
                        current_img.set_alpha(255)
                    elif selected == 445:
                        tama.brush = 100
                        current_img = tama_pet_brush_small
                        current_img.set_alpha(255)
                    else:
                        tama.play = 100
                        current_img = tama_pet_play_small
                        current_img.set_alpha(255)
                elif 565 <= event.pos[0] <= 635 and 500 <= event.pos[1] <= 570:
                    shift_select('right')
        # display background and pet
        display.fill(sky_blue)
        pet(current_img, display_width * .27, display_height * .27)

        eat(eat_small, 45, 60)
        sleep(sleep_small, 260, 60)
        brush(brush_small, 460, 60)
        ball(ball_small, 660, 60)
        select(select_small, selected, 33)
        display_carrot(carrot_small, 325, 365)

        # button display, top is white circle, bottom is black outline
        # params are display, color, position, radius, width for black outline
        button(200, 530, 35, grey, white, action="left")
        button(400, 530, 35, grey, white, action="middle")
        button(600, 530, 35, grey, white, action="right")

        # Health bar display
        health_bars(tama.hunger, tama.sleep, tama.brush, tama.play)

        # updates the hunger bar to decrease by 5% every second
        tama.hunger -= .05
        tama.sleep -= .05
        tama.play -= .05
        tama.brush -= .05


        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(tama.name, True, white, sky_blue)
        textRect = text.get_rect()
        textRect.center = (100, 20)
        display.blit(text, textRect)

        # update display, set fps to 60
        pygame.display.update()
        clock.tick(60)

    # exit code
    pygame.quit()
    quit()

# displays tamagotchi pet image. params are image and position
def pet(p, x, y):
    display.blit(p, (x, y))

# displays care functions, params are image and position
def eat(p, x, y):
    display.blit(p, (x, y))

def sleep(p, x, y):
    display.blit(p, (x, y))

def brush(p, x, y):
    display.blit(p, (x, y))

def ball(p, x, y):
    display.blit(p, (x, y))

def select(p, x, y):
    return display.blit(p, (x, y))

def display_carrot(p, x, y):
    return display.blit(p, (x,y))

# Displays buttons
def button(x, y, r, ic, ac, action = None):
    mouse = pygame.mouse.get_pos()

    # Displays and changes color of button when hovered over
    if x-r < mouse[0] < x+r and y-r < mouse[1] < y+r:
        pygame.draw.circle(display, ac, (x, y), r)
        pygame.draw.circle(display, black, (x, y), r, width=5)
    else:
        pygame.draw.circle(display, ic, (x, y), r)
        pygame.draw.circle(display, black, (x, y), r, width=5)

# Displays health bars
def health_bars(h, s, b, p):
    total = (h + s + b + p) / 2
    pygame.draw.rect(display, black, (300, 20, total, 20))
    pygame.draw.rect(display, black, (50, 140, h, 10))
    pygame.draw.rect(display, black, (250, 140, s, 10))
    pygame.draw.rect(display, black, (450, 140, b, 10))
    pygame.draw.rect(display, black, (650, 140, p, 10))


#def select_care_func(tama):
#    if selected == 45:
#        tama.hunger = 100
#        carrot_small.set_alpha(255)
#    elif selected == 245:
#        tama.sleep = 100
#    elif selected == 445:
#        tama.brush = 100
#        print('brush')
#    else:
#        tama.play = 100
#        print("play")


def shift_select(direc):
    global selected
    if direc == 'left' and selected == 45:
        selected = 645
    elif direc == 'right' and selected == 645:
        selected = 45
    elif direc == 'left':
        selected -= 200
    else:
        selected += 200

def menu():
# Supporting main menu functions
    # do if new game button is pressed (run game with default data values)
    def new_game():
        pygame_menu.events.EXIT
        run_game([textinp.get_value(), 0, 100, 100, 100, 100])

    # read data from save 1 and run game with those data values
    def initializeSave1():
        path = "./game_saves/"
        fileName = path + os.listdir("./game_saves")[0]
        save = open(fileName, 'r', encoding='utf8')
        run_game(save.readline().split())

    # read data from save 2 and run game with those data values
    def initializeSave2():
        path = "./game_saves/"
        fileName = path + os.listdir("./game_saves")[1]
        save = open(fileName, 'r', encoding='utf8')
        run_game(save.readline().split())

    # read data from save 3 and run game with those data values
    def initializeSave3():
        path = "./game_saves/"
        fileName = path + os.listdir("./game_saves")[2]
        save = open(fileName, 'r', encoding='utf8')
        run_game(save.readline().split())

    # do if load game button is pressed
    def load_game():
        # get rid of main menu
        pygame_menu.events.EXIT
        # set up new level select menu
        level_select = pygame_menu.Menu('Open Saved Game', display_width, display_height, theme=pygame_menu.themes.THEME_SOLARIZED)

        # determine number of saves in the file, make the corresponding number of
        # buttons and assign corresponding initialize fxn to each bttn
        saves = os.listdir("./game_saves")
        if(len(saves) == 0):
            level_select.add.label("No saves")
        if(len(saves) >= 1):
            level_select.add.button(saves[0], initializeSave1)
        if (len(saves) >= 2):
            level_select.add.button(saves[1], initializeSave2)
        if (len(saves) >= 3):
            level_select.add.button(saves[2], initializeSave3)

        # add back button
        level_select.add.vertical_margin(20)
        level_select.add.button('Back', menu)
        level_select.mainloop(display)

    # SET UP MAIN MENU
    pygame_menu.events.EXIT
    menu = pygame_menu.Menu('Main Menu', display_width, display_height, theme=pygame_menu.themes.THEME_SOLARIZED)

    menu.add.image('./ascii_logo_noBackground.png')
    menu.add.vertical_margin(20)
    textinp = menu.add.text_input('Pet Name:  ')
    menu.add.button('Start New Game', new_game)
    menu.add.button('Load Game', load_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(display)


if __name__ == '__main__':
    sky_blue = (173, 216, 230)
    white = (255, 255, 255)
    black = (0, 0, 0)
    grey = (240, 240, 240)
    # window setup
    display_width = 800
    display_height = 600
    display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Tamagotchi")
    # running timer since startup. may be useful for saves
    clock = pygame.time.Clock()

    # loading tamagotchi images and resize
    tama_pet = pygame.image.load('tamarabbit.png')
    tama_pet_small = pygame.transform.scale(tama_pet, (350, 350))
    tama_pet1 = pygame.image.load('tamarabbit1.png')
    tama_pet1_small = pygame.transform.scale(tama_pet1, (350, 350))
    tama_pet_eat = pygame.image.load('tamarabbiteat.png')
    tama_pet_eat_small = pygame.transform.scale(tama_pet_eat, (350, 350))
    tama_pet_sleep = pygame.image.load('tamarabbitsleep.png')
    tama_pet_sleep_small = pygame.transform.scale(tama_pet_sleep, (350, 350))
    tama_pet_brush = pygame.image.load('tamarabbitbrush.png')
    tama_pet_brush_small = pygame.transform.scale(tama_pet_brush, (350, 350))
    tama_pet_play = pygame.image.load('tamarabbitplay.png')
    tama_pet_play_small = pygame.transform.scale(tama_pet_play, (350, 350))

    # load care images and resize
    eat_pic = pygame.image.load('eat.png')
    eat_small = pygame.transform.scale(eat_pic, (110, 70))

    sleep_pic = pygame.image.load('sleep.png')
    sleep_small = pygame.transform.scale(sleep_pic, (80, 70))

    brush_pic = pygame.image.load('brush.png')
    brush_small = pygame.transform.scale(brush_pic, (80, 70))

    ball_pic = pygame.image.load('ball.png')
    ball_small = pygame.transform.scale(ball_pic, (80, 75))

    select_tr = pygame.image.load('select_tr.png')
    select_small = pygame.transform.scale(select_tr, (110, 110))

    carrot_pic = pygame.image.load('carrot.png')
    carrot_small = pygame.transform.scale(carrot_pic, (110, 110))
    carrot_small.set_alpha(0)

    main()
