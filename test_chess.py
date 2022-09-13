import unittest
import src.module
from src.pieces import *

class TestChess(unittest.TestCase):

    def test_pawn_1step(self):
        m = src.module.Module()
        m.moveCheck(m.gb.get((1,2)),(1,4))
        p = m.gb.get((1,4))
        square = m.gb.get((1,2))
        correct = Pawn(1,(1,4))
        self.assertEqual(square,0,"White Pawn shouldn't be in square where it left")
        self.assertEqual(p.character(),correct.character(), "Should be a pawn")
        self.assertEqual(p.getTeam(),correct.getTeam(), "Should be a white")
        pawn = Pawn(2,(3,3))
        m.gb.set((3,3),pawn)
        

    def test_pawn_move_ally(self):
        m = src.module.Module()
        m.gb.set((1,3), Knight(1,(1,3)))
        pawn = m.gb.get((1,2))
        knight = m.gb.get((1,3))
        m.moveCheck(m.gb.get((1,2)), (1,3))
        self.assertEqual(m.gb.get((1,2)), pawn, "Pawn should not move")
        self.assertEqual(m.gb.get((1,3)), knight, "Knight should not be replaced")

    def test_pawn_capture(self):
        m = src.module.Module()
        pawn = Pawn(1,(3,3))

if __name__ == "__main__":
    unittest.main()