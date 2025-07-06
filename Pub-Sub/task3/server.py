import socket
import threading
import sys

subscribers_by_topic = {}  # key: topic, value: list of subscriber sockets
lock = threading.Lock()

def handle_client(client_socket, addr, role, topic):
    global subscribers_by_topic

    print(f"[SERVER] {role} connected from {addr} on topic '{topic}'")

    if role == "SUBSCRIBER":
        with lock:
            if topic not in subscribers_by_topic:
                subscribers_by_topic[topic] = []
            subscribers_by_topic[topic].append(client_socket)

    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            if data.strip().lower() == "terminate":
                print(f"[SERVER] {role} from {addr} terminated.")
                break

            print(f"[{role} {addr} | {topic}] {data.strip()}")

            if role == "SUBSCRIBER":
                client_socket.sendall(b"You are a SUBSCRIBER. You cannot send messages.")
                continue

            if role == "PUBLISHER":
                with lock:
                    if topic in subscribers_by_topic:
                        for sub in subscribers_by_topic[topic]:
                            try:
                                sub.sendall(f"[{topic}] {data.strip()}".encode())
                            except:
                                continue

    finally:
        if role == "SUBSCRIBER":
            with lock:
                if topic in subscribers_by_topic and client_socket in subscribers_by_topic[topic]:
                    subscribers_by_topic[topic].remove(client_socket)
        client_socket.close()
        print(f"[SERVER] {role} from {addr} disconnected.")

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(10)
    print(f"[SERVER] Listening on port {port}...")

    while True:
        client_socket, addr = server_socket.accept()
        try:
            role_topic = client_socket.recv(1024).decode().strip()
            role, topic = role_topic.split(":", 1)
            role = role.upper()
            topic = topic.strip()

            if role not in ["PUBLISHER", "SUBSCRIBER"]:
                client_socket.sendall(b"Invalid role. Use PUBLISHER or SUBSCRIBER.")
                client_socket.close()
                continue

            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, role, topic))
            client_thread.daemon = True
            client_thread.start()

        except Exception as e:
            print(f"[SERVER ERROR] Invalid client format: {e}")
            client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <PORT>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
