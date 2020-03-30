from utils import manhattan, manhattan_lsq, linear, linear_lsq, convert_plain_text_to_list, convert_index_to_non_found, draw_path


class EightPuzzle:
    def __init__(self):
        self.value = 0
        self.current_depth = 0
        self.parent_node = None

        with open("puzzle.txt", "r") as puzzle:
            self.puzzle = convert_plain_text_to_list(puzzle)

        with open("goal.txt", "r") as puzzle_goal:
            self.puzzle_goal = convert_plain_text_to_list(puzzle_goal)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.puzzle == other.puzzle

    def __str__(self):
        res = ''
        for row in range(3):
            res += ' '.join(map(str, self.puzzle[row]))
            res += '\r\n'
        return res

    def clone_puzzle(self):
        puzzle = EightPuzzle()
        for i in range(3):
            puzzle.puzzle[i] = self.puzzle[i][:]
        return puzzle

    def get_legal_moves(self):
        legal_moves = []
        row, col = self.get_row_and_column_from_specified_value_in_graph(0)

        if row > 0:
            legal_moves.append((row - 1, col))
        if col > 0:
            legal_moves.append((row, col - 1))
        if row < 2:
            legal_moves.append((row + 1, col))
        if col < 2:
            legal_moves.append((row, col + 1))

        return legal_moves

    def get_moves(self):
        legal_moves = self.get_legal_moves()
        zero_in_graph = self.get_row_and_column_from_specified_value_in_graph(
            0)

        def swap_and_clone(a, b):
            clone_puzzle = self.clone_puzzle()
            clone_puzzle.swap_value_to_specified_coordinate(a, b)
            clone_puzzle.current_depth = self.current_depth + 1
            clone_puzzle.parent_node = self
            return clone_puzzle

        return map(lambda pair: swap_and_clone(zero_in_graph, pair), legal_moves)

    def get_solution_path(self, path):
        if self.parent_node == None:
            return path
        path.append(self)
        return self.parent_node.get_solution_path(path)

    def get_row_and_column_from_specified_value_in_graph(self, value):
        if value < 0 or value > 8:
            raise Exception("Incorrect value. Values must be between 0 and 8.")

        for row in range(3):
            for col in range(3):
                if self.puzzle[row][col] == value:
                    return row, col

    def get_value_from_specified_row_and_column_in_puzzle(self, row, col):
        return self.puzzle[row][col]

    def poke_value_to_specified_row_and_column(self, row, col, value):
        self.puzzle[row][col] = value

    def swap_value_to_specified_coordinate(self, a, b):
        temp = self.get_value_from_specified_row_and_column_in_puzzle(*a)
        self.poke_value_to_specified_row_and_column(
            a[0], a[1], self.get_value_from_specified_row_and_column_in_puzzle(*b))
        self.poke_value_to_specified_row_and_column(b[0], b[1], temp)

    def solver(self, fn_solver):
        def puzzle_is_solved(puzzle):
            return puzzle.puzzle == self.puzzle_goal

        open_graph = [self]
        close_graph = []
        move_count = 0
        while len(open_graph) > 0:
            open_graph_value = open_graph.pop(0)
            move_count += 1
            if (puzzle_is_solved(open_graph_value)):
                if len(close_graph) > 0:
                    return open_graph_value.get_solution_path([]), move_count
                return [open_graph_value]

            open_graph_moves = open_graph_value.get_moves()
            index_open = index_closed = -1
            for move in open_graph_moves:
                index_open = convert_index_to_non_found(move, open_graph)
                index_closed = convert_index_to_non_found(move, close_graph)
                value = fn_solver(move)
                fn_result = value + move.current_depth

                if index_closed == -1 and index_open == -1:
                    move.value = value
                    open_graph.append(move)
                elif index_open > -1:
                    copy = open_graph[index_open]
                    if fn_result < copy.value + copy.current_depth:
                        copy.value = value
                        copy.parent_node = move.parent_node
                        copy.current_depth = move.current_depth
                elif index_closed > -1:
                    copy = close_graph[index_closed]
                    if fn_result < copy.value + copy.current_depth:
                        move.value = value
                        close_graph.remove(copy)
                        open_graph.append(move)

            close_graph.append(open_graph_value)
            open_graph = sorted(
                open_graph, key=lambda graph: graph.value + graph.current_depth
            )
        return [], 0


def main():
    puzzle = EightPuzzle()

    paths, count = puzzle.solver(manhattan)
    paths.reverse()

    print("Graph solved:\n")
    for path in paths:
        draw_path(path)

    print("Manhattan:")
    print("- distance exploring", count, "states")

    (path, count) = puzzle.solver(manhattan_lsq)
    print("- least squares exploring", count, "states\n")

    print("Linear:")
    (path, count) = puzzle.solver(linear)
    print("- distance exploring", count, "states")

    (path, count) = puzzle.solver(linear_lsq)
    print("- least squares exploring", count, "states\n")


if __name__ == "__main__":
    main()
