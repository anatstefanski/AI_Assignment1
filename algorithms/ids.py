# IDS: Iterative Deepening Search
# Runs depth-limited DFS with depth_limit = 0,1,2,... until solution is found
def solve(start_state, n):
    
    #Builds a goal board
    goal = tuple(list(range(1, n * n)) + [0])

    #If already solved
    if start_state == goal:
        return ""

    #maximum depth limit 
    depth_limit = 0
    while True:
        close_list = set()

        # OPEN list 
        open_list = {start_state}
        result = _dls(start_state, n, goal, depth_limit, "", open_list, close_list)
        # if found a solution, return it,else try deeper
        if result is not None:
            return result
        depth_limit += 1

# opened = states in the current DFS path (OPEN)
# closed = states expanded in this depth iteration (CLOSE)
# Depth-Limited Search
def _dls(state, n, goal, limit, path, opened, closed):

    # Goal test
    if state == goal:
        return path

    #If no depth left, stop
    if limit == 0:
        return None

    closed.add(state)

    #Expand children in REQUIRED order: U, D, L, R
    for next_state, move_char in _udlr_moves(state, n):

        #if child is in OPEN or CLOSE ->no insert
        if next_state in opened or next_state in closed:
            continue

        opened.add(next_state)

        # Recurse deeper with limit-1, and append move char to path
        res = _dls(next_state, n, goal, limit - 1, path + move_char, opened, closed)
        if res is not None:
            return res

        #remove from current path
        opened.remove(next_state)

    # No solution 
    return None

# Generates all legal moves of the blank tile (0)
# Returns successor board states with their move labels in U, D, L, R order
def _udlr_moves(board, n):
   
    successors = []
    # Find the index of 0
    zero_index = board.index(0)
    row = zero_index // n
    col = zero_index % n

    # U: If 0 is not on the top row → up.
    if row > 0:
        swap_index = zero_index - n
        new_board = list(board)
        new_board[zero_index], new_board[swap_index] = new_board[swap_index], new_board[zero_index]
        successors.append((tuple(new_board), "U"))

    # D: If 0 is not on the bottom row → down.
    if row < n - 1:
        swap_index = zero_index + n
        new_board = list(board)
        new_board[zero_index], new_board[swap_index] = new_board[swap_index], new_board[zero_index]
        successors.append((tuple(new_board), "D"))

    # L: If 0 is not on the left column → left.
    if col > 0:
        swap_index = zero_index - 1
        new_board = list(board)
        new_board[zero_index], new_board[swap_index] = new_board[swap_index], new_board[zero_index]
        successors.append((tuple(new_board), "L"))

    # R: If 0 is not on the right column → right
    if col < n - 1:
        swap_index = zero_index + 1
        new_board = list(board)
        new_board[zero_index], new_board[swap_index] = new_board[swap_index], new_board[zero_index]
        successors.append((tuple(new_board), "R"))

    return successors

