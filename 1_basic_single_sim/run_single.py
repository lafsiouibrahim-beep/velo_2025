import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
from model import State, run_simulation


def parse_args():
    """Parse command line arguments for single simulation run.
    
    Returns:
        Parsed arguments containing:
        - steps: Number of simulation steps
        - p1: Probability of movement from Mailly to Moulin
        - p2: Probability of movement from Moulin to Mailly
        - init_mailly: Initial bikes at Mailly station
        - init_moulin: Initial bikes at Moulin station
        - seed: Random seed (default: 0)
        - out_csv: Output CSV file path
        - plot: Boolean flag to generate plots
    
    Note:
        Use argparse.ArgumentParser to define all required and optional arguments
    """
    # TODO: Implement argument parsing
    pass


def main():
    """Main function to run a single bike-sharing simulation.
    
    This function should:
    1. Parse command line arguments
    2. Run the simulation with specified parameters
    3. Save results to CSV files (timeseries and metrics)
    4. Optionally generate and save plots
    
    Output files:
    - Timeseries data: CSV with time, mailly, moulin columns
    - Metrics data: CSV with key-value pairs of simulation metrics
    - Optional plot: PNG showing bike counts over time for both stations
    
    Note:
        Create output directories if they don't exist
        Save metrics as tab-separated key-value pairs
    """
    # TODO: Implement main simulation workflow
    pass


if __name__ == "__main__":
    main()
