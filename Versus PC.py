import pygame
import QLearning
import numpy as np
import random
import time

def drawGrid():
    global screen
    blockSize = 300  # Set the size of the grid block
    for x in range(0, width, blockSize):
        for y in range(0, height, blockSize):
            rect = pygame.Rect(x, y,
                               blockSize, blockSize)
            pygame.draw.rect(screen, BLACK, rect, 1)

def available_spots(board):
    return np.array(np.where(board == 0)).T  # list of coordinates that don't have a symbol

def get_diag_winner(placed):
    diag1 = []
    diag2 = []
    for block, player in zip(placed.keys(), placed.values()):
        x, y = block
        if x + y != 1 or x + y != 3:
            if x == y:
                diag1.append(player)
            if x + y == 2:
                diag2.append(player)
    if (len(diag1) == 3 and len(set(diag1)) == 1):
        return True, diag1[0]
    elif (len(diag2) == 3 and len(set(diag2)) == 1):
        return True, diag2[0]
    return False, 'None'


def get_winner(placed):
    if not get_diag_winner(placed)[0]:
        X_count = [[0, 0], [0, 0], [0, 0]]
        O_count = [[0, 0], [0, 0], [0, 0]]
        for block, player in zip(placed.keys(), placed.values()):
            if player == 'X':
                x, y = block
                X_count[x][0] += 1
                X_count[y][1] += 1
            if player == 'O':
                x, y = block
                O_count[x][0] += 1
                O_count[y][1] += 1
        if max(sum(X_count, [])) >= 3:
            return True, 'X'
        elif max(sum(O_count, [])) >= 3:
            return True, 'O'
    else:
        return get_diag_winner(placed)
    return False, 'None'



# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

pygame.init()

# Set the width and height of the screen [width, height]
height = 900
width = 900
size = (height, width)
screen = pygame.display.set_mode(size)

font = pygame.font.Font('freesansbold.ttf', 64)

# create a rectangular object for the
# text surface object


pygame.display.set_caption("Tic Tac Toe")

screen.fill(WHITE)
drawGrid()

computer = QLearning.Agent("AI", exp_rate=0)
computer.loadPolicy("policy_Player1")
computer_board = np.zeros((3,3))
X = pygame.image.load('X.png')
O = pygame.image.load('O.png')
X = pygame.transform.smoothscale(X, (300, 300))
O = pygame.transform.smoothscale(O, (300, 300))
placed = {}
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
done = False
won = False
run = True
players = ['AI','Human']
pick = random.choice([0,1])
player_symbols = {'X': players.pop(pick), 'O': players.pop(0)}
turn = 'X'
printed_end = False
# -------- Main Program Loop -----------
while run:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if not won and not done:
            if player_symbols[turn] == 'AI':
                placeable = available_spots(computer_board)
                p1_action = computer.chooseAction(placeable, computer_board, 1)
                if p1_action is None:
                    done = True
                    break
                x,y = tuple(p1_action)
                computer_board[(x,y)] = 1
                placed[(x,y)] = turn
                screen.blit(X if turn == 'X' else O, (x * 300, y * 300))
                turn = 'O' if turn == 'X' else 'X'
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    x, y = x // 300, y // 300
                    if (x, y) not in placed:
                        computer_board[(x, y)] = -1
                        placed[(x, y)] = turn
                        screen.blit(O if turn == 'O' else X, (x * 300, y * 300))
                        turn = 'O' if turn == 'X' else 'X'
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                won = False
                done = False
                printed_end = False
                screen.fill(WHITE)
                drawGrid()
                placed = {}
                computer_board = np.zeros((3,3))
                turn = 'X'
                players = ['AI', 'Human']
                pick = random.choice([0, 1])
                player_symbols = {'X': players.pop(pick), 'O': players.pop(0)}
                print(player_symbols)
        # if done:
        #
        #     screen.fill(WHITE)
        #     drawGrid()
        #     placed = {}
        #     computer_board = np.zeros((3, 3))
        #     turn = 'X'
        #     players = ['AI', 'Human']
        #     pick = random.choice([0, 1])
        #     player_symbols = {'X': players.pop(pick), 'O': players.pop(0)}
    if len(placed.keys()) > 3 and not won and not done:
        won, winner = get_winner(placed)
    if won and not printed_end:
        vict = font.render(f'Game Over: {winner} won!', True, RED)
        textRect = vict.get_rect()
        textRect.center = (width // 2, height // 2)
        # screen.fill(WHITE)
        screen.blit(vict, textRect)
        printed_end = True

    if len(placed.keys()) == 9 and not won and not printed_end:
        done = True
        draw = font.render('Game Over: Draw', True, RED)
        textRect = draw.get_rect()
        textRect.center = (width // 2, height // 2)
        # screen.fill(WHITE)
        screen.blit(draw, textRect)
        printed_end = True
        # --- Game logic should go here

    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.

    # --- Drawing code should go here

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(10)

# Close the window and quit.
pygame.quit()
