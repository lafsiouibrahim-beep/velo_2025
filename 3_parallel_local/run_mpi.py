import argparse
import mpi4py
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
    parser = argparse.ArgumentParser(description="Parallel bike-sharing simulation sweep using MPI.")

    parser.add_argument(
        "--params",
        type=str,
        required=True,
        help="Path to CSV file with parameter combinations"
    )
    parser.add_argument(
        "--out-dir",
        type=str,
        default="results",
        help="Output directory for results"
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
        help="Generate plots after run"
    )

    return parser.parse_args()


def main():
    """Main function to run parallel parameter sweep using MPI.

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
        - Use the mpi4py module for parallel processing
    """

    
    args = parse_args()

    #Créer le répertoire de sortie s'il n'existe pas
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # MPI setup
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # if rank 0  we read the CSV and distribute work
    if rank == 0:
        df_params = pd.read_csv(args.params)
        param_list = df_params.to_dict(orient="records")
    else:
        param_list = None

    param_list = comm.bcast(param_list, root=0)

    # on distibue le travail seolon rank
    results = []
    for i, params in enumerate(param_list):
        if i % size != rank:
            continue  

        # Run simulation
        sim_result = run_simulation(
            initial_mailly=int(params["init_mailly"]),
            initial_moulin=int(params["init_moulin"]),
            steps=int(params["steps"]),
            p1=float(params["p1"]),
            p2=float(params["p2"]),
            seed=int(params["seed"])
        )

        sim_result["params_index"] = i
        sim_result.update(params)
        results.append(sim_result)

    # Rassembler tous les résultats au rang 0
    all_results = comm.gather(results, root=0)

    if rank == 0:
        flat_results = [item for sublist in all_results for item in sublist]

        # Convert to DataFrame
        metrics_df = pd.DataFrame(flat_results)
        metrics_csv_path = out_dir / "metrics.csv"
        metrics_df.to_csv(metrics_csv_path, index=False)
        print(f"Saved aggregated metrics to {metrics_csv_path}")

        # plotting
        if args.plot:
            for i, row in metrics_df.iterrows():
                plt.figure(figsize=(8, 4))
                plt.plot(row["mailly"], label="Mailly")
                plt.plot(row["moulin"], label="Moulin")
                plt.title(f"Simulation {i}")
                plt.xlabel("Time step")
                plt.ylabel("Number of bikes")
                plt.legend()
                plt.tight_layout()
                plot_path = out_dir / f"simulation_{i}.png"
                plt.savefig(plot_path)
                plt.close()


if __name__ == "__main__":
    main()
