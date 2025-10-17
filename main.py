import copy

TEST_PUZZLE = [
    [0,0,0, 0,0,0, 0,1,2],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,1, 0,0,0, 0,0,0],

    [0,0,0, 0,0,7, 0,0,0],
    [0,0,0, 0,6,0, 0,0,0],
    [0,0,0, 0,0,0, 3,0,0],

    [5,0,0, 0,0,0, 0,0,0],
    [0,0,0, 4,0,0, 0,0,0],
    [0,7,0, 0,0,0, 0,0,0],
]

def solve(puzzle):
    options = [[list() for _ in range(9)] for _ in range(9)]

    deterministic = True
    while deterministic:
        deterministic_num_found = False
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
                            deterministic_num_found = True
                else:
                    nonzero_count += 1

        if nonzero_count == 81:
            return puzzle
        
        if not deterministic_num_found:
            deterministic = False

    for num_options in range(2,10):
        for i in range(9):
            for j in range(9):
                box_num = (i//3)*3 + j//3
                options[i][j] = [n for n in range(1, 10) if n not in row_used_nums[i] | col_used_nums[j] | box_used_nums[box_num]]
                if len(options[i][j]) == num_options:
                    for option in options[i][j]:
                        new_puzzle = copy.deepcopy(puzzle)
                        new_puzzle[i][j] = option
                        print(f"Trying {option} at row {i+1} column {j+1}")
                        try:
                            return solve(new_puzzle)
                        except ValueError:
                            pass
    
    raise ValueError("Sudoku is not solvable")
            

if __name__ == "__main__":
    solved_puzzle = solve(TEST_PUZZLE)
    for line in solved_puzzle:
        for start in range(0,9,3):
            print(' '.join([str(line[i]) for i in range(start, start+3)]), end="  ")
        print()

'''
Find the first 0
Store each possible number (compare to row, column, and box)
If there's only 1 option, set it to that and update earlier options
If there's more than 1, store the possibilities
If you make it to the end and none have only 1 option, find the first with 2 (or 3, 4, etc)
Pick the first option and try solving the puzzle with it
*** Exclude that slot from diverting again or it gets stuck in a loop
'''