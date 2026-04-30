"""Fungsi untuk membaca dan memvalidasi dataset DBD."""

from pathlib import Path
from typing import Tuple

import pandas as pd

try:
    from .config import MAIN_DATASET_PATH, REQUIRED_MAIN_COLUMNS, SIMULATION_YEAR
except ImportError:
    from config import MAIN_DATASET_PATH, REQUIRED_MAIN_COLUMNS, SIMULATION_YEAR


def validate_columns(data: pd.DataFrame, required_columns: list[str]) -> None:
    """Memastikan semua kolom wajib tersedia di dataset."""
    missing_columns = [column for column in required_columns if column not in data.columns]
    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(f"Kolom wajib tidak ditemukan: {missing_text}")


def load_processed_dataset(file_path: Path = MAIN_DATASET_PATH) -> pd.DataFrame:
    """Membaca dataset utama dari folder data/processed."""
    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset utama tidak ditemukan: {file_path}. "
            "Pastikan file CSV sudah tersedia di folder data/processed."
        )

    data = pd.read_csv(file_path)
    validate_columns(data, REQUIRED_MAIN_COLUMNS)

    numeric_columns = [
        "tahun",
        "jumlah_penduduk_N",
        "I0_rekomendasi",
        "R0_rekomendasi",
        "S0_rekomendasi",
        "estimasi_kasus_harian",
        "estimasi_meninggal_harian",
        "estimasi_sembuh_harian",
    ]
    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    if data[numeric_columns].isna().any().any():
        raise ValueError("Dataset memiliki nilai numerik kosong/tidak valid pada kolom wajib.")

    return data


def get_simulation_initial_values(
    data: pd.DataFrame, year: int = SIMULATION_YEAR
) -> Tuple[float, float, float, float]:
    """Mengambil N, S0, I0, dan R0 untuk tahun simulasi."""
    year_data = data[data["tahun"] == year].copy()
    if year_data.empty:
        raise ValueError(f"Data tahun {year} tidak ditemukan pada dataset utama.")

    if "tanggal" in year_data.columns:
        year_data = year_data.sort_values("tanggal")

    first_row = year_data.iloc[0]
    n = float(first_row["jumlah_penduduk_N"])
    s0 = float(first_row["S0_rekomendasi"])
    i0 = float(first_row["I0_rekomendasi"])
    r0 = float(first_row["R0_rekomendasi"])

    return n, s0, i0, r0
