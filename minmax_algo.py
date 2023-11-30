import pygame
import sys
import time
import copy

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
LINE_COLOR = (0, 0, 0)
CIRCLE_COLOR = (255, 0, 100)
CROSS_COLOR = (100, 0, 255)
LINE_WIDTH = 15
FONT_SIZE = 50
FONT_COLOR = (100, 50, 0)
CIRCULAR_BG_COLOR = (250, 205, 155)

# Initialize the game board
board = [[' ' for _ in range(3)] for _ in range(3)]

# Initialize Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill((155, 255, 205))

# Pygame font
font = pygame.font.Font(None, FONT_SIZE)

# Draw the Tic Tac Toe grid
def draw_grid():
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, i * HEIGHT / 3), (WIDTH, i * HEIGHT / 3), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * WIDTH / 3, 0), (i * WIDTH / 3, HEIGHT), LINE_WIDTH)

# Draw X
# Draw X
def draw_x(row, col):
    x_pos = col * WIDTH / 3 + WIDTH / 6
    y_pos = row * HEIGHT / 3 + HEIGHT / 6
    pygame.draw.ellipse(screen, CIRCULAR_BG_COLOR, (x_pos - 55, y_pos - 55, 110, 110))
    pygame.draw.line(screen, CROSS_COLOR, (x_pos - 30, y_pos - 30), (x_pos + 30, y_pos + 30), LINE_WIDTH)
    pygame.draw.line(screen, CROSS_COLOR, (x_pos + 30, y_pos - 30), (x_pos - 30, y_pos + 30), LINE_WIDTH)

# Draw O
def draw_o(row, col):
    o_pos = (int(col * WIDTH / 3 + WIDTH / 6), int(row * HEIGHT / 3 + HEIGHT / 6))
    pygame.draw.ellipse(screen, CIRCULAR_BG_COLOR, (o_pos[0] - 55, o_pos[1] - 55, 110, 110))
    pygame.draw.circle(screen, CIRCLE_COLOR, o_pos, 50, LINE_WIDTH)

# Check for a winner
def check_winner():
    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != ' ':
            return board[row][0]

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]

    return None

# Check if the board is full
def is_board_full():
    for row in board:
        if ' ' in row:
            return False
    return True

# Minimax algorithm for the computer's move
def minimax(board, depth, maximizing_player):
    winner = check_winner()

    if winner == 'X':
        return -1
    elif winner == 'O':
        return 1
    elif is_board_full():
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
        return min_eval

# Get the computer's move using minimax
def get_computer_move():
    best_move = None
    best_eval = float('-inf')
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                eval = minimax(board, 0, False)
                board[i][j] = ' '
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)
    return best_move

# Display the winner and restart option
def display_result(result):
    text = font.render(result, True, FONT_COLOR)
    screen.blit(text, (WIDTH // 2 - FONT_SIZE * 2, HEIGHT // 2 - FONT_SIZE))
    pygame.display.update()
    pygame.time.delay(2000)  # Delay for 2 seconds
    restart_game()

# Restart the game
def restart_game():
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    screen.fill((255, 255, 255))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            clicked_row = int(mouseY // (HEIGHT / 3))
            clicked_col = int(mouseX // (WIDTH / 3))

            if board[clicked_row][clicked_col] == ' ' and check_winner() is None:
                board[clicked_row][clicked_col] = 'X'
                draw_x(clicked_row, clicked_col)

                winner = check_winner()
                if winner:
                    display_result(f'{winner} wins!')
                elif not is_board_full():
                    computer_move = get_computer_move()
                    board[computer_move[0]][computer_move[1]] = 'O'
                    draw_o(computer_move[0], computer_move[1])

                    winner = check_winner()
                    if winner:
                        display_result(f'{winner} wins!')
                    elif is_board_full():
                        display_result("It's a draw!")

    draw_grid()
    pygame.display.update()


