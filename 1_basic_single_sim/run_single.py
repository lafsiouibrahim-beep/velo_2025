import argparse
import json
from pathlib import Path

import matplotlib # Importez le module matplotlib complet
matplotlib.use('Agg') # ✅ Correct ! Appelé sur le module de base.
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

    
    parser = argparse.ArgumentParser(
        description="Run a bike-sharing simulation between Mailly and Moulin."
    )

    parser.add_argument("--steps", type=int, required=True,
                        help="Number of simulation steps")

    parser.add_argument("--p1", type=float, required=True,
                        help="Probability of movement from Mailly to Moulin")

    parser.add_argument("--p2", type=float, required=True,
                        help="Probability of movement from Moulin to Mailly")

    parser.add_argument("--init-mailly", type=int, required=True,
                        help="Initial number of bikes at Mailly station")

    parser.add_argument("--init-moulin", type=int, required=True,
                        help="Initial number of bikes at Moulin station")

    parser.add_argument("--seed", type=int, default=0,
                        help="Random seed (default: 0)")

    parser.add_argument("--out-csv", type=str, required=True,
                        help="Output CSV file for time series")

    parser.add_argument("--plot", action="store_true",
                        help="Generate and save plot")

    return parser.parse_args()

    


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

    
    #  Lire les arguments
    args = parse_args()

    # Lancer la simulation
    # cche -- Il faut importer pandas dans ce fichier parce que vous utilisez des dataframe ici.
    # Il ne faut pas s'appuyer sur l'importation dans model.
    df, metrics = run_simulation(
        initial_mailly=args.init_mailly,
        initial_moulin=args.init_moulin,
        steps=args.steps,
        p1=args.p1,
        p2=args.p2,
        seed=args.seed,
    )

    
    out_csv_path = Path(args.out_csv)
    out_csv_path.parent.mkdir(parents=True, exist_ok=True)

    # Sauvegarder les séries temporelles
    df.to_csv(out_csv_path, index=False)

    # Sauvegarder les métriques
    metrics_path = out_csv_path.with_suffix(".metrics.tsv")
    with open(metrics_path, "w") as f:
        for key, value in metrics.items():
            f.write(f"{key}\t{value}\n")

    # Générer le graphique si demandé
    if args.plot:
        plt.figure()
        plt.plot(df["time"], df["mailly"], label="Mailly")
        plt.plot(df["time"], df["moulin"], label="Moulin")
        plt.xlabel("Time")
        plt.ylabel("Number of bikes")
        plt.legend()
        plt.grid(True)

        plot_path = out_csv_path.with_suffix(".png")
        plt.savefig(plot_path)
        plt.close()


if __name__ == "__main__":
    main()
