import socket
import sys
import re

def establish_connection(client_socket, host, port): # Establish a connection to the server
    try:
        client_socket.connect((host, port))
        return 0
    except socket.error as e:
        print(f"Unable to connect to server: {e}")
        return -1

def close_connection(client_socket): # Close the connection
    client_socket.close()
    print("4001 Bye Bye")
    return 0

def send_message(client_socket, message): # Send a message to the server
    if not client_socket:
        print("No connection to server.")
        return -1
    try:
        # Send a message to the server
        client_socket.sendall(message.encode('utf-8'))
        return 0
    except socket.error as e:
        print(f"Socket error: {e}")
        return -1

def receive_message(client_socket): # Receive a message from the server
    try:
        response = client_socket.recv(1024)
        if not response:
            print("Server closed the connection.")
            return -1
        decoded_response = response.decode('utf-8')
        print(f"Received from server: {decoded_response}")
        return decoded_response
    except socket.error as e:
        print(f"Socket error: {e}")            
        return -1

def handle_out_of_game(client_socket): # Handle the out of game state
    user_name = input("Please enter your username: ")
    user_password = input("Please enter your password: ")
    cmd = f"/login {user_name} {user_password}"
    send_message(client_socket, cmd)
    received_message = receive_message(client_socket)
    return received_message

def handle_in_the_game_hall(client_socket): # Handle the in the game hall state
    cmd = input("Please enter a command: ")
    send_message(client_socket, cmd)
    received_message = receive_message(client_socket)
    return received_message

def handle_waiting_in_room(client_socket): # Handle the waiting in room state
    received_message = receive_message(client_socket)
    return received_message

def handle_playing_a_game(client_socket): # Handle the playing a game state
    cmd = input("Please enter your guess: ")
    send_message(client_socket, cmd)
    received_message = receive_message(client_socket)
    return received_message

if __name__ == "__main__":
    # Check the number of arguments
    if len(sys.argv) != 3:
        print("Usage: python GameClient.py <host> <port>")
        sys.exit(1)

    # Get the host and port from the command line arguments    
    host = sys.argv[1]
    port = int(sys.argv[2])

    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     
    # Establish a connection to the server
    if establish_connection(client_socket, host, port) == -1:
        sys.exit(1)

    # states = ("out_of_game" , "in_the_game_hall", "waiting_in_room","playing_a_game")
    # we got total 4 states, and we will use these states to control the flow of the game.
    state = "out_of_game"

    while True: # Main loop
        match state: # Match the state
            case "out_of_game": # Handle the out of game state
                received_message = handle_out_of_game(client_socket)
                match received_message:
                    case "1001":
                        print("1001 Authentication successful")
                        state = "in_the_game_hall"
                    case "1002":
                        print("1002 Authentication failed")
                    case "4002":
                        print("4002 Unrecognized message")

            case "in_the_game_hall": # Handle the in the game hall state
                received_message = handle_in_the_game_hall(client_socket)
                code = re.match(r"^\d+", received_message)  # extract the code from the message i.e. 3001 , since 3001 will receive a long message, rather then a code.
                match code.group():
                    case "3001": # print the room list , expected to receive a long message
                        print(received_message)
                    case "3011":
                        print("3011 Wait")
                        state = "waiting_in_room"
                    case "3012":
                        print("3012 Game started. Please guess true or false")
                        state = "playing_a_game"
                    case "3013":
                        print("3013 The room is full")
                        state = "in_the_game_hall"
                    case "4001": # Close the connection
                        close_connection(client_socket)
                        print("Client is ends")
                        sys.exit(0)
                    case "4002":
                        print("4002 Unrecognized message")

            case "waiting_in_room": # Handle the waiting in room state
                received_message = handle_waiting_in_room(client_socket)
                if received_message == "3012":
                    print("3012 Game started. Please guess true or false")
                    state = "playing_a_game"

            case "playing_a_game": # Handle the playing a game state
                received_message = handle_playing_a_game(client_socket)    
                match received_message:
                    case "3021":
                        print("3021 You are the winner")
                        state = "in_the_game_hall"
                    case "3022":
                        print("3022 You lost this game")
                        state = "in_the_game_hall"
                    case "3023":
                        print("3023 The result is a tie")
                        state = "in_the_game_hall"
                    case "4002":
                        print("4002 Unrecognized message")