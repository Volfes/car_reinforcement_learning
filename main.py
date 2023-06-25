import pygame
import time
import math
import utils
import numpy as np

GRASS = pygame.image.load('imgs/grass.jpg')
TRACK = pygame.image.load('imgs/track.png')
TRACK_BORDER = pygame.image.load('imgs/track-border.png')
FINISH = pygame.image.load('imgs/finish.png')
INTERSECTION = pygame.image.load('imgs/intersection.png')
FINISH_MASK = pygame.mask.from_surface(FINISH)
INTERSECTION_MASK = pygame.mask.from_surface(INTERSECTION)
RED_BULL_CAR = utils.scale_image(pygame.image.load('imgs/red-bull.png'), 0.35)
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH_POSITION = (36, 380)
INTERSECTION_POS_1 = (165, 430)
INTERSECTION_POS_2 = (304, 562)
INTERSECTION_POS_3 = (452, 170)
INTERSECTION_POS_4 = (35, 110)


# place and draw images
def draw(screen, images, images_intersection):
    for img, pos in images:
        screen.blit(img, pos)

    player_car.draw(screen)

    for img, pos in images_intersection:
        screen.blit(img, pos)



# constant images
images = [(GRASS, (0,0)),(TRACK, (0,0)), (FINISH, FINISH_POSITION)]

# intersections
images_intersection = [(INTERSECTION, INTERSECTION_POS_1), 
                       (INTERSECTION, INTERSECTION_POS_2), 
                       (INTERSECTION, INTERSECTION_POS_3),
                       (INTERSECTION, INTERSECTION_POS_4),]


class DefaultCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 180 # test na 0 zmienic
        self.x, self.y = self.START_POS
        self.acceleration = 0.2 


    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel


    def draw(self, screen):
        utils.blit_rotate_center(screen, self.img, (self.x, self.y), self.angle)

    
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel) # max vel
        self.move()


    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()


    def move(self):
        radians = math.radians(self.angle)
        vertical_vel = math.cos(radians) * self.vel
        horizontal_vel = math.sin(radians) * self.vel
        self.y -= vertical_vel
        self.x -= horizontal_vel

    
    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        point_of_intersection = mask.overlap(car_mask, offset)
        return point_of_intersection
    
    def bounce(self):
        self.vel = -self.vel/2
        self.move()


class PlayerCar(DefaultCar):
    IMG = RED_BULL_CAR
    START_POS = (45,335)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 4, 0)
        self.move()

    def disqualification(self):
        self.vel = 0
        self.acceleration = 0


def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()
    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if not moved:
        player_car.reduce_speed()


# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Race')
clock = pygame.time.Clock()
running = True
FPS = 60
speed = 6
angle_speed = 3
player_car = PlayerCar(speed, angle_speed)
points = np.array([0,0,0,0,0])


while running:
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break


    move_player(player_car)
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()
        print('collide')

    if player_car.collide(FINISH_MASK, *FINISH_POSITION) and points[3] == 1:
        print('win')
        points[4] += 1
        print(points)
        points[0:4] = 0

    if player_car.collide(INTERSECTION_MASK, *INTERSECTION_POS_1):
        points[0] = 1
        print(points)
    
    if player_car.collide(INTERSECTION_MASK, *INTERSECTION_POS_2) and points[0] == 1:
        points[1] = 1
        print(points)

    if player_car.collide(INTERSECTION_MASK, *INTERSECTION_POS_3) and points[1] == 1:
        points[2] = 1
        print(points)
    
    if player_car.collide(INTERSECTION_MASK, *INTERSECTION_POS_4) and points[2] == 1:
        points[3] = 1
        print(points)
    
    if player_car.collide(INTERSECTION_MASK, *INTERSECTION_POS_4) and points[2] == 0:
        print("DYSKFALIFIKACJA")
        points[4] = -1
        print(points)
    
    if points[4] == -1:  
        player_car.disqualification()
  


    # RENDER YOUR GAME HERE
    draw(screen, images, images_intersection)


    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(FPS)  # limits FPS to given value

pygame.quit()