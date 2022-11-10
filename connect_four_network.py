import cf_network_lib as network
import connect_four_lib as lib
import connectfour as connect

def play_networked() -> None:
    '''
    Runs the networked version of connect four by connecting to the server
    '''
    host = network.desired_host()
    port = network.desired_port()
    username = get_username()

    try:
        connection = network.connect_server(host, port)
    except:
        print('Could not connect to the server')
        return 
    print(prep_game(username, connection))
    
    columns, rows, = lib.get_dimensions()

    network.send_message(connection, f'AI_GAME {columns} {rows}')
    print(network.receive_message(connection))

    game = connect.new_game(columns, rows)
    lib.print_board(game)

    winner = 0
    while winner == 0:
        while True:
            try:
                response, invalid, desired_move, drop_location, pop_location = network.client_move(connection)
                if invalid == 1:
                    print('INVALID')
                    print('READY')
                    continue
            except:
                print('INVALID')
                continue

            if response == 'WINNER_RED' or response == 'WINNER_YELLOW':
                if desired_move == 'd':
                    game = lib.move_drop(game, drop_location)
                elif desired_move == 'p':
                    game = lib.move_pop(game, pop_location)
                lib.print_board(game)
                break
            elif response == 'OKAY':
                if desired_move == 'd':
                    game = lib.move_drop(game, drop_location)
                elif desired_move == 'p':
                    game = lib.move_pop(game, pop_location)
                lib.print_board(game)
                game = network.server_move(game, connection)
                
                third_response = network.receive_message(connection)
                if third_response == 'WINNER_YELLOW':
                    break
                else:
                    print(third_response)
            elif response == 'INVALID':
                sec_response = network.receive_message(connection)
                print(sec_response)
                continue
        winner = connect.winner(game)
    print(lib.winner_name(winner))
    network.close(connection)

def get_username() -> str:
    '''
    Continously asks user to enter a username until a 
    valid one is entered
    '''
    while True: 
        username = input('Please enter a valid username (no spaces): ')
        if ' ' in username or username == '':
            continue
        return username

def prep_game(username: str, connection: 'connection') -> str:
    '''
    Initiates the connection to the connect four server and 
    reads the first response from the server
    '''
    network.send_message(connection, f'I32CFSP_HELLO {username}')
    response = network.receive_message(connection)
    if response[0:7] == 'WELCOME':
        return response
    else:
        network.close(connection)

if __name__ == '__main__':
    play_networked()