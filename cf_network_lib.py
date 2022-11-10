import socket
import connect_four_lib as lib
import connectfour as connect

def desired_host() -> str:
    '''
    Asks user to specify the host that they want to connect to
    '''
    while True:
        host = input('Host: ').strip()
        if host == '':
            print('Please specify a host (either a name or IP address)')
        else:
            return host

def desired_port() -> int:
    '''
    Asks user for the port on which the server they entered is listening
    '''
    while True:
        try:
            port = int(input('Port: ').strip())
            if 0 <= port <= 65535:
                return port
        except ValueError:
            pass
        print('Ports must be an integer between 0 and 65535')

def connect_server(host: str, port: int) -> 'connection':
    '''
    Connects to a server given the host and port
    '''
    cf_socket = socket.socket()
    cf_socket.connect((host, port))

    cf_input = cf_socket.makefile('r')
    cf_output = cf_socket.makefile('w')

    return cf_socket, cf_input, cf_output

def close(connection: 'connection') -> None:
    '''Closes the connection'''
    cf_socket, cf_input, cf_output = connection
    cf_input.close()
    cf_output.close()
    cf_socket.close()

def send_message(connection: 'connection', message: str) -> None:
    '''
    Sends a message to a given server
    '''
    _, _, cf_socket = connection

    cf_socket.write(message + '\r\n')
    cf_socket.flush()

def receive_message(connection: 'connection') -> str:
    '''
    Receives a message from a given server
    '''
    _, cf_input, cf_output = connection
    return cf_input.readline()[:-1]

def check_move(desired_move: str, location: 'int', connection: 'connection') -> str:
    '''
    Takes the move of the user, sends it to the server, and
    returns the response from the server
    '''

    if desired_move == 'd':
        send_message(connection, f'DROP {location}')
        response = receive_message(connection)
        return response

    elif desired_move == 'p':
        send_message(connection, f'POP {location}')
        response = receive_message(connection)
        return response

def client_move(connection: 'connection'):
    '''
    Asks the user for their move and checks its validity. Then it returns
    the server response, validity, and the move. 
    '''
    desired_move = input('Do you want to drop (d) or pop (p)? ')

    response = ''
    invalid = 0
    drop_location = 0
    pop_location = 0
    if desired_move == 'd':
        drop_location = int(input(f'Where do you want to drop: '))
        response = check_move(desired_move, drop_location, connection)
        if not response == 'WINNER_RED':
            print(response)
    elif desired_move == 'p':
        pop_location = int(input(f'Where do you want to pop: '))
        response = check_move(desired_move, pop_location, connection)
        if not response == 'WINNER_RED':
            print(response)
    else:
        invalid = 1
    return response, invalid, desired_move, drop_location, pop_location



def server_move(game: connect.GameState, connection: 'connection') -> connect.GameState:
    '''
    Takes the server message and updates the game board based
    on the move. Prints out the game board after move it complete
    '''
    sec_response = receive_message(connection)
    move_type, column = sec_response.split()
    if move_type == 'DROP':
        game = lib.move_drop(game, int(column))
    else:
        game = lib.move_pop(game, int(column))
    print('')
    print(sec_response)
    lib.print_board(game)
    
    return game
    
