import pygame
import pygame_menu
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'
selected = 45
current_img = None
current_pet = 'bunny'


def main():
    pygame.init()
    menu()


class Pet:
    def __init__(self, tamaName, tamaAge, tamaHunger, tamaSleep, tamaBrush, tamaPlay, pet):
        self.name = tamaName
        self.age = tamaAge
        self.hunger = tamaHunger
        self.sleep = tamaSleep
        self.brush = tamaBrush
        self.play = tamaPlay
        self.pet = pet

    def toString(self):
        return str(self.name) + " " + str(int(self.age)) + " " + str(int(self.hunger)) + " " + str(int(self.sleep)) + \
               " " + str(int(self.brush)) + " " + str(int(self.play)) + " " + str(self.pet)


def run_game(tamaData, tama_pet_small, tama_pet1_small, tama_pet_eat_small, tama_pet_sleep_small, tama_pet_brush_small,
             tama_pet_play_small, tama_pet_sick_small, tama_pet_sick1_small, tama_pet_dead_small):
    # flag to see if player exited
    crashed = False

    # create tama instance
    tama = Pet(tamaData[0], int(tamaData[1]), int(tamaData[2]), int(tamaData[3]), int(tamaData[4]), int(tamaData[5]),
               tamaData[6])

    # setup for pet frame alternation every second
    current_img = tama_pet_small
    ALTERNATEimg = pygame.USEREVENT + 1
    INCREASEage = pygame.USEREVENT + 2
    pygame.time.set_timer(ALTERNATEimg, 1250)
    pygame.time.set_timer(INCREASEage, 10000)

    hungerAction = False
    sleepAction = False
    brushAction = False
    playAction = False

    # while game not exited
    while not crashed:
        # event handler
        for event in pygame.event.get():
            # exit if x pressed
            if event.type == pygame.QUIT:
                crashed = True
            # alternate image, alpha sets transparency
            if event.type == ALTERNATEimg:
                # carrot_small.set_alpha(0)
                current_img.set_alpha(0)
                # if hunger button was pressed, display animation on image switch
                if (tama.hunger + tama.play + tama.brush + tama.sleep) / 4 == 0:
                    current_img = tama_pet_dead_small
                    current_img.set_alpha(255)
                elif (tama.hunger + tama.play + tama.brush + tama.sleep) / 4 <= 25:
                    if current_img == tama_pet_small:
                        current_img = tama_pet_sick1_small
                        current_img.set_alpha(255)
                    elif current_img == tama_pet1_small:
                        current_img = tama_pet_sick_small
                        current_img.set_alpha(255)
                    elif current_img == tama_pet_sick_small:
                        current_img = tama_pet_sick1_small
                        current_img.set_alpha(255)
                    else:
                        current_img = tama_pet_sick_small
                        current_img.set_alpha(255)
                elif hungerAction:
                    # carrot_small.set_alpha(255)
                    current_img = tama_pet_eat_small
                    current_img.set_alpha(255)
                    hungerAction = False
                # if sleep button was pressed, display animation on image switch
                elif sleepAction:
                    current_img = tama_pet_sleep_small
                    current_img.set_alpha(255)
                    sleepAction = False
                # if brush button was pressed, display animation on image switch
                elif brushAction:
                    current_img = tama_pet_brush_small
                    current_img.set_alpha(255)
                    brushAction = False
                # if play button was pressed, display animation on image switch
                elif playAction:
                    current_img = tama_pet_play_small
                    current_img.set_alpha(255)
                    playAction = False
                # else, flip...
                elif current_img == tama_pet_small:
                    current_img = tama_pet1_small
                    current_img.set_alpha(255)
                # flop
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
                        hungerAction = True
                        tama.hunger = 100
                    elif selected == 245:
                        sleepAction = True
                        tama.sleep = 100
                    elif selected == 445:
                        brushAction = True
                        tama.brush = 100
                    else:
                        playAction = True
                        tama.play = 100
                # move select right
                elif 565 <= event.pos[0] <= 635 and 500 <= event.pos[1] <= 570:
                    shift_select('right')
                # Menu Button
                elif 0 <= event.pos[0] <= 124 and 0 <= event.pos[1] <= 29:
                    inGameMenufn(tama)
            # increase Tama age every 10 seconds
            if event.type == INCREASEage:
                tama.age += 1

        # display background and pet
        display.fill(sky_blue)
        pet(current_img, display_width * .27, display_height * .27)

        # display care function icons
        eat(eat_small, 45, 60)
        sleep(sleep_small, 260, 60)
        brush(brush_small, 460, 60)
        ball(ball_small, 660, 60)
        selector(select_small, selected, 33)
        # display_carrot(carrot_small, 325, 365)

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
        textRect_name.center = (display_width - text_name.get_width() / 2 - 10, text_name.get_height() / 2 + 5)
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

