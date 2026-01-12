from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict
import heapq
@dataclass
class State:
    board: Tuple[int, ...]
    parent_index: Optional[int]   
    operator: Optional[str]       
    g: int                        
    f: int                        

def manhattan(board: Tuple[int, ...], n: int, goal_pos: Dict[int, int]) -> int:
    dist = 0
    for i, v in enumerate(board):
        if v == 0:
            continue
        gi = goal_pos[v]
        r1, c1 = divmod(i, n)
        r2, c2 = divmod(gi, n)
        dist += abs(r1 - r2) + abs(c1 - c2)
    return dist



def get_neighbors(
    board: Tuple[int, ...],
    n: int,
    parent_index: int,
    g: int,
    goal_pos: Dict[int, int]
) -> List[State]:

    neighbors: List[State] = []
    zero_index = board.index(0)
    zr, zc = divmod(zero_index, n)

   
    if zr < n - 1:
        nb = list(board)
        idx = (zr + 1) * n + zc
        nb[zero_index], nb[idx] = nb[idx], nb[zero_index]
        nb_t = tuple(nb)
        h = manhattan(nb_t, n, goal_pos)
        neighbors.append(State(nb_t, parent_index, 'D', g + 1, g + 1 + h))


    if zr > 0:
        nb = list(board)
        idx = (zr - 1) * n + zc
        nb[zero_index], nb[idx] = nb[idx], nb[zero_index]
        nb_t = tuple(nb)
        h = manhattan(nb_t, n, goal_pos)
        neighbors.append(State(nb_t, parent_index, 'U', g + 1, g + 1 + h))


    if zc < n - 1:
        nb = list(board)
        idx = zr * n + (zc + 1)
        nb[zero_index], nb[idx] = nb[idx], nb[zero_index]
        nb_t = tuple(nb)
        h = manhattan(nb_t, n, goal_pos)
        neighbors.append(State(nb_t, parent_index, 'R', g + 1, g + 1 + h))

 
    if zc > 0:
        nb = list(board)
        idx = zr * n + (zc - 1)
        nb[zero_index], nb[idx] = nb[idx], nb[zero_index]
        nb_t = tuple(nb)
        h = manhattan(nb_t, n, goal_pos)
        neighbors.append(State(nb_t, parent_index, 'L', g + 1, g + 1 + h))

    return neighbors



def solve(start_state, n):
    start = tuple(start_state)
    goal = tuple(range(1, n * n)) + (0,)

    if start == goal:
        return ""


    goal_pos = {v: i for i, v in enumerate(goal)}

    open_heap = []
    visited: List[State] = []
    open_best: Dict[Tuple[int, ...], int] = {}
    closed = set()

    counter = 0

    h0 = manhattan(start, n, goal_pos)
    start_state_obj = State(start, None, None, 0, h0)

    heapq.heappush(open_heap, (start_state_obj.f, counter, start_state_obj))
    open_best[start] = start_state_obj.f
    counter += 1

    while open_heap:
        _, _, current = heapq.heappop(open_heap)

        if current.board in closed:
            continue

        visited.append(current)
        cur_index = len(visited) - 1

    
        if current.board == goal:
            path = []
            while current.parent_index is not None:
                path.append(current.operator)
                current = visited[current.parent_index]
            path.reverse()
            return "".join(path)

        closed.add(current.board)

        for neighbor in get_neighbors(
            current.board, n, cur_index, current.g, goal_pos
        ):
            if neighbor.board in closed:
                continue

            if (neighbor.board not in open_best or
                    neighbor.f < open_best[neighbor.board]):
                open_best[neighbor.board] = neighbor.f
                heapq.heappush(open_heap, (neighbor.f, counter, neighbor))
                counter += 1

    return ""
