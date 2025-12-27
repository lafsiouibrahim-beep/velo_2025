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
    parser = argparse.ArgumentParser(description="Run serial bike-sharing simulations")

    parser.add_argument(
        "--params",
        type=Path,
        required=True,
        help="CSV file containing simulation parameters",
    )

    parser.add_argument(
        "--out-dir",
        type=Path,
        required=True,
        help="Directory to save results",
    )

    parser.add_argument(
        "--plot",
        action="store_true",
        help="Generate plots after simulation",
    )

    parser.add_argument(
        "--smooth-window",
        type=int,
        default=1,
        help="Smoothing window size for plots (default: 1)",
    )

    return parser.parse_args()


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
    - Optional plots: PNG files for timeseries and metrics visualization

    Note:
        - Process each row in the parameters file as a separate simulation run
        - Add run_id to track individual simulations
        - **OPTIONAL**: plot timeseries for both stations
        - **OPTIONAL**: Handle smoothing for timeseries plots if requested
    """
    # TODO: Implement serial parameter sweep workflow
    args = parse_args()

    # créer le répertoire de sortie s'il n'existe pas
    args.out_dir.mkdir(parents=True, exist_ok=True)

    # llire les combinaisons de paramètres
    params_df = pd.read_csv(args.params)

    all_results = []

    # exécutez les simulations une par une.
    for run_id, row in params_df.iterrows():
        result = run_simulation(
            initial_mailly=int(row["init_mailly"]),
            initial_moulin=int(row["init_moulin"]),
            steps=int(row["steps"]),
            p1=float(row["p1"]),
            p2=float(row["p2"]),
            seed=int(row["seed"]),
        )

        df = pd.DataFrame(result)
        df["run_id"] = run_id

        all_results.append(df)

        # ploting
        if args.plot:
            plt.figure(figsize=(8, 4))

            plt.plot(df["mailly"], label="Mailly")
            plt.plot(df["moulin"], label="Moulin")
            plt.plot(df["final_imbalance"], label="Balance")

            plt.title(f"Simulation run {run_id}")
            plt.xlabel("Step")
            plt.ylabel("Number of bikes")
            plt.legend()
            plt.tight_layout()

            plot_path = args.out_dir / f"metrics_3plot_run_{run_id}.png"
            plt.savefig(plot_path)
            plt.close()

    final_df = pd.concat(all_results, ignore_index=True)

    # Enregistrer les mesures
    output_csv = args.out_dir / "metrics.csv"
    final_df.to_csv(output_csv, index=False)


if __name__ == "__main__":
    main()
