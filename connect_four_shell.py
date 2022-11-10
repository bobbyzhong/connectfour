import connectfour as connect
import connect_four_lib as lib

def play_game() -> None:
    '''
    Starts the shell version of connect four game
    '''
    columns, rows = lib.get_dimensions()
        
    game = connect.new_game(columns,rows)
    lib.print_board(game)

    winner = 0
    while winner == 0:
        try:
            current_player = lib.convert_name(game.turn)
            while True:
                desired_move = input('Do you want to drop (d) or pop (p)? ')
                if desired_move == 'd':
                    drop_location = int(input(f'What column do you want to drop ({current_player}): '))
                    game = lib.move_drop(game, drop_location)
                    break
                elif desired_move == 'p':
                    pop_location = int(input(f'What columns do you want to pop ({current_player}): '))
                    game = lib.move_pop(game, pop_location)
                    break
                else:
                    print('Not a valid move')
                    continue
            lib.print_board(game)
            winner = connect.winner(game)
        except:
            print('The value you entered is not valid')
            continue

    print(f'{lib.convert_name(winner)} has won!')


if __name__ == '__main__':
    play_game()
