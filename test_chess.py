import unittest
import src.module
from src.pieces import *

class TestChess(unittest.TestCase):

    def test_pawn_1step(self):
        m = src.module.Module()
        m.moveCheck(m.gb.get((1,2)),(1,4))
        p = m.gb.get((1,4))
        square = m.gb.get((1,2))
        correct = src.pieces.Pawn(1,(1,4))
        self.assertEqual(square,0,"Pawn shouldn't be in square where it left")
        self.assertEqual(p.character(),correct.character(), "Should be a pawn")
        self.assertEqual(p.getTeam(),correct.getTeam(), "Should be a white")


if __name__ == "__main__":
    unittest.main()