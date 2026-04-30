"""Fungsi untuk membaca dan memvalidasi dataset DBD."""

from pathlib import Path

import pandas as pd

try:
    from .config import (
        INCIDENCE_RATE_2024,
        MAIN_DATASET_PATH,
        REQUIRED_MAIN_COLUMNS,
        USE_EFFECTIVE_POPULATION,
        YEARLY_SUMMARY_PATH,
        YEAR_SIMULATION,
    )
except ImportError:
    from config import (
        INCIDENCE_RATE_2024,
        MAIN_DATASET_PATH,
        REQUIRED_MAIN_COLUMNS,
        USE_EFFECTIVE_POPULATION,
        YEARLY_SUMMARY_PATH,
        YEAR_SIMULATION,
    )


def validate_required_columns(data: pd.DataFrame, required_columns: list[str]) -> None:
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
            "Pastikan file CSV tersedia di folder data/processed."
        )

    data = pd.read_csv(file_path)
    validate_required_columns(data, REQUIRED_MAIN_COLUMNS)

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
        raise ValueError("Dataset memiliki nilai numerik kosong atau tidak valid pada kolom wajib.")

    return data


def load_yearly_summary(
    daily_data: pd.DataFrame,
    file_path: Path = YEARLY_SUMMARY_PATH,
) -> pd.DataFrame:
    """Membaca ringkasan tahunan jika ada, atau membuatnya dari dataset harian estimasi."""
    if file_path.exists():
        summary = pd.read_csv(file_path)
        validate_required_columns(summary, ["tahun"])
        return summary

    return (
        daily_data.groupby("tahun", as_index=False)
        .agg(
            jumlah_penduduk_N=("jumlah_penduduk_N", "first"),
            total_kasus=("estimasi_kasus_harian", "sum"),
            total_meninggal=("estimasi_meninggal_harian", "sum"),
            total_sembuh=("estimasi_sembuh_harian", "sum"),
        )
        .sort_values("tahun")
    )


def get_simulation_initial_values(
    data: pd.DataFrame, year: int = YEAR_SIMULATION
) -> tuple[float, float, float, float, float, float, float]:
    """Mengambil nilai awal simulasi dengan pendekatan populasi efektif."""
    year_data = data[data["tahun"] == year].copy()
    if year_data.empty:
        raise ValueError(f"Data tahun {year} tidak ditemukan pada dataset utama.")

    if "tanggal" in year_data.columns:
        year_data = year_data.sort_values("tanggal")

    first_row = year_data.iloc[0]
    n_asli = float(first_row["jumlah_penduduk_N"])
    incidence_rate = INCIDENCE_RATE_2024
    n_efektif = (incidence_rate / 100000) * n_asli
    n = n_efektif if USE_EFFECTIVE_POPULATION else n_asli
    i0 = float(first_row["I0_rekomendasi"])
    r0 = float(first_row["R0_rekomendasi"])
    s0 = n - i0 - r0

    if s0 < 0:
        raise ValueError(
            "Nilai awal tidak valid: S0 bernilai negatif. "
            f"N_simulasi={n:.2f}, I0={i0:.2f}, R0={r0:.2f}. "
            "Periksa incidence rate atau nilai awal I0/R0."
        )

    return n_asli, incidence_rate, n_efektif, n, s0, i0, r0
