#VATSAL RUSTAGI, 41346390, PROJECT 4
#OTHELLO
"""
GLOBAL CONSTANTS
"""

NONE = 0
BLACK = 1
WHITE = 2

"""
CLASSES
"""
class InvalidMoveError(Exception):
    '''Raised whenever an invalid move is made'''
    pass

class NoMoveError(Exception):
    '''Raised whenever there is no legal move available for a player'''
    pass

class Game:
    def __init__(self,row: int,col: int,turn: int,tl: int):
        """
        Intitalizes game board
        """
        self._turn = turn
        self._count_black = 0
        self._count_white = 0
        self.is_game_over = False

        self._board = []
        temp_row = []
        for c in range(col):
            temp_row.append(NONE)
        for r in range(row):
            self._board.append(temp_row[:])

        self._set_up_board(tl)

    def _set_up_board(self,tl_disc: int):
        """
        Sets up grid according to top left disc.
        """
        tl_row = int(len(self._board)/2) - 1            # 'tl' is top-left
        tl_col = int(len(self._board[0])/2) - 1         # 'tl' is top-left
        self._board[tl_row][tl_col] = tl_disc
        self._board[tl_row][tl_col+1] = _get_other_disc(tl_disc)
        self._board[tl_row+1][tl_col+1] = tl_disc
        self._board[tl_row+1][tl_col] = _get_other_disc(tl_disc)

    def add_disc(self,row: int,col: int):
        """
        Adds disc to the board and changes turn to other color.
        """
        self._board[row][col] = self._turn
        self.skip_turn()

    def flip_disc(self,row: int,col: int):
        """
        Flips disc to other color on the grid.
        """
        self._board[row][col] = _get_other_disc(self._board[row][col])

    def count_discs(self):
        """
        Resets the count variables after counting the discs in the grid.
        """
        self._count_black = 0
        self._count_white = 0
        for i in self._board:
            self._count_black += i.count(BLACK)
            self._count_white += i.count(WHITE)

    def get_count(self):
        """
        Returns a tuple with number of black and white discs respectively.
        """
        return (self._count_black,self._count_white)

    def get_turn(self):
        """
        Returns str 'B' or 'W' accoding to '_turn'.
        """
        return 'B' if self._turn == BLACK else 'W'

    def skip_turn(self):
        """
        Skips turn by changing the turn to the other disc.
        """
        self._turn = _get_other_disc(self._turn)

    def game_over(self):
        """
        Changes '_is_game_over' status.
        """
        self.is_game_over = True

    def rows(self):
        """
        Returns number of rows.
        """
        return len(self._board)

    def cols(self):
        """
        Returns number of columns.
        """
        return len(self._board[0])

"""
UTILITY METHODS
"""

def _get_other_disc(disc: int) -> int:
    """
    Returns the other color disc.
    """
    return WHITE if disc == BLACK else BLACK

def _get_direction(grid: Game, to_row: int, to_col: int, match: int) -> list:
    """
    Returns a list of all the directions with matching disc around the given
    coordinates.
    """
    result = []
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            x,y = to_row + i, to_col + j
            try:
                if x>=0 and y>=0:
                    if grid._board[x][y] == match:
                        result.append(_direction(x,y,to_row,to_col))
            except IndexError:
                pass
    return result

def _direction(x: int,y: int,row: int,col: int) -> str:
    """
    Returns the name of the direction (x,y) are with respect to (row,col).
    """
    d = {(row,col-1) : 'west',
         (row,col+1) : 'east',
         (row-1,col) : 'north',
         (row+1,col) : 'south',
         (row-1,col+1) : 'northeast',
         (row-1,col-1) : 'northwest',
         (row+1,col+1) : 'southeast',
         (row+1,col-1) : 'southwest'}
    return d[(x,y)]

def _is_valid_move(grid: Game, to_row: int, to_col: int) -> bool:
    """
    Checks if a move is valid.
    """
    if grid._board[to_row][to_col] != NONE:
        return False
    else:
        dirs = _get_direction(grid,to_row,to_col,_get_other_disc(grid._turn))
        for dir in dirs:
            if eval('_'+dir)(grid,to_row, to_col,grid._turn,False):
                return True
        return False

def _flip_in_direction(dirs: list,grid: Game,to_row: int, to_col: int,match: int) -> None:
    """
    Takes a list of directions and flips discs in those directions.
    """
    add_or_not = False
    for dir in dirs:
        if eval('_'+dir)(grid,to_row, to_col,match,True):
            add_or_not = True
    if add_or_not:
        grid.add_disc(to_row,to_col)

