def solve(start_state, n):
    """
    IDS (Iterative Deepening Search)
    Returns a string of moves using 'U','D','L','R'
    """
    #Builds a goal board
    goal = tuple(list(range(1, n * n)) + [0])

    #If already solved
    if start_state == goal:
        return ""

    depth_limit = 0
    while True:
        close_list = set()

        # OPEN list concept for DFS = current path (to avoid loops)
        path_set = {start_state}

        # Run depth-limited DFS
        result = _dls(start_state, n, goal, depth_limit, "", path_set, close_list)

        # If found a solution, return it
        if result is not None:
            return result

        # Otherwise, try deeper
        depth_limit += 1


def _dls(state, n, goal, limit, path, path_set, closed):
    """
    Depth-Limited Search (DFS with depth limit)
    Returns path string if found, else None
    """

    # A) Goal test
    if state == goal:
        return path

    # B) If no depth left, stop
    if limit == 0:
        return None

    # C) Mark this node as expanded in this iteration (CLOSE)
    closed.add(state)

    # D) Expand children in REQUIRED order: U, D, L, R
    for next_state, move_char in _successors_udlr(state, n):

        # Requirement: if child is in OPEN or CLOSE -> do not insert
        if next_state in path_set or next_state in closed:
            continue

        # Add to current path (OPEN)
        path_set.add(next_state)

        # Recurse deeper with limit-1, and append move char to path
        res = _dls(next_state, n, goal, limit - 1, path + move_char, path_set, closed)
        if res is not None:
            return res

        # Backtrack: remove from current path
        path_set.remove(next_state)

    # No solution found within this subtree at this limit
    return None


def _successors_udlr(board, n):
    """
    Generate successors in the required order:
    Up, Down, Left, Right  (U, D, L, R)
    Returns list of (new_board, move_char)
    """

    successors = []

    zero_index = board.index(0)
    row = zero_index // n
    col = zero_index % n

    # U: swap 0 with tile above
    if row > 0:
        swap_index = zero_index - n
        new_board = list(board)
        new_board[zero_index], new_board[swap_index] = new_board[swap_index], new_board[zero_index]
        successors.append((tuple(new_board), "U"))

    # D: swap 0 with tile below
    if row < n - 1:
        swap_index = zero_index + n
        new_board = list(board)
        new_board[zero_index], new_board[swap_index] = new_board[swap_index], new_board[zero_index]
        successors.append((tuple(new_board), "D"))

    # L: swap 0 with tile to the left
    if col > 0:
        swap_index = zero_index - 1
        new_board = list(board)
        new_board[zero_index], new_board[swap_index] = new_board[swap_index], new_board[zero_index]
        successors.append((tuple(new_board), "L"))

    # R: swap 0 with tile to the right
    if col < n - 1:
        swap_index = zero_index + 1
        new_board = list(board)
        new_board[zero_index], new_board[swap_index] = new_board[swap_index], new_board[zero_index]
        successors.append((tuple(new_board), "R"))

    return successors

