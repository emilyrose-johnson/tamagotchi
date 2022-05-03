import time
import pygame
import pygame_menu
import os
import enum
import datetime

os.environ['SDL_VIDEO_CENTERED'] = '1'
selected = 45
current_img = None
current_pet = 'bunny'
petNameAge = ''
petNameAgeRect = None
actionQueue = []
speed = 20
DEAD = pygame.USEREVENT + 4
flop = 0


def main():
    menu()


class Pet:
    def __init__(self, tamaName, tamaAge, tamaHunger, tamaSleep, tamaBrush, tamaPlay, pet_img):
        self.name = tamaName
        self.age = tamaAge
        self.hunger = tamaHunger
        self.sleep = tamaSleep
        self.brush = tamaBrush
        self.play = tamaPlay
        self.pet_img = pet_img

    def toString(self):
        return str(self.name) + " " + str(int(self.age)) + " " + str(int(self.hunger)) + " " + str(int(self.sleep)) + \
               " " + str(int(self.brush)) + " " + str(int(self.play)) + " " + str(self.pet_img)


class PetAction(enum.Enum):
    hunger = 1
    brush = 2
    sleep = 3
    play = 4


# Handles all changes in image animations
def changeImg(tama, tama_pet_small, tama_pet1_small, tama_pet_eat_small,
              tama_pet_sleep_small, tama_pet_brush_small, tama_pet_play_small,
              tama_pet_sick_small, tama_pet_sick1_small, tama_pet_dead_small):
    global current_img
    global flop
    current_img.set_alpha(0)
    # if health is 0, set pet to dead
    if tama.hunger + tama.play + tama.brush + tama.sleep <= 0:
        current_img = tama_pet_dead_small
        growth(tama)
        current_img.set_alpha(255)
        pygame.time.set_timer(DEAD, 1, True)

    # if health < 25%, set pet to sick
    elif (tama.hunger + tama.play + tama.brush + tama.sleep) / 4 <= 25:
        if current_img == tama_pet_small:
            current_img = tama_pet_sick1_small
            growth(tama)
            current_img.set_alpha(255)
        elif current_img == tama_pet1_small:
            current_img = tama_pet_sick_small
            growth(tama)
            current_img.set_alpha(255)
        elif current_img == tama_pet_sick_small:
            current_img = tama_pet_sick1_small
            growth(tama)
            current_img.set_alpha(255)
        else:
            current_img = tama_pet_sick_small
            growth(tama)
            current_img.set_alpha(255)
    # if hunger button was pressed, display animation on image switch
    elif len(actionQueue) > 0 and actionQueue[0] == PetAction.hunger:
        current_img = tama_pet_eat_small
        growth(tama)
        current_img.set_alpha(255)
        actionQueue.pop(0)
    # if sleep button was pressed, display animation on image switch
    elif len(actionQueue) > 0 and actionQueue[0] == PetAction.sleep:
        current_img = tama_pet_sleep_small
        growth(tama)
        current_img.set_alpha(255)
        actionQueue.pop(0)
    # if brush button was pressed, display animation on image switch
    elif len(actionQueue) > 0 and actionQueue[0] == PetAction.brush:
        current_img = tama_pet_brush_small
        growth(tama)
        current_img.set_alpha(255)
        actionQueue.pop(0)
    # if play button was pressed, display animation on image switch
    elif len(actionQueue) > 0 and actionQueue[0] == PetAction.play:
        current_img = tama_pet_play_small
        growth(tama)
        current_img.set_alpha(255)
        actionQueue.pop(0)
    # else, flip...
    elif flop == 1:
        current_img = tama_pet1_small
        growth(tama)
        current_img.set_alpha(255)
        flop = 0
    # flop
    else:
        current_img = tama_pet_small
        growth(tama)
        current_img.set_alpha(255)
        flop = 1


# display tama name and age
def displayNameAge(tama):
    global petNameAge
    global petNameAgeRect
    font_name = pygame.font.Font('PixeloidSans.ttf', 25)
    petNameAge = font_name.render(tama.name + '\'s age: ' + str(tama.age), True, black, sky_blue)
    if petNameAge.get_width() < 289:
        petNameAgeRect = petNameAge.get_rect()
        petNameAgeRect.center = (display_width - petNameAge.get_width() / 2 - 10, petNameAge.get_height() / 2 + 5)
    else:
        petNameAge = font_name.render('Pets\'s age: ' + str(tama.age), True, black, sky_blue)
        petNameAgeRect = petNameAge.get_rect()
        petNameAgeRect.center = (display_width - petNameAge.get_width() / 2 - 10, petNameAge.get_height() / 2 + 5)


