# SyncMaster — Thread Synchronization Simulator

A Python-based desktop application that visually simulates classic Operating System thread synchronization problems. Built with a Tkinter GUI and real-time performance metrics.

---

## What It Simulates

**Producer-Consumer Problem**
- Configurable buffer size, number of producers, consumers, and items per producer
- Tracks produced vs consumed items in real time
- Shows active thread count and buffer status

**Dining Philosophers Problem**
- Configurable number of philosophers and eating cycles
- Detects and reports deadlocks
- Tracks meals served per philosopher

**Reader-Writer Problem**
- Configurable readers, writers, and operation counts
- Detects starvation conditions
- Tracks concurrent read/write operations

---

## Features

- Tabbed GUI — each problem in its own tab
- Real-time output log as threads execute
- Live performance metrics panel (items processed, deadlocks, starvation, thread status)
- CLI version available via `main.py` for terminal use
- Custom Semaphore and Mutex implementations

---

## Tech Stack

| | |
|---|---|
| Language | Python 3 |
| GUI | Tkinter + ttk |
| Concurrency | Python `threading` module |
| Sync Primitives | Custom Semaphore, Mutex classes |

---

## Project Structure

```
syncmaster/
├── main.py               # CLI entry point
├── SyncMasterGUI.py      # GUI entry point
└── problems/
    ├── producer_consumer.py
    ├── dining_philosopher.py
    └── reader_writer.py
```

---

## How to Run

**GUI Version**
```bash
git clone https://github.com/kanishk-io/syncmaster.git
cd syncmaster
python SyncMasterGUI.py
```

**CLI Version**
```bash
python main.py
```

No external dependencies — uses Python standard library only.

---

## Project Context

Built as part of an Operating Systems course to demonstrate thread synchronization concepts including mutual exclusion, semaphores, deadlock prevention, and starvation handling.

---

## License

MIT