def _B_or_W(color: str) -> int:
    """
    Returns int BLACK if color is 'B' otherwise WHITE.
    """
    return BLACK if color == 'B' else WHITE

"""
HANDLING METHODS
"""
def if_valid_move_exists(grid: Game) -> bool:
    """
    Returns True if a valid move exists, False otherwise.
    """
    for i in range(grid.rows()):
        for j in range(grid.cols()):
            if _is_valid_move(grid,i,j):
                return True
    return False

def new_game(rows: int,cols: int,turn: str,top_left: str) -> Game:
    """
    Sets up an othello grid according to parameters and returns
    a Game object.
    """
    grid = Game(rows,cols,_B_or_W(turn),_B_or_W(top_left))
    return grid

def make_move(grid: Game, to_row, to_col):
    """
    Makes a move if the move for the given coordinates are valid,
    or raises an InvalidMoveError.
    """
    if _is_valid_move(grid, to_row, to_col):
        match = grid._turn
        dirs = _get_direction(grid, to_row,to_col,_get_other_disc(match))
        _flip_in_direction(dirs,grid,to_row, to_col,match)
    else:
        raise InvalidMoveError()

"""
Direction oriented functions:
These funtions checks if in a direction a possible move is available, and also are capable
of flipping in that direction.
"""
def _west(grid: Game,i, j,match,flip: bool) -> bool:
    j -= 1
    while j >= 0 and grid._board[i][j] != NONE:
        if grid._board[i][j] == match:
            if flip:
                j += 1
                while grid._board[i][j] != NONE:
                    grid.flip_disc(i,j)
                    j += 1
            return True
        j -= 1
    return False

def _east(grid: Game,i, j,match,flip: bool) -> bool:
    j += 1
    while j <= grid.cols()-1 and grid._board[i][j] != NONE:
        if grid._board[i][j] == match:
            if flip:
                j -= 1
                while grid._board[i][j] != NONE:
                    grid.flip_disc(i,j)
                    j -= 1
            return True
        j += 1
    return False

def _north(grid: Game,i, j,match,flip: bool) -> bool:
    i -= 1
    while i >= 0 and grid._board[i][j] != NONE:
        if grid._board[i][j] == match:
            if flip:
                i += 1
                while grid._board[i][j] != NONE:
                    grid.flip_disc(i,j)
                    i += 1
            return True
        i -= 1
    return False

def _south(grid: Game,i, j,match,flip: bool) -> bool:
    i += 1
    while i <= grid.rows()-1 \
            and grid._board[i][j] != NONE:
        if grid._board[i][j] == match:
            if flip:
                i -= 1
                while grid._board[i][j] != NONE:
                    grid.flip_disc(i,j)
                    i -= 1
            return True
        i += 1
    return False

def _southwest(grid: Game,i, j,match,flip: bool) -> bool:
    j -= 1
    i += 1
    while j >= 0 and i <= grid.rows()-1 and grid._board[i][j] != NONE:
        if grid._board[i][j] == match:
            if flip:
                j += 1
                i -= 1
                while grid._board[i][j] != NONE:
                    grid.flip_disc(i,j)
                    j += 1
                    i -= 1
            return True
        j -= 1
        i += 1
    return False

def _southeast(grid: Game,i, j,match,flip: bool) -> bool:
    j += 1
    i += 1
    while j <= grid.cols()-1 \
            and i <= grid.rows()-1 \
            and grid._board[i][j] != NONE:
        if grid._board[i][j] == match:
            if flip:
                j -= 1
                i -= 1
                while grid._board[i][j] != NONE:
                    grid.flip_disc(i,j)
                    j -= 1
                    i -= 1
            return True
        j += 1
        i += 1
    return False

def _northeast(grid: Game,i, j,match,flip: bool) -> bool:
    j += 1
    i -= 1
    while j <= grid.cols()-1 and i >= 0 and grid._board[i][j] != NONE:
        if grid._board[i][j] == match:
            if flip:
                j -= 1
                i += 1
                while grid._board[i][j] != NONE:
                    grid.flip_disc(i,j)
                    j -= 1
                    i += 1
            return True
        j += 1
        i -= 1
    return False

def _northwest(grid: Game,i, j,match,flip: bool) -> bool:
    j -= 1
    i -= 1
    while j >= 0 and i >= 0 and grid._board[i][j] != NONE:
        if grid._board[i][j] == match:
            if flip:
                j += 1
                i += 1
                while grid._board[i][j] != NONE:
                    grid.flip_disc(i,j)
                    j += 1
                    i += 1
            return True
        j -= 1
        i -= 1
    return False
