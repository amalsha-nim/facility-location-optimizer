"""
optimizer.py

This module contains the Optimizer class, which encapsulates the core logic for
running the K-Means clustering algorithm to find optimal facility locations.
"""

import numpy as np
from sklearn.cluster import KMeans

class Optimizer:
    """
    Handles the K-Means clustering algorithm for facility location optimization.
    """
    def run_kmeans(self, customer_data, initial_facility_locations):
        """
        Runs the K-Means algorithm on customer data using provided initial facility locations.

        Args:
            customer_data (list): A list of (x, y) tuples for customer locations.
            initial_facility_locations (list): A list of (x, y) tuples for initial
                                               facility locations (used as initial centroids).

        Returns:
            tuple: A tuple containing:
                   - numpy.ndarray: The optimal facility locations (cluster centers).
                   - numpy.ndarray: The cluster labels for each customer.
        """
        customer_np_data = np.array(customer_data)
        initial_locations = np.array(initial_facility_locations)
        k = len(initial_locations)

        # Initialize KMeans with the user-provided initial locations
        kmeans = KMeans(n_clusters=k, init=initial_locations, n_init=1, random_state=0)
        kmeans.fit(customer_np_data)

        optimal_facility_locations = kmeans.cluster_centers_
        cluster_labels = kmeans.labels_

        return optimal_facility_locations, cluster_labels

