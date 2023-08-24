# Thomas Stalmah
#
# Started 6/5/23
#
# class for playing a game of 2048

import numpy as np
import pygame

class Game:
    def __init__(self,
                 visual=False,
                 board=None,
                 add_nums=True,
                 move_count=0,
                 print_mode_standard=True) -> None:
        self.visual = visual
        self.nums = np.array([2,2,2,2,2,2,2,2,2,4])
        self.add_nums = add_nums
        self.print_mode_standard = print_mode_standard
        self.move_dic = {}
        self.game_over = False
        self.move_count = move_count
        if board is not None:
            self.board = board
            self.num_zeros = self.count_zeros()
            self.update()
        else:
            self.board = np.zeros((4,4), dtype=int)
            self.num_zeros = 14
            self.fill_init()
            self.move_dic = {"Left":1,
                            "Right":1,
                            "Up":1,
                            "Down":1}
        
    # function to fill board with initial numbers
    def fill_init(self) -> None:
        poses = np.random.permutation(16)[:2]
        np.random.shuffle(self.nums)
        self.board[poses[0]//4,poses[0]%4] = self.nums[0]
        np.random.shuffle(self.nums)
        self.board[poses[1]//4,poses[1]%4] = self.nums[0]

    # function to make a left move on the board
    def left(self) -> None:
        if self.move_dic["Left"]:
            self.board = self.move(self.board)
            if self.add_nums:
                self.board = self.add_number(self.board)
            self.move_count += 1
            self.update()
            return True
        return False

    # function to make a right move on the board
    def right(self) -> bool:
        if self.move_dic["Right"]:
            self.board = np.flip(self.move(np.flip(self.board,1)),1)
            if self.add_nums:
                self.board = self.add_number(self.board)
            self.move_count += 1
            self.update()
            return True
        return False

    # function to make a up move on the board
    def up(self) -> None:
        if self.move_dic["Up"]:
            self.board = self.move(self.board.T).T
            if self.add_nums:
                self.board = self.add_number(self.board)
            self.move_count += 1
            self.update()
            return True
        return False

    # function to make a down move on the board
    def down(self) -> None:
        if self.move_dic["Down"]:
            self.board = np.flip(self.move(np.flip(self.board.T,1)),1).T
            if self.add_nums:
                self.board = self.add_number(self.board)
            self.move_count += 1
            self.update()
            return True
        return False
    
    # function to set board to a new board
    def set_board(self, board, move_count = None) -> None:
        self.board = board
        self.num_zeros = self.count_zeros()
        self.update()
        if move_count:
            self.move_count = move_count

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

    # function to check if left is an allowable move on the board passed
    def check_move(self, board) -> bool:
        for row in board:
            for (i,num) in enumerate(row[1:]):
                if num != 0:
                    if row[i] == 0:
                        return True
                    elif row[i] == num:
                        return True
        return False
    
    # function to update the move_dic to show what moves are possible
    def update_move_dic(self):
        self.move_dic["Left"] = 1 if self.check_move(self.board) else 0
        self.move_dic["Right"] = 1 if self.check_move(np.flip(self.board,1)) else 0
        self.move_dic["Up"] = 1 if self.check_move(self.board.T) else 0
        self.move_dic["Down"] = 1 if self.check_move(np.flip(self.board.T,1)) else 0

    # function for updating class between moves
    def update(self):
        self.update_move_dic()
        self.game_over = False if 1 in self.move_dic.values() else True

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
        self.num_zeros -= 1
        return board
    
    # function to compare self.board to the board that is passed
    def compare_board(self, board) -> bool:
        for row1,row2 in zip(self.board,board):
            for num1,num2 in zip(row1,row2):
                if num1 != num2:
                    return False
        return True
    
    # function to work as game loop
    def game_loop(self):
        # set up the pygame variables
        pygame.init()
        screen = pygame.display.set_mode((500,500))

        # set up local variables
        running = True

        # print the initial board
        self.print_board()
        print("moves:", str(self.move_count), sep=" ")

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
                        if self.left():
                            self.print_board()
                            print("moves:", str(self.move_count), sep=" ")
                            if self.game_over:
                                print("Game Over :(")
                                running = False
                    # check for pressing right arrow
                    elif event.key == pygame.K_RIGHT:
                        if self.right():
                            self.print_board()
                            print("moves:", str(self.move_count), sep=" ")
                            if self.game_over:
                                print("Game Over :(")
                                running = False
                    # check for pressing up arrow
                    elif event.key == pygame.K_UP:
                        if self.up():
                            self.print_board()
                            print("moves:", str(self.move_count), sep=" ")
                            if self.game_over:
                                print("Game Over :(")
                                running = False
                    # check for pressing down arrow
                    elif event.key == pygame.K_DOWN:
                        if self.down():
                            self.print_board()
                            print("moves:", str(self.move_count), sep=" ")
                            if self.game_over:
                                print("Game Over :(")
                                running = False


if __name__ == '__main__':
    game = Game(print_mode_standard=False)
    game.game_loop()

    