from dataclasses import dataclass
from typing import Tuple, Dict
import numpy as np
import pandas as pd


@dataclass
class State:
    """Represents the state of bikes at two stations.

    Attributes:
        mailly: Number of bikes at Mailly station
        moulin: Number of bikes at Moulin station
    """

    mailly: int
    moulin: int
    unmet_mailly: int = 0
    unmet_moulin: int = 0


def step(
    state: State,
    p1: float,
    p2: float,
    rng: np.random.Generator,
    metrics: Dict[str, int],
) -> State:
    """Simulate one time step of the bike-sharing system.

    Args:
        state: Current state of the system (bike counts at each station)
        p1: Probability of a user wanting to go from Mailly to Moulin
        p2: Probability of a user wanting to go from Moulin to Mailly
        rng: Random number generator for stochastic events
        metrics: Dictionary to track simulation metrics (unmet demand, etc.)

    Returns:
        Updated state after one simulation step

    Note:
        - If a station has no bikes available, increment the appropriate unmet demand counter
        - Update the state by moving bikes between stations based on probabilities
    """
    new_state = State(
        mailly=state.mailly,
        moulin=state.moulin,
        unmet_mailly=state.unmet_mailly,
        unmet_moulin=state.unmet_moulin,
    )

    # Mailly vers Moulin
    if rng.random() < p1:
        if new_state.mailly > 0:
            new_state.mailly -= 1
            new_state.moulin += 1
        else:
            metrics["unmet_mailly"] += 1
            new_state.unmet_mailly += 1

    # Moulin vers Mailly
    if rng.random() < p2:
        if new_state.moulin > 0:
            new_state.moulin -= 1
            new_state.mailly += 1
        else:
            metrics["unmet_moulin"] += 1
            new_state.unmet_moulin += 1

    return new_state
    # User tries to go from mailly -> moulin with prob p1
    #pass
    


def run_simulation(
    initial_mailly: int,
    initial_moulin: int,
    steps: int,
    p1: float,
    p2: float,
    seed: int,
) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """Run a complete bike-sharing simulation.

    Args:
        initial_mailly: Initial number of bikes at Mailly station
        initial_moulin: Initial number of bikes at Moulin station
        steps: Number of simulation steps to run
        p1: Probability of movement from Mailly to Moulin
        p2: Probability of movement from Moulin to Mailly
        seed: Random seed for reproducibility

    Returns:
        Tuple containing:
        - DataFrame with columns ['time', 'mailly', 'moulin'] tracking bike counts over time
        - Dictionary with metrics including:
            - mailly: Number of bikes at Mailly station
            - moulin: Number of bikes at Moulin station
            - 'unmet_mailly': Number of unmet requests at Mailly
            - 'unmet_moulin': Number of unmet requests at Moulin
            - 'final_imbalance': Final difference between station bike counts

    Note:
        - Create the state object with initial bike counts
        - Initialize metrics dictionary with appropriate counters
        - Record state at each time step for the DataFrame
        - Calculate final imbalance as mailly - moulin
    """
    #  Initialiser le générateur aléatoire
    rng = np.random.default_rng(seed)

    #  État initial du système
    state = State(
        mailly=initial_mailly,
        moulin=initial_moulin
    )

    metrics = {
        "unmet_mailly": 0,
        "unmet_moulin": 0,
    }

    #  Historique des états (pour le tableau final)
    history = []

    # Enregistrer l'état initial (temps = 0)
    history.append({
        "time": 0,
        "mailly": state.mailly,
        "moulin": state.moulin,
    })

    #  Boucle de simulation
    for t in range(1, steps + 1):
        state = step(state, p1, p2, rng, metrics)
        
        history.append({
            "time": t,
            "mailly": state.mailly,
            "moulin": state.moulin,
        })

    # Créer le DataFrame final
    df = pd.DataFrame(history)

    metrics["final_mailly"] = state.mailly
    metrics["final_moulin"] = state.moulin
    metrics["final_imbalance"] = state.mailly - state.moulin
    metrics["total_bikes"] = state.mailly + state.moulin

    return df, metrics

