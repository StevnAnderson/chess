import src.module


m = src.module.Module()
m.moveCheck(m.gb.get((1,2)),(1,4))
m.moveCheck(m.gb.get((1,4)),(1,6))
m.moveCheck(m.gb.get((1,1)),(1,3))
m.moveCheck(m.gb.get((1,3)),(2,3))
m.moveCheck(m.gb.get((2,3)),(2,7))


m.display()