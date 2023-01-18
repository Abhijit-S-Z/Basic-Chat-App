# Import Required Modules
import socket
import threading

HOST = '127.0.0.1'
PORT = 1234 # One can use any port between 0 65535.
LISTNER_LIMIT = 5
active_clients = [] # List of all currently connected users

# Function to listen upcoming msg from a client
def listen_for_msg(client, username):
    while 1:
        msg = client.recv(2048).decode('utf-8')
        if msg == "":
            print(f"The message sent from {username} is empty.")
        else:
            final_msg = username + " ~ " + msg
            send_msg_to_all(msg)

#F FUnction to send message to a single client
def send_msg_to_client(client, msg):
    client.sendall(msg.encode())

# Function to send any msg to all clients in the server
def send_msg_to_all(msg):
    for user in active_clients:
        send_msg_to_client(user[1], msg)

# Function to handle clients
def client_handler(client):
    # Server will listen client msg containing username
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username == "":
            print("Client Username is empty")
            break
        else:
            active_clients.append((username, client))

    threading.Thread(target=listen_for_msg, args = (client, username, )).start()

# Main Function
def main():
    # Creating the socket class object
    # AF_INET : we are going to use IPv4 address.
    # SOCK_STREAM: we are using TCP packets for communication.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creating a try catch block
    try:
        # Provide the server with an address in th form of host IP and port
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and {PORT}.")

    # Set server limit.
    server.listen(LISTNER_LIMIT)

    # This while loop will keep listening to client connections
    while 1:
        client, address = server.accept()
        print(f"Successfully connected to the client {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client,)).start()



if __name__ == "__main__":
    main()
