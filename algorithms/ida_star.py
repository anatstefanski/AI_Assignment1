from typing import Tuple, List, Set, Dict


OPS_ORDER = ['U', 'D', 'L', 'R']


def _goal_state(n: int) -> Tuple[int, ...]:
    return tuple(list(range(1, n * n)) + [0])


def _goal_positions(n: int) -> Dict[int, int]:
    """Map tile -> its index in the goal state (for Manhattan)."""
    goal = _goal_state(n)
    return {v: i for i, v in enumerate(goal)}


def _manhattan(state: Tuple[int, ...], n: int, goal_pos: Dict[int, int]) -> int:
    """Manhattan distance heuristic (ignores tile 0)."""
    dist = 0
    for idx, v in enumerate(state):
        if v == 0:
            continue
        g = goal_pos[v]
        r1, c1 = divmod(idx, n)
        r2, c2 = divmod(g, n)
        dist += abs(r1 - r2) + abs(c1 - c2)
    return dist


def _neighbors_udlr(state: Tuple[int, ...], n: int):
    """
    Generate neighbors in U,D,L,R order.
    Move letter describes the numbered tile moving into the empty space.
    """
    z = state.index(0)
    zr, zc = divmod(z, n)

    cand = []
    if zr < n - 1:  # U: tile below moves up
        cand.append(('U', (zr + 1) * n + zc))
    if zr > 0:      # D: tile above moves down
        cand.append(('D', (zr - 1) * n + zc))
    if zc < n - 1:  # L: tile right moves left
        cand.append(('L', zr * n + (zc + 1)))
    if zc > 0:      # R: tile left moves right
        cand.append(('R', zr * n + (zc - 1)))

    order = {op: i for i, op in enumerate(OPS_ORDER)}
    cand.sort(key=lambda x: order[x[0]])

    for op, tile_idx in cand:
        lst = list(state)
        lst[z], lst[tile_idx] = lst[tile_idx], lst[z]
        yield op, tuple(lst)


def _ida_dfs(state: Tuple[int, ...],
             goal: Tuple[int, ...],
             n: int,
             goal_pos: Dict[int, int],
             g: int,
             threshold: int,
             path: List[str],
             open_set: Set[Tuple[int, ...]],
             close_set: Set[Tuple[int, ...]]):
   
   # IDA* DFS with f=g+h cutoff.
   # Returns: (found, solution_str, next_threshold)
   
    f = g + _manhattan(state, n, goal_pos)
    if f > threshold:
        return False, None, f
    if state == goal:
        return True, ''.join(path), threshold

    close_set.add(state)

    min_over = float('inf')
    for op, nxt in _neighbors_udlr(state, n):
        # Skip if already in OPEN (current path) or CLOSE (this iteration)
        if nxt in open_set or nxt in close_set:
            continue

        path.append(op)
        open_set.add(nxt)

        found, sol, t = _ida_dfs(nxt, goal, n, goal_pos, g + 1, threshold, path, open_set, close_set)
        if found:
            return True, sol, threshold

        if t < min_over:
            min_over = t

        open_set.remove(nxt)
        path.pop()

    return False, None, min_over


def solve(start_state, n):
    """Entry point called by main.py."""
    start = tuple(start_state)
    goal = _goal_state(n)
    if start == goal:
        return ""

    goal_pos = _goal_positions(n)
    threshold = _manhattan(start, n, goal_pos)

    while True:
        path: List[str] = []
        open_set: Set[Tuple[int, ...]] = {start}
        close_set: Set[Tuple[int, ...]] = set()

        found, sol, next_t = _ida_dfs(start, goal, n, goal_pos, 0, threshold, path, open_set, close_set)
        if found:
            return sol
        if next_t == float('inf'):
            return ""
        threshold = next_t
