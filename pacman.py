import pygame
from pacstructs import *
from pacfuncs import *
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

score = 0

pygame.init()

size = (600, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Ghost Maze")

background = pygame.image.load("modified_gridbackground_dark_purple.png").convert()
coin = pygame.image.load("nomdot.png").convert()
coin.set_colorkey(BLACK)
cells = init_grid("modified.jpeg")

font = pygame.font.SysFont('Calibri', 20, True, False)

pacman = PacMan()
pacman.rect.x = 7 * 40
pacman.rect.y = 13 * 40
pacman.gridloc = [7, 13]

INKY = Ghost("green", 6, 7)
BLINKY = Ghost("red", 7, 7)
CLYDE = Ghost("orange", 8, 7)

framecount = 0
done = False
clock = pygame.time.Clock()
start = time.time()

# Function to toggle dynamic walls every 5 seconds
def toggle_dynamic_walls(cells):
    current_time = time.time()
    for row in cells:
        for cell in row:
            if cell.dynamic and (current_time - cell.last_toggle_time >= 5):
                cell.traversable = not cell.traversable
                cell.last_toggle_time = current_time

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
                break
            if event.key == pygame.K_LEFT and is_valid_move(pacman, cells, -1, 0):
                pacman.goal_cell = [pacman.gridloc[0]-1, pacman.gridloc[1]]
                pacman.dir = 'l'
            elif event.key == pygame.K_RIGHT and is_valid_move(pacman, cells, 1, 0):
                pacman.goal_cell = [pacman.gridloc[0]+1, pacman.gridloc[1]]
                pacman.dir = 'r'
            elif event.key == pygame.K_UP and is_valid_move(pacman, cells, 0, -1):
                pacman.goal_cell = [pacman.gridloc[0], pacman.gridloc[1]-1]
                pacman.dir = 'u'
            elif event.key == pygame.K_DOWN and is_valid_move(pacman, cells, 0, 1):
                pacman.goal_cell = [pacman.gridloc[0], pacman.gridloc[1]+1]
                pacman.dir = 'd'

    pacman.update()
    toggle_dynamic_walls(cells)

    # Coin pickup
    cell = cells[pacman.gridloc[0]][pacman.gridloc[1]]
    if cell.coin:
        cell.coin = False
        score += 1
        print(f"Coin collected! Score: {score}")

    # Trap
    if cell.trap:
        print("Trap triggered!")
        score = max(0, score - 5)
        cell.trap = False

    # Powerup
    if cell.powerup:
        print("Powerup acquired!")
        score += 10
        cell.powerup = False

    # Score
    score_text = "Score: " + str(score)
    text = font.render(score_text, True, WHITE)

    # Win
    if score >= total_coins(cells):
        print("Congrats! All coins collected!")
        done = True
        break

    # Ghost AI
    if framecount == 0:
        INKY.goal_cell, _, _ = a_star(INKY, pacman, cells)
        BLINKY.goal_cell, _, _ = bfs(BLINKY, pacman, cells)
        CLYDE.goal_cell, _, _ = a_star(CLYDE, pacman, cells)

    update_ghost_direction(INKY)
    update_ghost_direction(BLINKY)
    update_ghost_direction(CLYDE)

    INKY.update()
    BLINKY.update()
    CLYDE.update()

    # Collision
    if check_collisions(pacman, [INKY, BLINKY, CLYDE]):
        print("Caught by a ghost! Final score:", score)
        done = True
        break

    screen.blit(background, [0, 0])
    screen.blit(text, [250, 10])

    draw_grid(screen, cells, coin)
    draw_obstacles(screen, cells)
    pacman.draw(screen)
    INKY.draw(screen)
    BLINKY.draw(screen)
    CLYDE.draw(screen)

    pygame.display.flip()
    framecount = (framecount + 1) % 32
    clock.tick(64)

pygame.quit()
