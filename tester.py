# Thomas Stalmah
#
# Started 8/20/23
#
# class for testing game class and assosiated functions

import unittest as ut
from game import Game

class Test_Game(ut.TestCase):

    # funnction for testing if Game.fill_init() adds 2 nunmbers
    def test_fill_init(self):
        game = Game()
        self.assertEqual(game.num_zeros, 14,
                         "Game init method should fill exactly " +
                         "2 spots with non zero numbers.")
        
if __name__ == '__main__':
    ut.main()