class Cell:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def at(self, cell):
        return self.x==cell.x and self.y==cell.y

    def move(self,dx,dy):
        self.x += dx
        self.y += dy