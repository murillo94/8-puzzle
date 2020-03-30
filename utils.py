def draw_path(path):
    print(path)
    print("  | ")
    print("  | ")
    print(" \\\'/ \n")


def manhattan(puzzle):
    return get_current_and_target_position_from_puzzle(
        puzzle,
        lambda r, tr, c, tc: abs(
            tr - r) + abs(tc - c),
        lambda t: t
    )


def manhattan_lsq(puzzle):
    import math
    return get_current_and_target_position_from_puzzle(
        puzzle,
        lambda r, tr, c, tc: (
            abs(tr - r) + abs(tc - c))**2,
        lambda t: math.sqrt(t)
    )


def linear(puzzle):
    import math
    return get_current_and_target_position_from_puzzle(
        puzzle,
        lambda r, tr, c, tc: math.sqrt(
            math.sqrt((tr - r)**2 + (tc - c)**2)),
        lambda t: t
    )


def linear_lsq(puzzle):
    import math
    return get_current_and_target_position_from_puzzle(
        puzzle,
        lambda r, tr, c, tc: (
            tr - r)**2 + (tc - c)**2,
        lambda t: math.sqrt(t)
    )


def convert_plain_text_to_list(plain_text):
    puzzle_list = []
    for line in plain_text:
        puzzle_list.append(line.rstrip('\n').split(" "))
        for x, list1 in enumerate(puzzle_list):
            for y, item in enumerate(list1):
                list1[y] = int(item)

    return puzzle_list


def convert_index_to_non_found(item, seq):
    if item in seq:
        return seq.index(item)
    return -1


def get_current_and_target_position_from_puzzle(puzzle, item_total_calc, total_calc):
    t = 0
    for row in range(3):
        for col in range(3):
            val = puzzle.get_value_from_specified_row_and_column_in_puzzle(
                row, col) - 1
            target_col = val % 3
            target_row = val / 3

            if target_row < 0:
                target_row = 2

            t += item_total_calc(row, target_row, col, target_col)
    return total_calc(t)
