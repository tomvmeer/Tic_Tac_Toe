import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

pygame.init()

class Game:

    def __init__(self, player1, player2):
        p1 = player1
        p2 = player2
        self.height = 900
        self.width = 900
        self.size = (self.height, self.width)
        self.screen = pygame.display.set_mode(self.size)

        self.font = pygame.font.Font('freesansbold.ttf', 64)

        # create a rectangular object for the
        # text surface object

        pygame.display.set_caption("Tic Tac Toe")

        self.screen.fill(WHITE)
        self.drawGrid()
        # Loop until the user clicks the close button.
        run = True
        X = pygame.image.load('X.png')
        O = pygame.image.load('O.png')
        self.blockSize = self.height/3
        self.X = pygame.transform.smoothscale(X, (self.height/3, self.width/3))
        self.O = pygame.transform.smoothscale(O, (self.height/3, self.width/3))
        self.placed = {}
        self.turn = 0
        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()
        self.done = False
        self.won = False

    def drawGrid(self):
          # Set the size of the grid block
        for x in range(0, self.width, self.blockSize):
            for y in range(0, self.height, self.blockSize):
                rect = pygame.Rect(x, y,
                                   self.blockSize, self.blockSize)
                pygame.draw.rect(self.screen, BLACK, rect, 1)

    def get_diag_winner(self):
        diag1 = []
        diag2 = []
        for block, player in zip(self.placed.keys(), self.placed.values()):
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

    def get_winner(self):
        print(self.get_diag_winner()[0])
        if not self.get_diag_winner()[0]:
            X_count = [[0, 0], [0, 0], [0, 0]]
            O_count = [[0, 0], [0, 0], [0, 0]]
            for block, player in zip(self.placed.keys(), self.placed.values()):
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
            return self.get_diag_winner()
        return False, 'None'

    def play_v_human(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                x, y = x // 300, y // 300
                if self.turn % 2 == 0:
                    if (x, y) not in self.placed:
                        self.placed[(x, y)] = 'X'
                        self.screen.blit(self.X, (x * 300, y * 300))
                        self.turn += 1
                        print(self.placed)
                else:
                    if (x, y) not in self.placed:
                        self.placed[(x, y)] = 'O'
                        self.screen.blit(self.O, (x * 300, y * 300))
                        self.turn += 1
                        print(self.placed)
                if self.won:
                    self.won = False
                    self.screen.fill(WHITE)
                    self.drawGrid()
                    self.placed = {}
                    self.turn = 0
                if self.done:
                    self.done = False
                    self.screen.fill(WHITE)
                    self.drawGrid()
                    self.placed = {}
                    self.turn = 0
        if len(self.placed.keys()) > 3:
            self.won, winner = self.get_winner(self.placed)
        if self.won:
            vict = self.font.render(f'Game Over: {winner} won!', True, WHITE, BLUE)
            textRect = vict.get_rect()
            textRect.center = (self.width // 2, self.height // 2)
            self.screen.fill(WHITE)
            self.screen.blit(vict, textRect)

        if len(self.placed.keys()) == 9 and not self.won:
            self.done = True
            draw = self.font.render('Game Over: Draw', True, RED, BLUE)
            textRect = draw.get_rect()
            textRect.center = (self.width // 2, self.height // 2)
            self.screen.fill(WHITE)
            self.screen.blit(draw, textRect)
