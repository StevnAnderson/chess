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
        self.saves[name] = self.copyBoard(self.grid)
   
    def load(self, name):
        if name in self.saves.keys():
            copyBoard = self.copyBoard(self.saves[name])
            self.grid = copyBoard
            return self.grid
        print(name, "save not found.")
        return
    
    def visit(self,function, param=None, piece=None):
        if param == None:
            if piece == None:
                for y in range(1, len(self.grid)+1):
                    for x in range(1, len(self.grid[0])+1):
                        function(self.get((x,y)))
            else:
                for y in range(1, len(self.grid)+1):
                    for x in range(1, len(self.grid[0])+1):
                        if piece == str(self.get((x,y))):
                            function(self.get((x,y)))
        else:
            if piece == None:
                for y in range(1, len(self.grid)+1):
                    for x in range(1, len(self.grid[0])+1):
                        function((x,y), param)
            else:
                for y in range(1, len(self.grid)+1):
                    for x in range(1, len(self.grid[0])+1):
                        if str(self.get((x,y))) == piece:
                            function((x,y), param)

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
        
    def copyBoard(self,board1):
        retBoard = list()
        for i,n in enumerate(board1):
            retBoard.append(list())
            for m in n:
                retBoard[i].append(m)
        return retBoard