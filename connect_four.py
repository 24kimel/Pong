import numpy as np
import math
import pygame
import sys
import pyautogui

# colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

PLAYER_COLORS = (RED, YELLOW)

# array manipulation
NUM_ROWS = 6
NUM_COLS = 7
OFFSET = 3

# design
GUI_OFFSET = 5
TIME_AFTER_WIN = 3000


def create_board():
    board = np.zeros((NUM_ROWS, NUM_COLS))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[NUM_ROWS-1][col] == 0


def get_next_open_row(board, col):
    for row in range(NUM_ROWS):
        if board[row][col] == 0:
            return row


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # brute force
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            # horizontal win
            if c + OFFSET < NUM_COLS and board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r][c + 3] == piece:
                return True
            # vertical win
            if r + OFFSET < NUM_ROWS and board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c] == piece:
                return True
            # negative slope win
            if r + OFFSET < NUM_ROWS and c + OFFSET < NUM_COLS:
                if board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == board[r + 3][c + 3] == piece:
                    return True
            # positive slope win
            if r - OFFSET >= 0 and c + OFFSET < NUM_COLS:
                if board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == board[r - 3][c + 3] == piece:
                    return True
    return False


def draw_board(board):
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZ, (r + 1) * SQUARE_SIZ, SQUARE_SIZ, SQUARE_SIZ))
            pygame.draw.circle(screen, BLACK, (int((c + 1 / 2) * SQUARE_SIZ), int((r + 3 / 2) * SQUARE_SIZ)), RADIUS)

    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int((c + 1/2) * SQUARE_SIZ), height - ((r + 1/2) * SQUARE_SIZ)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int((c + 1/2) * SQUARE_SIZ), height - int((r + 1/2) * SQUARE_SIZ)), RADIUS)
            elif board[r][c] != 0:
                print('System error [invalid value in array]')
                sys.exit()
    pygame.display.update()


_board = create_board()
game_over = False
turn = 0


SQUARE_SIZ = 100
width = NUM_COLS * SQUARE_SIZ
# extra space at the top
height = (NUM_ROWS + 1) * SQUARE_SIZ
# desired screen size
size = (width, height)
# monitor size
m_width, m_height = pyautogui.size()
# desired circle slot radius
RADIUS = int(SQUARE_SIZ / 2 - GUI_OFFSET)

# checking that we can fit this screen into our monitor
if m_width < width or m_height < height:
    print('Too many squares for this monitor')
    exit(69420)

pygame.init()
screen = pygame.display.set_mode(size)
draw_board(_board)
pygame.display.update()

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZ))
            hoverXPos = event.pos[0]
            pygame.draw.circle(screen, PLAYER_COLORS[turn], (hoverXPos, int(SQUARE_SIZ / 2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseXPos = event.pos[0]
            # check for the column the mouse is pointing at
            curr_col = int(math.floor(mouseXPos / SQUARE_SIZ))
            if is_valid_location(_board, curr_col):
                curr_row = get_next_open_row(_board, curr_col)
                drop_piece(_board, curr_row, curr_col, turn + 1)
                if winning_move(_board, turn + 1):
                    game_over = True

                draw_board(_board)
                turn = (turn + 1) % 2

pygame.time.wait(TIME_AFTER_WIN)