def growth(tama):
    global current_img
    if tama.pet_img == 'fox':
        if tama.age <= 15:
            current_img = pygame.transform.scale(current_img, (150, 200))
        elif 16 <= tama.age <= 30:
            current_img = pygame.transform.scale(current_img, (250, 300))
        else:
            current_img = pygame.transform.scale(current_img, (350, 400))
    else:
        if tama.age <= 15:
            current_img = pygame.transform.scale(current_img, (150, 150))
        elif 16 <= tama.age <= 30:
            current_img = pygame.transform.scale(current_img, (250, 250))
        else:
            current_img = pygame.transform.scale(current_img, (350, 350))


def run_game(tamaData, tama_pet_small):
    # flag to see if player exited
    crashed = False

    # create tama instance
    tama = None
    tama = Pet(tamaData[0], int(tamaData[1]), int(tamaData[2]), int(tamaData[3]), int(tamaData[4]),
               int(tamaData[5]), tamaData[6])

    # setup for pet frame alternation every second
    pet_imgs = get_images(tamaData[6])
    global current_img
    global speed
    global selected
    global petNameAge
    global petNameAgeRect
    current_img = tama_pet_small
    ALTERNATEimg = pygame.USEREVENT + 1
    INCREASEage = pygame.USEREVENT + 2
    DECREASEhealth = pygame.USEREVENT + 3
    pygame.time.set_timer(ALTERNATEimg, 1250)
    pygame.time.set_timer(INCREASEage, int(speed * 50))
    pygame.time.set_timer(DECREASEhealth, speed)

    displayNameAge(tama)
    display.fill(sky_blue)
    display_img(current_img, display_width * .27, display_height * .27)
    pygame.display.update()

    # while game not exited
    while not crashed:
        # event handler
        for event in pygame.event.get():
            # exit if x pressed
            if event.type == pygame.QUIT:
                crashed = True
            # Update pet image
            if event.type == ALTERNATEimg:
                changeImg(tama, *pet_imgs)
            # updates the hunger bar to decrease by 5% every speed/1000 seconds
            if event.type == DECREASEhealth:
                if tama.hunger > 0:
                    tama.hunger -= .05
                if tama.sleep > 0:
                    tama.sleep -= .05
                if tama.play > 0:
                    tama.play -= .05
                if tama.brush > 0:
                    tama.brush -= .05
            # handles if button is clicked
            if event.type == pygame.MOUSEBUTTONUP:
                # move select left
                if 165 <= event.pos[0] <= 235 and 500 <= event.pos[1] <= 570:
                    shift_select('left')
                # do action of selected function. Won't allow if pet is dead
                elif 365 <= event.pos[0] <= 435 and 500 <= event.pos[1] <= 570 and not (
                        tama.hunger + tama.play + tama.brush + tama.sleep <= 0):
                    # reset alternate img timer to 0 to display care action for correct time.
                    pygame.time.set_timer(ALTERNATEimg, 1250)
                    if selected == 45:
                        actionQueue.append(PetAction.hunger)
                        tama.hunger = 100
                    elif selected == 245:
                        actionQueue.append(PetAction.sleep)
                        tama.sleep = 100
                    elif selected == 445:
                        actionQueue.append(PetAction.brush)
                        tama.brush = 100
                    else:
                        actionQueue.append(PetAction.play)
                        tama.play = 100
                # move select right
                elif 565 <= event.pos[0] <= 635 and 500 <= event.pos[1] <= 570:
                    shift_select('right')
                # Menu Button
                elif 0 <= event.pos[0] <= 124 and 0 <= event.pos[1] <= 29:
                    inGameMenufn(tama)

            # increase Tama age based on speed
            if event.type == INCREASEage:
                if not (tama.hunger + tama.play + tama.brush + tama.sleep <= 0):
                    tama.age += 1
                displayNameAge(tama)
            if event.type == DEAD:
                time.sleep(3)
                gameOverMenu(tama)

        # display background and pet
        display.fill(sky_blue)
        display_img(current_img, display_width * .27, display_height * .27)

        # display care function icons
        display_img(eat_small, 45, 60)
        display_img(sleep_small, 260, 60)
        display_img(brush_small, 460, 60)
        display_img(ball_small, 660, 60)
        display_img(select_small, selected, 33)

        # display buttons
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

        # display pet name and age
        display.blit(petNameAge, petNameAgeRect)

        # Health bar display
        health_bars(tama.hunger, tama.sleep, tama.brush, tama.play)

        # update display, set fps to 60
        pygame.display.update()
        clock.tick(60)

    # exit code
    pygame.quit()
    quit()


