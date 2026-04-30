"""Perhitungan parameter sistem peringatan dini."""

import pandas as pd


def calculate_early_warning(
    simulation_df: pd.DataFrame, warning_window: int
) -> dict[str, float]:
    """Mencari infected maksimum, hari puncak, dan hari siaga."""
    if "I" not in simulation_df.columns or "hari" not in simulation_df.columns:
        raise ValueError("Data simulasi harus memiliki kolom 'hari' dan 'I'.")

    peak_index = simulation_df["I"].idxmax()
    infected_maksimum = float(simulation_df.loc[peak_index, "I"])
    hari_puncak = float(simulation_df.loc[peak_index, "hari"])
    hari_siaga = max(hari_puncak - warning_window, 0)

    return {
        "infected_maksimum": infected_maksimum,
        "hari_puncak": hari_puncak,
        "hari_siaga": hari_siaga,
    }
