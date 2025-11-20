# controller.py
import socket
import pickle
import threading
import queue

# Set this to the controller machine's LAN IP or "0.0.0.0" to listen on all interfaces
HOST = "0.0.0.0"
PORT = 5000

# Tasks to distribute (numbers to check for primality)
TASKS = [2, 3, 4, 5, 16, 17, 19, 21, 23, 29, 31]

TASK_QUEUE = queue.Queue()
RESULTS = []        # Each entry: ((n, is_prime), hostname, ip)
lock = threading.Lock()


def init_tasks():
    """Populate the task queue."""
    while not TASK_QUEUE.empty():
        try:
            TASK_QUEUE.get_nowait()
        except queue.Empty:
            break

    for t in TASKS:
        TASK_QUEUE.put(t)


def handle_worker(conn, addr, hostname):
    """
    Handle a worker connection.
    Worker protocol:
      - After handshake, controller sends one task (int) at a time (pickled).
      - Worker returns (task, is_prime) (pickled).
      - When no tasks remain, controller sends "STOP".
    """
    worker_ip = addr[0]
    print(f"[WORKER CONNECTED] {hostname} ({worker_ip})")

    while True:
        try:
            task = TASK_QUEUE.get_nowait()
        except queue.Empty:
            # No more tasks: tell worker to stop
            try:
                conn.sendall(pickle.dumps("STOP"))
            except OSError:
                pass
            break

        # Send task to worker
        try:
            conn.sendall(pickle.dumps(task))
        except OSError:
            print(f"[ERROR] Failed to send task to {hostname} ({worker_ip})")
            break

        # Receive result
        try:
            data = conn.recv(4096)
            if not data:
                print(f"[DISCONNECTED] Worker {hostname} ({worker_ip}) closed connection.")
                break
            task_val, is_prime = pickle.loads(data)
        except Exception as e:
            print(f"[ERROR] Failed to receive/parse result from {hostname} ({worker_ip}): {e}")
            break

        with lock:
            RESULTS.append(((task_val, is_prime), hostname, worker_ip))

        print(f"[RESULT] {task_val} -> Prime? {is_prime} (Processed by {hostname}, {worker_ip})")

    conn.close()
    print(f"[WORKER DISCONNECTED] {hostname} ({worker_ip})")


def handle_client(conn, addr):
    """
    Handle a client connection.
    Client protocol:
      - Client sends "CLIENT" as header.
      - Controller responds with the full RESULTS list (pickled).
    """
    client_ip = addr[0]
    print(f"[CLIENT CONNECTED] ({client_ip})")

    with lock:
        payload = list(RESULTS)

    try:
        conn.sendall(pickle.dumps(payload))
    except OSError:
        print(f"[ERROR] Failed to send results to client ({client_ip})")

    conn.close()
    print(f"[CLIENT DISCONNECTED] ({client_ip})")


def main():
    init_tasks()

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen()
    print(f"[CONTROLLER] Listening on {HOST}:{PORT}")
    print("[INFO] Waiting for workers and clients...")

    threads = []

    try:
        while True:
            conn, addr = server_sock.accept()
            # First message is a small header: "WORKER|hostname" or "CLIENT"
            try:
                header = conn.recv(1024).decode().strip()
            except Exception:
                conn.close()
                continue

            if header.startswith("WORKER|"):
                hostname = header.split("|", 1)[1]
                t = threading.Thread(target=handle_worker, args=(conn, addr, hostname), daemon=True)
                t.start()
                threads.append(t)
            elif header == "CLIENT":
                t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                t.start()
                threads.append(t)
            else:
                print(f"[UNKNOWN CONNECTION] {addr} sent header: {header}")
                conn.close()

    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Controller stopping...")

    # Not strictly necessary if daemon threads, but safe:
    for t in threads:
        t.join(timeout=0.1)

    print("\n[FINAL RESULTS]")
    with lock:
        for (number, is_prime), hostname, ip in sorted(RESULTS, key=lambda x: x[0][0]):
            print(f"{number} -> Prime? {is_prime} (Processed by {hostname}, {ip})")

    server_sock.close()
    print("[CONTROLLER] Finished.")


if __name__ == "__main__":
    main()
