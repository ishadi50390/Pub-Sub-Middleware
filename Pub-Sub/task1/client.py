import socket
import sys

def start_client(server_ip, port):
    # Create a socket object (IPv4, TCP)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server
    client_socket.connect((server_ip, port))
    print(f"[CLIENT] Connected to server {server_ip}:{port}")

    while True:
        msg = input("[YOU] Type message (type 'terminate' to quit): ")
        client_socket.sendall(msg.encode())

        if msg.strip().lower() == "terminate":
            print("[CLIENT] Terminating connection.")
            break

    client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client.py <SERVER_IP> <PORT>")
        sys.exit(1)

    server_ip = sys.argv[1]
    port = int(sys.argv[2])
    start_client(server_ip, port)
