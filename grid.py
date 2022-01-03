MOVE_RULES = [(-1, 2), (1, 2), (-1, -2), (1, -2), (-2, 1), (-2, -1), (2, 1), (2, -1)]



class Grid:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.size = X * Y
        self.cell = "_"
        self.board = self.generate()
        self.current_move = (0, 0)
        self.visited = []
        self.possible_moves = []
        self.count_possible_moves = []



    def generate(self):
        board = [[self.cell for _ in range(self.X)] for _ in range(self.Y)]
        return board

    def update(self, x_pos, y_pos):
        if self.visited == [] or (x_pos, y_pos) in self.possible_moves:
            # update visited
            self.visited.append((x_pos, y_pos))
            # update possible move
            self.update_possible_move(x_pos, y_pos)

    def update_possible_move(self, x_pos, y_pos):
        possible_moves = []
        for x, y in MOVE_RULES:
            x_possible = x_pos + x
            y_possible = y_pos + y
            count = self.move_count(x_possible, y_possible)
            if 1 <= x_possible <= self.X and 1 <= y_possible <= self.Y and (x_possible, y_possible) not in self.visited:
                possible_moves.append((count, x_possible, y_possible))
        # track possible moves
        possible_moves.sort(reverse=True)
        self.count_possible_moves = possible_moves
        self.possible_moves = [(x, y) for count, x, y in possible_moves]

    def move_count(self, x_pos, y_pos):
        count = 0
        for x, y in MOVE_RULES:
            x_possible = x_pos + x
            y_possible = y_pos + y
            if 1 <= x_possible <= self.X and 1 <= y_possible <= self.Y and (x_possible, y_possible) not in self.visited:
                count += 1
        return count

    def undo(self):
        if self.visited:
            self.visited.pop()
            if not self.visited:
                self.possible_moves = []
                self.count_possible_moves = []
            else:
                x_last, y_last = self.visited[-1]
                self.update_possible_move(x_last, y_last)

    # def solve(self, x, y):
    #     self.update(x, y)
    #     if len(self.visited) == self.size:
    #         return True
    #
    #     if len(self.possible_moves) == 0:
    #         return False
    #
    #     for move in self.possible_moves:
    #         pygame.time.delay(100)
    #         x_next, y_next = move
    #         if self.solve(x_next, y_next):
    #             return True
    #         self.undo()
    #     return False
    #

