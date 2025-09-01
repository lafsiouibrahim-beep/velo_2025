import argparse
from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt


def parse_args():
    """Parse command line arguments for collecting distributed results.
    
    Returns:
        Parsed arguments containing:
        - in_dir: Input directory containing subdirectories with individual run results
        - out_dir: Output directory for aggregated results
        - plot: Boolean flag to generate plots after collection
    
    Note:
        Use argparse.ArgumentParser to define all required and optional arguments
    """
    # TODO: Implement argument parsing
    pass


def main():
    """Main function to collect and aggregate results from distributed simulations.
    
    This function should:
    1. Parse command line arguments
    2. Scan input directory for numbered subdirectories (one per simulation run)
    3. Read individual results from each subdirectory
    4. Aggregate metrics and timeseries data
    5. Save aggregated results to CSV files
    6. Optionally generate plots
    
    Expected input structure:
    - {in_dir}/0/metrics.csv, timeseries.csv, metadata.json
    - {in_dir}/1/metrics.csv, timeseries.csv, metadata.json
    - ...
    
    Output files:
    - metrics.csv: Aggregated metrics for all runs with run_id column
    - timeseries.csv: Tidy format timeseries data for all runs
    - Optional plots: PNG files for timeseries and metrics visualization
    
    Note:
        - Extract run_id from subdirectory name (should be integer)
        - Merge metadata parameters into metrics with 'param_' prefix
        - Convert timeseries to tidy format (melt operation)
        - Handle missing files gracefully
        - Sort subdirectories numerically for consistent processing
    """
    # TODO: Implement results collection and aggregation workflow
    pass


if __name__ == "__main__":
    main()
