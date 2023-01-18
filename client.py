# Import required modules
import socket
import threading

HOST = "127.0.0.1"
PORT = 1234

def listen_for_msg_from_server(client):
    msg = client.recv(2048).decode('utf-8')
    if msg == "":
        print("Message recieved form client is empty.")
    else:
        username  = msg.split(" ~ ")[0]
        content = msg.split(" ~ ")[1]
        print(f"[{username}] {content}")

def send_message_to_server(client):
    while 1:
        msg = input("Message: ")

        if msg == "":
            print("Empty Message.")
        else:
            client.sendall(msg.encode())

def communicate_to_server(client):
    username = input("Enter Username: ")
    if username == "":
        print("Username can't be empty.")
        exit(0)
    else:
        client.sendall(username.encode())

    threading.Thread(target=listen_for_msg_from_server, args=(client, )).start()

    send_message_to_server(client)

# Main function
def main():

    # Creating a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to the server.")
    except:
        print("Unable to connect the server {HOST} {PORT}.")

    communicate_to_server(client)


if __name__ =="__main__":
    main()