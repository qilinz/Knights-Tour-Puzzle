MOVE_RULES = [(-1, 2), (1, 2), (-1, -2), (1, -2), (-2, 1), (-2, -1), (2, 1), (2, -1)]


class Board:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.size = X * Y
        self.cell_size = len(str(self.X * self.Y))
        self.cell = "_" * self.cell_size
        self.board = self.generate()
        self.visited = []
        self.possible_moves = []

    def generate(self):
        board = [[self.cell for _ in range(self.X)] for _ in range(self.Y)]
        return board

    def present(self):
        border = " " * len(str(self.Y)) + "-" * (self.X * (self.cell_size + 1) + 3)
        print(border)
        for _ in range(self.Y, 0, -1):
            y_label = " " * (len(str(self.Y)) - len(str(_))) + str(_)
            print(f"{y_label}| {' '.join(self.board[_ - 1])} |")
        print(border)
        x_labels = [" " * (self.cell_size - len(str(i))) + str(i) for i in range(1, self.X + 1)]
        print(f"{' ' * len(str(self.Y))}  {' '.join(x_labels)}")

    def mark(self, x_pos, y_pos, mark):
        self.board[y_pos - 1][x_pos - 1] = " " * (self.cell_size - len(mark)) + mark

    def mark_current_move(self, x_pos, y_pos):
        self.mark(x_pos, y_pos, "X")
        # add it to visited list
        self.visited.append((x_pos, y_pos))

    def mark_possible_move(self, x_pos, y_pos):
        possible_moves = []
        for x, y in MOVE_RULES:
            x_possible = x_pos + x
            y_possible = y_pos + y
            count = self.count_possible_move(x_possible, y_possible)
            if 1 <= x_possible <= self.X and 1 <= y_possible <= self.Y and (x_possible, y_possible) not in self.visited:
                possible_moves.append((count, x_possible, y_possible))
                self.mark(x_possible, y_possible, str(count))
        # track possible moves
        possible_moves.sort(reverse=True)
        self.possible_moves = [(x, y) for count, x, y in possible_moves]


    def count_possible_move(self, x_pos, y_pos):
        count = 0
        for x, y in MOVE_RULES:
            x_possible = x_pos + x
            y_possible = y_pos + y
            if 1 <= x_possible <= self.X and 1 <= y_possible <= self.Y and (x_possible, y_possible) not in self.visited:
                count += 1
        return count

    def mark_visited(self):
        x, y = self.visited[-1]
        self.mark(x, y, "*")

    def clear_possible_moves(self):
        for x, y in self.possible_moves:
            self.mark(x, y, self.cell)
