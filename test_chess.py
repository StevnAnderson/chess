import unittest
import src.module
from src.pieces import *

class TestChess(unittest.TestCase):

    def test_Wpawn_1step(self):
        m = src.module.Module()
        pawn = m.get((1,2))
        m.moveCheck((1,2),(1,3))
        self.assertEqual(m.get((1,2)),0,"White Pawn shouldn't be in square where it left")
        self.assertEqual(m.get((1,3)),pawn, "Pawn should have moved")
        
    def test_Bpawn_1step(self):
        m = src.module.Module()
        pawn = m.get((1,7))
        m.moveCheck((1,7),(1,6))
        self.assertEqual(m.get((1,7)),0,"White Pawn shouldn't be in square where it left")
        self.assertEqual(m.get((1,6)),pawn, "Pawn should have moved")

    def test_Bpawn_move_ally(self):
        m = src.module.Module() #Move on ally
        knight = Knight(m.genID(), 2,(1,6))
        pawn = m.get((1,7))
        m.set((1,6), knight)
        m.moveCheck((1,7), (1,6))
        try:
            self.assertEqual(m.get((1,7)), pawn, "A7 to A6 shouldn't move the pawn")
            self.assertEqual(m.get((1,6)), knight, "A7 to A6 should not replace the knight")
        except AssertionError:
            m.display()
            raise

        m = src.module.Module() #Move through ally
        knight = Knight(m.genID(), 2,(1,6))
        pawn = Pawn(m.genID(), 2,(1,7))
        m.set((1,6), knight)
        m.set((1,7), pawn)
        m.save("A7-A5")
        m.moveCheck((1,7), (1,5))
        try:
            self.assertEqual(m.get((1,7)), pawn, "Pawn should not move")
            self.assertEqual(m.get((1,6)), knight, "Knight should not be replaced")
            self.assertEqual(m.get((1,5)),0,"Pawn should not move through allied pieces")

        except AssertionError:
            m.load("A7-A5")
            m.display()
            raise

        m = src.module.Module() #Attack ally
        knight = Knight(m.genID(), 2,(2,6))
        pawn = m.get((1,7))
        m.gb.set((2,6), knight)
        m.gb.set((1,7), pawn)
        m.moveCheck((1,7), (2,6))
        self.assertEqual(m.get((1,7)), pawn, "Pawn should not move")
        self.assertEqual(m.get((2,6)), knight, "Knight should not be replaced")

    def test_Wpawn_ally(self):
        m = src.module.Module() #Move on ally
        knight = Knight(m.genID(), 1,(1,3))
        pawn = Pawn(m.genID(), 1,(1,2))
        m.gb.set((1,3), knight)
        m.gb.set((1,2), pawn)
        m.moveCheck((1,2), (1,3))
        self.assertEqual(m.get((1,2)), pawn, "Pawn should not move")
        self.assertEqual(m.get((1,3)), knight, "Knight should not be replaced")

        m = src.module.Module() #Move through ally
        knight = Knight(m.genID(), 1,(1,3))
        pawn = Pawn(m.genID(), 1,(1,2))
        m.set((1,3), knight)
        m.set((1,2), pawn)
        m.moveCheck((1,2), (1,4))
        self.assertEqual(m.get((1,2)), pawn, "Pawn should not move")
        self.assertEqual(m.get((1,3)), knight, "Knight should not be replaced")
        self.assertEqual(m.get((1,4)),0,"Pawn should not move through allied pieces")

        m = src.module.Module() #Attack ally
        knight = Knight(m.genID(), 1,(2,3))
        pawn = Pawn(m.genID(), 1,(1,2))
        m.set((2,3), knight)
        m.set((1,2), pawn)
        m.moveCheck((1,2), (2,3))
        self.assertEqual(m.get((1,2)), pawn, "Pawn should not move")
        self.assertEqual(m.get((2,3)), knight, "Knight should not be replaced")

    def test_Wpawn_capture(self):
        m = src.module.Module()
        pawn = Pawn(m.genID(), 1,(3,3))
        rook = Rook(m.genID(), 2,(4,4))
        m.set((3,3),pawn)
        m.set((4,4), rook)
        m.moveCheck((3,3),(4,4))
        self.assertEqual(m.get((3,3)),0,"After attacking, pawn should have moved")

    def test_Wrook_movementY(self):
        m = src.module.Module()
        rook = Rook(m.genID(), 1,(1,1))
        m.set((1,2),0)
        m.set((1,1),rook)
        move = "A1-A4"
        m.moveCheck((1,1),(1,4))
        try:
            self.assertEqual(m.get((1,4)), rook, "Rook should have moved here")
            self.assertEqual(m.get((1,1)), 0, "Rook should have left square")
        except AssertionError as e:
            print("\n", move, e)
            m.display()
            raise

    def test_Wrook_movementX(self):
        m = src.module.Module()
        rook = Rook(m.genID(), 1,(1,4))
        m.set((1,4), rook)
        m.moveCheck((1,4),(4,4))
        self.assertEqual(m.get((4,4)), rook, "Rook should have moved here")
        self.assertEqual(m.get((1,4)), 0, "Rook should have left square")

    def test_Wrook_capture(self):
        m = src.module.Module()
        rook = Rook(m.genID(), 1,(1,4))
        knight = Knight(m.genID(), 2,(8,4))
        m.set((1,4), rook)
        m.set((8,4), knight)
        move = "A4-H4"
        m.save(move)
        m.moveCheck((1,4), (8,4))
        try:
            self.assertEqual(m.get((8,4)), rook, "Rook should have captured")
            self.assertEqual(m.get((1,4)), 0, "Rook should have left the square")
        except AssertionError as e:
            print("\n\n")
            m.display()
            print("\n", move, e)
            m.load(move)
            m.display()
            raise

    def test_Wrook_jump(self):
        m = src.module.Module()
        rook = Rook(m.genID(), 1, (1,4))
        knight = Knight(m.genID(), 2, (8,4))
        Bbishop = Bishop(m.genID(), 2, (4,4))
        Wbishop = Bishop(m.genID(), 1, (5,4))
        m.set((1,4), rook)
        m.set((8,4), knight)
        m.set((4,4), Bbishop)
        m.set((5,4), Wbishop)
        move = "A4-A8"
        m.moveCheck((1,4), (8,4))
        try:
            self.assertEqual(m.get((1,4)), rook, "Rook be here, should have been stopped")
            self.assertEqual(m.get((5,4)), Wbishop, "Rook shouldn't have moved it's ally")
            self.assertEqual(m.get((4,4)), Bbishop, "Rook shouldn't not move a piece by jumping it")
            self.assertEqual(m.get((8,4)), knight, "Rook shouldn't be able to jump pieces")
        except AssertionError as e:
            print("\n", move, e)
            m.display()
            raise

    def test_Wrook_ally(self):
        m = src.module.Module()
        rook = Rook(m.genID(), 1,(1,4))
        knight = Knight(m.genID(), 1,(1,5))
        m.set((1,4), rook)
        m.set((1,5), knight)
        m.moveCheck((1,4), (1,5))
        self.assertEqual(m.get((1,4)), rook, "Rook should not have moved when attacking ally")
        self.assertEqual(m.get((1,5)), knight, "Rook shouldn't capture ally")

    def test_Brook_movementY(self):
        m = src.module.Module()
        rook = Rook(m.genID(), 2,(1,8))
        m.set((1,7),0)
        m.set((1,8),rook)
        move = "A8-A4"
        m.save(move)
        m.moveCheck((1,8),(1,4))
        try:
            self.assertEqual(m.get((1,4)).getID(), rook.getID(), move+" Rook should be at A4")
        except AssertionError as e:
            m.load(move)
            m.display()
            print(e,"\n\n")
            raise
        try:
            self.assertEqual(m.get((1,8)), 0, "Rook should have left square")
        except AssertionError as e:
            m.load(move)
            m.display()
            print(e,"\n\n")
            raise

    def test_Brook_movementX(self):
        m = src.module.Module()
        rook = Rook(m.genID(), 1,(1,4))
        m.set((1,4), rook)
        m.moveCheck((1,4),(4,4))
        self.assertEqual(m.get((4,4)), rook, "Rook should have moved here")
        self.assertEqual(m.get((1,4)), 0, "Rook should have left square")

    def test_Brook_capture(self):
        m = src.module.Module()
        rook = Rook(m.genID(), 2,(1,4))
        knight = Knight(m.genID(), 1,(8,4))
        m.set((1,4), rook)
        m.set((8,4), knight)
        move = "A4-H8"
        m.save(move)
        m.moveCheck((1,4), (8,4))
        try:
            self.assertEqual(m.get((8,4)), rook, "Rook should have captured")
            self.assertEqual(m.get((1,4)), 0, "Rook should have left the square")
        except AssertionError:
            m.load(move)
            m.display()
            raise

    def test_Brook_jump(self):
        m = src.module.Module()
        rook = Rook(m.genID(), 2, (1,4))
        knight = Knight(m.genID(), 1, (8,4))
        Bbishop = Bishop(m.genID(), 1, (7,4))
        Wbishop = Bishop(m.genID(), 2, (6,4))
        m.set((1,4), rook)
        m.set((8,4), knight)
        m.set((7,4), Bbishop)
        m.set((6,4), Wbishop)
        move = "A4-H4"
        m.save(move)
        m.moveCheck((1,4), (8,4))
        try:
            self.assertEqual(m.get((1,4)), rook, move + ", Illigal Move, Rook should stay")
            self.assertEqual(m.get((6,4)), Wbishop, move + "Rook shouldn't have moved it's ally")
            self.assertEqual(m.get((7,4)), Bbishop, move + "Rook shouldn't not move a piece by jumping it")
            self.assertEqual(m.get((8,4)), knight, move + "Rook shouldn't be able to jump pieces")
        except AssertionError as e:
            m.load(move)
            m.display()
            print(e, "\n\n")
            raise
    
    def test_Brook_ally(self):
        m = src.module.Module()
        rook = Rook(m.genID(), 2,(1,4))
        knight = Knight(m.genID(), 2,(1,5))
        m.set((1,4), rook)
        m.set((1,5), knight)
        m.moveCheck((1,4), (1,5))
        self.assertEqual(m.get((1,4)), rook, "Rook should not have moved when attacking ally")
        self.assertEqual(m.get((1,5)), knight, "Rook shouldn't capture ally")


if __name__ == "__main__":
    unittest.main()
