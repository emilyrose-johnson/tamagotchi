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

    def toString(self):
        return str(self.name) + " " + str(int(self.age)) + " " + str(int(self.hunger)) + " " + str(int(self.sleep)) + " " + str(int(self.brush)) + " " + str(int(self.play))


def run_game(tamaData):
    # flag to see if player exited
    crashed = False

    # create tama instance
    tama = Pet(tamaData[0], int(tamaData[1]), int(tamaData[2]), int(tamaData[3]), int(tamaData[4]), int(tamaData[5]))

    # setup for pet frame alternation every second
    current_img = tama_pet_small
    ALTERNATEimg = pygame.USEREVENT + 1
    INCREASEage = pygame.USEREVENT +2
    pygame.time.set_timer(ALTERNATEimg, 1250)
    pygame.time.set_timer(INCREASEage, 10000)

    # while game not exited
    while not crashed:
        # event handler
        for event in pygame.event.get():
            # exit if x pressed
            if event.type == pygame.QUIT:
                crashed = True
            # alternate image, alpha sets transparency
            if event.type == ALTERNATEimg:
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
                # move select left
                if 165 <= event.pos[0] <= 235 and 500 <= event.pos[1] <= 570:
                    shift_select('left')
                # do action of selected function
                elif 365 <= event.pos[0] <= 435 and 500 <= event.pos[1] <= 570:
                    # reset alternate img timer to 0 to display care action for correct time.
                    pygame.time.set_timer(ALTERNATEimg, 1250)
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
                # move select right
                elif 565 <= event.pos[0] <= 635 and 500 <= event.pos[1] <= 570:
                    shift_select('right')
                # Menu Button
                elif 0 <= event.pos[0] <= 124 and 0 <= event.pos[1] <= 29:
                    inGameMenufn(tama)
            if event.type == INCREASEage:
                tama.age += 1

        # display background and pet
        display.fill(sky_blue)
        pet(current_img, display_width * .27, display_height * .27)

        #display care function icons
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

        # draw menu border
        pygame.draw.rect(display, black, (0, 0, 124, 29))
        # draw menu button
        pygame.draw.rect(display, dark_grey, (2, 2, 120, 25))
        # display words "menu"
        font_menu = pygame.font.Font('PressStart2.ttf', 20)
        text_menu = font_menu.render("MENU", True, black, dark_grey)
        textRect_menu = text_menu.get_rect()
        textRect_menu.center = (62, 16)
        display.blit(text_menu, textRect_menu)

        # display tama name
        font_name = pygame.font.Font('PixeloidSans.ttf', 25)
        text_name = font_name.render(tama.name, True, black, sky_blue)
        textRect_name = text_name.get_rect()
        textRect_name.center = (display_width - text_name.get_width()/2 - 10, text_name.get_height()/2 + 5)
        display.blit(text_name, textRect_name)

        # Health bar display
        health_bars(tama.hunger, tama.sleep, tama.brush, tama.play)

        # updates the hunger bar to decrease by 5% every second
        if tama.hunger > 0:
            tama.hunger -= .05
        if tama.sleep > 0:
            tama.sleep -= .05
        if tama.play > 0:
            tama.play -= .05
        if tama.brush > 0:
            tama.brush -= .05


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

