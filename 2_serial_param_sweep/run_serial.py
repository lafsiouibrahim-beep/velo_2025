import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from model import State, run_simulation


def parse_args():
    """Parse command line arguments for serial parameter sweep.
    
    Returns:
        Parsed arguments containing:
        - params: Path to CSV file with parameter combinations
        - out_dir: Output directory for results
        - plot: Boolean flag to generate plots after run
        - smooth_window: Window size for smoothing timeseries (default: 1, no smoothing)
    
    Note:
        Use argparse.ArgumentParser to define all required and optional arguments
    """
    # TODO: Implement argument parsing
    pass


def main():
    """Main function to run serial parameter sweep.
    
    This function should:
    1. Parse command line arguments
    2. Read parameter combinations from CSV file
    3. Run simulations serially for each parameter combination
    4. Collect and aggregate results
    5. Save aggregated results to CSV files
    6. Optionally generate plots
    
    Expected parameter CSV columns:
    - init_mailly: Initial bikes at Mailly
    - init_moulin: Initial bikes at Moulin
    - steps: Number of simulation steps
    - p1: Probability Mailly->Moulin
    - p2: Probability Moulin->Mailly
    - seed: Random seed
    
    Output files:
    - metrics.csv: Aggregated metrics for all runs
    - timeseries.csv: Tidy format timeseries data for all runs
    - Optional plots: PNG files for timeseries and metrics visualization
    
    Note:
        - Process each row in the parameters file as a separate simulation run
        - Add run_id to track individual simulations
        - Convert timeseries to tidy format (melt operation)
        - Handle smoothing for timeseries plots if requested
    """
    # TODO: Implement serial parameter sweep workflow
    pass


if __name__ == "__main__":
    main()
