# tamagotchi emu first version by chloe
# just sets up basic display and pet
import pygame


def start_new():
    # flag to see if player exited
    crashed = False
    # setup for pet frame alternation every second
    current_img = tama_pet
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
                if current_img == tama_pet:
                    current_img = tama_pet1
                    current_img.set_alpha(255)
                else:
                    current_img = tama_pet
                    current_img.set_alpha(255)
        # display background and pet
        display.fill(sky_blue)
        pet(current_img, display_width*.22, display_height*.17)

        eat_small = pygame.transform.scale(eat_pic, (120, 80))
        eat(eat_small, 50, 20)
        sleep_small = pygame.transform.scale(sleep_pic, (90, 80))
        sleep(sleep_small, 245, 20)
        brush_small = pygame.transform.scale(brush_pic, (90, 80))
        brush(brush_small, 465, 20)
        ball_small = pygame.transform.scale(ball_pic, (90, 85))
        ball(ball_small, 655, 20)

        # button display, top is white circle, bottom is black outline
        # params are display, color, position, radius, width for black outline
        # Left button
        pygame.draw.circle(display, (255, 255, 255), (200, 530), 35)
        pygame.draw.circle(display, (0,0,0), (200,530), 35, width=5)

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
    display.blit(p, (x,y))

if __name__ == '__main__':
    # background color
    sky_blue = (173, 216, 230)
    # window setup
    pygame.init()
    display_width = 800
    display_height = 600
    display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("tamagotchi demo")
    # running timer since startup. may be useful for saves
    clock = pygame.time.Clock()
    # loading tamagotchi images
    tama_pet = pygame.image.load('tamarabbit.png')
    tama_pet1 = pygame.image.load('tamarabbit1.png')
    # load care images
    eat_pic = pygame.image.load('eat.png')
    sleep_pic = pygame.image.load('sleep.png')
    brush_pic = pygame.image.load('brush.png')
    ball_pic = pygame.image.load('ball.png')
    start_new()