def inGameMenufn(tama):

    def optionsMenufn():
        pygame_menu.events.EXIT
        optionsMenu = pygame_menu.Menu('options', display_width, display_height, theme=pygame_menu.themes.THEME_SOLARIZED)

        optionsMenu.add.label("Options")
        optionsMenu.add.vertical_margin(20)
        optionsMenu.add.button('Back', inGameMenu)

        optionsMenu.mainloop(display)

    def helpMenufn():
        pygame_menu.events.EXIT
        helpMenu = pygame_menu.Menu('Help', display_width, display_height, theme=pygame_menu.themes.THEME_SOLARIZED)

        helpMenu.add.label("Instructions Here")
        helpMenu.add.vertical_margin(20)
        helpMenu.add.button('Back', inGameMenu)

        helpMenu.mainloop(display)

    def saveMenufn():

        def save():
            slot = slotInp.get_value()[0]
            name = textInp.get_value()

            path = "./game_saves/"
            saves = os.listdir("./game_saves")

            if slot == '1':
                if len(saves) >= 1 and os.path.isfile(path + saves[0]):
                    os.remove(path + saves[0])
                filename = "SS1." + name + '.txt'
                with open(os.path.join(path, filename), 'w') as temp_file:
                    temp_file.write(tama.toString())

            if slot == '2':
                if len(saves) >= 2 and os.path.isfile(path + saves[1]):
                    os.remove(path + saves[1])
                filename = "SS2." + name + '.txt'
                with open(os.path.join(path, filename), 'w') as temp_file:
                    temp_file.write(tama.toString())

            if slot == '3':
                if len(saves) >= 3 and os.path.isfile(path + saves[2]):
                    os.remove(path + saves[2])
                filename = "SS3." + name + '.txt'
                with open(os.path.join(path, filename), 'w') as temp_file:
                    temp_file.write(tama.toString())

            inGameMenufn(tama)

        pygame_menu.events.EXIT
        saveMenu = pygame_menu.Menu('Save', display_width, display_height, theme=pygame_menu.themes.THEME_SOLARIZED)

        saveMenu.add.label("Current Saves")
        if not os.path.exists("./game_saves"):
            os.makedirs("./game_saves")
        saves = os.listdir("./game_saves")
        for i, e in enumerate(saves):
            saveMenu.add.label("Slot " + str(i+1) + ": " + e.split('.')[1])

        if len(saves) == 0:
            saveMenu.add.label("No Saves")

        saveMenu.add.vertical_margin(40)
        slotInp = saveMenu.add.selector("Save Slot: ", ['1', '2', '3'])
        textInp = saveMenu.add.text_input("Save Name: ", tama.name)
        saveMenu.add.button("Save", save)

        saveMenu.add.vertical_margin(30)
        saveMenu.add.button('Back', inGameMenu)

        saveMenu.mainloop(display)

    def exitfn():
        menu()

    def backfn():
        run_game(tama.toString().split())

    pygame_menu.events.EXIT
    inGameMenu = pygame_menu.Menu('Menu', display_width, display_height, theme=pygame_menu.themes.THEME_SOLARIZED)

    inGameMenu.add.vertical_margin(20)

    inGameMenu.add.button('Options', optionsMenufn)
    inGameMenu.add.button('Help', helpMenufn)
    inGameMenu.add.button('Save', saveMenufn)
    inGameMenu.add.button('Exit', exitfn)
    inGameMenu.add.vertical_margin(20)
    inGameMenu.add.button('Back', backfn)

    inGameMenu.mainloop(display)

def menu():
# Supporting main menu functions
    # do if new game button is pressed (run game with default data values)
    def new_game():
        pygame_menu.events.EXIT
        name = textinp.get_value()
        if name == '':
            name = 'Tamagotchi'
        run_game([name, 0, 100, 100, 100, 100])

    # read data from save 1 and run game with those data values
    def initializeSave1():
        path = "./game_saves/"
        fileName = path + os.listdir("./game_saves")[0]
        save = open(fileName, 'r', encoding='utf8')
        data = save.readline().split()
        save.close()
        run_game(data)

    # read data from save 2 and run game with those data values
    def initializeSave2():
        path = "./game_saves/"
        fileName = path + os.listdir("./game_saves")[1]
        save = open(fileName, 'r', encoding='utf8')
        data = save.readline().split()
        save.close()
        run_game(data)

    # read data from save 3 and run game with those data values
    def initializeSave3():
        path = "./game_saves/"
        fileName = path + os.listdir("./game_saves")[2]
        save = open(fileName, 'r', encoding='utf8')
        data = save.readline().split()
        save.close()
        run_game(data)

    # do if load game button is pressed
    def load_game():
        # get rid of main menu
        pygame_menu.events.EXIT
        # set up new level select menu
        level_select = pygame_menu.Menu('Open Saved Game', display_width, display_height, theme=pygame_menu.themes.THEME_SOLARIZED)

        # determine number of saves in the file, make the corresponding number of
        # buttons and assign corresponding initialize fxn to each bttn
        if not os.path.exists("./game_saves"):
            os.makedirs("./game_saves")
        saves = os.listdir("./game_saves")
        if(len(saves) == 0):
            level_select.add.label("No Saves")
        if(len(saves) >= 1):
            level_select.add.button("Slot 1: " + saves[0].split('.')[1], initializeSave1)
        if (len(saves) >= 2):
            level_select.add.button("Slot 2: " + saves[1].split('.')[1], initializeSave2)
        if (len(saves) >= 3):
            level_select.add.button("Slot 3: " + saves[2].split('.')[1], initializeSave3)

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
    dark_grey = (190, 190, 190)
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
