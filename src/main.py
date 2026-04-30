"""Program utama simulasi SIR DBD Jawa Barat."""

import pandas as pd

try:
    from .config import (
        BETA,
        CASE_TREND_FIGURE_PATH,
        GAMMA,
        H,
        OUTPUT_FIGURES_DIR,
        OUTPUT_TABLES_DIR,
        SIMULATION_SUMMARY_PATH,
        SIMULATION_YEAR,
        SIR_FIGURE_PATH,
        SIR_OUTPUT_PATH,
        T_MAX,
    )
    from .data_loader import get_simulation_initial_values, load_processed_dataset
    from .early_warning import calculate_early_warning
    from .euler_solver import euler_sir
    from .visualization import plot_case_trend, plot_sir
except ImportError:
    from config import (
        BETA,
        CASE_TREND_FIGURE_PATH,
        GAMMA,
        H,
        OUTPUT_FIGURES_DIR,
        OUTPUT_TABLES_DIR,
        SIMULATION_SUMMARY_PATH,
        SIMULATION_YEAR,
        SIR_FIGURE_PATH,
        SIR_OUTPUT_PATH,
        T_MAX,
    )
    from data_loader import get_simulation_initial_values, load_processed_dataset
    from early_warning import calculate_early_warning
    from euler_solver import euler_sir
    from visualization import plot_case_trend, plot_sir


def main() -> None:
    """Menghubungkan pembacaan data, simulasi, peringatan dini, dan output."""
    try:
        OUTPUT_FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_TABLES_DIR.mkdir(parents=True, exist_ok=True)

        data = load_processed_dataset()
        n, s0, i0, r0 = get_simulation_initial_values(data, SIMULATION_YEAR)

        simulation_result = euler_sir(
            n=n,
            s0=s0,
            i0=i0,
            r0=r0,
            beta=BETA,
            gamma=GAMMA,
            h=H,
            t_max=T_MAX,
        )

        max_infection, peak_day, warning_day = calculate_early_warning(simulation_result)

        simulation_result.to_csv(SIR_OUTPUT_PATH, index=False)

        summary = pd.DataFrame(
            [
                {"keterangan": "tahun_simulasi", "nilai": SIMULATION_YEAR},
                {"keterangan": "total_populasi_N", "nilai": n},
                {"keterangan": "S0", "nilai": s0},
                {"keterangan": "I0", "nilai": i0},
                {"keterangan": "R0", "nilai": r0},
                {"keterangan": "beta", "nilai": BETA},
                {"keterangan": "gamma", "nilai": GAMMA},
                {"keterangan": "h", "nilai": H},
                {"keterangan": "t_max", "nilai": T_MAX},
                {"keterangan": "puncak_infeksi_maksimum", "nilai": max_infection},
                {"keterangan": "hari_puncak_infeksi", "nilai": peak_day},
                {"keterangan": "hari_status_siaga", "nilai": warning_day},
            ]
        )
        summary.to_csv(SIMULATION_SUMMARY_PATH, index=False)

        plot_sir(simulation_result, SIR_FIGURE_PATH)
        plot_case_trend(data, CASE_TREND_FIGURE_PATH)

        print("=== Simulasi SIR DBD Jawa Barat ===")
        print(f"Tahun simulasi          : {SIMULATION_YEAR}")
        print(f"Total populasi (N)      : {n:,.0f}")
        print(f"Nilai awal S0           : {s0:,.2f}")
        print(f"Nilai awal I0           : {i0:,.2f}")
        print(f"Nilai awal R0           : {r0:,.2f}")
        print(f"Beta                    : {BETA}")
        print(f"Gamma                   : {GAMMA:.6f}")
        print(f"h                       : {H}")
        print(f"t_max                   : {T_MAX} hari")
        print(f"Puncak infeksi maksimum : {max_infection:,.2f}")
        print(f"Hari puncak infeksi     : {peak_day}")
        print(f"Hari status siaga       : {warning_day}")
        print()
        print(f"Hasil simulasi disimpan : {SIR_OUTPUT_PATH}")
        print(f"Ringkasan disimpan      : {SIMULATION_SUMMARY_PATH}")
        print(f"Grafik SIR disimpan     : {SIR_FIGURE_PATH}")
        print(f"Grafik tren disimpan    : {CASE_TREND_FIGURE_PATH}")

    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
    except Exception as error:
        print(f"Terjadi error yang tidak terduga: {error}")


if __name__ == "__main__":
    main()
