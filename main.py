import copy

def MRV(puzzle, options):
    min_options = 10
    best_cell = None
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == 0:
                num_options = len(options[row, col])
                if num_options < min_options:
                    min_options = num_options
                    best_cell = (row, col)

    return best_cell


def solve(puzzle):
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

    slot_solved = True
    while slot_solved:
        slot_solved = False
        options = dict()
        for row in range(9):
            for col in range(9):
                if puzzle[row][col] == 0:
                    box = (row//3)*3 + col//3
                    options[row, col] = [n for n in range(1, 10) if n not in row_used_nums[row] | col_used_nums[col] | box_used_nums[box]]

                    if len(options[row, col]) == 0:
                        raise ValueError("Puzzle is not solvable")   
                    
                    elif len(options[row, col]) == 1:
                        value = options[row, col][0]
                        puzzle[row][col] = value
                        row_used_nums[row].add(value)
                        col_used_nums[col].add(value)
                        box_used_nums[box].add(value)
                        slot_solved = True
                        break
            if slot_solved:
                break

        if all(puzzle[r][c] != 0 for r in range(9) for c in range(9)):
            return puzzle

    row, col = MRV(puzzle, options)
    for option in options[row, col].copy():
        new_puzzle = copy.deepcopy(puzzle)
        new_puzzle[row][col] = option
        try:
            return solve(new_puzzle)
        except ValueError:
            continue

    raise ValueError("Puzzle is not solvable")


def main():
    while True:
        user_nums = input(f"Input puzzle as comma-separated integers: ").strip().split(",")
        if len(user_nums) != 81:
            print("Invalid puzzle: Must have 81 slots")
            continue
        
        try: 
            nums = [int(num.strip()) for num in user_nums]
        except ValueError:
            print("Invalid puzzle: Slots must be integers")
            continue
    
        if any(num < 0 or num > 9 for num in nums):
            print("Invalid puzzle: Numbers must be between 0 and 9")
            continue

        puzzle = [nums[9*i:9*i+9] for i in range(9)]
        break

    try:
        solved_puzzle = solve(puzzle)
    except ValueError:
        print("Puzzle is not solvable")
        return
    
    print("\nSolved puzzle:")
    for i, line in enumerate(solved_puzzle):
        for start in range(0,9,3):
            print(" ".join([str(line[j]) for j in range(start, start+3)]), end="  ")
        if (i+1) % 3 == 0 and i < 8:
            print("\n")
        else:
            print()    

if __name__ == "__main__":
    main()