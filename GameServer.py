import socket
import threading
import random

def load_user_info():
    user_info = {}
    with open("UserInfo.txt", "r") as f:
        for line in f:
            user_name, user_password = line.strip().split(":")
            user_info[user_name] = user_password
    return user_info

def player_thread(client_socket, user_info,rooms,rooms_lock):
    while True :
        user_cmd = client_socket.recv(1024)
        user_cmd = user_cmd.decode('utf-8').split(" ")

        if user_cmd[0] == "/login": # login
            if user_cmd[1] in user_info and user_info[user_cmd[1]] == user_cmd[2]:
                client_socket.send("1001".encode('utf-8'))
            else:
                client_socket.send("1002".encode('utf-8'))

        elif user_cmd[0] == "/list": # list
            nums_of_rooms = len(rooms.keys())
            room_list = str(nums_of_rooms) + " "
            for room in rooms:
                room_list += str(rooms[room][0]) + " "
            client_socket.send(room_list.encode('utf-8'))

        elif user_cmd[0] == "/enter": # enter the game room and play?????
            room_id = int(user_cmd[1])
            room_key = "room" + str(room_id)
            if len(rooms[room_key]) >= 2:
                client_socket.send("3013".encode('utf-8'))
            else:
                with rooms_lock:
                    if len(rooms[room_key][0]) == 0:
                        rooms[room_key][1].append(client_socket)
                        client_socket.send("3011".encode('utf-8'))
                        #wait for another player and play game
                    if len(rooms[room_key][1]) == 1:
                        rooms[room_key][2].append(client_socket)
                        client_socket.send("3012".encode('utf-8'))
                        # play game

        elif user_cmd[0] == "/guess":
            with rooms_lock:
                if rooms[room_key][1][0] == client_socket :
                    rooms[room_key][1][1] = user_cmd[1]
                elif rooms[room_key][2][0] == client_socket :
                    rooms[room_key][2][1] = user_cmd[1]
                    
        elif user_cmd[0] == "/exit":# exit
            client_socket.send("4001".encode('utf-8'))
            client_socket.close()
            break

def gaming_thread(rooms,rooms_lock):
    while True :
        for room in rooms:
            if len(rooms[room][1]) == 2 and len(rooms[room][2]) == 2 :
                #generate a random boolean
                ans = random.choice([True, False])
                with rooms_lock:
                    player1 = rooms[room][1][0]
                    player2 = rooms[room][2][0]
                    player1_guess = rooms[room][1][1]
                    player2_guess = rooms[room][2][1]
                    if player1_guess == player2_guess:
                        player1.send("3023".encode('utf-8'))
                        player2.send("3023".encode('utf-8'))
                    elif player1_guess == ans:
                        player1.send("3021".encode('utf-8'))
                        player2.send("3022".encode('utf-8'))
                    else:
                        player1.send("3022".encode('utf-8'))
                        player2.send("3021".encode('utf-8'))
                    rooms[room][1] = []
                    rooms[room][2] = []
                    rooms[room][0] = 0


def main(): 
    # load UserInfo.txt to a dit
    user_info = load_user_info()

    #indexs (#player,[player1_socket,T or F],[player2_socket,T or F])
    rooms = {"room0" : [0,[],[]], "room1" : [0,[],[]], "room2" : [0,[],[]],
             "room3" : [0,[],[]], "room4" : [0,[],[]], "room5" : [0,[],[]],
             "room6" : [0,[],[]], "room7" : [0,[],[]], "room8" : [0,[],[]],
             "room9" : [0,[],[]] }
    rooms_lock = threading.Lock()
    serverPort = 22222

    # create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind( ("127.0.0.1", serverPort) )
    server_socket.listen(5)
    print("Server is listening on port 8888...")


    while True:
        gaming_thread = threading.Thread(target=gaming_thread, args=(rooms,rooms_lock))
        gaming_thread.start()
        # accept a connection
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established!")
        # create a thread to handle the client
        thread = threading.Thread(target=player_thread, args=(client_socket, user_info, rooms,rooms_lock))
        thread.start()


if __name__ == "__main__" :
    main()