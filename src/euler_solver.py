"""Penyelesaian model SIR menggunakan Metode Euler."""

import pandas as pd

try:
    from .sir_model import sir_derivatives
except ImportError:
    from sir_model import sir_derivatives


def euler_sir(
    n: float,
    s0: float,
    i0: float,
    r0: float,
    beta: float,
    gamma: float,
    h: float,
    t_max: int,
) -> pd.DataFrame:
    """Menjalankan simulasi SIR dengan Metode Euler."""
    if h <= 0:
        raise ValueError("Nilai h harus lebih besar dari 0.")
    if t_max < 0:
        raise ValueError("Nilai t_max tidak boleh negatif.")

    results = [{"hari": 0, "S": s0, "I": i0, "R": r0}]
    s, i, r = s0, i0, r0

    for day in range(1, t_max + 1):
        ds_dt, di_dt, dr_dt = sir_derivatives(s, i, r, n, beta, gamma)

        s = s + h * ds_dt
        i = i + h * di_dt
        r = r + h * dr_dt

        # Kompartemen tidak boleh negatif secara makna epidemiologis.
        s = max(s, 0)
        i = max(i, 0)
        r = max(r, 0)

        results.append({"hari": day, "S": s, "I": i, "R": r})

    return pd.DataFrame(results)