def selector(p, x, y):
    return display.blit(p, (x, y))


# Displays buttons
def button(x, y, r, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()

    # Displays and changes color of button when hovered over
    if x - r < mouse[0] < x + r and y - r < mouse[1] < y + r:
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


def get_images(pet_type):
    pet_imgs = []
    if pet_type == 'bunny':
        pet_imgs.append(tama_bunny_small)
        pet_imgs.append(tama_bunny1_small)
        pet_imgs.append(tama_bunny_eat_small)
        pet_imgs.append(tama_bunny_sleep_small)
        pet_imgs.append(tama_bunny_brush_small)
        pet_imgs.append(tama_bunny_play_small)
        pet_imgs.append(tama_bunny_sick_small)
        pet_imgs.append(tama_bunny_sick1_small)
        pet_imgs.append(tama_bunny_dead_small)

    elif pet_type == 'fox':
        pet_imgs.append(tama_fox_small)
        pet_imgs.append(tama_fox1_small)
        pet_imgs.append(tama_fox_eat_small)
        pet_imgs.append(tama_fox_sleep_small)
        pet_imgs.append(tama_fox_brush_small)
        pet_imgs.append(tama_fox_play_small)
        pet_imgs.append(tama_fox_sick_small)
        pet_imgs.append(tama_fox_sick2_small)
        pet_imgs.append(tama_fox_dead_small)

    elif pet_type == 'cat':
        pet_imgs.append(tama_cat1_small)
        pet_imgs.append(tama_cat2_small)
        pet_imgs.append(tama_cat_eat_small)
        pet_imgs.append(tama_cat_sleep_small)
        pet_imgs.append(tama_cat_brush_small)
        pet_imgs.append(tama_cat_play_small)
        pet_imgs.append(tama_cat_sick_small)
        pet_imgs.append(tama_cat_sick2_small)
        pet_imgs.append(tama_cat_dead_small)
    return pet_imgs


# in game menu function
def inGameMenufn(tama):
    # Supporting in game menu functions
    # Options menu function
    def optionsMenufn():
        pygame_menu.events.EXIT
        optionsMenu = pygame_menu.Menu('options', display_width, display_height,
                                       theme=pygame_menu.themes.THEME_SOLARIZED)

        optionsMenu.add.label("Options")
        optionsMenu.add.vertical_margin(20)
        optionsMenu.add.button('Back', inGameMenu)

        optionsMenu.mainloop(display)

    # help menu function
    def helpMenufn():
        pygame_menu.events.EXIT
        helpMenu = pygame_menu.Menu('Help', display_width, display_height, theme=pygame_menu.themes.THEME_SOLARIZED)

        helpMenu.add.label("Instructions Here")
        helpMenu.add.vertical_margin(20)
        helpMenu.add.button('Back', inGameMenu)

        helpMenu.mainloop(display)

    # save menu function
    def saveMenufn():

        # function that actually does the save file i/o
        def save():
            # get the save slot and name of the save
            slot = slotInp.get_value()[0]
            name = textInp.get_value()

            path = "./game_saves/"
            saves = os.listdir("./game_saves")

            # save to slot 1
            if slot == '1':
                # if theres already a save in slot 1, remove it
                if len(saves) >= 1 and os.path.isfile(path + saves[0]):
                    os.remove(path + saves[0])
                # create the new save in the save folder
                filename = "SS1." + name + '.txt'
                with open(os.path.join(path, filename), 'w') as temp_file:
                    temp_file.write(tama.toString())

            # save to slot 2
            if slot == '2':
                # if theres already a save in slot 1, remove it
                if len(saves) >= 2 and os.path.isfile(path + saves[1]):
                    os.remove(path + saves[1])
                    # create the new save in the save folder
                filename = "SS2." + name + '.txt'
                with open(os.path.join(path, filename), 'w') as temp_file:
                    temp_file.write(tama.toString())

            # save to slot 3
            if slot == '3':
                # if theres already a save in slot 1, remove it
                if len(saves) >= 3 and os.path.isfile(path + saves[2]):
                    os.remove(path + saves[2])
                    # create the new save in the save folder
                filename = "SS3." + name + '.txt'
                with open(os.path.join(path, filename), 'w') as temp_file:
                    temp_file.write(tama.toString())

            # return to the in game menu
            inGameMenufn(tama)

        # mak the save menu
        pygame_menu.events.EXIT
        saveMenu = pygame_menu.Menu('Save', display_width, display_height, theme=pygame_menu.themes.THEME_SOLARIZED)

        # does the game_saves folder exist? if no, make one.
        saveMenu.add.label("Current Saves")
        if not os.path.exists("./game_saves"):
            os.makedirs("./game_saves")

        # list the current saves
        saves = os.listdir("./game_saves")
        for i, e in enumerate(saves):
            saveMenu.add.label("Slot " + str(i + 1) + ": " + e.split('.')[1])
        # no saves
        if len(saves) == 0:
            saveMenu.add.label("No Saves")

        # save menu selector, name input, buttons
        saveMenu.add.vertical_margin(40)
        slotInp = saveMenu.add.selector("Save Slot: ", ['1', '2', '3'])
        textInp = saveMenu.add.text_input("Save Name: ", tama.name)
        saveMenu.add.button("Save", save)

        saveMenu.add.vertical_margin(30)
        saveMenu.add.button('Back', inGameMenu)

        saveMenu.mainloop(display)

    # return to main menu
    def exitfn():
        menu()

    # return back to game (does not run in background)
    def backfn():
        data = tama.toString().split()
        run_game(data, *get_images(data[6]))

    # Make in game menu buttons
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

    def new_game(data=None):
        name = textinp.get_value()
        if name == '':
            name = 'Tamagotchi'
        if data is None:
            data = [name, 0, 100, 100, 100, 100, current_pet]
        pygame_menu.events.EXIT
        pet_imgs = get_images(data[6])
        run_game(data, *pet_imgs)

    # read data from save 1 and run game with those data values
    def initializeSave1():
        path = "./game_saves/"
        fileName = path + os.listdir("./game_saves")[0]
        save = open(fileName, 'r', encoding='utf8')
        data = save.readline().split()
        save.close()
        new_game(data)

    # read data from save 2 and run game with those data values
    def initializeSave2():
        path = "./game_saves/"
        fileName = path + os.listdir("./game_saves")[1]
        save = open(fileName, 'r', encoding='utf8')
        data = save.readline().split()
        save.close()
        new_game(data)

    # read data from save 3 and run game with those data values
    def initializeSave3():
        path = "./game_saves/"
        fileName = path + os.listdir("./game_saves")[2]
        save = open(fileName, 'r', encoding='utf8')
        data = save.readline().split()
        save.close()
        new_game(data)

    # do if load game button is pressed
    def load_game():
        # get rid of main menu
        pygame_menu.events.EXIT
        # set up new level select menu
        level_select = pygame_menu.Menu('Open Saved Game', display_width, display_height,
                                        theme=pygame_menu.themes.THEME_SOLARIZED)

        # determine number of saves in the file, make the corresponding number of
        # buttons and assign corresponding initialize fxn to each bttn.
        # If game_saves file does not exist, make it.
        if not os.path.exists("./game_saves"):
            os.makedirs("./game_saves")
        saves = os.listdir("./game_saves")
        if len(saves) == 0:
            level_select.add.label("No Saves")
        if len(saves) >= 1:
            level_select.add.button("Slot 1: " + saves[0].split('.')[1], initializeSave1)
        if len(saves) >= 2:
            level_select.add.button("Slot 2: " + saves[1].split('.')[1], initializeSave2)
        if len(saves) >= 3:
            level_select.add.button("Slot 3: " + saves[2].split('.')[1], initializeSave3)

        # add back button
        level_select.add.vertical_margin(20)
        level_select.add.button('Back', menu)
        level_select.mainloop(display)

    def select_pet():
        pygame_menu.events.EXIT
        global current_pet
        current_pet = 'bunny'
        # set up pet select menu
        pet_select = pygame_menu.Menu('Select Pet', display_width, display_height,
                                      theme=pygame_menu.themes.THEME_SOLARIZED)

        bunny_img = pet_select.add.image('tamarabbit.png', image_id='bunny', scale=(0.4, 0.4))
        fox_img = pet_select.add.image('fox-happy1.png', image_id='fox', scale=(0.1, 0.1))
        cat_img = pet_select.add.image('cat1.png', image_id='cat', scale=(0.4, 0.4))
        bunny_img.set_border(2, 'black')
        fox_img.set_border(2, 'black')
        cat_img.set_border(2, 'black')
        bunny_img.set_float(origin_position=True)
        fox_img.set_float(origin_position=True)
        cat_img.set_float(origin_position=True)
        bunny_img.translate(100, 100)
        fox_img.translate(300, 45)
        cat_img.translate(500, 110)

        pet_select.add.vertical_margin(300)
        pet_select.add.selector("Select Pet: ", [('Bunny', 'bunny'), ('Fox', 'fox'), ('Cat', 'cat')],
                                onchange=update_pet)
        pet_select.add.button('Done', new_game)
        pet_select.add.button('Back', menu)
        pet_select.mainloop(display)

    def update_pet(tup, selection):
        global current_pet
        current_pet = selection

    # SET UP MAIN MENU
    pygame_menu.events.EXIT
    menu = pygame_menu.Menu('Main Menu', display_width, display_height, theme=pygame_menu.themes.THEME_SOLARIZED)

    menu.add.image('./ascii_logo_noBackground.png')
    menu.add.vertical_margin(20)
    textinp = menu.add.text_input('Pet Name:  ')
    menu.add.button('Start New Game', select_pet)
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
    tama_fox = pygame.image.load('Fox-happy1.png')
    tama_fox_small = pygame.transform.scale(tama_fox, (350, 400))
    tama_fox1 = pygame.image.load('Fox-happy2.png')
    tama_fox1_small = pygame.transform.scale(tama_fox1, (350, 400))
    tama_fox_eat = pygame.image.load('Fox-eat.png')
    tama_fox_eat_small = pygame.transform.scale(tama_fox_eat, (350, 400))
    tama_fox_sleep = pygame.image.load('Fox-sleep.png')
    tama_fox_sleep_small = pygame.transform.scale(tama_fox_sleep, (350, 400))
    tama_fox_brush = pygame.image.load('Fox-brush.png')
    tama_fox_brush_small = pygame.transform.scale(tama_fox_brush, (350, 400))
    tama_fox_play = pygame.image.load('Fox-play.png')
    tama_fox_play_small = pygame.transform.scale(tama_fox_play, (350, 400))
    tama_fox_sick = pygame.image.load('Fox-sad.png')
    tama_fox_sick_small = pygame.transform.scale(tama_fox_sick, (350, 400))
    tama_fox_sick2 = pygame.image.load('Fox-sad2.png')
    tama_fox_sick2_small = pygame.transform.scale(tama_fox_sick2, (350, 400))
    tama_fox_dead = pygame.image.load('Fox-dead.png')
    tama_fox_dead_small = pygame.transform.scale(tama_fox_dead, (350, 400))


    tama_bunny = pygame.image.load('tamarabbit.png')
    tama_bunny_small = pygame.transform.scale(tama_bunny, (350, 350))
    tama_bunny1 = pygame.image.load('tamarabbit1.png')
    tama_bunny1_small = pygame.transform.scale(tama_bunny1, (350, 350))
    tama_bunny_eat = pygame.image.load('tamarabbiteat.png')
    tama_bunny_eat_small = pygame.transform.scale(tama_bunny_eat, (350, 350))
    tama_bunny_sleep = pygame.image.load('tamarabbitsleep.png')
    tama_bunny_sleep_small = pygame.transform.scale(tama_bunny_sleep, (350, 350))
    tama_bunny_brush = pygame.image.load('tamarabbitbrush.png')
    tama_bunny_brush_small = pygame.transform.scale(tama_bunny_brush, (350, 350))
    tama_bunny_play = pygame.image.load('tamarabbitplay.png')
    tama_bunny_play_small = pygame.transform.scale(tama_bunny_play, (350, 350))
    tama_bunny_sick = pygame.image.load('tamarabbit-sad.png')
    tama_bunny_sick_small = pygame.transform.scale(tama_bunny_sick, (350, 350))
    tama_bunny_sick1 = pygame.image.load('tamarabbit1-sad.png')
    tama_bunny_sick1_small = pygame.transform.scale(tama_bunny_sick1, (350, 350))
    tama_bunny_dead = pygame.image.load('tamarabbit-dead.png')
    tama_bunny_dead_small = pygame.transform.scale(tama_bunny_dead, (350, 350))

    tama_cat1 = pygame.image.load('cat1.png')
    tama_cat1_small = pygame.transform.scale(tama_cat1, (350, 350))
    tama_cat2 = pygame.image.load('cat2.png')
    tama_cat2_small = pygame.transform.scale(tama_cat2, (350, 350))
    tama_cat_eat = pygame.image.load('cat_eat.png')
    tama_cat_eat_small = pygame.transform.scale(tama_cat_eat, (350, 350))
    tama_cat_sleep = pygame.image.load('cat_sleep.png')
    tama_cat_sleep_small = pygame.transform.scale(tama_cat_sleep, (350, 350))
    tama_cat_brush = pygame.image.load('cat_brush.png')
    tama_cat_brush_small = pygame.transform.scale(tama_cat_brush, (350, 350))
    tama_cat_play = pygame.image.load('cat_play.png')
    tama_cat_play_small = pygame.transform.scale(tama_cat_play, (525, 325))
    tama_cat_sick = pygame.image.load('cat_sick1.png')
    tama_cat_sick_small = pygame.transform.scale(tama_cat_sick, (350, 350))
    tama_cat_sick2 = pygame.image.load('cat_sick2.png')
    tama_cat_sick2_small = pygame.transform.scale(tama_cat_sick2, (350, 350))
    tama_cat_dead = pygame.image.load('cat_dead.png')
    tama_cat_dead_small = pygame.transform.scale(tama_cat_dead, (350, 350))


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

    main()
