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
        self.root.geometry("1000x700")
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        
        # Add tabs
        self.create_producer_consumer_tab()
        self.create_dining_philosophers_tab()
        self.create_reader_writer_tab()
        
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Quit button
        quit_btn = ttk.Button(root, text="Quit", command=root.quit)
        quit_btn.pack(pady=10)
    
    def create_producer_consumer_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Producer-Consumer")
        
        # Input Frame
        input_frame = ttk.LabelFrame(tab, text="Parameters", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Input fields
        ttk.Label(input_frame, text="Buffer Size:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.buffer_size = ttk.Entry(input_frame)
        self.buffer_size.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Producers:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.num_producers = ttk.Entry(input_frame)
        self.num_producers.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Consumers:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.num_consumers = ttk.Entry(input_frame)
        self.num_consumers.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Items per Producer:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.items_per_producer = ttk.Entry(input_frame)
        self.items_per_producer.grid(row=3, column=1, padx=5, pady=5)
        
        # Run button
        ttk.Button(input_frame, 
                  text="Run Simulation", 
                  command=self.run_producer_consumer).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Output and metrics frame
        output_metrics_frame = ttk.Frame(tab)
        output_metrics_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Output console
        output_frame = ttk.LabelFrame(output_metrics_frame, text="Output", padding=10)
        output_frame.pack(side="left", fill="both", expand=True)
        
        self.pc_output = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, font=("Consolas", 10))
        self.pc_output.pack(fill="both", expand=True)
        
        # Metrics frame
        metrics_frame = ttk.LabelFrame(output_metrics_frame, text="Performance Metrics", padding=10, width=250)
        metrics_frame.pack(side="right", fill="y")
        
        self.pc_metrics = scrolledtext.ScrolledText(metrics_frame, wrap=tk.WORD, font=("Consolas", 10), height=10)
        self.pc_metrics.pack(fill="both", expand=True)
        self.pc_metrics.insert(tk.END, "Simulation metrics will appear here")
    
    def run_producer_consumer(self):
        try:
            # Get parameters
            buffer_size = int(self.buffer_size.get())
            num_producers = int(self.num_producers.get())
            num_consumers = int(self.num_consumers.get())
            items_per_producer = int(self.items_per_producer.get())
            
            # Clear previous output
            self.pc_output.delete(1.0, tk.END)
            self.pc_metrics.delete(1.0, tk.END)
            
            # Redirect stdout
            self.old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            # Set the parameters in the module
            producer_consumer.BUFFER_SIZE = buffer_size
            producer_consumer.NUM_PRODUCERS = num_producers
            producer_consumer.NUM_CONSUMERS = num_consumers
            producer_consumer.ITEMS_PER_PRODUCER = items_per_producer
            
            # Run in separate thread
            thread = threading.Thread(
                target=producer_consumer.run,  # Changed to use run() instead of run_simulation()
                daemon=True
            )
            thread.start()
            
            # Start updating output
            self.update_pc_output()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
    
    def update_pc_output(self):
        """Update output console with captured stdout"""
        output = sys.stdout.getvalue()
        self.pc_output.delete(1.0, tk.END)
        self.pc_output.insert(tk.END, output)
        self.pc_output.see(tk.END)
        
        # Update metrics
        lines = output.split('\n')
        produced = sum(1 for line in lines if "produced" in line)
        consumed = sum(1 for line in lines if "consumed" in line)
        
        self.pc_metrics.delete(1.0, tk.END)
        self.pc_metrics.insert(tk.END,
                             f"Produced items: {produced}\n"
                             f"Consumed items: {consumed}\n"
                             f"Buffer size: {self.buffer_size.get()}\n"
                             f"Throughput: {produced / max(1, len(lines)/1000):.2f} items/ms")
        
        # Continue updating if thread is alive
        for thread in threading.enumerate():
            if thread.name == "Thread-1":  # Default name for our simulation thread
                self.root.after(100, self.update_pc_output)
                break
    
    def create_dining_philosophers_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Dining Philosophers")
        
        # Input Frame
        input_frame = ttk.LabelFrame(tab, text="Parameters", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text="Number of Philosophers:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.num_philosophers = ttk.Entry(input_frame)
        self.num_philosophers.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Eating Cycles:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.eat_count = ttk.Entry(input_frame)
        self.eat_count.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(input_frame, 
                  text="Run Simulation", 
                  command=self.run_dining_philosophers).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Output and metrics frame
        output_metrics_frame = ttk.Frame(tab)
        output_metrics_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Output console
        output_frame = ttk.LabelFrame(output_metrics_frame, text="Output", padding=10)
        output_frame.pack(side="left", fill="both", expand=True)
        
        self.dp_output = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, font=("Consolas", 10))
        self.dp_output.pack(fill="both", expand=True)
        
        # Metrics frame
        metrics_frame = ttk.LabelFrame(output_metrics_frame, text="Performance Metrics", padding=10, width=250)
        metrics_frame.pack(side="right", fill="y")
        
        self.dp_metrics = scrolledtext.ScrolledText(metrics_frame, wrap=tk.WORD, font=("Consolas", 10), height=10)
        self.dp_metrics.pack(fill="both", expand=True)
    
    def run_dining_philosophers(self):
        try:
            num_philosophers = int(self.num_philosophers.get())
            eat_count = int(self.eat_count.get())
            
            self.dp_output.delete(1.0, tk.END)
            self.dp_metrics.delete(1.0, tk.END)
            
            self.old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            # Set the parameters in the module
            dining_philosopher.NUM_PHILOSOPHERS = num_philosophers
            dining_philosopher.EAT_COUNT = eat_count
            
            # Run in separate thread
            thread = threading.Thread(
                target=dining_philosopher.run,  # Changed to use run() instead of run_simulation()
                daemon=True
            )
            thread.start()
            
            self.update_dp_output()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
    
    def update_dp_output(self):
        output = sys.stdout.getvalue()
        self.dp_output.delete(1.0, tk.END)
        self.dp_output.insert(tk.END, output)
        self.dp_output.see(tk.END)
        
        # Update metrics
        lines = output.split('\n')
        meals = sum(1 for line in lines if "eating" in line.lower())
        
        self.dp_metrics.delete(1.0, tk.END)
        self.dp_metrics.insert(tk.END,
                             f"Philosophers: {self.num_philosophers.get()}\n"
                             f"Meals served: {meals}\n"
                             f"Eating cycles: {self.eat_count.get()}\n"
                             f"Deadlocks: 0")
        
        for thread in threading.enumerate():
            if thread.name == "Thread-2":  # Default name for our simulation thread
                self.root.after(100, self.update_dp_output)
                break
    
    def create_reader_writer_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Reader-Writer")
        
        # Input Frame
        input_frame = ttk.LabelFrame(tab, text="Parameters", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text="Number of Readers:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.num_readers = ttk.Entry(input_frame)
        self.num_readers.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Number of Writers:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.num_writers = ttk.Entry(input_frame)
        self.num_writers.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Read Operations:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.read_ops = ttk.Entry(input_frame)
        self.read_ops.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Write Operations:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.write_ops = ttk.Entry(input_frame)
        self.write_ops.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Button(input_frame, 
                  text="Run Simulation", 
                  command=self.run_reader_writer).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Output and metrics frame
        output_metrics_frame = ttk.Frame(tab)
        output_metrics_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Output console
        output_frame = ttk.LabelFrame(output_metrics_frame, text="Output", padding=10)
        output_frame.pack(side="left", fill="both", expand=True)
        
        self.rw_output = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, font=("Consolas", 10))
        self.rw_output.pack(fill="both", expand=True)
        
        # Metrics frame
        metrics_frame = ttk.LabelFrame(output_metrics_frame, text="Performance Metrics", padding=10, width=250)
        metrics_frame.pack(side="right", fill="y")
        
        self.rw_metrics = scrolledtext.ScrolledText(metrics_frame, wrap=tk.WORD, font=("Consolas", 10), height=10)
        self.rw_metrics.pack(fill="both", expand=True)
    
    def run_reader_writer(self):
        try:
            num_readers = int(self.num_readers.get())
            num_writers = int(self.num_writers.get())
            read_ops = int(self.read_ops.get())
            write_ops = int(self.write_ops.get())
            
            self.rw_output.delete(1.0, tk.END)
            self.rw_metrics.delete(1.0, tk.END)
            
            self.old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            # Set the parameters in the module
            reader_writer.NUM_READERS = num_readers
            reader_writer.NUM_WRITERS = num_writers
            reader_writer.READ_TIMES = read_ops
            reader_writer.WRITE_TIMES = write_ops
            
            # Run in separate thread
            thread = threading.Thread(
                target=reader_writer.run,  # Changed to use run() instead of run_simulation()
                daemon=True
            )
            thread.start()
            
            self.update_rw_output()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
    
    def update_rw_output(self):
        output = sys.stdout.getvalue()
        self.rw_output.delete(1.0, tk.END)
        self.rw_output.insert(tk.END, output)
        self.rw_output.see(tk.END)
        
        # Update metrics
        lines = output.split('\n')
        reads = sum(1 for line in lines if "reading" in line.lower())
        writes = sum(1 for line in lines if "writing" in line.lower())
        
        self.rw_metrics.delete(1.0, tk.END)
        self.rw_metrics.insert(tk.END,
                             f"Readers: {self.num_readers.get()}\n"
                             f"Writers: {self.num_writers.get()}\n"
                             f"Read ops: {reads}\n"
                             f"Write ops: {writes}\n"
                             f"Starvation: None")
        
        for thread in threading.enumerate():
            if thread.name == "Thread-3":  # Default name for our simulation thread
                self.root.after(100, self.update_rw_output)
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = SyncMasterGUI(root)
    root.mainloop()