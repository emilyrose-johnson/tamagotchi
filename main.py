import pygame
import pygame_menu
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'


def main():
    pygame.init()
    menu()

def run_game():
    # flag to see if player exited
    crashed = False
    # setup for pet frame alternation every second
    current_img = tama_pet_small
    ALT = pygame.USEREVENT + 1
    pygame.time.set_timer(ALT, 1000)

    # while game not exited
    while not crashed:
        for event in pygame.event.get():
            # exit if x pressed
            if event.type == pygame.QUIT:
                crashed = True
            # alternate image, alpha sets transparency
            if event.type == ALT:
                current_img.set_alpha(0)
                if current_img == tama_pet_small:
                    current_img = tama_pet1_small
                    current_img.set_alpha(255)
                else:
                    current_img = tama_pet_small
                    current_img.set_alpha(255)
        # display background and pet
        display.fill(sky_blue)
        pet(current_img, display_width * .27, display_height * .27)

        eat(eat_small, 50, 60)
        sleep(sleep_small, 245, 60)
        brush(brush_small, 465, 60)
        ball(ball_small, 655, 60)

        # button display, top is white circle, bottom is black outline
        # params are display, color, position, radius, width for black outline
        # Left button
        pygame.draw.circle(display, (255, 255, 255), (200, 530), 35)
        pygame.draw.circle(display, (0, 0, 0), (200, 530), 35, width=5)

        # middle button
        pygame.draw.circle(display, (255, 255, 255), (400, 530), 35)
        pygame.draw.circle(display, (0, 0, 0), (400, 530), 35, width=5)

        # right button
        pygame.draw.circle(display, (255, 255, 255), (600, 530), 35)
        pygame.draw.circle(display, (0, 0, 0), (600, 530), 35, width=5)

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

def menu():

    def new_game():
        pygame_menu.events.EXIT
        run_game()

    def load_game():
        # Do the job here !
        pass

    menu = pygame_menu.Menu('Welcome', display_width, display_height,
                           theme=pygame_menu.themes.THEME_SOLARIZED)

    menu.add.image('./ascii_logo_noBackground.png')
    menu.add.text_input('Name:  ', default='John Doe')
    menu.add.button('Start New Game', new_game)
    menu.add.button('Load Game', load_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(display)


if __name__ == '__main__':
    sky_blue = (173, 216, 230)
    # window setup
    display_width = 800
    display_height = 600
    display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("tamagotchi demo")
    # running timer since startup. may be useful for saves
    clock = pygame.time.Clock()
    # loading tamagotchi images and resize
    tama_pet = pygame.image.load('tamarabbit.png')
    tama_pet_small = pygame.transform.scale(tama_pet, (350, 350))
    tama_pet1 = pygame.image.load('tamarabbit1.png')
    tama_pet1_small = pygame.transform.scale(tama_pet1, (350, 350))

    # load care images and resize
    eat_pic = pygame.image.load('eat.png')
    eat_small = pygame.transform.scale(eat_pic, (110, 70))

    sleep_pic = pygame.image.load('sleep.png')
    sleep_small = pygame.transform.scale(sleep_pic, (80, 70))

    brush_pic = pygame.image.load('brush.png')
    brush_small = pygame.transform.scale(brush_pic, (80, 70))

    ball_pic = pygame.image.load('ball.png')
    ball_small = pygame.transform.scale(ball_pic, (80, 75))
    main()