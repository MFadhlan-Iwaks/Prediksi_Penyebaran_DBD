"""Model matematika SIR."""

from typing import Tuple


def sir_derivatives(
    s: float, i: float, r: float, n: float, beta: float, gamma: float
) -> Tuple[float, float, float]:
    """Menghitung turunan dS/dt, dI/dt, dan dR/dt pada model SIR."""
    if n <= 0:
        raise ValueError("Total populasi N harus lebih besar dari 0.")

    ds_dt = -beta * s * i / n
    di_dt = beta * s * i / n - gamma * i
    dr_dt = gamma * i

    return ds_dt, di_dt, dr_dt
