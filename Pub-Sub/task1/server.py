import socket
import sys

def start_server(port):
    # Create a socket object (IPv4, TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind to the given port
    server_socket.bind(('', port))
    server_socket.listen(5)

    print(f"[SERVER] Listening on port {port}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[SERVER] Client connected from {addr}")

        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"[CLIENT] {data}")

            if data.strip().lower() == "terminate":
                print("[SERVER] Client requested termination.")
                break

        client_socket.close()
        print(f"[SERVER] Client from {addr} disconnected.\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <PORT>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
