"""
data_manager.py

This module contains the DataManager class, which is responsible for managing
all data related to customer locations and facility locations. It handles
adding, clearing, and importing data.
"""

import pandas as pd
from tkinter import filedialog, messagebox

class DataManager:
    """
    Manages all data for the application, including customer and facility locations.

    Attributes:
        customer_data (list): A list of tuples storing customer (x, y) coordinates.
        initial_facility_locations (list): A list of tuples for initial facility (x, y) coordinates.
        optimal_facility_locations (numpy.ndarray or None): The optimized facility locations from K-Means.
        cluster_labels (numpy.ndarray or None): The cluster assignment for each customer.
    """
    def __init__(self):
        """Initializes the DataManager with empty data lists."""
        self.customer_data = []
        self.initial_facility_locations = []
        self.optimal_facility_locations = None
        self.cluster_labels = None

    def add_customer(self, x, y):
        """Adds a new customer location to the data."""
        self.customer_data.append((x, y))

    def add_initial_facility(self, x, y):
        """Adds a new initial facility location to the data."""
        self.initial_facility_locations.append((x, y))

    def clear_customers(self):
        """Clears all customer data."""
        self.customer_data = []

    def clear_facilities(self):
        """
        Clears all initial and optimal facility data.
        """
        self.initial_facility_locations = []
        self.optimal_facility_locations = None
        self.cluster_labels = None

    def set_optimal_facilities(self, locations, labels):
        """
        Sets the results of the optimization.

        Args:
            locations (numpy.ndarray): The calculated optimal facility locations.
            labels (numpy.ndarray): The cluster labels for each customer.
        """
        self.optimal_facility_locations = locations
        self.cluster_labels = labels

    def import_customers_excel(self):
        """
        Opens a file dialog to import customer locations from an Excel file.

        Returns:
            bool: True if the import was successful, False otherwise.
        """
        filepath = filedialog.askopenfilename(
            title="Select Customer Locations Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if not filepath:
            return False
            
        try:
            df = pd.read_excel(filepath)
            if 'X' not in df.columns or 'Y' not in df.columns:
                messagebox.showerror("Error", "Excel file must contain 'X' and 'Y' columns")
                return False
                
            new_customers = list(zip(df['X'], df['Y']))
            self.customer_data.extend(new_customers)
            messagebox.showinfo("Success", f"Added {len(new_customers)} customer locations from Excel")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import Excel file:\n{str(e)}")
            return False

    def import_facilities_excel(self):
        """
        Opens a file dialog to import initial facility locations from an Excel file.
        
        Returns:
            bool: True if the import was successful, False otherwise.
        """
        filepath = filedialog.askopenfilename(
            title="Select Facility Locations Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if not filepath:
            return False
            
        try:
            df = pd.read_excel(filepath)
            if 'X' not in df.columns or 'Y' not in df.columns:
                messagebox.showerror("Error", "Excel file must contain 'X' and 'Y' columns")
                return False
                
            new_facilities = list(zip(df['X'], df['Y']))
            self.initial_facility_locations.extend(new_facilities)
            messagebox.showinfo("Success", f"Added {len(new_facilities)} facility locations from Excel")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import Excel file:\n{str(e)}")
            return False
