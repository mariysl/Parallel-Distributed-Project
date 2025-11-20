# controller.py
import socket
import pickle
import threading
import queue

HOST =  "127.0.0.1"         #"0.0.0.0"  # Accept connections from all machines
PORT = 5000

TASKS = [2, 3, 4, 5, 16, 17, 19, 21, 23, 29, 31]  # Numbers to check
TASK_QUEUE = queue.Queue()
RESULTS = []
WORKERS = []

# Populate the task queue
for task in TASKS:
    TASK_QUEUE.put(task)

lock = threading.Lock()

def handle_worker(conn, addr):
    """Thread to handle a connected worker."""
    hostname = conn.recv(1024).decode()  # Receive worker hostname for logging
    print(f"Worker connected: {hostname} ({addr[0]})")
    WORKERS.append((conn, hostname, addr[0]))

    while not TASK_QUEUE.empty():
        try:
            task = TASK_QUEUE.get_nowait()
        except queue.Empty:
            break
        # Send the task
        conn.sendall(pickle.dumps(task))
        # Receive result
        data = conn.recv(4096)
        result = pickle.loads(data)
        with lock:
            RESULTS.append((result, hostname, addr[0]))
        print(f"Task {result[0]} completed by {hostname} ({addr[0]})")

    # Send stop signal
    conn.sendall(pickle.dumps("STOP"))
    conn.close()
    print(f"Worker {hostname} ({addr[0]}) disconnected.")


def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((HOST, PORT))
    server_sock.listen()
    print(f"Controller listening on {HOST}:{PORT}")

    threads = []

    try:
        while True:
            conn, addr = server_sock.accept()
            t = threading.Thread(target=handle_worker, args=(conn, addr))
            t.start()
            threads.append(t)
            # Optional: Stop accepting if all tasks are assigned
            if TASK_QUEUE.empty():
                break
    except KeyboardInterrupt:
        print("Shutting down controller...")

    # Wait for all worker threads
    for t in threads:
        t.join()

    print("\nAll results:")
    for number, hostname, ip in sorted(RESULTS, key=lambda x: x[0][0]):
        print(f"{number[0]} -> Prime? {number[1]} (Processed by {hostname}, {ip})")

    server_sock.close()
    print("Controller finished.")


if __name__ == "__main__":
    main()
