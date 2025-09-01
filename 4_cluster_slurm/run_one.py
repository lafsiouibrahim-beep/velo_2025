import argparse
import json
from pathlib import Path
import pandas as pd

from model import State, run_simulation


def parse_args():
    """Parse command line arguments for running one simulation from parameter file.
    
    Returns:
        Parsed arguments containing:
        - params: Path to CSV file with parameter combinations (default: params.csv)
        - row_index: Index of the row to execute from the parameters file
        - out_dir: Output directory for this simulation's results
        - base_seed: Base seed to use if row doesn't have seed column (default: 0)
    
    Note:
        Use argparse.ArgumentParser to define all required and optional arguments
    """
    # TODO: Implement argument parsing
    pass


def main():
    """Main function to run a single simulation specified by row index.
    
    This function should:
    1. Parse command line arguments
    2. Read the parameters CSV file
    3. Extract the specified row by index
    4. Handle seed generation (use row seed or base_seed + row_index)
    5. Run the simulation with extracted parameters
    6. Save results to individual output directory
    7. Save metadata about the run
    
    Expected parameter CSV columns:
    - init_mailly: Initial bikes at Mailly
    - init_moulin: Initial bikes at Moulin
    - steps: Number of simulation steps
    - p1: Probability Mailly->Moulin
    - p2: Probability Moulin->Mailly
    - seed: Random seed (optional)
    
    Output structure:
    - {out_dir}/{row_index}/timeseries.csv: Simulation timeseries
    - {out_dir}/{row_index}/metrics.csv: Simulation metrics
    - {out_dir}/{row_index}/metadata.json: Run parameters and metadata
    
    Note:
        - Create subdirectory named after row_index
        - Handle missing seed column gracefully
        - Save metadata as JSON with all parameters including final seed used
    """
    # TODO: Implement single simulation workflow for cluster execution
    pass


if __name__ == "__main__":
    main()
