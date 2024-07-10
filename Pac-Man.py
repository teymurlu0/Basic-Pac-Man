import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
MAZE_ROWS = HEIGHT // CELL_SIZE
MAZE_COLS = WIDTH // CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Generate random maze
def generate_maze():
    maze = []
    for row in range(MAZE_ROWS):
        if row == 0 or row == MAZE_ROWS - 1:
            maze.append('|' * MAZE_COLS)
        else:
            maze_row = '|'
            for col in range(1, MAZE_COLS - 1):
                if random.random() < 0.2:  # Adjust wall probability '|'
                    maze_row += '|'
                else:
                    maze_row += '.'
            maze_row += '|'
            maze.append(maze_row)
    return maze

# Initialize maze and enemies
maze = generate_maze()
player_x, player_y = WIDTH // 2, HEIGHT // 2
enemies = [{'row': random.randint(1, MAZE_ROWS-2), 'col': random.randint(1, MAZE_COLS-2), 'dx': 0, 'dy': 0} for _ in range(3)]
score = 0

# Screen settings
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman Maze")

# Collision detection function
def collision_check(player_x, player_y, enemies):
    for enemy in enemies:
        distance_sq = (player_x - (enemy['col'] * CELL_SIZE + CELL_SIZE // 2))**2 + (player_y - (enemy['row'] * CELL_SIZE + CELL_SIZE // 2))**2
        if distance_sq <= (CELL_SIZE // 2)**2:
            return True
    return False

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= 5
    elif keys[pygame.K_RIGHT]:
        player_x += 5
    elif keys[pygame.K_UP]:
        player_y -= 5
    elif keys[pygame.K_DOWN]:
        player_y += 5

    # Player boundaries check
    if player_x < 0:
        player_x = 0
    elif player_x >= WIDTH:
        player_x = WIDTH - 1
    if player_y < 0:
        player_y = 0
    elif player_y >= HEIGHT:
        player_y = HEIGHT - 1

    # Collect green dots and update score
    player_cell_x = player_x // CELL_SIZE
    player_cell_y = player_y // CELL_SIZE
    if maze[player_cell_y][player_cell_x] == '.':
        maze[player_cell_y] = maze[player_cell_y][:player_cell_x] + ' ' + maze[player_cell_y][player_cell_x+1:]
        score += 1

    # Draw maze
    for row in range(MAZE_ROWS):
        for col in range(MAZE_COLS):
            if maze[row][col] == '|':
                pygame.draw.rect(screen, WHITE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[row][col] == '.':
                pygame.draw.circle(screen, GREEN, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), 5)

    # Draw enemies (ghosts)
    for enemy in enemies:
        pygame.draw.circle(screen, RED, (enemy['col'] * CELL_SIZE + CELL_SIZE // 2, enemy['row'] * CELL_SIZE + CELL_SIZE // 2), 10)

    # Update enemies' positions randomly
    for enemy in enemies:
        if random.random() < 0.4:  # Adjust movement probability
            enemy['dx'] = random.choice([-1, 0, 1])
            enemy['dy'] = random.choice([-1, 0, 1])

        # Calculate new position
        new_row = enemy['row'] + enemy['dy']
        new_col = enemy['col'] + enemy['dx']

        # Check boundaries and walls
        if 0 <= new_row < MAZE_ROWS and 0 <= new_col < MAZE_COLS:
            if maze[new_row][new_col] == '.' or maze[new_row][new_col] == '|':
                enemy['row'] = new_row
                enemy['col'] = new_col

    # Collision check with enemies
    if collision_check(player_x, player_y, enemies):
        # Reset player position
        player_x, player_y = WIDTH // 2, HEIGHT // 2
        # Reset maze and enemies
        maze = generate_maze()
        enemies = [{'row': random.randint(1, MAZE_ROWS-2), 'col': random.randint(1, MAZE_COLS-2), 'dx': 0, 'dy': 0} for _ in range(3)]
        score = 0  # Reset score

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, YELLOW)
    screen.blit(score_text, (10, 10))

    # Show My Full Name for 5 seconds when score reaches 100
    if score >= 100:
        name_text = font.render("By Mahir Teymurlu", True, YELLOW)
        screen.blit(name_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(5000)  # Wait for 5 seconds
        score = 0  # Reset score after displaying name

    # Draw player
    pygame.draw.circle(screen, YELLOW, (player_x, player_y), 10)

    # Update screen
    pygame.display.flip()

    # Adjust frame rate
    pygame.time.Clock().tick(10)

# Quit Pygame
pygame.quit()
sys.exit()
