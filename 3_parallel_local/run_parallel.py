import argparse
from pathlib import Path
import multiprocessing as mp
import pandas as pd
import matplotlib.pyplot as plt

from model import State, run_simulation


def parse_args():
    """Parse command line arguments for parallel parameter sweep.

    Returns:
        Parsed arguments containing:
        - params: Path to CSV file with parameter combinations
        - out_dir: Output directory for results
        - workers: Number of worker processes ('auto' for automatic detection)
        - plot: Boolean flag to generate plots after run

    Note:
        Use argparse.ArgumentParser to define all required and optional arguments
    """
    
    parser = argparse.ArgumentParser(description="Parallel bike-sharing simulation sweep using multiprocessing.")

    parser.add_argument(
        "--csv-file",
        type=str,
        required=True,
        help="Path to CSV file containing simulation parameters"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="results",
        help="Directory to save output results"
    )
    parser.add_argument(
        "--workers",
        type=str,
        default="auto",
        help="Number of worker processes ('auto' for automatic detection)"
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Generate plots after simulations"
    )

    return parser.parse_args()
    
def main():
    """Main function to run parallel parameter sweep using multiprocessing.

    This function should:
    1. Parse command line arguments
    2. Read parameter combinations from CSV file
    3. Set up parallel processing with appropriate number of workers
    4. Submit simulation jobs to worker processes
    5. Collect results as they complete
    6. Aggregate and save results
    7. Optionally generate plots

    Expected parameter CSV columns:
    - steps: Number of simulation steps
    - p1: Probability Mailly->Moulin
    - p2: Probability Moulin->Mailly
    - init_mailly: Initial bikes at Mailly
    - init_moulin: Initial bikes at Moulin
    - seed: Random seed

    Output files:
    - metrics.csv: Aggregated metrics for all runs
    - Optional plots: PNG files for timeseries and metrics visualization

    Note:
        - Use multiprocessing for parallel processing
    """
    # TODO: Implement parallel parameter swep workflow

    
    args = parse_args()

    #créer le répertoire de sortie
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    #  lire le fichier CSV avec les paramètres
    simulation_table = pd.read_csv(args.csv_file)
    simulation_table = simulation_table.reset_index().rename(columns={"index": "simulation_id"})
    simulation_list = simulation_table.to_dict(orient="records")

    #  déterminer le nombres de workers
    if args.workers == "auto":
        num_workers = mp.cpu_count()
    else:
        num_workers = int(args.workers)

    print(f"Running {len(simulation_list)} simulations using {num_workers} workers")

# exécuter les simulation en paralèle et collecter les résultatt
    with mp.Pool(num_workers) as pool:
        sim_results = pool.map(d
            lambda sim_params: run_simulation(
                initial_mailly=int(sim_params["init_mailly"]),
                initial_moulin=int(sim_params["init_moulin"]),
                steps=int(sim_params["steps"]),
                p1=float(sim_params["p1"]),
                p2=float(sim_params["p2"]),
                seed=int(sim_params["seed"])
            ),
            simulation_list
        )

    # ajouter les information de paramètres à chaque résultat
    for res, sim_params in zip(sim_results, simulation_list):
        res["simulation_id"] = sim_params["simulation_id"]
        res.update(sim_params)

#Sauvegarder les résultat agrégeés dans un cvs
    results_df = pd.DataFrame(sim_results)
    metrics_csv_path = out_dir / "metrics.csv"
    results_df.to_csv(metrics_csv_path, index=False)
    print(f"Saved aggregated metrics to {metrics_csv_path}")

    # Générer éventuelement des graphihque
    if args.plot:
        for _, row in results_df.iterrows():
            plt.figure(figsize=(8, 4))
            plt.plot(row["mailly"], label="Mailly")
            plt.plot(row["moulin"], label="Moulin")
            plt.title(f"Simulation {row['simulation_id']}")
            plt.xlabel("Time step")
            plt.ylabel("Number of bikes")
            plt.legend()
            plt.tight_layout()
            plot_path = out_dir / f"simulation_{row['simulation_id']}.png"
            plt.savefig(plot_path)
            plt.close()


if __name__ == "__main__":
    main()
