"""
plotter.py

This module contains the Plotter class, which is responsible for all
Matplotlib visualization and embedding it within the Tkinter GUI.
"""

import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.patches as patches
# We will get data from an instance of DataManager, so no direct import here
# from data_manager import DataManager

class Plotter:
    """
    Handles the Matplotlib plotting for the application.

    This class creates the plot, embeds it in a Tkinter frame, and provides
    a method to update the plot based on the current data state.
    """
    def __init__(self, root):
        """
        Initializes the plotter component.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = None
        self.toolbar = None
        self.data_manager = None # This will be set by the main app

    def set_data(self, data_manager):
        """Sets the reference to the DataManager instance."""
        self.data_manager = data_manager

    def setup_plot(self, master):
        """
        Sets up the Matplotlib plot and embeds it into a Tkinter frame.

        Args:
            master (tk.Frame): The master widget to embed the plot into.
        """
        plot_frame = tk.Frame(master)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, plot_frame)
        self.toolbar.update()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_plot(self):
        """
        Clears the current plot and redraws all customer, initial facility,
        and optimal facility locations based on the data in the DataManager.
        """
        self.ax.clear()
        
        customer_np_data = np.array(self.data_manager.customer_data)
        initial_locations = np.array(self.data_manager.initial_facility_locations)
        optimal_locations = self.data_manager.optimal_facility_locations
        cluster_labels = self.data_manager.cluster_labels

        if customer_np_data.size > 0:
            # Plot customer points
            if cluster_labels is not None and optimal_locations is not None:
                self._plot_clustered_customers(customer_np_data, optimal_locations, cluster_labels)
                self._plot_optimal_facilities(optimal_locations, cluster_labels)
            else:
                self.ax.scatter(customer_np_data[:, 0], customer_np_data[:, 1], 
                                s=50, color='blue', label='Customer Locations')

            # Plot initial facility locations if available
            if initial_locations.size > 0:
                self.ax.scatter(initial_locations[:, 0], initial_locations[:, 1],
                                marker='o', s=150, color='orange', 
                                edgecolor='black', linewidth=1.5,
                                label='Initial Facilities')

            self._adjust_plot_limits(customer_np_data, initial_locations, optimal_locations)

        # Set labels and legend
        self.ax.set_title('Facility Location Optimization with Service Areas', fontsize=16)
        self.ax.set_xlabel('X Coordinate')
        self.ax.set_ylabel('Y Coordinate')
        self.ax.grid(True)
        
        # Improved legend handling to avoid duplicate labels
        handles, labels = self.ax.get_legend_handles_labels()
        if handles:
            unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
            self.ax.legend(*zip(*unique), loc='upper right')
        
        self.canvas.draw()

    def _plot_clustered_customers(self, customer_np_data, optimal_locations, cluster_labels):
        """Plots customers colored by their assigned cluster."""
        try:
            cmap = plt.colormaps['tab10']
        except AttributeError:
            cmap = plt.get_cmap('tab10')

        for i in range(len(customer_np_data)):
            color = cmap(cluster_labels[i] % cmap.N)
            self.ax.scatter(customer_np_data[i, 0], customer_np_data[i, 1],
                            color=color, s=50, alpha=0.7,
                            label=f'Cluster {cluster_labels[i]+1}' if i == 0 else "")

    def _plot_optimal_facilities(self, optimal_locations, cluster_labels):
        """Plots optimal facilities and their service areas (circles)."""
        try:
            cmap = plt.colormaps['tab10']
        except AttributeError:
            cmap = plt.get_cmap('tab10')

        radii = []
        for i in range(len(optimal_locations)):
            cluster_points = np.array(self.data_manager.customer_data)[cluster_labels == i]
            if len(cluster_points) > 0:
                distances = np.linalg.norm(cluster_points - optimal_locations[i], axis=1)
                radii.append(np.max(distances))
            else:
                radii.append(0)

        for i, (facility, radius) in enumerate(zip(optimal_locations, radii)):
            # Draw service area circle
            circle = patches.Circle(
                (facility[0], facility[1]),
                radius,
                color=cmap(i % cmap.N),
                alpha=0.15,
                fill=True,
                linestyle='-',
                linewidth=1
            )
            self.ax.add_patch(circle)
            
            # Draw facility marker
            self.ax.scatter(facility[0], facility[1],
                            marker='X', s=200, color='red', 
                            edgecolor='black', linewidth=2,
                            label='Optimal Facilities' if i == 0 else "")
            
            # Add facility number label
            self.ax.text(facility[0], facility[1], f'F{i+1}',
                         ha='center', va='center', 
                         color='black', fontweight='bold')

    def _adjust_plot_limits(self, customer_data, initial_data, optimal_data):
        """Dynamically adjusts the plot limits to fit all data points and circles."""
        all_x = []
        all_y = []
        if customer_data.size > 0:
            all_x.extend(customer_data[:, 0])
            all_y.extend(customer_data[:, 1])
        if initial_data.size > 0:
            all_x.extend(initial_data[:, 0])
            all_y.extend(initial_data[:, 1])
        if optimal_data is not None:
            all_x.extend(optimal_data[:, 0])
            all_y.extend(optimal_data[:, 1])

            # Include circle edges in the plot limits
            if self.data_manager.cluster_labels is not None:
                radii = []
                for i in range(len(optimal_data)):
                    cluster_points = np.array(self.data_manager.customer_data)[self.data_manager.cluster_labels == i]
                    if len(cluster_points) > 0:
                        distances = np.linalg.norm(cluster_points - optimal_data[i], axis=1)
                        radii.append(np.max(distances))
                    else:
                        radii.append(0)
                max_radius = max(radii) if radii else 0
                all_x.extend([x + max_radius for x in optimal_data[:, 0]])
                all_x.extend([x - max_radius for x in optimal_data[:, 0]])
                all_y.extend([y + max_radius for y in optimal_data[:, 1]])
                all_y.extend([y - max_radius for y in optimal_data[:, 1]])

        if all_x and all_y:
            min_x, max_x = np.min(all_x), np.max(all_x)
            min_y, max_y = np.min(all_y), np.max(all_y)
            
            padding_x = (max_x - min_x) * 0.1
            padding_y = (max_y - min_y) * 0.1
            padding_x = padding_x if padding_x > 0 else 1.0
            padding_y = padding_y if padding_y > 0 else 1.0
            
            self.ax.set_xlim(min_x - padding_x, max_x + padding_x)
            self.ax.set_ylim(min_y - padding_y, max_y + padding_y)
