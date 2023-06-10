# Thomas Stalmah
#
# Started 6/5/23
#
# class for playing a game

import numpy as np

class Game:
    def __init__(self, visual=False, board=None) -> None:
        self.visual = visual
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
        nums = np.array([2,2,2,2,2,2,2,2,2,4])
        np.random.shuffle(nums)
        self.board[poses[0]//4,poses[0]%4] = nums[0]
        np.random.shuffle(nums)
        self.board[poses[1]//4,poses[1]%4] = nums[0]

    # function to make a left move on the board
    def left(self) -> None:
        self.board = self.move(self.board)

    # function to make a right move on the board
    def right(self) -> None:
        self.board = np.flip(self.move(np.flip(self.board,1)),1)

    # function to make a up move on the board
    def up(self) -> None:
        self.board = self.move(self.board.T).T

    # function to make a down move on the board
    def down(self) -> None:
        self.board = np.flip(self.move(np.flip(self.board.T,1)),1).T

    # function that takes a 4x4 matrix and returns a
    # coresponding 4x4 matrix where a left move has been
    # made
    def move(self, board) -> np.ndarray:
        return np.array([self.shift(self.combine(self.shift(row)))
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

if __name__ == '__main__':
    game = Game(board=np.array([[0,2,0,2],
                                [0,0,0,0],
                                [0,2,4,0],
                                [0,0,0,0]]))
    print(game.board)
    game.down()
    print(game.board)

    