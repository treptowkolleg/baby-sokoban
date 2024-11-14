import sokoban

class Target(sokoban.Cell):
    def __init__(self, x=None, y=None):
        super().__init__(x, y)

class Box(sokoban.Cell):
    def __init__(self, x=None, y=None):
        super().__init__(x, y)

class Player(sokoban.Cell):
    def __init__(self, x=None, y=None):
        super().__init__(x, y)