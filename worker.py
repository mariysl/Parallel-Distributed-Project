# worker.py
import socket
import pickle
import socket as sk

# Change this to the LAN IP of the controller machine
CONTROLLER_HOST = "192.168.1.2"
PORT = 5000


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def main():
    hostname = sk.gethostname()
    ip = sk.gethostbyname(hostname)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((CONTROLLER_HOST, PORT))

    # Send role + hostname to controller
    header = f"WORKER|{hostname}"
    sock.sendall(header.encode())

    print(f"[WORKER STARTED] {hostname} ({ip}) connected to controller {CONTROLLER_HOST}:{PORT}")

    while True:
        data = sock.recv(4096)
        if not data:
            print("[WORKER] Connection closed by controller.")
            break

        task = pickle.loads(data)

        if task == "STOP":
            print("[WORKER] Received STOP signal. Exiting.")
            break

        # Compute result
        result = is_prime(task)
        print(f"[WORKER LOG] {hostname} ({ip}) processed {task} -> Prime? {result}")

        # Send result back as (task, result)
        sock.sendall(pickle.dumps((task, result)))

    sock.close()
    print("[WORKER] Stopped.")


if __name__ == "__main__":
    main()
