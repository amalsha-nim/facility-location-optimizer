"""
main.py

This is the main entry point for the Facility Location Optimization application.
It initializes the Tkinter root window and creates an instance of the KMeansApp,
which handles the GUI and application logic.
"""

import tkinter as tk
from src.gui import KMeansApp

if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()

    # Instantiate the application
    app = KMeansApp(root)

    # Start the Tkinter event loop
    root.mainloop()

