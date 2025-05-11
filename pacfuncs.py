import pygame
from pacstructs import GridCell, SearchNode
from PIL import Image
import random
import time

BLACK = (0, 0, 0)


def init_grid(file):
    bc = Image.open(file)
    pix = bc.load()
    bc.close()

    cols = 15
    rows = 15
    cells = [[GridCell() for _ in range(cols)] for _ in range(rows)]

    for x in range(cols):
        for y in range(rows):
            cells[x][y].gridloc = [x, y]
            cells[x][y].pixelloc = [x * 40, y * 40]

            if pix[x * 40, y * 40] == BLACK:
                cells[x][y].traversable = True
                cells[x][y].coin = True
            else:
                cells[x][y].traversable = False

    # Traps
    cells[3][3].trap = True
    cells[11][11].trap = True

    # Power-ups
    cells[7][1].powerup = True
    cells[7][13].powerup = True

    # Dynamic wall
    cells[7][7].dynamic = True
    cells[7][7].traversable = True
    cells[7][7].last_toggle_time = time.time()  # ← Add this line

    # Add 3 random obstacles
    obstacle_locations = []
    while len(obstacle_locations) < 3:
        x = random.randint(0, 14)
        y = random.randint(0, 14)
        if (x,y) not in [(7,13), (6,7), (7,7), (8,7), (3,3), (11,11), (7,1), (7,13)] and cells[x][y].traversable:
            cells[x][y].obstacle = True
            cells[x][y].traversable = False
            cells[x][y].coin = False
            obstacle_locations.append((x,y))

    return cells


def neighbors(loc, cells):
    x, y = loc
    dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    result = []
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 15 and 0 <= ny < 15 and cells[nx][ny].traversable:
            result.append((nx, ny))
    return result


def heuristic(loc1, loc2):
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])


def a_star(ghost, pac, cells):
    start = SearchNode(ghost.gridloc)
    target = pac.gridloc if not hasattr(pac, 'powered') or not pac.powered else [14 - pac.gridloc[0], 14 - pac.gridloc[1]]
    goal = SearchNode(target)
    open_list = [start]
    closed_set = set()

    while open_list:
        current = min(open_list, key=lambda node: node.f)
        open_list.remove(current)
        closed_set.add(tuple(current.gridloc))

        if current.gridloc == goal.gridloc:
            while current.parent and current.parent.parent:
                current = current.parent
            return current.gridloc, target, True

        for nx, ny in neighbors(current.gridloc, cells):
            if (nx, ny) in closed_set:
                continue
            neighbor = SearchNode([nx, ny])
            neighbor.parent = current
            neighbor.g = current.g + 1
            neighbor.f = neighbor.g + heuristic(neighbor.gridloc, goal.gridloc)

            if all(node.gridloc != neighbor.gridloc for node in open_list):
                open_list.append(neighbor)
    return ghost.gridloc, target, False


def bfs(ghost, pac, cells):
    fringe = [SearchNode(ghost.gridloc)]
    visited = set()

    while fringe:
        node = fringe.pop(0)
        if node.gridloc == pac.gridloc:
            while node.parent and node.parent.parent:
                node = node.parent
            return node.gridloc, pac.gridloc, True

        visited.add(tuple(node.gridloc))

        for nx, ny in neighbors(node.gridloc, cells):
            if (nx, ny) not in visited:
                neighborNode = SearchNode([nx, ny])
                neighborNode.parent = node
                fringe.append(neighborNode)
    return ghost.gridloc, pac.gridloc, False


def is_valid_move(pacman, cells, dx, dy):
    x, y = pacman.gridloc
    nx, ny = x + dx, y + dy
    return 0 <= nx < 15 and 0 <= ny < 15 and cells[nx][ny].traversable


def update_ghost_direction(ghost):
    dx = ghost.goal_cell[0] - ghost.gridloc[0]
    dy = ghost.goal_cell[1] - ghost.gridloc[1]
    if dx == 1:
        ghost.dir = 'r'
    elif dx == -1:
        ghost.dir = 'l'
    elif dy == 1:
        ghost.dir = 'd'
    elif dy == -1:
        ghost.dir = 'u'


def total_coins(cells):
    return sum(1 for row in cells for cell in row if cell.coin)


def draw_grid(screen, cells, coin_img):
    for x in range(15):
        for y in range(15):
            cell = cells[x][y]
            if cell.coin:
                screen.blit(coin_img, (x * 40, y * 40))


def draw_obstacles(screen, cells):
    for x in range(15):
        for y in range(15):
            if hasattr(cells[x][y], 'obstacle') and cells[x][y].obstacle:
                pygame.draw.rect(screen, (150, 75, 0), (x * 40, y * 40, 40, 40))
                pygame.draw.rect(screen, (100, 50, 0), (x * 40, y * 40, 40, 40), 2)


def check_collisions(pacman, ghosts):
    for ghost in ghosts:
        if pacman.gridloc == ghost.gridloc:
            return True
    return False
