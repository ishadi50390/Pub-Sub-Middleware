import socket
import threading
import sys

subscribers = []  # List to keep track of subscriber sockets
lock = threading.Lock()  # To handle shared resource access

def handle_client(client_socket, addr, role):
    global subscribers

    print(f"[SERVER] New {role} connected from {addr}")

    if role == "SUBSCRIBER":
        with lock:
            subscribers.append(client_socket)

    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"[{role} {addr}] {data.strip()}")

            if data.strip().lower() == "terminate":
                print(f"[SERVER] {role} from {addr} terminated.")
                break

            # If publisher, broadcast message to all subscribers
            if role == "PUBLISHER":
                with lock:
                    for sub in subscribers:
                        try:
                            sub.sendall(f"[MESSAGE] {data.strip()}".encode())
                        except:
                            continue  # Skip dead subscribers

    finally:
        if role == "SUBSCRIBER":
            with lock:
                if client_socket in subscribers:
                    subscribers.remove(client_socket)

        client_socket.close()
        print(f"[SERVER] {role} from {addr} disconnected.")


def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(10)

    print(f"[SERVER] Listening on port {port}...")

    while True:
        client_socket, addr = server_socket.accept()
        # First message must be the role
        role = client_socket.recv(1024).decode().strip().upper()
        if role not in ["PUBLISHER", "SUBSCRIBER"]:
            client_socket.sendall(b"Invalid role. Use PUBLISHER or SUBSCRIBER.")
            client_socket.close()
            continue

        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, role))
        client_thread.daemon = True
        client_thread.start()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <PORT>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
