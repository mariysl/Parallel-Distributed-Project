# client.py
import socket
import pickle

# Set this to the controller machine LAN IP
CONTROLLER_HOST = "192.168.1.2"
PORT = 5000


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((CONTROLLER_HOST, PORT))

    # Identify as CLIENT
    sock.sendall(b"CLIENT")

    # Receive all results
    data = sock.recv(65536)
    if not data:
        print("No data received from controller.")
        sock.close()
        return

    results = pickle.loads(data)
    if not results:
        print("No results available yet. Workers may still be running.")
        sock.close()
        return

    print("Distributed Prime Check Results:\n")
    for (number, is_prime), hostname, ip in sorted(results, key=lambda x: x[0][0]):
        print(f"{number} -> Prime? {is_prime} (Processed by {hostname}, {ip})")

    sock.close()


if __name__ == "__main__":
    main()
