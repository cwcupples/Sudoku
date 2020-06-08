"""This is the Sudoku version that builds off of the text one. It creates a GUI, instead of just text based.
    This is the second version. It has 5 lives, and a screen that lets you know if you won at the end.
    User gets to choose between 3 different difficulties. User can change selected cube using arrow keys too.
    I couldn't get the solve_game() function to work corredtly and it was very slow. Not sure why
    I think the problem is the pygame.display.update()"""
import pygame
from Sudoku.Sudoku_solver import solve, valid, solvable, find_empty


# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
# Sizes
SCREEN_X = SCREEN_Y = 600
BOTTOM = 50
THICK = 5
THIN = 2
BOX = (SCREEN_X - 4 * THICK - 6 * THIN) / 9
# start the game
pygame.init()
pygame.font.init()
pygame.display.set_caption("Sudoku")
CLOCK = pygame.time.Clock()
WIN = pygame.display.set_mode([SCREEN_X, SCREEN_Y + BOTTOM])


class Board:
    """Board class to store the 2D list that is used and the cubes that are used"""
    def __init__(self, rows, cols, board, screen):
        """Initialize the whole thing"""
        self.game = board
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.game[i][j], i, j) for j in range(cols)] for i in range(rows)]
        self.selected = None
        self.screen = screen
        self.solved = False
        self.lost = False
        self.lives = 5

    def place(self):
        """Method to update the board with a correct value"""
        # make sure that we have a cube selected
        if self.selected is not None:
            row, col = self.selected
            # make sure that it is a value that we can update
            if self.cubes[row][col].value == 0 and self.cubes[row][col].temp != 0:
                self.game[row][col] = self.cubes[row][col].temp
                if solvable(self.game):
                    # This means the player has made a valid move and the board can still be solved
                    self.cubes[row][col].set()
                else:
                    # Sorry bud, that didn't work
                    self.cubes[row][col].temp = 0
                    self.game[row][col] = 0
                    self.lives -= 1

    def temp(self, value):
        """Method to update the board with the temporary value"""
        if self.selected is not None:
            row, col = self.selected
            if self.cubes[row][col].value == 0:
                self.cubes[row][col].temp_set(value)

    def delete(self):
        """Method to clear the temp value in the space"""
        if self.selected is not None:
            row, col = self.selected
            self.cubes[row][col].temp = 0

    def draw_board(self):
        """Method to draw the board out on the screen"""
        self.screen.fill(WHITE)
        # these loops draw the grid lines
        for i in range(4):
            coordinate = i * (THICK + 2 * THIN + 3 * BOX) + THICK / 2
            pygame.draw.lines(self.screen, BLACK, False, [(coordinate, 0), (coordinate, SCREEN_X)], THICK)
            pygame.draw.lines(self.screen, BLACK, False, [(0, coordinate), (SCREEN_Y, coordinate)], THICK)
            for t in range(2):
                coordinate2 = coordinate + THICK / 2 + (t + 1) * BOX + (1 + 2 * t) * (THIN / 2)
                pygame.draw.lines(self.screen, BLACK, False, [(coordinate2, 0), (coordinate2, SCREEN_X)], THIN)
                pygame.draw.lines(self.screen, BLACK, False, [(0, coordinate2), (SCREEN_Y, coordinate2)], THIN)
        # now fill in the actual numbers
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.screen)

    def select(self, row, col):
        """Highlight a box"""
        if -1 < row < 9 and -1 < col < 9:
            if self.selected is not None:
                self.cubes[self.selected[0]][self.selected[1]].selected = False
            self.selected = row, col
            self.cubes[self.selected[0]][self.selected[1]].selected = True

    def move_arrow(self, x, y):
        row, col = self.selected
        self.select(row + y, col + x)

    def solve_game(self):
        """Press space bar to solve the board ya cheater"""
        pos = find_empty(self.game)
        if not pos:
            return True
        row, col = pos
        for i in range(1, 10):
            if valid(self.game, row, col, i):
                self.game[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.screen, True)
                # print("update", pos, i)
                pygame.display.flip()

                if self.solve_game():
                    return True

                self.cubes[row][col].set(0)
                self.cubes[row][col].draw_change(self.screen, False)
                pygame.display.update()
            self.game[row][col] = 0
        return False

    def solve(self):
        """Press space bar to solve the board ya cheater"""
        solve(self.game)
        for row in range(self.rows):
            for col in range(self.cols):
                self.cubes[row][col].value = self.game[row][col]

    def finished(self):
        """Method to determine if the game has been finished by solving"""
        if not find_empty(self.game):
            self.solved = True
        else:
            self.solved = False

    def strikes(self):
        """Let's draw the strikes at the bottom of the screen"""
        if self.lives <= 0:
            self.lost = True
        size = 20
        font = pygame.font.Font('freesansbold.ttf', size)
        pygame.draw.rect(self.screen, WHITE, [0, SCREEN_Y, SCREEN_X, BOTTOM], 0)
        for i in range(self.lives):
            message = font.render("X", True, RED)
            message_rect = message.get_rect()
            message_rect.center = (size + i * size, SCREEN_Y + BOTTOM // 2)
            WIN.blit(message, message_rect)


class Cube:
    """Cube is how we will keep track of where all the numbers are"""
    def __init__(self, value, row, col):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.selected = False

    def set(self, val=-1):
        """"Method to set the value stored in the cube"""
        if val == -1:
            val = self.temp
        self.value = val
        self.temp = 0

    def temp_set(self, value):
        """Method to set the temp value stored in the cube"""
        self.temp = value

    def draw(self, screen):
        """Method to draw the value stored in the cube on screen"""
        font = pygame.font.Font('freesansbold.ttf', 30)
        # get the x and y coordinates of where to put the number on the screen
        x = int(THICK * ((self.col // 3) + 1) + BOX * self.col + THIN * (self.col - (self.col // 3)))
        y = int(THICK * ((self.row // 3) + 1) + BOX * self.row + THIN * (self.row - (self.row // 3)))
        # write the temp value in grey
        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), True, GREY)
            screen.blit(text, (x + 5, y + 5))
        # write the actual value in the square in black, temp value gets removed
        elif self.value != 0:
            text = font.render(str(self.value), True, BLACK)
            screen.blit(text, (x + BOX / 3 + 2, y + BOX / 3 - 1))
        # highlight the selected box
        if self.selected:
            pygame.draw.rect(screen, RED, (x, y, BOX + 1, BOX + 1), THIN)

    def draw_change(self, screen, good=True):
        """Method to draw the change in the solving function"""
        font = pygame.font.Font('freesansbold.ttf', 30)
        # get the x and y coordinates of where to put the number on the screen
        x = int(THICK * ((self.col // 3) + 1) + BOX * self.col + THIN * (self.col - (self.col // 3)))
        y = int(THICK * ((self.row // 3) + 1) + BOX * self.row + THIN * (self.row - (self.row // 3)))

        pygame.draw.rect(screen, WHITE, (x, y, BOX, BOX))

        text = font.render(str(self.value), True, BLACK)
        screen.blit(text, (x + BOX / 3 + 2, y + BOX / 3 - 1))

        if good:
            # if the cube is valid, highlight in green
            pygame.draw.rect(screen, GREEN, (x, y, BOX + 1, BOX + 1), THIN)
        else:
            # invalid, so highlight in red
            pygame.draw.rect(screen, RED, (x, y, BOX + 1, BOX + 1), THIN)


def welcome(font, mode=None):
    WIN.fill(BLACK)
    text = ["Easy", "Medium", "Hard"]
    for i in range(len(text)):
        word = font.render(text[i], True, WHITE)
        word_rect = word.get_rect()
        word_rect.center = (SCREEN_X // 3 * i + SCREEN_X // 6, SCREEN_Y // 2)
        WIN.blit(word, word_rect)
    pygame.display.update()
    while not mode:
        for event in pygame.event.get():  # User did something
            # get row and column of the piece to move
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x1 = SCREEN_X // 3
                x2 = 2 * x1
                if pos[0] < x1:
                    mode = easy
                elif pos[0] < x2:
                    mode = medium
                else:
                    mode = hard
            if event.type == pygame.QUIT:  # If user clicked close
                quit()
    return mode


"""" 
# pygame.draw.rect(surface, color, [x, y, w, l])
# pygame.draw.lines(surface, color, closed=false (or true), [points list], thickness)
"""

# here is our game board
grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
easy = [
    [5, 0, 1, 0, 4, 3, 8, 9, 0],
    [3, 0, 0, 8, 5, 7, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 7, 3, 0],
    [8, 0, 0, 0, 0, 0, 0, 0, 2],
    [0, 6, 3, 0, 0, 0, 0, 0, 5],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 2, 4, 0, 0, 6],
    [0, 4, 8, 7, 9, 0, 3, 0, 1]
]
medium = [
    [0, 4, 0, 0, 2, 0, 8, 7, 0],
    [6, 0, 7, 0, 0, 0, 0, 0, 0],
    [0, 0, 8, 0, 7, 4, 0, 0, 0],
    [9, 3, 0, 0, 0, 8, 4, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 2, 4, 0, 0, 0, 5, 3],
    [0, 0, 0, 7, 8, 0, 3, 0, 0],
    [0, 0, 0, 0, 0, 0, 7, 0, 9],
    [0, 2, 1, 0, 3, 0, 0, 8, 0]
]
hard = [
    [0, 0, 0, 7, 3, 0, 0, 6, 8],
    [0, 0, 0, 4, 0, 8, 0, 9, 1],
    [0, 7, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 6, 0, 0, 0, 0, 3, 2],
    [0, 8, 0, 0, 0, 0, 0, 5, 0],
    [7, 2, 0, 0, 0, 0, 6, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 0],
    [2, 5, 0, 9, 0, 3, 0, 0, 0],
    [6, 9, 0, 0, 1, 7, 0, 0, 0]
]


# this is the overall function that will run the code
def main():
    font = pygame.font.Font('freesansbold.ttf', 30)
    mode = welcome(font)
    run = True
    space = False
    lost = False
    game = Board(9, 9, mode, WIN)
    game.draw_board()
    while run:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                run = False
                quit()
            if event.type == pygame.KEYDOWN:
                # this first elif chain sets the key for the temp value
                if event.key == pygame.K_1:
                    key = 1
                elif event.key == pygame.K_2:
                    key = 2
                elif event.key == pygame.K_3:
                    key = 3
                elif event.key == pygame.K_4:
                    key = 4
                elif event.key == pygame.K_5:
                    key = 5
                elif event.key == pygame.K_6:
                    key = 6
                elif event.key == pygame.K_7:
                    key = 7
                elif event.key == pygame.K_8:
                    key = 8
                elif event.key == pygame.K_9:
                    key = 9
                else:
                    key = 0
                if event.key == pygame.K_UP:
                    game.move_arrow(0, -1)
                if event.key == pygame.K_DOWN:
                    game.move_arrow(0, 1)
                if event.key == pygame.K_LEFT:
                    game.move_arrow(-1, 0)
                if event.key == pygame.K_RIGHT:
                    game.move_arrow(1, 0)
                # here we actually set the temp value
                if key != 0:
                    game.temp(key)
                # make the temp value the set value (if it is valid)
                if event.key == pygame.K_RETURN:
                    game.place()
                # remove the temp value
                if event.key == pygame.K_BACKSPACE:
                    game.delete()
                # rage quit
                if event.key == pygame.K_SPACE:
                    game.solve()
                    space = True

            # detect mouse and find the correct square
            if event.type == pygame.MOUSEBUTTONDOWN:
                denominator = THICK/3 + BOX + THIN - THIN/3
                position = pygame.mouse.get_pos()
                row = int((position[1] - THICK) / denominator)
                col = int((position[0] - THICK) / denominator)
                game.select(row, col)

        # Here we see if the game has been finished
        game.finished()
        if game.solved:
            pygame.time.delay(100)
            run = False
        if game.lost:
            lost = True
            pygame.time.delay(100)
            run = False

        game.draw_board()
        game.strikes()
        # update the display
        pygame.display.flip()
    if not space and not lost:
        text = "Congrats you won!"
    elif lost:
        text = "Sorry, you lost :("
    else:
        text = "Congrats I solved it for you."
    message = font.render(text, True, WHITE, BLACK)
    message_rect = message.get_rect()
    message_rect.center = (SCREEN_X // 2, SCREEN_Y // 2)
    WIN.blit(message, message_rect)
    pygame.display.flip()    # Loop so game doesn't end until they click
    done = False
    while not done:
        for event in pygame.event.get():  # User did something
            # get row and column of the piece to move
            if event.type == pygame.MOUSEBUTTONDOWN:
                done = True
            if event.type == pygame.QUIT:  # If user clicked close
                done = True


main()
quit()
