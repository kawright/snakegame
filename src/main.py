"""
This is the main module for a simple snake game.

Kristoffer A. Wright
"""

import pygame
import random
import sys

# SIZE CONSTANTS
TILE_SIZE = 16
SCORE_BAR_SIZE = 48
SCREEN_TILES_X = 50
SCREEN_TILES_Y = 50
SCREEN_SIZE_Y = SCREEN_TILES_Y * TILE_SIZE + SCORE_BAR_SIZE
SCREEN_SIZE_X = SCREEN_TILES_X * TILE_SIZE
FONT_SIZE = 48
SEG_RADIUS = 7

# COLOR CONSTANTS
SNAKE_COLOR = (0, 200, 0)
FOOD_COLOR = (200, 0, 0)
BG_COLOR = (0, 0 ,0)
FONT_COLOR = (255, 255, 255)
SCOREBAR_COLOR = (64, 64, 64)

# OTHER CONSTANTS
START_LEN = 5
START_X = 25
START_Y = 25
FPS = 16
FRAME_MILLIS = int((1 / FPS) * 1000)

def create_seg(color):
    """
    Create a segment tile.
    """

    # Create a new surface in which to paint the segment:
    seg_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))

    # Draw the segment onto the surface:
    pygame.draw.circle(seg_surf, color, (TILE_SIZE/2, TILE_SIZE/2), SEG_RADIUS)

    return seg_surf

def create_blank():
    """
    Create a blank tile.
    """

    return pygame.Surface((TILE_SIZE, TILE_SIZE))

def game_over(screen):
    """
    Print the game over screen.
    """

    surf = pygame.Surface((SCREEN_SIZE_X, SCREEN_SIZE_Y))
    gameover_font = pygame.font.SysFont("monospace", FONT_SIZE)
    gameover_label = gameover_font.render("GAME OVER!", 1, FONT_COLOR)
    surf.blit(gameover_label, (250, 250))
    screen.blit(surf, (0, 0))
    pygame.display.flip()

    while (True):

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit(0)

def main():

    # Initialize the screen:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))

    # Initialize snake:
    direction = "LEFT"
    xpos = START_X
    ypos = START_Y
    snakelen = START_LEN
    is_growing = False
    snakesegs = []

    # Initialize the list containing the position of the snake segments:
    for i in range(xpos, xpos+snakelen):
        snakesegs.append((i, ypos))
        screen.blit(create_seg(SNAKE_COLOR), ((i*TILE_SIZE), (ypos*TILE_SIZE + \
            SCORE_BAR_SIZE)))

    # Initialize food:
    while(True):
        xfood = random.randint(0, 49)
        yfood = random.randint(0, 49)

        # Ensure that the food is not in the snake before breaking:
        if ((xfood, yfood) not in snakesegs):
            break
    screen.blit(create_seg(FOOD_COLOR), ((xfood*TILE_SIZE), (yfood*TILE_SIZE + \
        SCORE_BAR_SIZE)))

    # Other initializations:
    score = 0

    #===========#
    # MAIN LOOP #
    #===========#
    while (True):

        # Get the start time for this frame:
        starttime = pygame.time.get_ticks()

        # Clear the snake's butt (unless we are growing):
        if not is_growing:
            screen.blit(create_blank(), ((snakesegs[-1][0]*TILE_SIZE), \
                (snakesegs[-1][1]*TILE_SIZE + SCORE_BAR_SIZE)))
            snakesegs.pop()
        else:
            is_growing = False

        # Move the head to the next position:
        if (direction == "RIGHT"):
            xpos += 1
        elif (direction == "LEFT"):
            xpos -= 1
        elif (direction == "UP"):
            ypos -= 1
        elif (direction == "DOWN"):
            ypos += 1

        # Check for game over conditions:

        # 1. Collision with border
        if ((xpos < 0) or (xpos >= SCREEN_TILES_X)):
            game_over(screen)
        if ((ypos < 0) or (ypos >= SCREEN_TILES_Y)):
            game_over(screen)

        # 2. Collision with self
        if ((xpos, ypos) in (snakesegs)):
            game_over(screen)

        # Add the new head to snakesegs
        snakesegs.insert(0, (xpos, ypos))

        # Check for collisions with food:
        if ((xpos == xfood) and (ypos == yfood)):

            # Increment the score:
            score += 1

            # Spawn new food:
            while(True):
                xfood = random.randint(0, 49)
                yfood = random.randint(0, 49)
                if ((xfood, yfood) not in snakesegs):
                    break

            # Paint the food:
            screen.blit(create_seg(FOOD_COLOR), ((xfood*TILE_SIZE), \
                (yfood*TILE_SIZE + SCORE_BAR_SIZE)))

            # Set the growing flag so that we don't delete the butt on the next 
            # frame:
            is_growing = True


        # Move and blit the snake's head:
        screen.blit(create_seg(SNAKE_COLOR), ((xpos*TILE_SIZE), \
            (ypos*TILE_SIZE + SCORE_BAR_SIZE)))
        

        # Paint the score bar:
        scorebar_surf = pygame.Surface((SCREEN_SIZE_X, SCORE_BAR_SIZE))
        scorebar_surf.fill(SCOREBAR_COLOR)
        score_font = pygame.font.SysFont("monospace", FONT_SIZE)
        score_label = score_font.render("SCORE: {}".format(score), 1, \
            FONT_COLOR)
        scorebar_surf.blit(score_label, (0, 0))
        screen.blit(scorebar_surf, (0, 0))
        
        # Flip the screen:
        pygame.display.flip()

        # Event handler:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                return 0

            # Check for key presses:
            elif event.type == pygame.KEYDOWN:

                # Handle direction changes:
                if event.key == pygame.K_LEFT:
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    direction = "RIGHT"
                elif event.key == pygame.K_DOWN:
                    direction = "DOWN"
                elif event.key == pygame.K_UP:
                    direction = "UP"

        # Get the current time, then wait until the end of the frame:
        currtime = pygame.time.get_ticks()
        deltatime = currtime - starttime
        pygame.time.wait(FRAME_MILLIS - deltatime)

if __name__ == "__main__":
    sys.exit(main())
    