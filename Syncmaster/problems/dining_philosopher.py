import threading
import time
import random
from primitives.mutex import Mutex

forks = []
NUM_PHILOSOPHERS = 5  # Default, overridden by user input

def philosopher(philosopher_id, eat_count):
    left_index = philosopher_id
    right_index = (philosopher_id + 1) % NUM_PHILOSOPHERS
    left = forks[left_index]
    right = forks[right_index]

    for i in range(eat_count):
        print(f"Philosopher {philosopher_id} is thinking...")
        time.sleep(random.uniform(0.5, 1.0))

        # Asymmetric acquisition to avoid deadlock
        if philosopher_id % 2 == 0:
            left.acquire()
            right.acquire()
            print(
                f"Philosopher {philosopher_id} is eating using forks "
                f"{left_index} (left) and {right_index} (right)."
            )
        else:
            right.acquire()
            left.acquire()
            print(
                f"Philosopher {philosopher_id} is eating using forks "
                f"{right_index} (right) and {left_index} (left)."
            )

        time.sleep(random.uniform(0.5, 1.0))

        left.release()
        right.release()
        print(f"Philosopher {philosopher_id} released forks {left_index} and {right_index}.\n")

def run():
    global forks, NUM_PHILOSOPHERS
    print("\n--- Running Dining Philosophers Problem ---\n")

    NUM_PHILOSOPHERS = int(input("Enter number of philosophers (≥2): "))
    eat_count = int(input("Enter number of times each philosopher eats: "))
    forks = [Mutex() for _ in range(NUM_PHILOSOPHERS)]

    threads = [
        threading.Thread(target=philosopher, args=(i, eat_count), name=f"Philosopher-{i}")
        for i in range(NUM_PHILOSOPHERS)
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("\n--- Dining Philosophers Simulation Complete ---\n")
