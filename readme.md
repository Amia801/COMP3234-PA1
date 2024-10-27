# Game Server and Client

This repository contains two Python scripts: `GameServer.py` and `GameClient.py`. These scripts are designed to work together to create a simple game server and client.

## Files

- `GameServer.py`: This script sets up a server that can handle multiple client connections, manage game state, and facilitate communication between clients.
- `GameClient.py`: This script connects to the game server, sends user inputs, and receives game updates from the server.

## Requirements

- Python 3.x
- Used additional libraries required (e.g., `socket`, `threading`, `random`, `time`, `sys`, `re`)

## Usage

### Running the Server

1. Navigate to the directory containing `gameserver.py`.
2. Run the server script:
    ```sh
    python3 GameServer.py
    ```

### Running the Client

1. Navigate to the directory containing `gameclient.py`.
2. Run the client script:
    ```sh
    python3 GameClient.py <target_server_IP_addr> <target_server_port>
    ```

## Detail

### `GameClient.py`
The GameClient.py implements a simple Mealy finite state machine (FSM), containing states such as out_of_game, in_the_game_hall, and waiting_in_room.   
By receiving four-digit codes like "1001" sent by the server, it determines which state it should transition to from the current state and provides an output.

### `GameServer.py`
The GameServer.py implements a server that first initializes necessary variables, such as user_info, rooms, and current_user. The server is implemented using two separate threads.  
First, there is the gaming_thread, which continuously iterates over the rooms list to check if there is a room where a result can be determined. If there is such a room, it generates a random boolean value, then uses this boolean to decide which player is the winner.  
Then, there is the player_thread, which handles user input and potential errors, such as unexpected player disconnections.
