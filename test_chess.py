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
        m.turn = 2
        m.moveCheck((1,7),(1,6))
        self.assertEqual(m.get((1,7)),0,"Black Pawn shouldn't be in square where it left")
        self.assertEqual(m.get((1,6)),pawn, "Pawn should have moved")

    def test_Bpawn_move_ally(self):
        m = src.module.Module() #Move on ally
        knight = Knight(m.genID(), 2,(1,6))
        pawn = m.get((1,7))
        m.set((1,6), knight)
        m.turn = 2
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

    def test_Wbish_move(self):
        m = src.module.Module()
        bishop = Bishop(m.genID(), 1, (1,3))
        m.set((1,3), bishop)
        move = "A3-D6"
        m.save(move)
        m.moveCheck((1,3),(4,6))
        try:
            self.assertEqual(m.get((1,3)), 0, "Bishop should have left A4")
            self.assertEqual(m.get((4,6)), bishop, "Bishop should have moved to D6")
        except AssertionError as e:
            print("White Bishop Move\n",move,e)
            m.display()
            raise
    
    def test_Bbish_move(self):
        m = src.module.Module()
        m.turn = 2
        bishop = Bishop(m.genID(), 2, (1,3))
        m.set((1,3), bishop)
        move = "A3-D6"
        m.save(move)
        m.turn = 2
        m.moveCheck((1,3),(4,6))
        try:
            self.assertEqual(m.get((1,3)), 0, "Bishop should have left A3")
            self.assertEqual(m.get((4,6)), bishop, "Bishop should have moved to D6")
        except AssertionError as e:
            print("Black Bishop Move\n",move,e)
            m.display()
            raise

    def test_Bbish_move_fail(self):
        m = src.module.Module()
        m.turn = 2
        bishop = Bishop(m.genID(), 2, (1,3))
        m.set((1,3), bishop)
        move = "A3-B3"
        m.save(move)
        m.turn = 2
        m.moveCheck((1,3),(2,3))
        try:
            self.assertEqual(m.get((1,3)), bishop, "Bishop should not have left A4")
            self.assertEqual(m.get((2,3)), 0, "Bishop should not have moved to D6")
        except AssertionError as e:
            print("Black Bishop move fail\n",move,e)
            m.display()
            raise

    def test_Wbish_move_fail(self):
        m = src.module.Module()
        m.turn = 1
        bishop = Bishop(m.genID(), 1, (1,3))
        m.set((1,3), bishop)
        move = "A3-B3"
        m.save(move)
        m.moveCheck((1,3),(2,3))
        try:
            self.assertEqual(m.get((1,3)), bishop, "Bishop should not have left A4")
            self.assertEqual(m.get((2,3)), 0, "Bishop should not have moved to D6")
        except AssertionError as e:
            print("White Bishop move fail\n",move,e)
            m.display()
            raise

    def test_Wbish_capture(self):
        m = src.module.Module()
        bishop = Bishop(m.genID(), 1, (1,3))
        knight = Knight(m.genID(), 2, (2,4))
        m.set((1,3), bishop)
        m.set((2,4), knight)
        move = "A3-B4"
        m.save(move)
        m.moveCheck((1,3),(2,4))
        try:
            self.assertEqual(m.get((1,3)), 0, "Bishop should have left A4")
            self.assertEqual(m.get((2,4)), bishop, "Bishop should have captured on B4")
        except AssertionError as e:
            print("White Bishop capture\n",move,e)
            m.display()
            raise

    def test_Bbish_capture(self):
        m = src.module.Module()
        bishop = Bishop(m.genID(), 2, (1,3))
        knight = Knight(m.genID(), 1, (2,4))
        m.set((1,3), bishop)
        m.set((2,4), knight)
        move = "A3-B4"
        m.save(move)
        m.turn = 2
        m.moveCheck((1,3),(2,4))
        try:
            self.assertEqual(m.get((1,3)), 0, "Bishop should have left A3")
            self.assertEqual(m.get((2,4)), bishop, "Bishop should have captured on B4")
        except AssertionError as e:
            print("Black Bishop Capture\n",move,e)
            m.display()
            raise

    def test_Wbish_allyCapture(self):
        m = src.module.Module()
        bishop = Bishop(m.genID(), 1, (1,3))
        knight = Knight(m.genID(), 1, (2,4))
        m.set((1,3), bishop)
        m.set((2,4), knight)
        move = "A3-B4"
        m.save(move)
        m.moveCheck((1,4),(3,6))
        try:
            self.assertEqual(m.get((1,3)), bishop, "Bishop should not have left A3")
            self.assertEqual(m.get((2,4)), knight, "Bishop should not have captured on B4")
        except AssertionError as e:
            print("White Bishop Ally Capture\n",move,e)
            m.display()
            raise

    def test_Bbish_allyCapture(self):
        m = src.module.Module()
        bishop = Bishop(m.genID(), 2, (1,3))
        knight = Knight(m.genID(), 2, (2,4))
        m.set((1,3), bishop)
        m.set((2,4), knight)
        move = "A3-B4"
        m.save(move)
        m.turn = 2
        m.moveCheck((1,3),(2,4))
        try:
            self.assertEqual(m.get((1,3)), bishop, "Bishop should not have left A3")
            self.assertEqual(m.get((2,4)), knight, "Bishop should not have captured on B4")
        except AssertionError as e:
            print("Black Bishop Ally Capture\n",move,e)
            m.display()
            raise

    def test_Wbish_jumpAlly(self):
        m = src.module.Module()
        bishop = Bishop(m.genID(), 1, (1,3))
        knight = Knight(m.genID(), 1, (2,4))
        m.set((1,3), bishop)
        m.set((2,4), knight)
        move = "A3-B4"
        m.save(move)
        m.moveCheck((1,3),(3,5))
        try:
            self.assertEqual(m.get((1,3)), bishop, "Bishop should not have left A3")
            self.assertEqual(m.get((2,4)), knight, "Knight should not have moved")
            self.assertEqual(m.get((3,5)), 0, "Bishop should not have jumped ally on C5")
        except AssertionError as e:
            print("White Bishop Jump Ally\n",move,e)
            m.display()
            raise

    def test_Bbish_jumpAlly(self):
        m = src.module.Module()
        bishop = Bishop(m.genID(), 2, (1,3))
        knight = Knight(m.genID(), 2, (2,4))
        m.set((1,3), bishop)
        m.set((2,4), knight)
        move = "A3-C5"
        m.save(move)
        m.turn = 2
        m.moveCheck((1,3),(3,5))
        try:
            self.assertEqual(m.get((1,3)), bishop, "Bishop should not have left A3")
            self.assertEqual(m.get((2,4)), knight, "Knight should not have moved")
            self.assertEqual(m.get((3,5)), 0, "Bishop should not have jumped ally on B4")
        except AssertionError as e:
            print("Black Bishop Jump Ally\n",move,e)
            m.display()
            raise

    def test_Wbish_jumpOpponent(self):
        m = src.module.Module()
        bishop = Bishop(m.genID(), 1, (1,3))
        knight = Knight(m.genID(), 2, (2,5))
        m.set((1,4), bishop)
        m.set((2,5), knight)
        move = "A4-C6"
        m.save(move)
        m.moveCheck((1,4),(3,6))
        try:
            self.assertEqual(m.get((1,4)), 0, "Bishop should not have left A4")
            self.assertEqual(m.get((3,6)), bishop, "Bishop should not have jumped opponent on C5")
        except AssertionError as e:
            print("White Bishop Jump Opponent\n",move,e)
            m.display()
            raise

    def test_Wbish_jumpOpponent(self):
        m = src.module.Module()
        bishop = Bishop(m.genID(), 2, (1,3))
        knight = Knight(m.genID(), 1, (2,4))
        m.set((1,3), bishop)
        m.set((2,4), knight)
        move = "A3-C5"
        m.save(move)
        m.moveCheck((1,3),(3,5))
        try:
            self.assertEqual(m.get((1,3)), bishop, "Bishop should not have left A3")
            self.assertEqual(m.get((2,4)), knight, "Knight should not have moved")
            self.assertEqual(m.get((3,5)), 0, "Bishop should not have jumped opponent on C5")
        except AssertionError as e:
            print("White Bishop Jump Opponent\n",move,e)
            m.display()
            raise

    def test_Wkngt_move(self):
        m = src.module.Module()
        knight = Knight(m.genID(),1,(3,3))
        m.set((3,3), knight)
        move = "C3-D5"
        m.moveCheck((3,3), (4,5))
        try:
            self.assertEqual(m.get((3,3)), 0, "Knight should have left C3")
            self.assertEqual(m.get((4,5)), knight, "Knight should have moved to D5")
        except AssertionError as e:
            print("\nWhite Knight Move\n", move, e)
            m.display()
            raise

    def test_Bkngt_move(self):
        m = src.module.Module()
        knight = Knight(m.genID(),2,(3,3))
        m.set((3,3), knight)
        move = "C3-D5"
        m.turn = 2
        m.moveCheck((3,3), (4,5))
        try:
            self.assertEqual(m.get((3,3)), 0, "Knight should have left C3")
            self.assertEqual(m.get((4,5)), knight, "Knight should have moved to D5")
        except AssertionError as e:
            print("\nBlack Knight Move\n", move, e)
            m.display()
            raise

    def test_Wkngt_move_fail(self):
        m = src.module.Module()
        knight = Knight(m.genID(),1,(3,3))
        m.set((3,3), knight)
        move = "C3-D6"
        m.moveCheck((3,3), (3,6))
        try:
            self.assertEqual(m.get((3,3)), knight, "Knight should not have left C3")
            self.assertEqual(m.get((3,6)), 0, "Knight should not have moved to D5")
        except AssertionError as e:
            print("\nWhite Knight Move Fail\n", move, e)
            m.display()
            raise

    def test_Bkngt_move_fail(self):
        m = src.module.Module()
        knight = Knight(m.genID(),2,(3,3))
        m.set((3,3), knight)
        move = "C3-D6"
        m.turn = 2
        m.moveCheck((3,3), (3,6))
        try:
            self.assertEqual(m.get((3,3)), knight, "Knight should not have left C3")
            self.assertEqual(m.get((3,6)), 0, "Knight should not have moved to D5")
        except AssertionError as e:
            print("\nBlack Knight Move Fail")
            m.display()
            raise
   
    def test_Wkngt_capture(self):
        m = src.module.Module()
        knight = Knight(m.genID(),1,(3,3))
        bishop = Bishop(m.genID(), 2, ((4,5)))
        m.set((3,3), knight)
        m.set((4,5), bishop)
        move = "C3-D6"
        m.moveCheck((3,3), (4,5))
        try:
            self.assertEqual(m.get((3,3)), 0, "Knight should have left C3")
            self.assertEqual(m.get((4,5)), knight, "Knight should have captured D5")
        except AssertionError as e:
            print("\nWhite Knight Capture\n", move, e)
            m.display()
            raise

    def test_Bkngt_capture(self):
        m = src.module.Module()
        knight = Knight(m.genID(), 2,(3,3))
        bishop = Bishop(m.genID(), 1, (4,5))
        m.set((3,3), knight)
        m.set((4,5), bishop)
        move = "C3-D6"
        m.turn = 2
        m.moveCheck((3,3), (4,5))
        try:
            self.assertEqual(m.get((3,3)), 0, "Knight should have left C3")
            self.assertEqual(m.get((4,5)), knight, "Knight should have captured D5")
        except AssertionError as e:
            print("\nBlack Knight Capture\n", move, e)
            m.display()
            raise

    def test_Wkngt_capture_Ally(self):
        m = src.module.Module()
        knight = Knight(m.genID(), 1,(3,3))
        bishop = Bishop(m.genID(), 1, ((4,5)))
        m.set((3,3), knight)
        m.set((4,5), bishop)
        move = "C3-D6"
        m.moveCheck((3,3), (4,5))
        try:
            self.assertEqual(m.get((3,3)), knight, "Knight should not have left C3")
            self.assertEqual(m.get((4,5)), bishop, "Knight should not have captured D5")
        except AssertionError as e:
            print("\nWhite Knight Capture Ally\n", move, e)
            m.display()
            raise

    def test_Bkngt_capture_Ally(self):
        m = src.module.Module()
        knight = Knight(m.genID(), 2,(3,3))
        bishop = Bishop(m.genID(), 2, ((4,5)))
        m.set((3,3), knight)
        m.set((4,5), bishop)
        move = "C3-D6"
        m.turn = 2
        m.moveCheck((3,3), (4,5))
        try:
            self.assertEqual(m.get((3,3)), knight, "Knight should not have left C3")
            self.assertEqual(m.get((4,5)), bishop, "Knight should not have captured D5")
        except AssertionError as e:
            print("\nBlack Knight Capture Ally\n", move, e)
            m.display()
            raise

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
        m.turn = 2
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
        rook = Rook(m.genID(), 2,(1,4))
        m.set((1,4), rook)
        m.turn = 2
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
        m.turn = 2
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
        m.turn = 2
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
        m.turn = 2
        m.moveCheck((1,4), (1,5))
        self.assertEqual(m.get((1,4)), rook, "Rook should not have moved when attacking ally")
        self.assertEqual(m.get((1,5)), knight, "Rook shouldn't capture ally")

    def test_Wqueen_move_tile(self):
        m = src.module.Module()
        queen = Queen(m.genID(),1,(3,3))
        m.set((3,3), queen)
        move = "C3-C4"
        m.moveCheck((3,3), (3,4))
        try:
            self.assertEqual(m.get((3,3)), 0, "Queen should have moved from C3")
            self.assertEqual(m.get((3,4)), queen, "Queen should have moved to C4")
        except AssertionError as e:
            print("\nWhite Queen Move Tile\n", move, e)
            m.display()
            raise

    def test_Bqueen_move_tile(self):
        m = src.module.Module()
        queen = Queen(m.genID(),2,(3,3))
        m.set((3,3), queen)
        move = "C3-C4"
        m.turn = 2
        m.moveCheck((3,3), (3,4))
        try:
            self.assertEqual(m.get((3,3)), 0, "Queen should have moved from C3")
            self.assertEqual(m.get((3,4)), queen, "Queen should have moved to C4")
        except AssertionError as e:
            print("\nBlack Queen Move Tile\n", move, e)
            m.display()
            raise

    def test_Wqueen_move_row(self):
        m = src.module.Module()
        queen = Queen(m.genID(),1,(3,3))
        m.set((3,3), queen)
        move = "C3-D3"
        m.moveCheck((3,3), (4,3))
        try:
            self.assertEqual(m.get((3,3)), 0, "Queen should have moved from C3")
            self.assertEqual(m.get((4,3)), queen, "Queen should have moved to D3")
        except AssertionError as e:
            print("\nWhite Queen Move Row\n", move, e)
            m.display()
            raise

    def test_Bqueen_move_row(self):
        m = src.module.Module()
        queen = Queen(m.genID(),2,(3,3))
        m.set((3,3), queen)
        move = "C3-D3"
        m.turn = 2
        m.moveCheck((3,3), (4,3))
        try:
            self.assertEqual(m.get((3,3)), 0, "Queen should have moved from C3")
            self.assertEqual(m.get((4,3)), queen, "Queen should have moved to D3")
        except AssertionError as e:
            print("\nBlack Queen Move Tile\n", move, e)
            m.display()
            raise

    def test_Wqueen_move_diagnal(self):
        m = src.module.Module()
        queen = Queen(m.genID(),1,(3,3))
        m.set((3,3), queen)
        move = "C3-D4"
        m.moveCheck((3,3), (4,4))
        try:
            self.assertEqual(m.get((3,3)), 0, "Queen should have moved from C3")
            self.assertEqual(m.get((4,4)), queen, "Queen should have moved to D4")
        except AssertionError as e:
            print("\nWhite Queen Move Diagnal\n", move, e)
            m.display()
            raise

    def test_Bqueen_move_diagnal(self):
        m = src.module.Module()
        queen = Queen(m.genID(),2,(3,3))
        m.set((3,3), queen)
        move = "C3-D4"
        m.turn = 2
        m.moveCheck((3,3), (4,4))
        try:
            self.assertEqual(m.get((3,3)), 0, "Queen should have moved from C3")
            self.assertEqual(m.get((4,4)), queen, "Queen should have moved to D4")
        except AssertionError as e:
            print("\nBlack Queen Move Diagnal\n", move, e)
            m.display()
            raise

    def test_Wqueen_capture(self):
        m = src.module.Module()
        queen = Queen(m.genID(),1,(3,3))
        knight = Knight(m.genID(),2,(3,4))
        m.set((3,3), queen)
        m.set((3,4), knight)
        move = "C3-C4"
        m.moveCheck((3,3), (3,4))
        try:
            self.assertEqual(m.get((3,3)), 0, "Queen should have moved from C3")
            self.assertEqual(m.get((3,4)), queen, "Queen should have captured on C4")
        except AssertionError as e:
            print("\nWhite Queen Capture\n", move, e)
            m.display()
            raise

    def test_Bqueen_capture(self):
        m = src.module.Module()
        queen = Queen(m.genID(),2,(3,3))
        knight = Knight(m.genID(),1,(3,4))
        m.set((3,3), queen)
        m.set((3,4), knight)
        move = "C3-C4"
        m.turn = 2
        m.moveCheck((3,3), (3,4))
        try:
            self.assertEqual(m.get((3,3)), 0, "Queen should have moved from C3")
            self.assertEqual(m.get((3,4)), queen, "Queen should have captured on C4")
        except AssertionError as e:
            print("\nBlack Queen Capture\n", move, e)
            m.display()
            raise

    def test_Wqueen_capture_ally(self):
        m = src.module.Module()
        queen = Queen(m.genID(),1,(3,3))
        knight = Knight(m.genID(),1,(3,4))
        m.set((3,3), queen)
        m.set((3,4), knight)
        move = "C3-C4"
        m.moveCheck((3,3), (3,4))
        try:
            self.assertEqual(m.get((3,3)), queen, "Queen should not have moved from C3")
            self.assertEqual(m.get((3,4)), knight, "Queen should not have captured on C4")
        except AssertionError as e:
            print("\nWhite Queen Capture Ally\n", move, e)
            m.display()
            raise

    def test_Bqueen_capture_ally(self):
        m = src.module.Module()
        queen = Queen(m.genID(),2,(3,3))
        knight = Knight(m.genID(),2,(3,4))
        m.set((3,3), queen)
        m.set((3,4), knight)
        move = "C3-C4"
        m.turn = 2
        m.moveCheck((3,3), (3,4))
        try:
            self.assertEqual(m.get((3,3)), queen, "Queen should not have moved from C3")
            self.assertEqual(m.get((3,4)), knight, "Queen should not have captured on C4")
        except AssertionError as e:
            print("\nBlack Queen Capture Ally\n", move, e)
            m.display()
            raise

    def test_Wqueen_jump_ally(self):
        m = src.module.Module()
        queen = Queen(m.genID(),1,(3,3))
        knight = Knight(m.genID(),1,(3,4))
        m.set((3,3), queen)
        m.set((3,4), knight)
        move = "C3-C5"
        m.moveCheck((3,3), (3,5))
        try:
            self.assertEqual(m.get((3,3)), queen, "Queen should not have moved from C3")
            self.assertEqual(m.get((3,4)), knight, "Knight should not have moved on C4")
            self.assertEqual(m.get((3,5)), 0, "Queen should not have jumped ally on C4")
        except AssertionError as e:
            print("\nWhite Queen Jump Ally\n", move, e)
            m.display()
            raise

    def test_Bqueen_jump_ally(self):
        m = src.module.Module()
        queen = Queen(m.genID(),2,(3,3))
        knight = Knight(m.genID(),2,(3,4))
        m.set((3,3), queen)
        m.set((3,4), knight)
        move = "C3-C5"
        m.turn = 2
        m.moveCheck((3,3), (3,5))
        try:
            self.assertEqual(m.get((3,3)), queen, "Queen should not have moved from C3")
            self.assertEqual(m.get((3,4)), knight, "Knight should not have moved on C4")
            self.assertEqual(m.get((3,5)), 0, "Queen should not have jumped ally on C4")
        except AssertionError as e:
            print("\nBlack Queen Jump Ally\n", move, e)
            m.display()
            raise

    def test_Wqueen_jump_opponent(self):
        m = src.module.Module()
        queen = Queen(m.genID(),1,(3,3))
        knight = Knight(m.genID(),2,(3,4))
        m.set((3,3), queen)
        m.set((3,4), knight)
        move = "C3-C5"
        m.moveCheck((3,3), (3,5))
        try:
            self.assertEqual(m.get((3,3)), queen, "Queen should not have moved from C3")
            self.assertEqual(m.get((3,4)), knight, "Knight should not have moved on C4")
            self.assertEqual(m.get((3,5)), 0, "Queen should not have jumped ally on C4")
        except AssertionError as e:
            print("\nWhite Queen Jump Opponent\n", move, e)
            m.display()
            raise

    def test_Bqueen_jump_opponent(self):
        m = src.module.Module()
        queen = Queen(m.genID(),2,(3,3))
        knight = Knight(m.genID(),1,(3,4))
        m.set((3,3), queen)
        m.set((3,4), knight)
        move = "C3-C5"
        m.turn = 2
        m.moveCheck((3,3), (3,5))
        try:
            self.assertEqual(m.get((3,3)), queen, "Queen should not have moved from C3")
            self.assertEqual(m.get((3,4)), knight, "Knight should not have moved on C4")
            self.assertEqual(m.get((3,5)), 0, "Queen should not have jumped ally on C4")
        except AssertionError as e:
            print("\nBlack Queen Jump Opponent\n", move, e)
            m.display()
            raise

    def test_Wking_move(self):
        m = src.module.Module()
        king = King(m.genID(),1,(3,3))
        m.set((3,3), king)
        move = "C3-C4"
        m.moveCheck((3,3), (3,4))
        try:
            self.assertEqual(m.get((3,3)), 0, "King should have left C3")
            self.assertEqual(m.get((3,4)), king, "King should have moved to C4")
        except AssertionError as e:
            print("\nWhite King Move\n", move, e)
            m.display()
            raise

    def test_Bking_move(self):
        m = src.module.Module()
        king = King(m.genID(),2,(3,3))
        m.set((3,3), king)
        move = "C3-C4"
        m.turn = 2
        m.moveCheck((3,3), (3,4))
        try:
            self.assertEqual(m.get((3,3)), 0, "King should have left C3")
            self.assertEqual(m.get((3,4)), king, "King should have moved to C4")
        except AssertionError as e:
            print("\nBlack King Move\n", move, e)
            m.display()
            raise

    def test_Wking_move_fail(self):
        m = src.module.Module()
        king = King(m.genID(),1,(3,3))
        m.set((3,3), king)
        move = "C3-C5"
        m.moveCheck((3,3), (3,5))
        try:
            self.assertEqual(m.get((3,3)), king, "King should not have left C3")
            self.assertEqual(m.get((3,5)), 0, "King should not have moved to C4")
        except AssertionError as e:
            print("\nWhite King Move Fail\n", move, e)
            m.display()
            raise

    def test_Bking_move_fail(self):
        m = src.module.Module()
        king = King(m.genID(),2,(3,3))
        m.set((3,3), king)
        move = "C3-C5"
        m.turn = 2
        m.moveCheck((3,3), (3,5))
        try:
            self.assertEqual(m.get((3,3)), king, "King should not have left C3")
            self.assertEqual(m.get((3,5)), 0, "King should not have moved to C4")
        except AssertionError as e:
            print("\nBlack King Move Fail\n", move, e)
            m.display()
            raise

    def test_Wking_capture(self):
        m = src.module.Module()
        king = King(m.genID(),1,(3,3))
        knight = Knight(m.genID(), 2,(3,4))
        m.set((3,3), king)
        m.set((3,4), knight)
        move = "C3-C4"
        m.moveCheck((3,3), (3,4))
        try:
            self.assertEqual(m.get((3,3)), 0, "King should have left C3")
            self.assertEqual(m.get((3,4)), king, "King should have captured on C4")
        except AssertionError as e:
            print("\nWhite King Capture\n", move, e)
            m.display()
            raise

    def test_Bking_capture(self):
        m = src.module.Module()
        king = King(m.genID(), 2, (3,3))
        knight = Knight(m.genID(), 1,(3,4))
        m.set((3,3), king)
        m.set((3,4), knight)
        move = "C3-C4"
        m.turn = 2
        m.moveCheck((3,3), (3,4))
        try:
            self.assertEqual(m.get((3,3)), 0, "King should have left C3")
            self.assertEqual(m.get((3,4)), king, "King should have captured on C4")
        except AssertionError as e:
            print("\nBlack King Capture\n", move, e)
            m.display()
            raise

    def test_Wking_capture_ally(self):
        m = src.module.Module()
        king = King(m.genID(),1,(3,3))
        knight = Knight(m.genID(), 1,(3,4))
        m.set((3,3), king)
        m.set((3,4), knight)
        move = "C3-C4"
        m.moveCheck((3,3), (3,4))
        try:
            self.assertEqual(m.get((3,3)), king, "King should not have left C3")
            self.assertEqual(m.get((3,4)), knight, "King should not have captured ally on C4")
        except AssertionError as e:
            print("\nWhite King Capture Ally\n", move, e)
            m.display()
            raise

    def test_Wking_capture_ally(self):
        m = src.module.Module()
        king = King(m.genID(),2,(3,3))
        knight = Knight(m.genID(), 2,(3,4))
        m.set((3,3), king)
        m.set((3,4), knight)
        move = "C3-C4"
        m.moveCheck((3,3), (3,4))
        try:
            self.assertEqual(m.get((3,3)), king, "King should not have left C3")
            self.assertEqual(m.get((3,4)), knight, "King should not have captured ally on C4")
        except AssertionError as e:
            print("\nBlack King Capture Ally\n", move, e)
            m.display()
            raise

    def test_Wcastle_queenside(self):
        m = src.module.Module()
        king = m.get((5,1))
        rook = m.get((1,1))
        m.set((2,1), 0)
        m.set((3,1), 0)
        m.set((4,1), 0)
        move = "E1-C1"
        m.moveCheck((5,1), (3,1))
        try:
            self.assertEqual(m.get((3,1)), king, "King should have castled to C1")
            self.assertEqual(m.get((4,1)), rook, "Rook should have calsted to D1")
        except AssertionError as e:
            print("\nWhite Castle Queenside\n", move, e)
            m.display()
            raise

    def test_Wcastle_queenside_fail(self):
        m = src.module.Module()
        king = m.get((5,1))
        rook = m.get((1,1))
        m.set((3,1), 0)
        m.set((4,1), 0)
        move = "E1-C1"
        m.moveCheck((5,1), (3,1))
        try:
            self.assertEqual(m.get((3,1)), 0, "King should not have castled to C1")
            self.assertEqual(m.get((4,1)), 0, "Rook should not have castled to D1")
            self.assertEqual(m.get((1,1)), rook, "Rook should have stayed at A1")
            self.assertEqual(m.get((5,1)), king, "King should have stayed at E1")
        except AssertionError as e:
            print("\nWhite Castle Queenside\n", move, e)
            m.display()
            raise

    def test_Wcastle_kingside(self):
        m = src.module.Module()
        king = m.get((5,1))
        rook = m.get((8,1))
        m.set((6,1), 0)
        m.set((7,1), 0)
        move = "E1-G1"
        m.moveCheck((5,1), (7,1))
        try:
            self.assertEqual(m.get((7,1)), king, "King should have castled to F1")
            self.assertEqual(m.get((6,1)), rook, "Rook should have calsted to E1")
        except AssertionError as e:
            print("\nWhite Castle Queenside\n", move, e)
            m.display()
            raise
   
    def test_Wcastle_kingside_fail(self):
        m = src.module.Module()
        king = m.get((5,1))
        rook = m.get((8,1))
        knight = m.get((7,1))
        m.set((6,1), 0)
        move = "E1-G1"
        m.moveCheck((5,1), (7,1))
        try:
            self.assertEqual(m.get((5,1)), king, "King should not have castled to G1")
            self.assertEqual(m.get((6,1)), 0, "Rook should not have castled to D1")
            self.assertEqual(m.get((8,1)), rook, "Rook should have stayed at H1")
            self.assertEqual(m.get((7,1)), knight, "Knight should have stayed at G1")
        except AssertionError as e:
            print("\nWhite Castle Kingside Fail\n", move, e)
            m.display()
            raise

    def test_Bcastle_queenside(self):
        m = src.module.Module()
        king = m.get((5,8))
        rook = m.get((1,8))
        m.set((2,8), 0)
        m.set((3,8), 0)
        m.set((4,8), 0)
        move = "E8-C8"
        m.turn = 2
        m.moveCheck((5,8), (3,8))
        try:
            self.assertEqual(m.get((3,8)), king, "King should have castled to C8")
            self.assertEqual(m.get((4,8)), rook, "Rook should have calsted to D8")
        except AssertionError as e:
            print("\nBlack Castle Queenside\n", move, e)
            m.display()
            raise

    def test_Bcastle_queenside_fail(self):
        m = src.module.Module()
        king = m.get((5,8))
        rook = m.get((1,8))
        m.set((3,8), 0)
        m.set((4,8), 0)
        move = "E8-C8"
        m.turn = 2
        m.moveCheck((5,8), (3,8))
        try:
            self.assertEqual(m.get((3,8)), 0, "King should not have castled to C8")
            self.assertEqual(m.get((4,8)), 0, "Rook should not have castled to D8")
            self.assertEqual(m.get((1,8)), rook, "Rook should have stayed at A8")
            self.assertEqual(m.get((5,8)), king, "King should have stayed at E8")
        except AssertionError as e:
            print("\Black Castle Queenside\n", move, e)
            m.display()
            raise

    def test_Bcastle_kingside(self):
        m = src.module.Module()
        king = m.get((5,8))
        rook = m.get((8,8))
        m.set((6,8), 0)
        m.set((7,8), 0)
        move = "E8-G8"
        m.turn = 2
        m.moveCheck((5,8), (7,8))
        try:
            self.assertEqual(m.get((7,8)), king, "King should have castled to F8")
            self.assertEqual(m.get((6,8)), rook, "Rook should have calsted to E8")
        except AssertionError as e:
            print("\Black Castle Queenside\n", move, e)
            m.display()
            raise

    def test_threatons(self):
        m = src.module.Module()
        queen = m.get((4,1))
        knight = m.get((7,1))
        pawn = m.get((7,2))
        m.moveCheck((5,2), (5,4))
        tList = m.threatons((6,3))
        try:
            self.assertIn(queen, tList, "queen should threaton F3")
            self.assertIn(knight, tList, "knight should threaton F3")
            self.assertIn(pawn, tList, "G Pawn should threaton F3")
        except AssertionError as e:
            print("\nThreatons\n", e)
            raise
    
if __name__ == "__main__":
    unittest.main()
