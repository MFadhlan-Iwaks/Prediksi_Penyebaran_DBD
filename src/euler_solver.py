"""Penyelesaian model SIR menggunakan Metode Euler."""

import numpy as np
import pandas as pd

try:
    from .sir_model import sir_derivatives
except ImportError:
    from sir_model import sir_derivatives


def euler_sir(
    N: float,
    S0: float,
    I0: float,
    R0: float,
    beta: float,
    gamma: float,
    h: float,
    t_max: int,
) -> pd.DataFrame:
    """Menjalankan simulasi SIR dengan Metode Euler.

    Jika h = 0.5, kolom hari akan berisi 0, 0.5, 1.0, 1.5, dan seterusnya.
    """
    if h <= 0:
        raise ValueError("Nilai h harus lebih besar dari 0.")
    if t_max < 0:
        raise ValueError("Nilai t_max tidak boleh negatif.")

    time_points = np.arange(0, t_max + h, h)
    S, I, R = S0, I0, R0
    results = [{"hari": float(time_points[0]), "S": S, "I": I, "R": R}]

    for day in time_points[1:]:
        dS_dt, dI_dt, dR_dt = sir_derivatives(S, I, R, beta, gamma, N)

        S = max(S + h * dS_dt, 0)
        I = max(I + h * dI_dt, 0)
        R = max(R + h * dR_dt, 0)

        results.append({"hari": float(day), "S": S, "I": I, "R": R})

    return pd.DataFrame(results)
