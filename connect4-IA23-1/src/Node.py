import Connect4


class node:
    """Class to model the nodes for the search model."""

    def __init__(self, connect4, current_player: int, parent=None, height: int = 0) -> None:
        """Constructor of a node"""
        assert type(connect4) == Connect4.connect4
        assert type(current_player) == int
        assert height >= 0
        assert current_player == 1 or current_player == 2
        self.__connect4 = Connect4.connect4(False, connect4.get_board())
        self.__children = []
        self.__current_player = current_player
        self.__parent = parent
        self.__heuristic = 0
        self.__height = height

    def __str__(self) -> str:
        return str(self.__connect4) + "\nplayer: " + str(self.__current_player) + ", height: " + str(self.__height) + ", heuristic: " + str(self.__heuristic) + "\n\n"

    def expand(self) -> None:
        """Function to expand this node. Won't expand finished games"""
        if self.__connect4.finished() != 0:
            return
        next_player = 1 if self.__current_player == 2 else 2
        for play in self.__connect4.possible_plays():
            copy = Connect4.connect4(False, self.__connect4.get_board())
            copy.make_play(True if next_player == 1 else False, play)
            new_node = node(copy, next_player, self, self.__height + 1)
            new_node.__heuristic = self.heuristic(new_node, play)
            self.__children.append((new_node, play))

    def heuristic(self, next_node, move):
        """Heuristic of a play, the better the play the higher value."""
        board = next_node.__connect4.get_board()
        row = 0
        while row < 5 and board[row][move] == 0:
            row += 1
        player = board[row][move]
        assert player != 0
        if next_node.__connect4.finished() == player:
            return 1000000000
        return self.__check_contiguous(row, move, player, board)

    def __check_contiguous(self, row: int, column: int, player: int, board: list) -> int:
        """Aux private function to check for contiguous chips of the player."""
        contiguous = 0
        # down
        mult = 1
        curr_row = row + 1
        while curr_row < 6 and board[curr_row][column] == player:
            contiguous += mult
            mult += 4
            curr_row += 1

        # left
        mult = 1
        curr_col = column - 1
        while curr_col > -1 and board[row][curr_col] == player:
            contiguous += mult
            mult += 4
            curr_col -= 1

        # right
        mult = 1
        curr_col = column + 1
        while curr_col < 7 and board[row][curr_col] == player:
            contiguous += mult
            mult += 4
            curr_col += 1

        # up-right
        mult = 1
        curr_row = row - 1
        curr_col = column + 1
        while curr_col < 7 and curr_row > -1 and board[curr_row][curr_col] == player:
            contiguous += mult
            mult += 4
            curr_row -= 1
            curr_col += 1

        # up-left
        mult = 1
        curr_row = row - 1
        curr_col = column - 1
        while curr_col > -1 and curr_row > -1 and board[curr_row][curr_col] == player:
            contiguous += mult
            mult += 4
            curr_row -= 1
            curr_col -= 1

        # down-right
        mult = 1
        curr_row = row + 1
        curr_col = column + 1
        while curr_col < 7 and curr_row < 6 and board[curr_row][curr_col] == player:
            contiguous += mult
            mult += 4
            curr_row += 1
            curr_col += 1

        # down-left
        mult = 1
        curr_row = row + 1
        curr_col = column - 1
        while curr_col > -1 and curr_row < 6 and board[curr_row][curr_col] == player:
            contiguous += mult
            mult += 4
            curr_row += 1
            curr_col -= 1
        return contiguous

    def get_children(self) -> list:
        """Function to get the children of this node."""
        return self.__children

    def get_height(self) -> int:
        """Function to get the height of this node."""
        return self.__height

    def get_parent(self):
        """Function to get the parent of this node."""
        return self.__parent

    def get_heuristic(self) -> int:
        """Function to get the heuristic of this node."""
        return self.__heuristic

    def get_current_player(self) -> int:
        """Function to get the current player of this node."""
        return self.__current_player

    def get_board(self) -> list:
        """Function to get the board of this node."""
        return self.__connect4.get_board()

    def height_4_tree(self) -> None:
        """This node is taken as root and generates a tree of all the posible
        moves 4 shifts ahead using a limited (by height) breadth first search.
        """
        queue = [self]
        expected_height = self.__height + 4
        nodes = {self.__height: [self], self.__height +
                 1: [], self.__height + 2: [], self.__height + 3: []}
        while queue != []:
            curr_node = queue.pop(0)
            if curr_node.get_children() == []:
                curr_node.expand()
            for (child, _) in curr_node.get_children():
                if child.__height < expected_height:
                    queue.append(child)
                    nodes[child.__height].append(child)

        levels = [3, 2, 1, 0]
        for level in levels:
            # update heuristic of nodes of that level
            for inner_node in nodes[self.__height + level]:
                for (child, _) in inner_node.get_children():
                    inner_node.__heuristic -= child.__heuristic * .2

    def get_all_leaves(self) -> list:
        """Returns all the leaves of this subtree."""
        leaves = []
        queue = []
        queue.append(self)
        while queue != []:
            curr_node = queue.pop(0)
            if curr_node.get_children() == []:
                leaves.append(curr_node)
                continue
            for child in curr_node.get_children():
                queue.append(child[0])
        return leaves
