# GUI for dynamic signal analyzer

## 🚀 Getting Started

### 1. Clone the Repository
 

```bash
git clone git@github.com:ShiyaoJ/GUI-dynamic-signal-analyzer.git
cd GUI-dynamic-signal-analyzer
````

> ❗ Make sure you have configured SSH access to GitHub on your local machine. Follow GitHub's [SSH setup guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) if you're unsure.

### 2. Prerequisites

* [Install Docker](https://docs.docker.com/get-docker/)

> ❗ Make sure Docker is installed on your machine. If Docker is not installed, please follow the official installation guide before continuing.

---

## 🐳 Run with Docker

Start the application using Docker Compose:

```bash
docker-compose up -d     
```

This command builds and runs the necessary containers for the GUI.

---

## 🧪 Testing with Simulated Signals

This project provides a test client to simulate signals, and a receiver program to send it to the GUI.

### 1. Run the Receiver (`tcp_receive.py`)

In a separate terminal, run the signal receiver:

```bash
python3 tcp_receive.py
```

This script listens for incoming TCP signal data and send it to the GUI to visualize it.

### 2. Run the Test Client (`tcp_client.py`)

In another terminal:

```bash
python3 tcp_client.py
```

This will generate and send test signal data to the running TCP server (`tcp_receive.py`).
