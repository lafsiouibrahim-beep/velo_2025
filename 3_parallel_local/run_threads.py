import argparse
from pathlib import Path
import threading
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
    # TODO: Implement argument parsing
    
    parser = argparse.ArgumentParser(
        description="Parallel bike-sharing simulation sweep using threading."
    )

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
        help="Number of worker threads ('auto' for automatic detection)"
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Generate plots after simulations"
    )

    return parser.parse_args()


def main():
    """Main function to run parallel parameter sweep using threading.

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
        - Use the threading module for parallel processing
    """
    args = parse_args()

    # Créer le répertoire de sortie
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # lire le fichier Csv avec les paramètres
    simulation_table = pd.read_csv(args.csv_file)
    simulation_table = simulation_table.reset_index().rename(
        columns={"index": "simulation_id"}
    )
    simulation_list = simulation_table.to_dict(orient="records")

    # Déterminer le nombre de workers
    if args.workers == "auto":
        num_workers = len(simulation_list)
    else:
        num_workers = int(args.workers)

    print(f"Running {len(simulation_list)} simulations using {num_workers} threads")

    # Structures partagées
    simulation_results = []
    results_lock = threading.Lock()
    index_lock = threading.Lock()
    current_index = {"value": 0}
    
# fonction exécutée par chaque thread
    def worker():
        while True:
            with index_lock:
                #if current 
                if current_index["value"] >= len(simulation_list):
                    return
                sim_params = simulation_list[current_index["value"]]
                current_index["value"] += 1

            result = run_simulation(
                initial_mailly=int(sim_params["init_mailly"]),
                initial_moulin=int(sim_params["init_moulin"]),
                steps=int(sim_params["steps"]),
                p1=float(sim_params["p1"]),
                p2=float(sim_params["p2"]),
                seed=int(sim_params["seed"])
            )

            result["simulation_id"] = sim_params["simulation_id"]
            result.update(sim_params)

            with results_lock:
                simulation_results.append(result)

# Lancer les threads et collecter les résultats
    threads = []
    for _ in range(num_workers):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    #sauvegarder les résultat agrégés
    results_df = pd.DataFrame(simulation_results)
    metrics_csv_path = out_dir / "metrics.csv"
    results_df.to_csv(metrics_csv_path, index=False)
    print(f"Saved aggregated metrics to {metrics_csv_path}")

    # Générer éventuellement des graphiques
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
