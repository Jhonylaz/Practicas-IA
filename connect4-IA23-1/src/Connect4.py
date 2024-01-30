import copy


class connect4:
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
