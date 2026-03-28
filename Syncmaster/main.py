# main.py
from problems import producer_consumer, dining_philosopher, reader_writer

def main():
    print("Select a problem to run:")
    print("1. Producer-Consumer")
    print("2. Dining Philosopher")
    print("3. Reader-Writer")

    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        producer_consumer.run()
    elif choice == '2':
        dining_philosopher.run()
    elif choice == '3':
        reader_writer.run()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
