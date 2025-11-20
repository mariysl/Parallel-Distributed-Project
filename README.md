# Distributed Prime Checker

## Project Overview

This project implements a **distributed system** to check if numbers are prime. The system uses a **controller-worker architecture**, where:

- **Controller**: Assigns tasks (numbers to check) to connected worker machines.
- **Workers**: Process the tasks in parallel using multiple processes and send results back to the controller.
- **Client**: Allows students to submit numbers to check without directly touching the controller.

This system demonstrates **scalability**, **distributed task execution**, and **class-wide access**.

---

## Files

- `controller.py` – Runs the controller, manages tasks, and collects results.
- `worker.py` – Runs on each worker machine to process tasks.
- `client.py` – Python client to submit numbers to the controller (optional for classmates).
- `README.md` – This file.

---

## How It Works

1. **Controller starts first**:
   - Listens for incoming worker connections on a specific port.
   - Holds a list of numbers to check for primality.
   - Assigns tasks dynamically to connected workers.
   - Collects results and prints which worker processed each task.

2. **Workers connect to the controller**:
   - Each worker sends its hostname for logging.
   - Receives tasks from the controller.
   - Uses **multiple processes** (`multiprocessing`) to check numbers in parallel.
   - Sends results back to the controller.
   - Prints logs including the worker’s hostname and IP.

3. **Dynamic Worker Scaling**:
   - You can start additional workers at any time.
   - Controller automatically accepts new workers and assigns remaining tasks.
   - Minimal setup: only change `CONTROLLER_HOST` in `worker.py` to the controller’s LAN IP.

4. **Client Script**:
   - Students can run `client.py` to submit numbers to check.
   - Returns the primality of numbers with worker information.
   - Works independently of the controller console.

---

## Setup Instructions

### 1. Controller

1. On one machine, run the controller:
```bash
python controller.py
