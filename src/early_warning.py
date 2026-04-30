"""Perhitungan parameter sistem peringatan dini."""

from typing import Tuple

import pandas as pd


def calculate_early_warning(simulation_result: pd.DataFrame) -> Tuple[float, int, int]:
    """Mencari puncak infeksi, hari puncak, dan hari siaga."""
    if "I" not in simulation_result.columns or "hari" not in simulation_result.columns:
        raise ValueError("Data simulasi harus memiliki kolom 'hari' dan 'I'.")

    peak_index = simulation_result["I"].idxmax()
    max_infection = float(simulation_result.loc[peak_index, "I"])
    peak_day = int(simulation_result.loc[peak_index, "hari"])
    warning_day = max(peak_day - 14, 0)

    return max_infection, peak_day, warning_day
