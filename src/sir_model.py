"""Model matematika SIR."""


def sir_derivatives(
    S: float, I: float, R: float, beta: float, gamma: float, N: float
) -> tuple[float, float, float]:
    """Menghitung dS/dt, dI/dt, dan dR/dt pada model SIR."""
    if N <= 0:
        raise ValueError("Total populasi N harus lebih besar dari 0.")

    dS_dt = -beta * S * I / N
    dI_dt = beta * S * I / N - gamma * I
    dR_dt = gamma * I

    return dS_dt, dI_dt, dR_dt
