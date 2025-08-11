# Facility Location Optimizer with K-Means

This project is a desktop application built with Python and Tkinter that uses the K-Means clustering algorithm to find the optimal locations for new facilities (like warehouses or stores) based on existing customer data. The application provides a graphical user interface (GUI) for users to input customer and initial facility locations, run the optimization, and visualize the results.

## Features

- **GUI Interface:** An intuitive and user-friendly interface for managing data and running the optimization.  
- **Customer & Facility Input:** Manually add customer and initial facility locations.  
- **Excel Import:** Import customer and facility data directly from Excel files for large datasets.  
- **K-Means Optimization:** Calculates optimal facility locations that minimize the total distance to all assigned customers.  
- **Interactive Plotting:** Visualizes customer locations, initial facilities, optimal facilities, and their service areas using Matplotlib.  
- **Modular Codebase:** The project is organized into separate files for a clear separation of concerns (GUI, data management, optimization, and plotting).

## Prerequisites

Before you begin, ensure you have the following installed:  
- Python 3.x  
- Git (for cloning the repository)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/facility-location-optimizer.git
    cd facility-location-optimizer
    ```
2. Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    ```
3. Activate the virtual environment:  
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```  
    - On macOS and Linux:
      ```bash
      source venv/bin/activate
      ```
4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the application, make sure your virtual environment is active and then execute the main.py file:
```bash
python main.py
