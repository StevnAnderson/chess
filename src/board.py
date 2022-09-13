class Board:
    grid = list()
    saves = {}

    def __init__(self,x,y):
        self.buildGrid(x,y)

    def buildGrid(self,x,y):
        if x < 1 or y < 1:
            return -1
        self.grid = list()
        for yaxis in range(y):
            tempList = list()
            for xaxis in range(x):
                tempList.append(0)
            self.grid.append(tempList)
    
    def save(self, name):
        self.saves[name] = self.grid
        
    def load(self, name):
        if name in self.saves.keys():
            return self.saves[name]
        print(name, "save not found.")
        return
    
    def visit(self,function):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                function(self.get(x,y))
    
    def set(self,d,value):
        x, y = d[0], d[1]
        if x > len(self.grid) or x <= 0 \
            or y > len(self.grid[0] or y <= 0):
            return False
        self.grid[y-1][x-1] = value
        return True

    def get(self,d):
        x,y = d[0],d[1]
        if x > len(self.grid) or x <= 0 \
            or y > len(self.grid[0] or y <= 0):
            return None
        return self.grid[y-1][x-1]
        