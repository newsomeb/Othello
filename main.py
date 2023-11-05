class Player:
    """A class to represent and register players. Used by Othello class"""

    def __init__(self, name, color):
        """Constructor for Player class. All data members private"""
        self._name = name
        self._color = color
        #  if someone tries to enter a color other than black or white raise error
        if color != "white" and color != "black":
            raise ValueError("Invalid piece color")

    def get_player_name(self):
        """defines name of player class"""
        return self._name

    def get_color(self):
        """Defines piece color of player class"""
        return self._color


class Othello:
    """A class to represent the game as played"""

    def __init__(self):
        """Constructor for Othello class. Initializes the board with players one and two placed in correct positions.
        All data members are private."""
        self.turn = 0  # keeps track of whose turn it is
        self.player_list = []
        self.board = [["."] * 10 for _ in range(10)]  # creates 10x10 board
        self.board[0] = ["*"] * 10  # adds * to first row
        self.board[9] = ["*"] * 10  # adds * to last row
        #  adds * to first and last column
        for i in range(len(self.board)):
            self.board[i][0] = "*"
            self.board[i][-1] = "*"
        #  adds the starting pieces
        self.board[4][4] = "O"
        self.board[5][5] = "O"
        self.board[4][5] = "X"
        self.board[5][4] = "X"

    def get_turn(self):
        """returns whose turn it is"""
        return self.turn

    def take_turn(self):
        """Keeps track of whose turn it is by increasing turn counter by one each turn."""
        #  if turn is even then it's x's turn otherwise it's o's turn
        player = 'X' if self.turn % 2 == 0 else 'O'
        turn = f"It's {player}'s turn"
        self.turn += 1
        return turn, player

    def print_board(self):
        """Prints current board including boundaries"""
        for i in self.board:
            print('  '.join(i))

    def create_player(self, player_name, color):
        """Creates player object with given name and color and adds it to the player list"""
        player = Player(player_name, color)
        self.player_list.append(player)

    def count_pieces(self):
        """Counts pieces"""
        x_count = 0
        o_count = 0

        #  iterates over board to count pieces
        for row in self.board:
            for cell in row:
                if cell == 'X':
                    x_count += 1
                elif cell == 'O':
                    o_count += 1

        return x_count, o_count

    def return_winner(self):
        """Returns winner"""
        x_count, o_count = self.count_pieces()

        if x_count > o_count:
            return f'Winner is black player: {self.player_list[1].get_player_name()}'
        elif o_count > x_count:
            return f'Winner is white player: {self.player_list[0].get_player_name()}'
        else:
            return 'The game is a tie'

    def return_available_positions(self, color):
        """Returns list of possible positions for the player with the given color to move on the current board"""
        #  sets the current player to return available positions for current player only
        current_player = 'X' if color == 'black' else 'O'
        opponent = 'O' if current_player == 'X' else 'X'

        #  looks at all possible connections a piece can have
        possible_neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        #  empty list to store available positions
        available_positions = []

        #  iterates over board
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                #  if a cell is blank check neigboring cells
                if self.board[i][j] == '.':
                    #  loops over each combination in possible_neighbors
                    for xi, yj in possible_neighbors:
                        # compute board coordinates
                        x, y = i + xi, j + yj
                        #  if the neighboring position is within the boundaries of the board
                        if 0 <= x < len(self.board) and 0 <= y < len(self.board[i]) and self.board[x][y] == opponent:
                            while 0 <= x + xi < len(self.board) and 0 <= y + yj < len(self.board[i]):
                                x, y = x + xi, y + yj
                                if self.board[x][y] == '.':
                                    break
                                if self.board[x][y] == current_player:
                                    available_positions.append((i, j))
                                    break
        #  returns available_positions if it's not empty
        return available_positions

    def make_move(self, color, position):
        """Put a piece of specified color at given position and updates board accordingly"""
        available_positions = self.return_available_positions(color)

        if not available_positions:
            return []

        row, column = position

        if position not in available_positions:
            raise ValueError(f"The move is not valid")

        #  determine piece color
        piece = 'X' if color == 'black' else 'O'

        # place piece if move is valid
        self.board[row][column] = piece
        print(f"Placed {color} piece at position {position}")

        # possible directions of lines to be flipped
        lines = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        # checks all possible directions for pieces to flip
        for line in lines:
            flipped_pieces = []
            i, j = row + line[0], column + line[1]
            opponent_piece = False

            # check to see if the piece is a legal move within the bounds of the board
            while 0 <= i < len(self.board) and 0 <= j < len(self.board[i]):
                if self.board[i][j] == '.':  # if cell is empty stop
                    break
                elif self.board[i][j] == piece:  # if another of the player's (current turn) piece is found
                    if opponent_piece:  # found opponent piece
                        #  flip opponent's piece
                        for x, y in flipped_pieces:
                            self.board[x][y] = piece
                    break
                else:
                    flipped_pieces.append((i, j))
                    opponent_piece = True

                #  move to next cell in line
                i, j = i + line[0], j + line[1]

        return self.board

    def play_game(self, color, piece_position):
        """Attempts to make move for the player with the given color at specified position"""
        #  determines player's turn
        player = 'black' if self.turn % 2 == 0 else 'white'
        if color != player:
            return f"It's not your turn. It's {player}'s turn."

        #  defines available_postions
        available_positions = self.return_available_positions(color)

        #  checcks if position is invalid. if it is returns available positions
        if piece_position not in available_positions:
            print(f"Here are the valid moves: {available_positions}")
            return "Invalid move"

        self.make_move(color, piece_position)

        #  if game is over then count pieces and return both player count
        if not self.return_available_positions("black") and not self.return_available_positions("white"):
            black_count, white_count = self.count_pieces()
            result = f"Game is ended white piece: {white_count} black piece: {black_count}\n"
            result += self.return_winner()
            return result
        else:
            self.take_turn()
            return player