# display images. params are image and position
def display_img(p, x, y):
    display.blit(p, (x, y))


# Display buttons, params are position, inactive color, active color and action
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


# moved square select icon
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


# creates list of selected pet images
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


def gameOverMenu(tama):
    # return to main menu
    def exitfn():
        main()

    # create theme color
    mytheme = pygame_menu.themes.THEME_BLUE.copy()
    mytheme.widget_font_color = (78, 23, 159)
    mytheme.background_color = sky_blue

    # Make in game menu buttons
    goMenu = pygame_menu.Menu('End of Game', display_width, display_height, theme=mytheme)

    goMenu.add.image('./ascii_GameOver_noBack.png')

    goMenu.add.vertical_margin(10)
    goMenu.add.label(tama.name + '\'s age: ' + str(tama.age))
    goMenu.add.vertical_margin(150)
    goMenu.add.button('Exit to Main Menu', exitfn)

    goMenu.mainloop(display)


# in game menu function
def inGameMenufn(tama):
    # create theme color
    mytheme = pygame_menu.themes.THEME_BLUE.copy()
    mytheme.widget_font_color = (78, 23, 159)
    mytheme.background_color = sky_blue

    # Options menu function
    def optionsMenufn():
        optionsMenu = pygame_menu.Menu('Options', display_width, display_height, theme=mytheme)

        def back():
            optionsMenu.disable()

        optionsMenu.add.label("The only option is whether or not to keep your pet alive")
        optionsMenu.add.vertical_margin(20)
        optionsMenu.add.button('Back', back)

        optionsMenu.mainloop(display)

    # help menu function
    def helpMenufn():
        helpMenu = pygame_menu.Menu('Help', display_width, display_height, theme=mytheme)

        def back():
            helpMenu.disable()

        helpMenu.add.label("As your pet ages, their needs will need to be met to\n keep them healthy."
                           " Make sure you check on your pet\n often to ensure their survival!\n"
                           "To care for your pet, when you notice the health bar\n"
                           "for a need going down, use the center button to raise\n"
                           "that need!")
        helpMenu.add.vertical_margin(20)
        helpMenu.add.button('Back', back)

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
                    temp_file.write(tama.toString() + ' ' + str(datetime.datetime.now().timestamp()))

            # save to slot 2
            if slot == '2':
                # if theres already a save in slot 1, remove it
                if len(saves) >= 2 and os.path.isfile(path + saves[1]):
                    os.remove(path + saves[1])
                    # create the new save in the save folder
                filename = "SS2." + name + '.txt'
                with open(os.path.join(path, filename), 'w') as temp_file:
                    temp_file.write(tama.toString() + ' ' + str(datetime.datetime.now().timestamp()))

            # save to slot 3
            if slot == '3':
                # if theres already a save in slot 1, remove it
                if len(saves) >= 3 and os.path.isfile(path + saves[2]):
                    os.remove(path + saves[2])
                    # create the new save in the save folder
                filename = "SS3." + name + '.txt'
                with open(os.path.join(path, filename), 'w') as temp_file:
                    temp_file.write(tama.toString() + ' ' + str(datetime.datetime.now().timestamp()))

            # return to the in game menu
            inGameMenufn(tama)

        # make the save menu
        saveMenu = pygame_menu.Menu('Save', display_width, display_height, theme=mytheme)

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

        def back():
            saveMenu.disable()

        saveMenu.add.vertical_margin(30)
        saveMenu.add.button('Back', back)

        saveMenu.mainloop(display)

    # return to main menu
    def exitfn():
        menu()

    # return back to game (does not run in background)
    def backfn():
        inGameMenu.disable()

    # Make in game menu buttons
    inGameMenu = pygame_menu.Menu('Menu', display_width, display_height, theme=mytheme)

    inGameMenu.add.vertical_margin(20)

    inGameMenu.add.button('Options', optionsMenufn)
    inGameMenu.add.button('Help', helpMenufn)
    inGameMenu.add.button('Save', saveMenufn)
    inGameMenu.add.button('Exit', exitfn)
    inGameMenu.add.vertical_margin(20)
    inGameMenu.add.button('Back', backfn)

    inGameMenu.mainloop(display)


