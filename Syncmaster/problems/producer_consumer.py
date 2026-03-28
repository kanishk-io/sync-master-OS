# problems/producer_consumer.py

import threading
import time
import random
from primitives.mutex import Mutex
from primitives.semaphore import Semaphore

# Declare global shared objects
buffer = []
empty_slots = None
full_slots = None
mutex = None

def producer(producer_id, items_to_produce):
    global buffer, empty_slots, full_slots, mutex

    for i in range(items_to_produce):
        item = f"Item-{producer_id}-{i}"
        time.sleep(random.uniform(0.2, 0.5))  # Simulate work

        empty_slots.wait()            # Wait for an empty slot
        mutex.acquire()               # Enter critical section
        buffer.append(item)
        print(f"Producer {producer_id} produced: {item}")
        mutex.release()               # Exit critical section
        full_slots.signal()           # Signal that an item is available

def consumer(consumer_id, items_to_consume):
    global buffer, empty_slots, full_slots, mutex

    for i in range(items_to_consume):
        full_slots.wait()             # Wait for an item to be available
        mutex.acquire()               # Enter critical section
        item = buffer.pop(0)
        print(f"Consumer {consumer_id} consumed: {item}")
        mutex.release()               # Exit critical section
        empty_slots.signal()          # Signal that a slot is now empty
        time.sleep(random.uniform(0.2, 0.5))  # Simulate work

def run():
    global buffer, empty_slots, full_slots, mutex

    print("\n--- Running Producer-Consumer Problem ---\n")

    # Get user input
    buffer_size = int(input("Enter buffer size: "))
    num_producers = int(input("Enter number of producers: "))
    num_consumers = int(input("Enter number of consumers: "))
    items_per_producer = int(input("Enter number of items each producer will produce: "))

    # Initialize buffer and synchronization primitives
    buffer = []
    empty_slots = Semaphore(buffer_size)
    full_slots = Semaphore(0)
    mutex = Mutex()

    total_items = num_producers * items_per_producer
    base_items_per_consumer = total_items // num_consumers
    remaining = total_items % num_consumers

    # Create producer threads
    producers = [
        threading.Thread(target=producer, args=(i, items_per_producer), name=f"Producer-{i}")
        for i in range(num_producers)
    ]

    # Create consumer threads with load-balanced item counts
    consumers = []
    for i in range(num_consumers):
        items = base_items_per_consumer + (1 if i < remaining else 0)
        consumers.append(
            threading.Thread(target=consumer, args=(i, items), name=f"Consumer-{i}")
        )

    # Start and wait for all threads
    for t in producers + consumers:
        t.start()
    for t in producers + consumers:
        t.join()

    print("\n--- Producer-Consumer Simulation Complete ---\n")
