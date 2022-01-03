from board import Board


def play_game(game_board, x_pos, y_pos):
    # Mark current and possible move
    game_board.mark_current_move(x_pos, y_pos)
    game_board.mark_possible_move(x_pos, y_pos)

    # present the board.py
    game_board.present()

    # count how many moves have been visited
    count = 1

    # start the loop until the end
    while True:
        # WIN: if every cell is visited
        if len(game_board.visited) == game_board.size:
            print("What a great tour! Congratulations!")
            break

        # LOSE: if no available moves
        if len(game_board.possible_moves) == 0:
            print("No more possible moves!")
            print(f"Your knight visited {count} squares!")
            break

        # Get the next move
        try:
            x_pos, y_pos = [int(num) for num in input("Enter your next move: ").split()]
        except ValueError or TypeError:
            print("Invalid dimensions!")
        else:
            if (x_pos, y_pos) not in game_board.possible_moves:
                print("Invalid move! ")
            else:
                # 1. visited -> *
                game_board.mark_visited()
                # 2. remove possible moves
                game_board.clear_possible_moves()
                # 3. Mark current and possible move
                game_board.mark_current_move(x_pos, y_pos)
                game_board.mark_possible_move(x_pos, y_pos)
                # 4. Show the board.py
                game_board.present()

                count += 1


def find_solution(game_board, x_pos, y_pos):
    game_board.mark_current_move(x_pos, y_pos)
    game_board.mark_possible_move(x_pos, y_pos)
    # print(" \nNew level")
    # print(f"Visited: {game_board.visited}, {len(game_board.visited)} squares, {game_board.size} total")

    # If solution exists
    if len(game_board.visited) == game_board.size:
        # mark the board.py in the correct order
        for i in range(len(game_board.visited)):
            x_pos, y_pos = game_board.visited[i]
            game_board.mark(x_pos, y_pos, str(i + 1))
        return True
        # return the solution
        # No solution
    if len(game_board.possible_moves) == 0:
        return False
        # print(f"All possible moves: {game_board.possible_moves}")
    for move in game_board.possible_moves:
        # print(f"Current move to search: {move}")
        x_next, y_next = move
        if find_solution(game_board, x_next, y_next):
            return True
        game_board.visited.pop()
    return False


# ----------------------------- 1. Create the board.py ---------------------------------- #
while True:
    try:
        X, Y = [int(num) for num in input("Enter your board.py.py dimensions: ").split()]
    except ValueError or TypeError:
        print("Invalid dimensions!")
    else:
        if X < 1 or Y < 1:
            print("Invalid dimensions!")
        else:
            break

board = Board(X, Y)


# --------------------------- 2. Get the first move ------------------------------- #
while True:
    try:
        x, y = [int(num) for num in input("Enter the knight's starting position: ").split()]
    except ValueError or TypeError:
        print("Invalid dimensions!")
    else:
        if x < 1 or x > X or y < 1 or y > Y:
            print("Invalid dimensions!")
        else:
            break


# --------------------- 3. Clarify the mode: play or show answer ------------------- #
while True:
    mode = input("Do you want to try the puzzle? (y/n): ").strip()
    if mode == "y" or mode == "n":
        break
    else:
        print("Invalid input!")


# -------------------------------- 4. Start the puzzle ------------------------------- #
solution = find_solution(board, x, y)
if solution:
    if mode == "y":
        new_board = Board(X, Y)
        play_game(new_board, x, y)
    else:
        print("Here's the solution!")
        board.present()

else:
    print("No solution exists!")