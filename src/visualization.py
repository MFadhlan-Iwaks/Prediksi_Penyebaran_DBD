"""Visualisasi hasil simulasi dan tren kasus DBD."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

try:
    from .config import YEARLY_SUMMARY_PATH
except ImportError:
    from config import YEARLY_SUMMARY_PATH


def plot_sir(simulation_result: pd.DataFrame, output_path: Path) -> None:
    """Membuat grafik kurva SIR."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.plot(simulation_result["hari"], simulation_result["S"], label="Susceptible (S)")
    plt.plot(simulation_result["hari"], simulation_result["I"], label="Infected (I)")
    plt.plot(simulation_result["hari"], simulation_result["R"], label="Recovered (R)")
    plt.title("Simulasi SIR Penyebaran DBD Jawa Barat Tahun 2024")
    plt.xlabel("Hari")
    plt.ylabel("Jumlah Populasi")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def _get_case_trend_from_yearly_summary(summary_path: Path) -> pd.DataFrame:
    summary = pd.read_csv(summary_path)
    if "tahun" not in summary.columns:
        raise ValueError("File ringkasan tahunan tidak memiliki kolom 'tahun'.")

    case_column = None
    for candidate in ["jumlah_kasus", "total_kasus_tahunan", "estimasi_kasus_tahunan"]:
        if candidate in summary.columns:
            case_column = candidate
            break

    if case_column is None:
        raise ValueError("File ringkasan tahunan tidak memiliki kolom jumlah kasus.")

    trend = summary[["tahun", case_column]].copy()
    trend.columns = ["tahun", "total_kasus"]
    return trend


def _get_case_trend_from_daily_data(data: pd.DataFrame) -> pd.DataFrame:
    if "tahun" not in data.columns or "estimasi_kasus_harian" not in data.columns:
        raise ValueError("Dataset utama harus memiliki kolom 'tahun' dan 'estimasi_kasus_harian'.")

    return (
        data.groupby("tahun", as_index=False)["estimasi_kasus_harian"]
        .sum()
        .rename(columns={"estimasi_kasus_harian": "total_kasus"})
    )


def plot_case_trend(
    data: pd.DataFrame,
    output_path: Path,
    yearly_summary_path: Path = YEARLY_SUMMARY_PATH,
) -> None:
    """Membuat grafik tren total kasus DBD 2016-2024."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if yearly_summary_path.exists():
        trend = _get_case_trend_from_yearly_summary(yearly_summary_path)
    else:
        trend = _get_case_trend_from_daily_data(data)

    trend["tahun"] = pd.to_numeric(trend["tahun"], errors="coerce")
    trend["total_kasus"] = pd.to_numeric(trend["total_kasus"], errors="coerce")
    trend = trend.dropna().sort_values("tahun")

    plt.figure(figsize=(10, 6))
    plt.plot(trend["tahun"].astype(int), trend["total_kasus"], marker="o", color="#b22222")
    plt.title("Tren Total Kasus DBD Jawa Barat 2016-2024")
    plt.xlabel("Tahun")
    plt.ylabel("Total Kasus")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
