import socket
import threading

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
                room_list += str(rooms[room]) + " "
            client_socket.send(room_list.encode('utf-8'))

        elif user_cmd[0] == "/enter": # enter the game room and play?????
            room_id = int(user_cmd[1])
            room_key = "room" + str(room_id)
            if len(rooms[room_key]) >= 2:
                client_socket.send("3013".encode('utf-8'))
            else:
                with rooms_lock:
                    if len(rooms[room_key]) == 0:
                        rooms[room_key] += 1
                        client_socket.send("3011".encode('utf-8'))

                        while rooms[room_key] < 2:
                            pass
                        #wait for another player and play game
                    if len(rooms[room_key]) == 1:
                        rooms[room_key] += 1
                        client_socket.send("3012".encode('utf-8'))
                        # play game
        elif user_cmd[0] == "/exit":# exit
            client_socket.send("4001".encode('utf-8'))
def main(): 
    # load UserInfo.txt to a dit
    user_info = load_user_info()
    rooms = {"room0" : 0, "room1" : 0, "room2" : 0, "room3" : 0, "room4" : 0, "room5" : 0, "room6" : 0, "room7" : 0, "room8" : 0, "room9" : 0}

    # use this to paly games??????????? ,idk
    #rooms_result = {"room0" : [], "room1" : [], "room2" : [], "room3" : [], "room4" : [], "room5" : [], "room6" : [], "room7" : [], "room8" : [], "room9" : []}
    
    rooms_lock = threading.Lock()
    serverPort = 22222

    # create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind( ("127.0.0.1", serverPort) )
    server_socket.listen(5)
    print("Server is listening on port 8888...")


    while True:
        # accept a connection
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established!")
        # create a thread to handle the client
        thread = threading.Thread(target=player_thread, args=(client_socket, user_info, rooms,rooms_lock))
        thread.start()


if __name__ == "__main__" :
    main()