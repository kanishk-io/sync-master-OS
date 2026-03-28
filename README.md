

# SyncMaster - Thread Synchronization Visualizer

A comprehensive educational tool for visualizing and understanding classic operating system synchronization problems through interactive simulations.

## 📋 Overview

SyncMaster provides both CLI and GUI interfaces to demonstrate three fundamental concurrency problems in computer science:
- **Producer-Consumer Problem** - Demonstrates bounded buffer synchronization
- **Dining Philosophers Problem** - Illustrates deadlock and resource contention
- **Reader-Writer Problem** - Shows concurrent read/write access control

## ✨ Features

- **Interactive GUI** - Built with tkinter, featuring tabbed interface for each synchronization problem
- **Real-time Visualization** - Live output streaming and thread status monitoring
- **Performance Metrics** - Track operations, thread states, and detect synchronization issues
- **Configurable Parameters** - Adjust buffer sizes, thread counts, and operation cycles
- **Educational Tool** - Perfect for students learning operating systems and concurrent programming

## 🚀 Quick Start

### CLI Mode
```bash
python main.py
```

### GUI Mode
```bash
python SyncMasterGUI.py
```

## 🎯 Synchronization Problems

### Producer-Consumer
- Configurable buffer size
- Multiple producers and consumers
- Semaphore-based synchronization
- Tracks produced/consumed items

### Dining Philosophers
- Adjustable number of philosophers
- Fork contention visualization
- Deadlock detection
- Configurable eating cycles

### Reader-Writer
- Concurrent readers support
- Writer exclusivity enforcement
- Starvation detection
- Operation tracking

## 🛠️ Technologies

- **Python 3.x**
- **tkinter** - GUI framework
- **threading** - Concurrency implementation
- Custom synchronization primitives (Semaphore, Mutex)

## 📊 Use Cases

- Operating Systems coursework
- Concurrent programming education
- Debugging synchronization issues
- Understanding thread synchronization patterns

---

