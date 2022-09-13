import src.module


m = src.module.Module()
m.moveCheck((1,2),(1,4))
m.moveCheck((1,4),(1,6))
m.moveCheck((1,1),(1,3))
m.moveCheck((1,3),(2,3))
m.moveCheck((2,3),(2,7))


m.display()