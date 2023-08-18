# Thomas Stalmah
#
# Started 6/5/23
#
# class for playing a game

import numpy as np
import pygame

class Game:
    def __init__(self,
                 visual=False,
                 board=None,
                 add_nums=True,
                 print_mode_standard=True) -> None:
        self.visual = visual
        self.nums = np.array([2,2,2,2,2,2,2,2,2,4])
        self.add_nums = add_nums
        self.print_mode_standard = print_mode_standard
        if board is not None:
            self.board = board
            self.num_zeros = self.count_zeros()
        else:
            self.board = np.zeros((4,4), dtype=int)
            self.num_zeros = 14
            self.fill_init()
        
    # function to fill board with initial numbers
    def fill_init(self) -> None:
        poses = np.random.permutation(16)[:2]
        np.random.shuffle(self.nums)
        self.board[poses[0]//4,poses[0]%4] = self.nums[0]
        np.random.shuffle(self.nums)
        self.board[poses[1]//4,poses[1]%4] = self.nums[0]

    # function to make a left move on the board
    def left(self) -> None:
        self.board = self.move(self.board)
        if self.add_nums:
            self.board = self.add_number(self.board)

    # function to make a right move on the board
    def right(self) -> None:
        self.board = self.add_number(np.flip(self.move(np.flip(self.board,1)),1))

    # function to make a up move on the board
    def up(self) -> None:
        self.board = self.add_number(self.move(self.board.T).T)

    # function to make a down move on the board
    def down(self) -> None:
        self.board = self.add_number(np.flip(self.move(np.flip(self.board.T,1)),1).T)

    # function that prints the board to the standard output
    def print_board(self) -> None:
        # standard print mode
        if self.print_mode_standard:
            print(self.board)
        # fancy print mode
        else:
            for row in self.board:
                for num in row:
                    out = "_" if num == 0 else str(int(np.log2(num)))
                    print(out, end="")
                print()

    # function that takes a 4x4 matrix and returns a
    # coresponding 4x4 matrix where a left move has been
    # made
    def move(self, board) -> np.ndarray:
        return np.array([
            self.shift(
            self.combine(
            self.shift(row)))
            for row in board])

    # function to shift the numbers of an array over any zeros
    def shift(self, arr) -> np.ndarray:
        ret = np.zeros(4, dtype=int)
        for num in reversed(arr):
            if num != 0:
                ret = np.append(ret, num)
        return np.flip(ret)[:4]
    
    # function to combine numbers that are the same and adjacent
    def combine(self, arr) -> np.ndarray:
        for i in range(3):
            if arr[i] == arr[i+1]:
                arr[i] = arr[i]*2
                arr[i+1] = 0
        return arr
    
    # function to count the number of zeros in the board
    def count_zeros(self) -> int:
        count = 0
        for row in self.board:
            for num in row:
                if num == 0:
                    count += 1
        return count
    
    # function to add a number to the board
    def add_number(self, board) -> np.ndarray:
        opens = []
        for (i,row) in enumerate(board):
            for (j,num) in enumerate(row):
                if num == 0:
                    opens.append((4*i)+j)
        np.random.shuffle(opens)
        np.random.shuffle(self.nums)
        board[opens[0]//4,opens[0]%4] = self.nums[0]
        return board
    
    # function to work as game loop
    def game_loop(self):
        # set up the pygame variables
        pygame.init()
        screen = pygame.display.set_mode((500,500))

        # set up local variables
        running = True
        move_count = 0

        # print the initial board
        self.print_board()
        print("moves:", str(move_count), sep=" ")

        # game loop
        while running:
            for event in pygame.event.get():
                # check for clicking the x on the window
                if event.type == pygame.QUIT:
                    print("quit")
                    running = False
                # check for key presses
                elif event.type == pygame.KEYDOWN:
                    # check for pressing escape
                    if event.key == pygame.K_ESCAPE:
                        print("esc")
                        running = False
                    # check for pressing left arrow
                    elif event.key == pygame.K_LEFT:
                        move_count += 1
                        self.left()
                        self.print_board()
                        print("moves:", str(move_count), sep=" ")
                    # check for pressing right arrow
                    elif event.key == pygame.K_RIGHT:
                        move_count += 1
                        self.right()
                        self.print_board()
                        print("moves:", str(move_count), sep=" ")
                    # check for pressing up arrow
                    elif event.key == pygame.K_UP:
                        move_count += 1
                        self.up()
                        self.print_board()
                        print("moves:", str(move_count), sep=" ")
                    # check for pressing down arrow
                    elif event.key == pygame.K_DOWN:
                        move_count += 1
                        self.down()
                        self.print_board()
                        print("moves:", str(move_count), sep=" ")


if __name__ == '__main__':
    game = Game(print_mode_standard=False)
    game.game_loop()

    