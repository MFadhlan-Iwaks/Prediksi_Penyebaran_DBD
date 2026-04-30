"""Konfigurasi utama project simulasi SIR DBD Jawa Barat."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
MAIN_DATASET_PATH = DATA_PROCESSED_DIR / "dataset_harian_estimasi_dbd_jabar_2016_2024_agregat.csv"
YEARLY_SUMMARY_PATH = DATA_PROCESSED_DIR / "ringkasan_tahunan_dbd_jabar_2016_2024.csv"

OUTPUT_FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"

SIR_OUTPUT_PATH = OUTPUT_TABLES_DIR / "hasil_simulasi_sir_2024.csv"
SIMULATION_SUMMARY_PATH = OUTPUT_TABLES_DIR / "ringkasan_hasil_simulasi.csv"
SIR_FIGURE_PATH = OUTPUT_FIGURES_DIR / "grafik_sir_2024.png"
CASE_TREND_FIGURE_PATH = OUTPUT_FIGURES_DIR / "grafik_tren_kasus_2016_2024.png"

SIMULATION_YEAR = 2024
BETA = 0.30
GAMMA = 1 / 7
H = 1
T_MAX = 150

REQUIRED_MAIN_COLUMNS = [
    "tahun",
    "jumlah_penduduk_N",
    "I0_rekomendasi",
    "R0_rekomendasi",
    "S0_rekomendasi",
    "estimasi_kasus_harian",
    "estimasi_meninggal_harian",
    "estimasi_sembuh_harian",
]
