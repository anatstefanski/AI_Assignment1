from dataclasses import dataclass
from typing import Optional, Tuple

# Define the State dataclass to represent each state in the BFS
@dataclass
class State:
    board: Tuple[int, ...]  
    parent_index: Optional[int] #Index of the parent state in the visited list
    operator: Optional[str]  #'U', 'D', 'L', 'R' or None

def get_neighbors(board: Tuple[int, ...], n: int, parent_index: int) :
    neighbors = []
    zero_index = board.index(0) #Find the index of the empty tile (0)
#up
    if 0<= zero_index - n:
        new_board = list(board)
        new_board[zero_index], new_board[zero_index - n] = new_board[zero_index - n], new_board[zero_index]
        neighbors.append(State(tuple(new_board), parent_index, "U"))
#down
    if zero_index + n < len(board):
        new_board = list(board)
        new_board[zero_index], new_board[zero_index + n] = new_board[zero_index + n], new_board[zero_index]
        neighbors.append(State(tuple(new_board), parent_index, "D"))
#left
    if 0 <= zero_index - 1 and zero_index % n != 0 :
        new_board = list(board)
        new_board[zero_index], new_board[zero_index - 1] = new_board[zero_index - 1], new_board[zero_index]
        neighbors.append(State(tuple(new_board), parent_index, "L"))
#right
    if (zero_index + 1) < len(board) and zero_index % n != n-1:
        new_board = list(board)
        new_board[zero_index], new_board[zero_index + 1] = new_board[zero_index + 1], new_board[zero_index]
        neighbors.append(State(tuple(new_board), parent_index, "R"))

    return neighbors


def solve(start_state, n):
        # Define the goal state
        goal_state = tuple(range(1,n*n)) + (0,)
        s_start =State(board=start_state, parent_index=None, operator=None)
       # Initialize the BFS queue and visited list
        queue = [s_start]
        visited = list()
        solution = []

        while queue:
            cur_state = queue.pop(0)
            visited.append(cur_state)

            # Check if we have reached the goal state
            if (cur_state.board==goal_state):
                while cur_state.parent_index is not None:
                    solution.append(cur_state.operator)
                    cur_state = visited[cur_state.parent_index]
                solution.reverse() #Reverse the solution to get the correct order
                return solution
            
            # Generate neighbors
            for neighbor in get_neighbors(cur_state.board, n,len(visited)-1):
                if neighbor.board not in {state.board for state in visited} :
                    queue.append(neighbor)   

        return solution 
