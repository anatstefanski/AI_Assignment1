import re
from algorithms.ids import solve as ids_solve
from algorithms.bfs import solve as bfs_solve
from algorithms.a_star import solve as astar_solve
from algorithms.ida_star import solve as idastar_solve
from algorithms.dfs import solve as dfs_solve

#Reading from the file
def read_input(path="input.txt"):
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip() != ""]
    number_algo = int(lines[0]) #Number of the algorithm
    n = int(lines[1]) #Size of the board
    nums = re.findall(r'-?\d+', lines[2])
    board = tuple(int(x) for x in nums) #The board
    return number_algo, n, board

def validate_input(number_algo, n, board):
    # number_algo
    if number_algo not in {1, 2, 3, 4, 5}:
        return "Invalid algorithm number"

    # n
    if n <= 0:
        return "Board size must be a positive integer"

    # board length
    if len(board) != n * n:
        return "Invalid board size"

    # values range + duplicates
    max_val = n * n - 1
    seen = set()
    for x in board:
        if x < 0 or x > max_val:
            return "There is an invalid number on the board"
        if x in seen:
            return "There are duplicates in the board"
        seen.add(x)

    return None


#Writing to the file
def write_output(solution, path="output.txt"):
    with open(path, "w", encoding="utf-8") as f:
        f.write(str(solution))

#Main function
def main():
    #Validating on the txt file
    try:
        number, n, board = read_input()
    except FileNotFoundError:
        write_output("Input file not found")
        return
    except IndexError:
        write_output("Input file format is invalid")
        return
    except ValueError:
        write_output("Input file contains non-numeric values")
        return
    
    error = validate_input(number, n, board)
    if error is not None:
        write_output(error)
        return

    #Mapping algorithm numbers to functions
    solvers = {
        1: ids_solve,
        2: bfs_solve,
        3: astar_solve,
        4: idastar_solve,
        5: dfs_solve,
    }
    
    #Calling the appropriate solver
    solution = solvers[number](board, n)
    write_output(solution)


if __name__ == "__main__":
    main()
