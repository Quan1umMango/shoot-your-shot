import pygame

# Screen consts
SCREEN_W, SCREEN_H = 1280,720

# Color consts
MAROON = 128, 0, 0
RED = 255,0,0
DARK_GREEN =  0, 100,0 
LIGHT_GREEN =  0, 238, 0 

# Game object consts

""" Represents the borders width (if its verticle) or its height (if its horizontal) """
BORDER_SIZE = 30

""" Represents the sizes of squares where all the game objects such as holes and obstacles """
SQUARE_SIZE = 30

BALL_RADIUS = 30
BALL_COLOR = RED


def draw_borders(screen):
    pygame.draw.rect(screen,MAROON,pygame.Rect(0,0,SCREEN_W,BORDER_SIZE)) 
    pygame.draw.rect(screen,MAROON,pygame.Rect(0,SCREEN_H-BORDER_SIZE,SCREEN_W,BORDER_SIZE)) 


    pygame.draw.rect(screen,MAROON,pygame.Rect(0,0,BORDER_SIZE,SCREEN_H)) 

    pygame.draw.rect(screen,MAROON,pygame.Rect(SCREEN_W-BORDER_SIZE,0,BORDER_SIZE,SCREEN_H)) 


def draw_bg_squares(screen):
    start_x, end_x = BORDER_SIZE, SCREEN_W - BORDER_SIZE
    start_y, end_y = BORDER_SIZE, SCREEN_H - BORDER_SIZE

    count = 0 

    for y in range(start_y, end_y,SQUARE_SIZE):
        for x in range(start_x,end_x,SQUARE_SIZE):
            r = pygame.Rect(x,y,SQUARE_SIZE,SQUARE_SIZE)
            c = LIGHT_GREEN if count % 2 == 0 else DARK_GREEN
            pygame.draw.rect(screen,c,r)
            count += 1

class Ball:
    def __init__(self,x,y):
        self.position = (x,y)

    def draw(self,screen):
        pygame.draw.circle(screen,BALL_COLOR,self.position,BALL_RADIUS)


def main():

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))
    clock = pygame.time.Clock()
    running = True

    ball = Ball(SCREEN_W/2,SCREEN_H/2)

    while running:
        # poll for events
    # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("green")

        draw_bg_squares(screen)
        draw_borders(screen)
        ball.draw(screen)


        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

if __name__ == "__main__":
    main()
