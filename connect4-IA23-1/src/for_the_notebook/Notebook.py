# script that works in a notebook
import copy


class Connect4:
    """Class to model a connect4 board."""

    def __init__(self, new_game: bool = True, game_board: list = []):
        """Constructor of the connect4."""
        assert type(game_board) == list
        self.winner = 0
        self.__board = []
        if not new_game:
            assert len(game_board) == 6
            for row in game_board:
                assert len(row) == 7
                for cell in row:
                    assert type(cell) == int and cell > -1 and cell < 3
            self.__board = game_board
            return
        for i in range(6):
            self.__board.append([0, 0, 0, 0, 0, 0, 0])

    def __str__(self) -> str:
        """str function of a connect4."""
        string = ""
        n = 0
        string += "    0 1 2 3 4 5 6\n"
        string += "    _____________\n"
        for row in self.__board:
            string += str(n) + " | "
            n += 1
            for cell in row:
                string += str(cell) + " "
            string += "\n"
        return string

    def __eq__(self, connect4) -> bool:
        """Equals function to compare two connect4."""
        if type(self) != type(connect4):
            return False
        if self.winner != connect4.winner:
            return False
        for i in range(6):
            for j in range(7):
                if self.__board[i][j] != connect4.__board[i][j]:
                    return False
        return True

    def make_play(self, player_one: bool, column: int) -> bool:
        """Function to make a play on the board.
        Returns True if the play could not be made."""
        if type(player_one) != bool or type(column) != int:
            raise Exception("Wrong argument.")
        if 0 > column or column > 6:
            raise Exception("Wrong column.")

        row = 5
        while self.__board[row][column] != 0:
            row -= 1
            if row < 0:
                return True

        if player_one:
            self.__board[row][column] = 1
        else:
            self.__board[row][column] = 2
        return False

    def get_board(self) -> list:
        """Returns a copy of the board"""
        return copy.deepcopy(self.__board)

    def finished(self) -> int:
        """Checks the board for a winner. If there is a winnner, 
        returns the player number of the winner, otherwise returns 0."""
        (current, contiguous) = (0, 0)
        # check for win by a horizontal play
        for row in range(6):
            (current, contiguous) = (0, 0)
            for column in range(7):
                (current, contiguous) = self.__check_contiguous(
                    row, column, current, contiguous)
                if contiguous == 4:
                    self.winner = current
                    return current
        # check for win by a vertical play
        for column in range(7):
            (current, contiguous) = (0, 0)
            for row in range(6):
                (current, contiguous) = self.__check_contiguous(
                    row, column, current, contiguous)
                if contiguous == 4:
                    self.winner = current
                    return current
        # check for win by a diagonal play (/)
        l = [(0, 3), (0, 4), (0, 5), (0, 6), (1, 6), (2, 6)]
        for i in l:
            (row, column) = i
            (current, contiguous) = (0, 0)
            while row < 6 and column > -1:
                (current, contiguous) = self.__check_contiguous(
                    row, column, current, contiguous)
                if contiguous == 4:
                    self.winner = current
                    return current
                row += 1
                column -= 1
        # check for win by a diagonal play (/)
        l = [(2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (0, 3)]
        for i in l:
            (row, column) = i
            (current, contiguous) = (0, 0)
            while row < 6 and column < 7:
                (current, contiguous) = self.__check_contiguous(
                    row, column, current, contiguous)
                if contiguous == 4:
                    self.winner = current
                    return current
                row += 1
                column += 1


        return 0

    def __check_contiguous(self, row, column, current, contiguous) -> tuple:
        """Auxiliary function to check winning plays."""
        cell = self.__board[row][column]
        if cell == 0:
            return (0, 0)
        if cell != current:
            return (cell, 1)
        return (current, contiguous + 1)

    def possible_plays(self) -> list:
        """Function to get all possible plays."""
        plays = []
        count = 0
        for cell in self.__board[0]:
            if cell == 0:
                plays.append(count)
            count += 1
        return plays

#-------------------------------------------------------------------------



class Node:
    """Class to model the nodes for the search model."""

    def __init__(self, connect4, current_player: int, parent=None, height: int = 0) -> None:
        """Constructor of a node"""
        assert type(connect4) == type(Connect4())
        assert type(current_player) == int
        assert height >= 0
        assert current_player == 1 or current_player == 2
        self.__connect4 = Connect4(False, connect4.get_board())
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
            copy = Connect4(False, self.__connect4.get_board())
            copy.make_play(True if next_player == 1 else False, play)
            new_node = Node(copy, next_player, self, self.__height + 1)
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

#-----------------------------------------------------------------------

def user_input() -> int:
    """Function to get a valid play from the user."""
    not_finished = True
    while not_finished:
        usr_input = input()
        usr_int = -1
        try:
            usr_int = int(usr_input)
        except:
            print("Must enter a number!!\n\nTry again: ",end="")
            continue
        if usr_int > 6 or usr_int < 0:
            print("Invalid number!!\n\nTry again: ",end="")
            continue
        not_finished = False 

    return usr_int 

game = Connect4()
curr_node = Node(game, 2)
curr_node.expand()

player1 = True
print(game)
while game.finished() == 0 and game.possible_plays() != []:
    play = None
    if player1:
        print("player1 make a play: ", end="")
        play = user_input() 
        print()
    else:
        # children is a list of tuples, (child, play)
        children = curr_node.get_children()
        (curr_best_heuristic, curr_best_play) = (children[0][0].get_heuristic(), children[0][1])
        for (child, curr_play) in children:
            if child.get_heuristic() > curr_best_heuristic:
                curr_best_heuristic = child.get_heuristic()
                curr_best_play = curr_play
        play = curr_best_play


    if game.make_play(player1, play):
        print(" Invalid play!!!!!!!!\n")
        continue
    print(game)
    if player1:
        print("\nAI making a move")
        curr_node = Node(game, 1)
        curr_node.height_4_tree()
        player1 = False
    else:
        player1 = True
    print()

print(game)
if game.winner == 0:
    print("There was a tie.")
else:    
    print("The winner is player " + str(game.winner))
