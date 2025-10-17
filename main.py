TEST_PUZZLE = [
    [5,3,0, 0,7,0, 0,0,0],
    [6,0,0, 1,9,5, 0,0,0],
    [0,9,8, 0,0,0, 0,6,0],

    [8,0,0, 0,6,0, 0,0,3],
    [4,0,0, 8,0,3, 0,0,1],
    [7,0,0, 0,2,0, 0,0,6],

    [0,6,0, 0,0,0, 2,8,0],
    [0,0,0, 4,1,9, 0,0,5],
    [0,0,0, 0,8,0, 0,7,9],
]

def solve(puzzle):
    options = [[set() for _ in range(9)] for _ in range(9)]
    row_used_nums = [{n for n in row if n != 0} for row in puzzle]
    column_used_nums = [{row[i] for row in puzzle if row[i] != 0} for i in range(9)]
    box_used_nums = [set() for _ in range(9)]

    box_num = 0
    for row_start in range(0,9,3):
        for col_start in range(0,9,3):
            for i in range(row_start, row_start+3):
                box_used_nums[box_num].update(puzzle[i][col_start:col_start+3])
            box_used_nums[box_num].discard(0)
            box_num += 1

    for i in range(9):
        for j in range(9):
            box_num = (i//3)*3 + j//3
            if puzzle[i][j] == 0:
                options[i][j] = [n for n in range(1, 10) if n not in row_used_nums[i] | column_used_nums[j] | box_used_nums[box_num]]
                if len(options[i][j]) == 1:
                    puzzle[i][j] = options[i][j][0]
                    options[i][j].clear()
                    solve(puzzle)
                
    return puzzle

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
If you make it to the end and none have only 1 option, find the first with 2 (or 3, 4, etc) and divert

row 4, column 7 -> box 5

0, 1, 2 -> 0
3, 4, 5 -> 3
6, 7, 8 -> 6
'''