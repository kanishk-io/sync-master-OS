import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import sys
from io import StringIO
from problems import producer_consumer, dining_philosopher, reader_writer

class SyncMasterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SyncMaster - Thread Synchronization")
        self.root.geometry("1100x750")

        self.notebook = ttk.Notebook(root)
        self.create_producer_consumer_tab()
        self.create_dining_philosophers_tab()
        self.create_reader_writer_tab()
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Quit Button
        button_frame = tk.Frame(root)
        button_frame.pack(side=tk.BOTTOM, pady=10)
        quit_btn = ttk.Button(button_frame, text="Quit", command=root.quit)
        quit_btn.pack(padx=10, pady=5)

    # ========== PRODUCER-CONSUMER TAB ==========
    def create_producer_consumer_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Producer-Consumer")

        # Input Frame
        input_frame = ttk.LabelFrame(tab, text="Parameters", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Input fields
        self.buffer_size = self._create_labeled_entry(input_frame, "Buffer Size:", 0)
        self.num_producers = self._create_labeled_entry(input_frame, "Producers:", 1)
        self.num_consumers = self._create_labeled_entry(input_frame, "Consumers:", 2)
        self.items_per_producer = self._create_labeled_entry(input_frame, "Items per Producer:", 3)

        # Run button
        ttk.Button(input_frame, 
                 text="Run Simulation", 
                 command=self.run_producer_consumer).grid(row=4, column=0, columnspan=2, pady=10)

        # Output and metrics
        self._create_output_metrics_frames(tab, "pc")

    def run_producer_consumer(self):
        try:
            buffer_size = int(self.buffer_size.get())
            num_producers = int(self.num_producers.get())
            num_consumers = int(self.num_consumers.get())
            items_per_producer = int(self.items_per_producer.get())

            self.pc_output.delete(1.0, tk.END)
            self.pc_metrics.delete(1.0, tk.END)

            # Redirect stdout
            self.old_stdout = sys.stdout
            self.stdout_capture = StringIO()
            sys.stdout = self.stdout_capture

            # Initialize simulation parameters
            producer_consumer.buffer = []
            producer_consumer.empty_slots = producer_consumer.Semaphore(buffer_size)
            producer_consumer.full_slots = producer_consumer.Semaphore(0)
            producer_consumer.mutex = producer_consumer.Mutex()

            # Create and start threads
            self.pc_threads = []
            for i in range(num_producers):
                t = threading.Thread(
                    target=producer_consumer.producer,
                    args=(i, items_per_producer),
                    daemon=True
                )
                self.pc_threads.append(t)
                t.start()

            total_items = num_producers * items_per_producer
            base_items = total_items // num_consumers
            remaining = total_items % num_consumers
            
            for i in range(num_consumers):
                items = base_items + (1 if i < remaining else 0)
                t = threading.Thread(
                    target=producer_consumer.consumer,
                    args=(i, items),
                    daemon=True
                )
                self.pc_threads.append(t)
                t.start()

            # Start updating output
            self.update_pc_output()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
            sys.stdout = self.old_stdout

    def update_pc_output(self):
        output = self.stdout_capture.getvalue()
        self.pc_output.delete(1.0, tk.END)
        self.pc_output.insert(tk.END, output)
        self.pc_output.see(tk.END)

        # Calculate metrics
        lines = output.strip().split('\n')
        produced = sum(1 for line in lines if "produced" in line.lower())
        consumed = sum(1 for line in lines if "consumed" in line.lower())
        
        # Update metrics
        self.pc_metrics.delete(1.0, tk.END)
        self.pc_metrics.insert(tk.END,
            f"Total Produced Items: {produced}\n"
            f"Total Consumed Items: {consumed}\n"
            f"Buffer Size: {self.buffer_size.get()}\n"
            f"Threads Active: {sum(1 for t in self.pc_threads if t.is_alive())}\n"
            f"Status: {'Running' if any(t.is_alive() for t in self.pc_threads) else 'Completed'}")

        # Continue updating if any threads are alive
        if any(t.is_alive() for t in self.pc_threads):
            self.root.after(100, self.update_pc_output)
        else:
            sys.stdout = self.old_stdout
            self.pc_metrics.insert(tk.END, "\n\nSimulation completed successfully!")

    # ========== DINING PHILOSOPHERS TAB ==========
    def create_dining_philosophers_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Dining Philosophers")

        # Input Frame
        input_frame = ttk.LabelFrame(tab, text="Parameters", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Input fields
        self.num_philosophers = self._create_labeled_entry(input_frame, "Number of Philosophers:", 0)
        self.eat_count = self._create_labeled_entry(input_frame, "Eating Cycles:", 1)

        # Run button
        ttk.Button(input_frame, 
                 text="Run Simulation", 
                 command=self.run_dining_philosophers).grid(row=2, column=0, columnspan=2, pady=10)

        # Output and metrics
        self._create_output_metrics_frames(tab, "dp")

    def run_dining_philosophers(self):
        try:
            num_philosophers = int(self.num_philosophers.get())
            eat_count = int(self.eat_count.get())

            self.dp_output.delete(1.0, tk.END)
            self.dp_metrics.delete(1.0, tk.END)

            # Redirect stdout
            self.old_stdout = sys.stdout
            self.stdout_capture = StringIO()
            sys.stdout = self.stdout_capture

            # Initialize simulation parameters
            dining_philosopher.NUM_PHILOSOPHERS = num_philosophers
            dining_philosopher.forks = [dining_philosopher.Mutex() for _ in range(num_philosophers)]

            # Create and start threads
            self.dp_threads = []
            for i in range(num_philosophers):
                t = threading.Thread(
                    target=dining_philosopher.philosopher,
                    args=(i, eat_count),
                    daemon=True
                )
                self.dp_threads.append(t)
                t.start()

            # Start updating output
            self.update_dp_output()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
            sys.stdout = self.old_stdout

    def update_dp_output(self):
        output = self.stdout_capture.getvalue()
        self.dp_output.delete(1.0, tk.END)
        self.dp_output.insert(tk.END, output)
        self.dp_output.see(tk.END)

        # Calculate metrics
        lines = output.strip().split('\n')
        meals = sum(1 for line in lines if "eating" in line.lower())
        deadlocks = sum(1 for line in lines if "deadlock" in line.lower())
        
        # Update metrics
        self.dp_metrics.delete(1.0, tk.END)
        self.dp_metrics.insert(tk.END,
            f"Philosophers: {self.num_philosophers.get()}\n"
            f"Meals Served: {meals}\n"
            f"Eating Cycles: {self.eat_count.get()}\n"
            f"Deadlocks Detected: {deadlocks}\n"
            f"Status: {'Running' if any(t.is_alive() for t in self.dp_threads) else 'Completed'}")

        # Continue updating if any threads are alive
        if any(t.is_alive() for t in self.dp_threads):
            self.root.after(100, self.update_dp_output)
        else:
            sys.stdout = self.old_stdout
            self.dp_metrics.insert(tk.END, "\n\nSimulation completed successfully!")

    # ========== READER-WRITER TAB ==========
    def create_reader_writer_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Reader-Writer")

        # Input Frame
        input_frame = ttk.LabelFrame(tab, text="Parameters", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Input fields
        self.num_readers = self._create_labeled_entry(input_frame, "Number of Readers:", 0)
        self.num_writers = self._create_labeled_entry(input_frame, "Number of Writers:", 1)
        self.read_ops = self._create_labeled_entry(input_frame, "Read Operations:", 2)
        self.write_ops = self._create_labeled_entry(input_frame, "Write Operations:", 3)

        # Run button
        ttk.Button(input_frame, 
                 text="Run Simulation", 
                 command=self.run_reader_writer).grid(row=4, column=0, columnspan=2, pady=10)

        # Output and metrics
        self._create_output_metrics_frames(tab, "rw")

    def run_reader_writer(self):
        try:
            num_readers = int(self.num_readers.get())
            num_writers = int(self.num_writers.get())
            read_ops = int(self.read_ops.get())
            write_ops = int(self.write_ops.get())

            self.rw_output.delete(1.0, tk.END)
            self.rw_metrics.delete(1.0, tk.END)

            # Redirect stdout
            self.old_stdout = sys.stdout
            self.stdout_capture = StringIO()
            sys.stdout = self.stdout_capture

            # Initialize simulation parameters
            reader_writer.read_count = 0
            reader_writer.read_count_mutex = reader_writer.Mutex()
            reader_writer.resource_access = reader_writer.Semaphore(1)

            # Create and start threads
            self.rw_threads = []
            for i in range(num_readers):
                t = threading.Thread(
                    target=reader_writer.reader,
                    args=(i, read_ops),
                    daemon=True
                )
                self.rw_threads.append(t)
                t.start()

            for i in range(num_writers):
                t = threading.Thread(
                    target=reader_writer.writer,
                    args=(i, write_ops),
                    daemon=True
                )
                self.rw_threads.append(t)
                t.start()

            # Start updating output
            self.update_rw_output()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
            sys.stdout = self.old_stdout

    def update_rw_output(self):
        output = self.stdout_capture.getvalue()
        self.rw_output.delete(1.0, tk.END)
        self.rw_output.insert(tk.END, output)
        self.rw_output.see(tk.END)

        # Calculate metrics
        lines = output.strip().split('\n')
        reads = sum(1 for line in lines if "reading" in line.lower())
        writes = sum(1 for line in lines if "writing" in line.lower())
        starvations = sum(1 for line in lines if "starvation" in line.lower())
        
        # Update metrics
        self.rw_metrics.delete(1.0, tk.END)
        self.rw_metrics.insert(tk.END,
            f"Readers: {self.num_readers.get()}\n"
            f"Writers: {self.num_writers.get()}\n"
            f"Read Operations: {reads}\n"
            f"Write Operations: {writes}\n"
            f"Starvations Detected: {starvations}\n"
            f"Status: {'Running' if any(t.is_alive() for t in self.rw_threads) else 'Completed'}")

        # Continue updating if any threads are alive
        if any(t.is_alive() for t in self.rw_threads):
            self.root.after(100, self.update_rw_output)
        else:
            sys.stdout = self.old_stdout
            self.rw_metrics.insert(tk.END, "\n\nSimulation completed successfully!")

    # ========== HELPER METHODS ==========
    def _create_labeled_entry(self, frame, text, row):
        ttk.Label(frame, text=text).grid(row=row, column=0, padx=5, pady=5, sticky="e")
        entry = ttk.Entry(frame)
        entry.grid(row=row, column=1, padx=5, pady=5)
        return entry

    def _create_output_metrics_frames(self, tab, prefix):
        """Helper to create consistent output/metrics frames for each tab"""
        output_metrics_frame = ttk.Frame(tab)
        output_metrics_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Output frame
        output_frame = ttk.LabelFrame(output_metrics_frame, text="Output", padding=10)
        output_frame.pack(side="left", fill="both", expand=True)
        output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, font=("Consolas", 10))
        output_text.pack(fill="both", expand=True)
        setattr(self, f"{prefix}_output", output_text)

        # Metrics frame
        metrics_frame = ttk.LabelFrame(output_metrics_frame, text="Performance Metrics", padding=10, width=250)
        metrics_frame.pack(side="right", fill="y")
        metrics_text = scrolledtext.ScrolledText(metrics_frame, wrap=tk.WORD, font=("Consolas", 10), height=10)
        metrics_text.pack(fill="both", expand=True)
        metrics_text.insert(tk.END, "Waiting for simulation...")
        setattr(self, f"{prefix}_metrics", metrics_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = SyncMasterGUI(root)
    root.mainloop()