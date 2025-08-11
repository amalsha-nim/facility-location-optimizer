"""
gui.py

This module contains the main KMeansApp class, which sets up the Tkinter GUI
and orchestrates the interactions between the data manager, optimizer, and plotter.
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
from data_manager import DataManager
from optimizer import Optimizer
from plotter import Plotter

class KMeansApp:
    """
    The main application class for the K-Means Facility Location Optimizer.

    This class is responsible for building the user interface, handling events
    from the widgets, and coordinating the data management, optimization, and
    plotting components.
    """
    def __init__(self, root):
        """
        Initializes the application, setting up the GUI and internal components.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("K-Means Clustering for Facility Location")
        self.root.geometry("1200x800")

        # Instantiate the modular components
        self.data_manager = DataManager()
        self.optimizer = Optimizer()
        self.plotter = Plotter(root)
        
        # Set up a reference for the plotter to access app data
        self.plotter.set_data(self.data_manager)

        self._create_widgets()
        
        # Initial plot update
        self.plotter.update_plot()

    def _create_widgets(self):
        """
        Creates and packs all the Tkinter widgets for the application.
        This includes the input frames, buttons, text displays, and the plot frame.
        """
        # --- Left Panel: Input Controls ---
        input_frame = tk.Frame(self.root, padx=10, pady=10, bd=2, relief="groove")
        input_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Customer Input Section
        tk.Label(input_frame, text="Customer Locations (X, Y):", font=("Arial", 12, "bold")).pack(pady=(0, 5))
        customer_input_frame = tk.Frame(input_frame)
        customer_input_frame.pack(pady=5)
        tk.Label(customer_input_frame, text="X:").grid(row=0, column=0, padx=2)
        self.customer_x_entry = tk.Entry(customer_input_frame, width=10)
        self.customer_x_entry.grid(row=0, column=1, padx=2)
        tk.Label(customer_input_frame, text="Y:").grid(row=0, column=2, padx=2)
        self.customer_y_entry = tk.Entry(customer_input_frame, width=10)
        self.customer_y_entry.grid(row=0, column=3, padx=2)

        customer_button_frame = tk.Frame(input_frame)
        customer_button_frame.pack(pady=5)
        add_customer_btn = tk.Button(customer_button_frame, text="Add Customer", command=self._add_customer)
        add_customer_btn.pack(side=tk.LEFT, padx=5)
        import_customers_btn = tk.Button(customer_button_frame, text="Import Customers (Excel)", command=self._import_customers_excel)
        import_customers_btn.pack(side=tk.LEFT, padx=5)
        clear_customers_btn = tk.Button(input_frame, text="Clear All Customers", command=self._clear_customers)
        clear_customers_btn.pack(pady=5)

        tk.Label(input_frame, text="Added Customers:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        self.customer_list_text = scrolledtext.ScrolledText(input_frame, width=30, height=10, wrap=tk.WORD)
        self.customer_list_text.pack(pady=5)
        self.customer_list_text.config(state=tk.DISABLED)

        # Facility Input Section
        tk.Label(input_frame, text="\nInitial Facility Locations (X, Y):", font=("Arial", 12, "bold")).pack(pady=(10, 5))
        facility_input_frame = tk.Frame(input_frame)
        facility_input_frame.pack(pady=5)
        tk.Label(facility_input_frame, text="X:").grid(row=0, column=0, padx=2)
        self.facility_x_entry = tk.Entry(facility_input_frame, width=10)
        self.facility_x_entry.grid(row=0, column=1, padx=2)
        tk.Label(facility_input_frame, text="Y:").grid(row=0, column=2, padx=2)
        self.facility_y_entry = tk.Entry(facility_input_frame, width=10)
        self.facility_y_entry.grid(row=0, column=3, padx=2)

        facility_button_frame = tk.Frame(input_frame)
        facility_button_frame.pack(pady=5)
        add_facility_btn = tk.Button(facility_button_frame, text="Add Facility", command=self._add_facility)
        add_facility_btn.pack(side=tk.LEFT, padx=5)
        import_facilities_btn = tk.Button(facility_button_frame, text="Import Facilities (Excel)", command=self._import_facilities_excel)
        import_facilities_btn.pack(side=tk.LEFT, padx=5)
        clear_facilities_btn = tk.Button(input_frame, text="Clear All Facilities", command=self._clear_facilities)
        clear_facilities_btn.pack(pady=5)

        tk.Label(input_frame, text="Added Facilities:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        self.facility_list_text = scrolledtext.ScrolledText(input_frame, width=30, height=5, wrap=tk.WORD)
        self.facility_list_text.pack(pady=5)
        self.facility_list_text.config(state=tk.DISABLED)

        tk.Label(input_frame, text="Optimal Facilities:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        self.optimal_facility_list_text = scrolledtext.ScrolledText(input_frame, width=30, height=5, wrap=tk.WORD)
        self.optimal_facility_list_text.pack(pady=5)
        self.optimal_facility_list_text.config(state=tk.DISABLED)

        # Calculate Button
        calculate_btn = tk.Button(input_frame, text="Calculate Optimal Facilities", 
                                 command=self._run_calculation, 
                                 font=("Arial", 14, "bold"), 
                                 bg="lightblue")
        calculate_btn.pack(pady=20)
        
        # --- Right Panel: Matplotlib Plot ---
        self.plotter.setup_plot(self.root)

    def _update_display(self):
        """Updates all the text displays and the plot."""
        self._update_customer_list_display()
        self._update_facility_list_display()
        self._update_optimal_facility_list_display()
        self.plotter.update_plot()
        
    def _add_customer(self):
        """Adds a customer location from the input fields and updates the display."""
        try:
            x = float(self.customer_x_entry.get())
            y = float(self.customer_y_entry.get())
            self.data_manager.add_customer(x, y)
            self.customer_x_entry.delete(0, tk.END)
            self.customer_y_entry.delete(0, tk.END)
            self._update_display()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for X and Y coordinates.")

    def _add_facility(self):
        """Adds an initial facility location from the input fields and updates the display."""
        try:
            x = float(self.facility_x_entry.get())
            y = float(self.facility_y_entry.get())
            self.data_manager.add_initial_facility(x, y)
            self.facility_x_entry.delete(0, tk.END)
            self.facility_y_entry.delete(0, tk.END)
            self._update_display()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for X and Y coordinates.")

    def _import_customers_excel(self):
        """Handles the import of customer locations from an Excel file."""
        if self.data_manager.import_customers_excel():
            self._update_display()

    def _import_facilities_excel(self):
        """Handles the import of initial facility locations from an Excel file."""
        if self.data_manager.import_facilities_excel():
            self._update_display()

    def _clear_customers(self):
        """Clears all customer data and updates the display."""
        self.data_manager.clear_customers()
        messagebox.showinfo("Cleared", "All customer locations cleared.")
        self._update_display()

    def _clear_facilities(self):
        """Clears all facility data and updates the display."""
        self.data_manager.clear_facilities()
        messagebox.showinfo("Cleared", "All facility locations cleared.")
        self._update_display()
        
    def _update_customer_list_display(self):
        """Updates the scrolled text widget with the current customer data."""
        self.customer_list_text.config(state=tk.NORMAL)
        self.customer_list_text.delete(1.0, tk.END)
        for i, (x, y) in enumerate(self.data_manager.customer_data):
            self.customer_list_text.insert(tk.END, f"Customer {i+1}: ({x:.2f}, {y:.2f})\n")
        self.customer_list_text.config(state=tk.DISABLED)

    def _update_facility_list_display(self):
        """Updates the scrolled text widget with the current initial facility data."""
        self.facility_list_text.config(state=tk.NORMAL)
        self.facility_list_text.delete(1.0, tk.END)
        for i, (x, y) in enumerate(self.data_manager.initial_facility_locations):
            self.facility_list_text.insert(tk.END, f"Facility {i+1}: ({x:.2f}, {y:.2f})\n")
        self.facility_list_text.config(state=tk.DISABLED)

    def _update_optimal_facility_list_display(self):
        """Updates the scrolled text widget with the current optimal facility data."""
        self.optimal_facility_list_text.config(state=tk.NORMAL)
        self.optimal_facility_list_text.delete(1.0, tk.END)
        if self.data_manager.optimal_facility_locations is not None:
            for i, (x, y) in enumerate(self.data_manager.optimal_facility_locations):
                self.optimal_facility_list_text.insert(tk.END, 
                    f"Facility {i+1}: ({x:.2f}, {y:.2f})\n")
        self.optimal_facility_list_text.config(state=tk.DISABLED)

    def _run_calculation(self):
        """Triggers the K-Means calculation and updates the plot with the results."""
        if not self.data_manager.customer_data:
            messagebox.showwarning("No Customers", "Please add customer locations first.")
            return
        if not self.data_manager.initial_facility_locations:
            messagebox.showwarning("No Facilities", "Please add initial facility locations first.")
            return

        try:
            optimal_locations, cluster_labels = self.optimizer.run_kmeans(
                self.data_manager.customer_data,
                self.data_manager.initial_facility_locations
            )
            self.data_manager.set_optimal_facilities(optimal_locations, cluster_labels)
            
            self._update_display()
            messagebox.showinfo("Calculation Complete", "Optimal facility locations calculated!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during calculation: {e}")
