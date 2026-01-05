def read_input(path="input.txt"):
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip() != ""]
    algo = int(lines[0])
    n = int(lines[1])
    board = tuple(int(x) for x in lines[2].split("-"))
    return algo, n, board


def write_output(solution, path="output.txt"):
    with open(path, "w", encoding="utf-8") as f:
        f.write(solution)


def main():
    algo, n, board = read_input()
    # בדיקה זמנית: כרגע אין אלגוריתמים, אז רק נכתוב משהו
    print("algo =", algo)
    print("n =", n)
    print("board =", board)

    write_output("NOT_IMPLEMENTED")


if __name__ == "__main__":
    main()
