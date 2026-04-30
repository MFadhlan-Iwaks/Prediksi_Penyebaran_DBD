"""Visualisasi hasil simulasi dan tren kasus DBD."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_sir(simulation_df: pd.DataFrame, output_path: Path) -> None:
    """Membuat grafik kurva SIR."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.plot(simulation_df["hari"], simulation_df["S"], label="Susceptible (S)")
    plt.plot(simulation_df["hari"], simulation_df["I"], label="Infected (I)")
    plt.plot(simulation_df["hari"], simulation_df["R"], label="Recovered (R)")
    plt.title("Simulasi SIR Penyebaran DBD Jawa Barat Tahun 2024")
    plt.xlabel("Hari")
    plt.ylabel("Jumlah Populasi")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def _case_column(summary_df: pd.DataFrame) -> str:
    for candidate in ["jumlah_kasus", "total_kasus_tahunan", "total_kasus"]:
        if candidate in summary_df.columns:
            return candidate
    raise ValueError("Ringkasan tahunan tidak memiliki kolom jumlah kasus.")


def plot_case_trend(summary_df: pd.DataFrame, output_path: Path) -> None:
    """Membuat grafik tren total kasus DBD 2016-2024."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    case_column = _case_column(summary_df)
    trend = summary_df[["tahun", case_column]].copy()
    trend.columns = ["tahun", "total_kasus"]
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


def plot_stability_comparison(simulations: dict[str, pd.DataFrame], output_path: Path) -> None:
    """Membandingkan kurva Infected untuk skenario step size h."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    for label, simulation_df in simulations.items():
        plt.plot(simulation_df["hari"], simulation_df["I"], label=label)
    plt.title("Uji Stabilitas Metode Euler Berdasarkan Step Size h")
    plt.xlabel("Hari")
    plt.ylabel("Jumlah Infected")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_beta_sensitivity(simulations: dict[str, pd.DataFrame], output_path: Path) -> None:
    """Membandingkan kurva Infected untuk beberapa nilai beta."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    for label, simulation_df in simulations.items():
        plt.plot(simulation_df["hari"], simulation_df["I"], label=label)
    plt.title("Uji Sensitivitas Beta terhadap Kurva Infected")
    plt.xlabel("Hari")
    plt.ylabel("Jumlah Infected")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_gamma_sensitivity(simulations: dict[str, pd.DataFrame], output_path: Path) -> None:
    """Membandingkan kurva Infected untuk beberapa nilai gamma."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    for label, simulation_df in simulations.items():
        plt.plot(simulation_df["hari"], simulation_df["I"], label=label)
    plt.title("Uji Sensitivitas Gamma terhadap Kurva Infected")
    plt.xlabel("Hari")
    plt.ylabel("Jumlah Infected")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
