#VATSAL RUSTAGI, 41346390, PROJECT 4
#OTHELLO

import othello

"""
'get' Methods
"""
def get_decider() -> str:
    """
    Returns ['>','<'] according to user input.
    """
    try:
        decider = input()
        if decider not in ['<','>']:
            raise Exception
    except:
        raise SystemExit
    else:
        return decider

def get_color(element: int) -> str:
    """
    Returns a str from ['B','W','.'] corresponding to the given int element.
    """
    d = {othello.BLACK : 'B',
         othello.WHITE : 'W',
         othello.NONE  : '.'}
    return d[element]

def get_num() -> int:
    """
    Returns an even int between 4 and 16 inclusive according to user input.
    """
    try:
        num = int(input())
        if not (4<= num <=16) and num%2 == 0:
            raise Exception
    except:
        raise SystemExit
    else:
        return num

def get_b_or_w() -> str:
    """
    Returns 'B' or 'W' strings according to user input.
    """
    try:
        color = input()
        if color not in ['B','W']:
            raise Exception
    except:
        raise SystemExit
    else:
        return color

def get_move() -> list:
    """
    Returns a list of int, which are the coordinates of the move.
    """
    try:
        temp = input().strip().split()
        for n in temp:
            if not n.isdigit():
                raise Exception
        move = [int(temp[0])-1,int(temp[1])-1]
    except:
        raise SystemExit
    else:
        return move

"""
Printing Board Methods
"""
def print_board(grid) -> None:
    """
    Prints the grid.
    """
    for i in grid._board:
        print()
        for j in i:
            print('{}'.format(get_color(j)),end=" ")

def display(grid) -> None:
    """
    Displays the game layout in the required format.
    """
    grid.count_discs()
    b,w = grid.get_count()
    print("B: {}  W: {}".format(b,w),end="")
    print_board(grid)
    if not grid.is_game_over:
        print("\nTURN: {}".format(grid.get_turn()))

"""
Main Methods
"""
def play(grid,decider) -> None:
    """
    Runs a while loop to play/run the game 'Othello'.
    """
    display(grid)
    while True:
        try:
            move = get_move()
            othello.make_move(grid,move[0],move[1])
            print("VALID")
            if not othello.if_valid_move_exists(grid):
                raise othello.NoMoveError()
            display(grid)
        except othello.InvalidMoveError:
            print("INVALID")
        except othello.NoMoveError:
            grid.skip_turn()
            if not othello.if_valid_move_exists(grid):
                declare_winner(grid,decider)
            else:
                display(grid)

def declare_winner(grid,decider) -> None:
    """
    Prints the winner by checking the count of discs.
    """
    grid.game_over()
    display(grid)
    black,white = grid.get_count()
    if  black > white and decider == '>' or black < white and decider == '<':
        print('\nWINNER: B')
    elif black == white:
        print('\nWINNER: NONE')
    else:
        print('\nWINNER: W')
    raise SystemExit

def user_interface() -> None:
    print("FULL")
    grid = othello.new_game(get_num(),get_num(),get_b_or_w(),get_b_or_w())
    play(grid,get_decider())

if __name__ == '__main__':
    user_interface()