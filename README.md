# **Distributed Prime Checker – Final Exam Project**

## 📌 **Project Overview**

This project implements a distributed system that checks whether numbers are prime using a **Controller–Worker architecture**.
The controller distributes tasks to multiple worker machines, and each worker processes numbers and returns results.
A student client script can retrieve the final distributed results from the controller.

This project demonstrates:

* Distributed computing
* Task scheduling
* Worker scalability (add new workers at any time)
* Logging of worker hostname + IP
* Class-wide access through a Python client

---

# 📂 **Files Included**

| File            | Description                                                                                    |
| --------------- | ---------------------------------------------------------------------------------------------- |
| `controller.py` | Runs the controller node (master). Assigns tasks, receives results, logs worker activity.      |
| `worker.py`     | Runs on worker machines. Receives tasks, computes primality, returns output to the controller. |
| `client.py`     | Script for classmates to request results from the controller.                                  |
| `README.md`     | Documentation (this file).                                                                     |

---

# ⚙️ **How the System Works**

## **1. Controller**

* Listens for incoming workers and clients
* Distributes tasks one by one
* Logs:

  ```
  [RESULT] 23 -> Prime? True (Processed by worker-B, 192.168.1.103)
  ```
* Stores final results
* Sends results to `client.py` when requested

## **2. Workers**

* Connect to the controller automatically
* Receive one task at a time
* Compute `is_prime(number)`
* Log:

  ```
  [WORKER LOG] worker-C (192.168.1.104) processed 29 -> Prime? True
  ```
* Send results back to the controller
* Stop when the controller sends `"STOP"`

## **3. Client**

* Lets students fetch results from the controller
* Shows which worker processed each number
* Works without accessing the controller console

---

# 🚀 **Setup Instructions**

## **1. Start the Controller (Machine A)**

1. Open `controller.py`
2. Confirm:

   ```python
   HOST = "0.0.0.0"
   PORT = 5000
   ```
3. Run:

   ```bash
   python3 controller.py
   ```

You should see:

```
[CONTROLLER] Listening on 0.0.0.0:5000
```

---

## **2. Start a Worker (Machine B, C, D...)**

1. Open `worker.py`
2. Set the controller’s LAN IP:

   ```python
   CONTROLLER_HOST = "192.168.1.X"
   ```
3. Run:

   ```bash
   python3 worker.py
   ```

The worker logs something like:

```
[WORKER STARTED] worker-B (192.168.1.103)
```

---

# 🔥 **3. Add New Workers (Scalability Requirement)**

To add workers:

1. Copy `worker.py` to the new machine
2. Change **ONE line**:

   ```python
   CONTROLLER_HOST = "192.168.1.X"
   ```
3. Run:

   ```bash
   python3 worker.py
   ```

✔ No changes to controller
✔ Worker joins instantly
✔ Satisfies “minimal configuration change” requirement

---

## **4. Run the Client (Class-Wide Access)**

Students can run `client.py` anytime.

1. Set controller IP:

   ```python
   CONTROLLER_HOST = "192.168.1.X"
   ```
2. Run:

   ```bash
   python3 client.py
   ```

Example output:

```
2  -> Prime? True (Processed by worker-1, 192.168.1.101)
23 -> Prime? True (Processed by worker-2, 192.168.1.102)
```

---

# 📊 **Logs & Distributed Execution Evidence**

### Controller logs which worker processed each task:

```
[RESULT] 29 -> Prime? True (Processed by worker-C, 192.168.1.150)
```

### Workers identify themselves and show processing:

```
[WORKER LOG] worker-A (192.168.1.102) processed 17 -> Prime? True
```

These logs satisfy the assignment requirement for **visible distributed task execution**.

---

# 🎓 **Class-Wide Access Requirement**

This project uses the **Python client option** (approved method).
To satisfy the assignment requirements:

### ✔ Post `client.py` on the Canvas Project Discussion Board

Explain:

* Students must update `CONTROLLER_HOST` to your IP
* Then run `python3 client.py`

This satisfies the “application must be accessible to all students” rule.

---

# 📄 **Summary**

This distributed system:

* Uses a controller-worker architecture
* Allows dynamic worker scaling
* Logs distributed computation
* Provides class-wide access via a client script
* Meets all project submission requirements
