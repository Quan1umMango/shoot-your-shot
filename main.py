import pygame

# Screen consts
SCREEN_W, SCREEN_H = 1280,720

# Color consts
BLACK = 0,0,0
MAROON = 128, 0, 0
RED = 255,0,0
DARK_GREEN =  0, 100,0 
LIGHT_GREEN =  45, 207, 70

BG_COLOR = 45,207,70

# Game object consts

""" Represents the borders width (if its verticle) or its height (if its horizontal) """
BORDER_SIZE = 30

""" Represents the sizes of squares where all the game objects such as holes and obstacles """
SQUARE_SIZE = 30

BALL_RADIUS = 30
BALL_COLOR = RED

FRICTION = 0.1 
MAX_VELOCITY = 750

# Misc
MOUSE_BUTTON_ONE = 1

class Ball:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,BALL_RADIUS,BALL_RADIUS)
        # You may wonder why we represent velocity as a scalar but also have a dir vector component. it just works better this way
        self.dir = pygame.math.Vector2(0,0)
        self.velocity = 0.0 

    def draw(self,screen):
        pygame.draw.circle(screen,BALL_COLOR,(self.rect.x,self.rect.y),BALL_RADIUS)
        # border
        pygame.draw.circle(screen,BLACK,(self.rect.x,self.rect.y),BALL_RADIUS,2)

    def update(self,objects):
        # So we predict if the next position where our ball is going to be is gonna collide with something
        # We create a dummy rectangle to test our predicitions with and assign it the values our actual ball would take if we didnt check for collisions
        rect = self.rect
        rect.x += self.velocity * self.dir.x * 0.01
        rect.y += self.velocity * self.dir.y * 0.01

        for obj in objects:
            # Now, now, theres 4 cases.
            # 1.Ball collides a block with its top surface touching the block's bottom surface (ball makes contact with an object above it)
            # 2.Ball collides a block with its bottom surface touching the block's top surface
            # 3.Ball collides a block with its left surface touching the block's right surface
            # 4.Ball collides a block with its right surface touching the block's left surface

            # Depending on the situation, we need to change the ball's velocity accordingly.
            # Example: If the ball touches an object on its right, we change the velocity (or here, the dir)'s x component to be the opposite of that
            # that is, dir.x = -dir.x
            

            obj_rect = obj.rect.copy()
            
            if not rect.colliderect(obj_rect): continue


            dx = rect.centerx - obj_rect.centerx
            dy = rect.centery - obj_rect.centery

            overlap_x = (rect.width + obj_rect.width)/2 - abs(dx)
            overlap_y = (rect.height + obj_rect.height)/2 - abs(dy)

            if overlap_x < overlap_y:
                self.dir.x *= -1
            else:
                self.dir.y *= -1


        self.move()



    def move(self):
        self.rect.x += self.velocity  * self.dir.x
        self.rect.y += self.velocity * self.dir.y

        if abs(self.velocity) > 1:
            self.velocity -= FRICTION * -1 if self.velocity < 0 else 1
        else:
            self.velocity = 0
    
    """ Calculates the force (with its direction) when initial and final position of the mouse are given. This is what we use when we drag and release the mouse to shoot the ball """
    def calc_force(self,initial_pos,final_pos):
        initial_pos = pygame.math.Vector2(initial_pos)
        final_pos = pygame.math.Vector2(final_pos)

        #direction = (initial_pos - final_pos).normalize()
        #force_magnitude = (initial_pos - final_pos).magnitude()

        # In our game, force and velocity mean the same thing ok (just simplyifes things)
        vel = min((initial_pos - final_pos).magnitude(),MAX_VELOCITY)
        if vel == 0: return

        dir_ = (initial_pos-final_pos).normalize()
        self.velocity = vel * 0.1
        self.dir = dir_
         


class StaticBlock:
    def __init__(self,x,y,w,h):
        self.rect = pygame.Rect(x,y,w,h)
        
    def draw(self,screen):
        pygame.draw.rect(screen,MAROON,self.rect)

def create_borders():
    rects = [
            (0,0,SCREEN_W,BORDER_SIZE), 
            (0,SCREEN_H-BORDER_SIZE,SCREEN_W,BORDER_SIZE), 
            (0,0,BORDER_SIZE,SCREEN_H), 
            (SCREEN_W-BORDER_SIZE,0,BORDER_SIZE,SCREEN_H)    ]
    return [ StaticBlock(v[0],v[1],v[2],v[3]) for v in rects ]

def draw_bg_squares(screen):
    start_x, end_x = BORDER_SIZE, SCREEN_W - BORDER_SIZE
    start_y, end_y = BORDER_SIZE, SCREEN_H - BORDER_SIZE

    count = 0 

    for y in range(start_y, end_y,SQUARE_SIZE):
        for x in range(start_x,end_x,SQUARE_SIZE):
            r = pygame.Rect(x,y,SQUARE_SIZE,SQUARE_SIZE)
            #c = LIGHT_GREEN if count % 2 == 0 else DARK_GREEN
            c = BG_COLOR 
            pygame.draw.rect(screen,c,r)
            count += 1


def main():

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))
    clock = pygame.time.Clock()
    running = True

    (mouse_initial_pos,mouse_current_pos) = (None,None)

    borders = create_borders()
    ball = Ball(SCREEN_W/2,SCREEN_H/2)

    while running:
        # poll for events
    # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    running = False
                case pygame.MOUSEBUTTONDOWN:
                    btn = event.button
                    pos = event.pos
                    if btn == MOUSE_BUTTON_ONE:
                        mouse_initial_pos = pos
                case pygame.MOUSEBUTTONUP:
                    btn = event.button
                    pos = event.pos
                    if btn == MOUSE_BUTTON_ONE:
                        mouse_current_pos = pos
                    ball.calc_force(mouse_initial_pos,mouse_current_pos)
                    mouse_initial_pos,mouse_current_pos = None,None

        ball.update(borders)

        screen.fill(BG_COLOR)

        # draw_bg_squares(screen)
        for border in borders:
            border.draw(screen)
        ball.draw(screen)


        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

if __name__ == "__main__":
    main()
