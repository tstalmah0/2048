# Thomas Stalmah
#
# Started 8/20/23
#
# class for testing game class and assosiated functions

import unittest as ut
from game import Game
import numpy as np

class Test_Game(ut.TestCase):

    # funnction for testing if Game.fill_init() adds 2 nunmbers
    def test_fill_init(self):
        game = Game()
        self.assertEqual(game.num_zeros, 14,
                         "Game init method should fill exactly " +
                         "2 spots with non zero numbers.")
        
    # function for testing if Game's move functions work as expected 
    # when no number is added and move is possiible
    def test_move_shift(self):
        game = Game(add_nums=False)

        # test for shifting number left
        game.set_board(np.array([[0,0,0,1],
                                 [0,0,0,0],
                                 [0,0,0,0],
                                 [0,0,0,0]]))
        game.left()
        left_correct = np.array([[1,0,0,0],
                                 [0,0,0,0],
                                 [0,0,0,0],
                                 [0,0,0,0]])
        self.assertTrue(game.compare_board(left_correct),
                        "Game failed to shift number left on no number " +
                        "added mode.")
        
        # test for shifting number right
        game.set_board(np.array([[1,0,0,0],
                                 [0,0,0,0],
                                 [0,0,0,0],
                                 [0,0,0,0]]))
        game.right()
        right_correct = np.array([[0,0,0,1],
                                  [0,0,0,0],
                                  [0,0,0,0],
                                  [0,0,0,0]])
        self.assertTrue(game.compare_board(right_correct),
                        "Game failed to shift number right on no number " +
                        "added mode.")
        
        # test for shifting number up
        game.set_board(np.array([[0,0,0,0],
                                 [0,0,0,0],
                                 [0,0,0,0],
                                 [1,0,0,0]]))
        game.up()
        up_correct = np.array([[1,0,0,0],
                               [0,0,0,0],
                               [0,0,0,0],
                               [0,0,0,0]])
        self.assertTrue(game.compare_board(up_correct),
                        "Game failed to shift number up on no number " +
                        "added mode.")
        
        # test for shifting number down
        game.set_board(np.array([[1,0,0,0],
                                 [0,0,0,0],
                                 [0,0,0,0],
                                 [0,0,0,0]]))
        game.down()
        down_correct = np.array([[0,0,0,0],
                                 [0,0,0,0],
                                 [0,0,0,0],
                                 [1,0,0,0]])
        self.assertTrue(game.compare_board(down_correct),
                        "Game failed to shift number down on no number " +
                        "added mode.")
        
if __name__ == '__main__':
    ut.main()