# Calculates how much to change the pet's age when opening a saved file
def calcNewData(data):
    # get time when save was made
    old = datetime.datetime.fromtimestamp(float(data[7]))
    # get current time
    new = datetime.datetime.now()
    # get time difference
    tdelta = (new - old).total_seconds()

    # **global speed var = # of milliseconds/action
    # why 50 not 500? (should be 500 b/c ((# of milliseconds/action) / 1000) = # of actions/second  &
    # (1 / (# actions/second)) = # seconds/action  &  (time between saves) * (# seconds/action) = # of actions
    # **500 b/c divide 1000 in half since its only -.5 health per second, not 1
    subtractor = tdelta * (1 / (speed / 50))
    # set to 0 if new data < 0, otherwise set data
    for i in range(4):
        if int(data[i + 2]) - subtractor < 0:
            data[i + 2] = '0'
        else:
            data[i + 2] = str(int(int(data[i + 2]) - subtractor))
    return data


# Main menus before game screen
def menu():
    # create theme color
    mytheme = pygame_menu.themes.THEME_BLUE.copy()
    mytheme.widget_font_color = (78, 23, 159)
    mytheme.background_color = sky_blue

    # do if new game button is pressed (run game with default data values)
    def new_game(data=None):
        name = textinp.get_value()
        if name == '':
            name = 'Tamagotchi'
        if data is None:
            data = [name, 0, 100, 100, 100, 100, current_pet]
        pet_imgs = get_images(data[6])
        run_game(data, pet_imgs[0])

    # read data from save 1 and run game with those data values
    def initializeSave1():
        path = "./game_saves/"
        fileName = path + os.listdir("./game_saves")[0]
        save = open(fileName, 'r', encoding='utf8')
        data = save.readline().split()
        data = calcNewData(data)
        save.close()
        new_game(data)

    # read data from save 2 and run game with those data values
    def initializeSave2():
        path = "./game_saves/"
        fileName = path + os.listdir("./game_saves")[1]
        save = open(fileName, 'r', encoding='utf8')
        data = save.readline().split()
        data = calcNewData(data)
        save.close()
        new_game(data)

    # read data from save 3 and run game with those data values
    def initializeSave3():
        path = "./game_saves/"
        fileName = path + os.listdir("./game_saves")[2]
        save = open(fileName, 'r', encoding='utf8')
        data = save.readline().split()
        data = calcNewData(data)
        save.close()
        new_game(data)

    # do if load game button is pressed
    def load_game():
        # get rid of main menu
        # set up new level select menu
        level_select = pygame_menu.Menu('Open Saved Game', display_width, display_height, theme=mytheme)

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

        def back():
            level_select.disable()

        # add back button
        level_select.add.vertical_margin(20)
        level_select.add.button('Back', back)
        level_select.mainloop(display)

    # menu to select a pet
    def select_pet():
        global current_pet
        current_pet = 'bunny'
        # set up pet select menu
        pet_select = pygame_menu.Menu('Select Pet', display_width, display_height, theme=mytheme)

        # set up images
        bunny_img = pet_select.add.image('tamarabbit-crop.png', image_id='bunny', scale=(0.448, 0.448))
        fox_img = pet_select.add.image('fox-crop.png', image_id='fox', scale=(0.1, 0.1))
        cat_img = pet_select.add.image('cat-crop.png', image_id='cat', scale=(0.51, 0.51))
        bunny_img.set_border(2, 'black')
        fox_img.set_border(2, 'black')
        cat_img.set_border(2, 'black')
        bunny_img.set_float(origin_position=True)
        fox_img.set_float(origin_position=True)
        cat_img.set_float(origin_position=True)
        bunny_img.translate(130, 97)
        fox_img.translate(325, 97)
        cat_img.translate(498, 97)

        # set up buttons
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
    menu = pygame_menu.Menu('Main Menu', display_width, display_height, theme=mytheme)

    menu.add.image('./ascii_logo_noBackground.png')
    menu.add.vertical_margin(20)
    textinp = menu.add.text_input('Pet Name:  ')
    menu.add.button('Start New Game', select_pet)
    menu.add.button('Load Game', load_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(display)


if __name__ == '__main__':
    # create colors
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

    # loading fox images and resize
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

    # loading bunny images and resize
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

    # loading cat images and resize
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

    pygame.init()
    main()
