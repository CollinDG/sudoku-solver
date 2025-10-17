import copy

HARD_PUZZLE = [
    [0,0,1, 0,6,2, 0,0,0],
    [0,0,0, 3,0,0, 0,0,0],
    [4,0,0, 8,1,0, 0,0,0],

    [2,0,0, 0,0,3, 7,0,0],
    [7,3,0, 1,2,0, 5,9,0],
    [6,0,0, 4,9,0, 1,0,0],

    [1,0,0, 0,0,5, 6,0,3],
    [0,0,0, 0,0,8, 0,0,0],
    [5,0,0, 9,3,0, 0,0,0],
]

def solve_deterministic(puzzle, options, row_used_nums, col_used_nums, box_used_nums):
    deterministic = True
    while deterministic:
        deterministic_value_found = False
        nonzero_count = 0    
        for i in range(9):
            for j in range(9):
                box_num = (i//3)*3 + j//3
                if puzzle[i][j] == 0:
                    options[i][j] = [n for n in range(1, 10) if n not in row_used_nums[i] | col_used_nums[j] | box_used_nums[box_num]]
                    match len(options[i][j]):
                        case 0:
                            raise ValueError("Sudoku is not solvable")
                        case 1:
                            value = options[i][j][0]
                            puzzle[i][j] = value
                            row_used_nums[i].add(value)
                            col_used_nums[j].add(value)
                            box_used_nums[box_num].add(value)
                            options[i][j] = []
                            deterministic_value_found = True
                else:
                    nonzero_count += 1

        if nonzero_count == 81:
            return puzzle, True
        elif not deterministic_value_found:
            return puzzle, False


def solve(puzzle, tried_values={}):
    options = [[set() for _ in range(9)] for _ in range(9)]
    row_used_nums = [{n for n in row if n != 0} for row in puzzle]
    col_used_nums = [{row[i] for row in puzzle if row[i] != 0} for i in range(9)]
    box_used_nums = [set() for _ in range(9)]

    box_num = 0
    for row_start in range(0,9,3):
        for col_start in range(0,9,3):
            for i in range(row_start, row_start+3):
                box_used_nums[box_num].update(puzzle[i][col_start:col_start+3])
            box_used_nums[box_num].discard(0)
            box_num += 1
    
    puzzle, solved = solve_deterministic(puzzle, options, row_used_nums, col_used_nums, box_used_nums)

    if solved:
        return puzzle

    for num_options in range(2,10):
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] == 0:
                    pos = (i,j)
                    if pos not in tried_values:
                        tried_values[pos] = set()

                    box_num = (i//3)*3 + j//3
                    options[i][j] = [n for n in range(1, 10) 
                                    if n not in row_used_nums[i] | col_used_nums[j] | box_used_nums[box_num]
                                    and n not in tried_values[pos]]
                    
                    if len(options[i][j]) == num_options:
                        for option in options[i][j]:
                            tried_values[pos].add(option)
                            new_puzzle = copy.deepcopy(puzzle)
                            new_puzzle[i][j] = option
                            try:
                                return solve(new_puzzle, tried_values)
                            except ValueError:
                                pass
    
    raise ValueError("Sudoku is not solvable")
            

if __name__ == "__main__":
    solved_puzzle = solve(HARD_PUZZLE)
    print("\nSolved puzzle:\n")
    for i, line in enumerate(solved_puzzle):
        for start in range(0,9,3):
            print('  '.join([str(line[i]) for i in range(start, start+3)]), end="   ")
        if (i+1) % 3 == 0:
            print("\n")
        else:
            print()