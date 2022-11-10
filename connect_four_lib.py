import connectfour as connect
from collections import namedtuple

def get_dimensions() -> int:
    '''
    Asks user for input on the number of columns and rows for 
    the game and continues asking until a valid one is submitted
    '''
    while True:
        try:
            columns = int(input('Enter the number of columns (between 4 and 20): '))
            if 4 <= columns <= 20:
                rows = int(input('Enter the number of rows (between 4 and 20): '))
                if 4 <= rows <= 20:
                    return columns, rows
                else:
                    print('Invalid Entry')
                    continue
            else:
                print('Invalid Entry')
        except:
            print('Invalid Entry')
            continue

def print_board(game_board: connect.GameState) -> None:
    '''
    Prints out the current game board
    '''
    columns = connect.columns(game_board)
    rows = connect.rows(game_board)
    top_line = ''
    for i in range(1,columns+1):
        top_line+= str(i)
        if i < 9:
            top_line += '  '
        else:
            top_line += ' '
    print(top_line)
    for r in range(0,rows):
        line = ''
        for c in range(0, columns):
            line += slot_letter(game_board.board[c][r]) + '  '
        print(line)

def slot_letter(letter: int) -> str:
    '''
    Takes the number representing a slot in the game board
    and changes it to either R, Y, or .
    '''
    if letter == connect.RED:
        return 'R'
    elif letter == connect.YELLOW:
        return 'Y'
    else:
        return '.'

def move_drop(current_board: connect.GameState, column: int) -> connect.GameState:
    '''
    Executes the drop move on a given column and returns
    the game state that results from the move
    '''
    return connect.drop(current_board, column-1)

def move_pop(current_board: connect.GameState, column: int) -> connect.GameState:
    '''
    Executes the pop move on a given column and returns
    the game state that results from the move
    '''
    return connect.pop(current_board, column-1)

def convert_name(num: int) -> str:
    '''
    Takes a given number representing the player and
    converts it to either RED or YELLOW as winner
    '''
    if num == 1:
        return 'Red'
    elif num == 2:
        return 'Yellow'

def winner_name(num: int) -> str:
    '''
    Takes a given number representing the player and
    converts it to either RED or YELLOW as winner
    '''
    if num == 1:
        return 'WINNER_RED'
    elif num == 2:
        return 'WINNER_YELLOW'
        