# Distributed Prime Checker

Final Exam Project – Parallel & Distributed Systems

## Project Overview

This project implements a distributed system that checks whether numbers are prime. The system uses a controller–worker architecture. The controller assigns tasks to connected workers, and each worker processes the numbers it receives and sends the results back. A separate client script allows students or classmates to request and view the final results from the controller.

The project demonstrates distributed task execution, worker scalability, and basic inter-machine communication using TCP sockets.

## Files in This Repository

* **controller.py** – Runs the controller (master node), assigns tasks, receives results, and logs which worker processed each number.
* **worker.py** – Runs on worker machines, connects to the controller, computes prime checks, and returns results.
* **client.py** – A simple script for classmates to connect to the controller and view all processed results.
* **README.md** – Documentation on how to set up and run the system.

---

## How the System Works

### Controller

* Listens on a network interface for worker and client connections.
* Distributes tasks one at a time from an internal queue.
* Receives results and records the worker hostname and IP address.
* Sends the full list of results to clients when they connect.

### Workers

* Connect to the controller using its LAN IP address.
* Identify themselves to the controller using hostname.
* Receive a task (a number), compute whether it is prime, and send the result back.
* Print logs showing the task and the worker’s hostname and IP.
* Stop automatically once all tasks are completed.

### Client

* Connects to the controller and retrieves the final results.
* Displays the numbers, their primality status, and which worker processed them.
* Allows classmates to interact with the application without accessing the controller directly.

---

## Setup Instructions

### 1. Starting the Controller (Machine A)

1. Open `controller.py`.
2. Make sure the host is set to:

   ```
   HOST = "0.0.0.0"
   PORT = 5000
   ```
3. Run:

   ```
   python3 controller.py
   ```

You should see it listening for workers and clients.

---

### 2. Starting a Worker (Machine B, C, etc.)

1. Open `worker.py`.
2. Update the controller’s IP address:

   ```
   CONTROLLER_HOST = "192.168.1.X"
   ```
3. Run:

   ```
   python3 worker.py
   ```

The worker will automatically connect to the controller and wait for tasks.

---

### 3. Adding Additional Workers (Scalability)

To add more workers, repeat the same steps as above:

* Copy `worker.py` to a new machine
* Change only the controller IP
* Run `python3 worker.py`

No changes on the controller are required.

The controller will immediately begin sending tasks to the new worker if tasks remain.

---

### 4. Running the Client Script (Class-Wide Access)

1. Open `client.py`.
2. Update the controller IP:

   ```
   CONTROLLER_HOST = "192.168.1.X"
   ```
3. Run:

   ```
   python3 client.py
   ```

The client prints all results, including which worker processed each number.

---

## Logging and Output

Workers will produce logs such as:

```
[WORKER LOG] worker-C (192.168.1.104) processed 29 -> Prime? True
```

The controller will show:

```
[RESULT] 29 -> Prime? True (Processed by worker-C, 192.168.1.104)
```

This provides clear evidence of distributed execution as required by the project instructions.

---

## Summary

This project includes:

* A controller that manages tasks and results
* Workers that join dynamically and compute prime checks
* A client script for class-wide result access
* Logging that identifies each worker and the work it performed
* Simple setup that only requires updating the controller IP on worker and client machines

This satisfies the project’s requirements for distributed execution, worker scalability, and accessibility.
