import socket
import sys
import threading

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print(f"\n{msg}")
            else:
                break
        except:
            break

def start_client(server_ip, port, role, topic):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, port))

    # Send role and topic to server
    sock.sendall(f"{role}:{topic}".encode())

    print(f"[CLIENT] Connected as {role} on topic '{topic}'")

    if role == "SUBSCRIBER":
        print(f"[INFO] You will receive messages on topic: {topic}")
        threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

        while True:
            msg = input(">> ")
            if msg.strip().lower() == "terminate":
                sock.sendall(msg.encode())
                break
            else:
                print(" Only PUBLISHERS can send messages.")

    else:  # PUBLISHER
        while True:
            msg = input(">> ")
            sock.sendall(msg.encode())

            if msg.strip().lower() == "terminate":
                break

    sock.close()
    print("[CLIENT] Disconnected.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python client.py <SERVER_IP> <PORT> <ROLE> <TOPIC>")
        sys.exit(1)

    server_ip = sys.argv[1]
    port = int(sys.argv[2])
    role = sys.argv[3].upper()
    topic = sys.argv[4]

    if role not in ["PUBLISHER", "SUBSCRIBER"]:
        print("Error: Role must be PUBLISHER or SUBSCRIBER")
        sys.exit(1)

    start_client(server_ip, port, role, topic)
