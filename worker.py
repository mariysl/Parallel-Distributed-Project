# worker.py
import socket
import pickle
import multiprocessing as mp
import os
import socket as sk

CONTROLLER_HOST = "127.0.0.1"  # 192.168.1.2 Change to controller LAN IP
PORT = 5000

NUM_PROCESSES = 4

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def worker_process(task, result_queue, worker_id):
    result = is_prime(task)
    hostname = sk.gethostname()
    ip = sk.gethostbyname(hostname)
    print(f"Worker {worker_id} ({hostname}, {ip}) processed {task} -> {result}")
    result_queue.put((task, result))

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((CONTROLLER_HOST, PORT))

    # Send hostname for logging
    hostname = sk.gethostname()
    sock.sendall(hostname.encode())

    while True:
        data = sock.recv(4096)
        if not data:
            break
        task = pickle.loads(data)
        if task == "STOP":
            break

        # Multiprocessing pool
        result_queue = mp.Queue()
        processes = []

        for i in range(NUM_PROCESSES):
            p = mp.Process(target=worker_process, args=(task, result_queue, i))
            p.start()
            processes.append(p)

        # Collect results
        results = []
        for _ in processes:
            res = result_queue.get()
            results.append(res)

        # Send results back
        sock.sendall(pickle.dumps(results))

        # Join processes
        for p in processes:
            p.join()

    sock.close()
    print("Worker stopped.")


if __name__ == "__main__":
    main()
