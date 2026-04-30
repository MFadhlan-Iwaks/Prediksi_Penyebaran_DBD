"""Program utama simulasi SIR DBD Jawa Barat."""

from time import perf_counter

import pandas as pd

try:
    from .config import (
        BETA,
        BETA_SCENARIOS,
        BETA_SENSITIVITY_FIGURE_PATH,
        BETA_SENSITIVITY_OUTPUT_PATH,
        CASE_TREND_FIGURE_PATH,
        GAMMA,
        GAMMA_SCENARIOS,
        GAMMA_SENSITIVITY_FIGURE_PATH,
        GAMMA_SENSITIVITY_OUTPUT_PATH,
        H,
        HISTORICAL_SUMMARY_OUTPUT_PATH,
        OUTPUT_FIGURES_DIR,
        OUTPUT_TABLES_DIR,
        PARAMETER_OUTPUT_PATH,
        SIMULATION_SUMMARY_PATH,
        SIR_FIGURE_PATH,
        SIR_OUTPUT_PATH,
        STABILITY_FIGURE_PATH,
        STABILITY_H_VALUES,
        STABILITY_OUTPUT_PATH,
        T_MAX,
        WARNING_WINDOW,
        YEAR_SIMULATION,
    )
    from .data_loader import get_simulation_initial_values, load_processed_dataset, load_yearly_summary
    from .early_warning import calculate_early_warning
    from .euler_solver import euler_sir
    from .visualization import (
        plot_beta_sensitivity,
        plot_case_trend,
        plot_gamma_sensitivity,
        plot_sir,
        plot_stability_comparison,
    )
except ImportError:
    from config import (
        BETA,
        BETA_SCENARIOS,
        BETA_SENSITIVITY_FIGURE_PATH,
        BETA_SENSITIVITY_OUTPUT_PATH,
        CASE_TREND_FIGURE_PATH,
        GAMMA,
        GAMMA_SCENARIOS,
        GAMMA_SENSITIVITY_FIGURE_PATH,
        GAMMA_SENSITIVITY_OUTPUT_PATH,
        H,
        HISTORICAL_SUMMARY_OUTPUT_PATH,
        OUTPUT_FIGURES_DIR,
        OUTPUT_TABLES_DIR,
        PARAMETER_OUTPUT_PATH,
        SIMULATION_SUMMARY_PATH,
        SIR_FIGURE_PATH,
        SIR_OUTPUT_PATH,
        STABILITY_FIGURE_PATH,
        STABILITY_H_VALUES,
        STABILITY_OUTPUT_PATH,
        T_MAX,
        WARNING_WINDOW,
        YEAR_SIMULATION,
    )
    from data_loader import get_simulation_initial_values, load_processed_dataset, load_yearly_summary
    from early_warning import calculate_early_warning
    from euler_solver import euler_sir
    from visualization import (
        plot_beta_sensitivity,
        plot_case_trend,
        plot_gamma_sensitivity,
        plot_sir,
        plot_stability_comparison,
    )


def run_simulation(
    N: float,
    S0: float,
    I0: float,
    R0: float,
    beta: float,
    gamma: float,
    h: float,
    t_max: int,
) -> tuple[pd.DataFrame, float]:
    """Menjalankan simulasi dan mengembalikan DataFrame serta waktu komputasi."""
    start_time = perf_counter()
    simulation_df = euler_sir(N, S0, I0, R0, beta, gamma, h, t_max)
    elapsed_time = perf_counter() - start_time
    return simulation_df, elapsed_time


def save_parameter_table(
    N_asli: float,
    incidence_rate: float,
    N_efektif: float,
    N: float,
    S0: float,
    I0: float,
    R0: float,
) -> None:
    """Menyimpan parameter simulasi utama tahun 2024."""
    parameter_df = pd.DataFrame(
        [
            {
                "tahun_simulasi": YEAR_SIMULATION,
                "jumlah_penduduk_asli": N_asli,
                "incidence_rate_2024": incidence_rate,
                "N_efektif": N_efektif,
                "N_simulasi": N,
                "S0": S0,
                "I0": I0,
                "R0": R0,
                "beta": BETA,
                "gamma": GAMMA,
                "h": H,
                "t_max": T_MAX,
                "warning_window": WARNING_WINDOW,
                "sumber_I0": "I0_rekomendasi dari dataset agregat tahun 2024",
                "catatan_dataset": (
                    "Dataset harian merupakan estimasi dari data tahunan 2016-2024. "
                    "Populasi simulasi menggunakan populasi efektif berbasis incidence rate, "
                    "bukan seluruh penduduk Jawa Barat."
                ),
            }
        ]
    )
    parameter_df.to_csv(PARAMETER_OUTPUT_PATH, index=False)


def save_main_summary(
    N_asli: float,
    incidence_rate: float,
    N_efektif: float,
    N: float,
    S0: float,
    I0: float,
    R0: float,
    warning_result: dict[str, float],
    elapsed_time: float,
) -> None:
    """Menyimpan ringkasan hasil simulasi utama."""
    summary_df = pd.DataFrame(
        [
            {
                "tahun_simulasi": YEAR_SIMULATION,
                "jumlah_penduduk_asli": N_asli,
                "incidence_rate_2024": incidence_rate,
                "N_efektif": N_efektif,
                "N_simulasi": N,
                "S0": S0,
                "I0": I0,
                "R0": R0,
                "beta": BETA,
                "gamma": GAMMA,
                "h": H,
                "t_max": T_MAX,
                "infected_maksimum": warning_result["infected_maksimum"],
                "hari_puncak": warning_result["hari_puncak"],
                "warning_window": WARNING_WINDOW,
                "hari_siaga": warning_result["hari_siaga"],
                "waktu_komputasi_detik": elapsed_time,
            }
        ]
    )
    summary_df.to_csv(SIMULATION_SUMMARY_PATH, index=False)


def run_stability_test(N: float, S0: float, I0: float, R0: float) -> None:
    """Menjalankan uji stabilitas step size h = 1 dan h = 0.5."""
    rows = []
    simulations = {}
    baseline_infected = None
    baseline_peak_day = None

    for h_value in STABILITY_H_VALUES:
        simulation_df, elapsed_time = run_simulation(N, S0, I0, R0, BETA, GAMMA, h_value, T_MAX)
        warning_result = calculate_early_warning(simulation_df, WARNING_WINDOW)
        simulations[f"h = {h_value}"] = simulation_df

        if h_value == 1:
            baseline_infected = warning_result["infected_maksimum"]
            baseline_peak_day = warning_result["hari_puncak"]

        rows.append(
            {
                "skenario": f"h = {h_value}",
                "h": h_value,
                "infected_maksimum": warning_result["infected_maksimum"],
                "hari_puncak": warning_result["hari_puncak"],
                "hari_siaga": warning_result["hari_siaga"],
                "waktu_komputasi_detik": elapsed_time,
            }
        )

    stability_df = pd.DataFrame(rows)
    stability_df["selisih_infected_maksimum_dari_h1"] = (
        stability_df["infected_maksimum"] - baseline_infected
    ).abs()
    stability_df["selisih_hari_puncak_dari_h1"] = (
        stability_df["hari_puncak"] - baseline_peak_day
    ).abs()

    stability_df.to_csv(STABILITY_OUTPUT_PATH, index=False)
    plot_stability_comparison(simulations, STABILITY_FIGURE_PATH)


def run_beta_sensitivity_test(N: float, S0: float, I0: float, R0: float) -> None:
    """Menjalankan uji sensitivitas beta."""
    rows = []
    simulations = {}

    for beta_value in BETA_SCENARIOS:
        simulation_df, elapsed_time = run_simulation(N, S0, I0, R0, beta_value, GAMMA, H, T_MAX)
        warning_result = calculate_early_warning(simulation_df, WARNING_WINDOW)
        simulations[f"beta = {beta_value:.2f}"] = simulation_df
        rows.append(
            {
                "beta": beta_value,
                "gamma": GAMMA,
                "h": H,
                "infected_maksimum": warning_result["infected_maksimum"],
                "hari_puncak": warning_result["hari_puncak"],
                "hari_siaga": warning_result["hari_siaga"],
                "waktu_komputasi_detik": elapsed_time,
            }
        )

    pd.DataFrame(rows).to_csv(BETA_SENSITIVITY_OUTPUT_PATH, index=False)
    plot_beta_sensitivity(simulations, BETA_SENSITIVITY_FIGURE_PATH)


def run_gamma_sensitivity_test(N: float, S0: float, I0: float, R0: float) -> None:
    """Menjalankan uji sensitivitas gamma."""
    rows = []
    simulations = {}

    for gamma_value in GAMMA_SCENARIOS:
        simulation_df, elapsed_time = run_simulation(N, S0, I0, R0, BETA, gamma_value, H, T_MAX)
        warning_result = calculate_early_warning(simulation_df, WARNING_WINDOW)
        simulations[f"gamma = {gamma_value:.3f}"] = simulation_df
        rows.append(
            {
                "beta": BETA,
                "gamma": gamma_value,
                "h": H,
                "infected_maksimum": warning_result["infected_maksimum"],
                "hari_puncak": warning_result["hari_puncak"],
                "hari_siaga": warning_result["hari_siaga"],
                "waktu_komputasi_detik": elapsed_time,
            }
        )

    pd.DataFrame(rows).to_csv(GAMMA_SENSITIVITY_OUTPUT_PATH, index=False)
    plot_gamma_sensitivity(simulations, GAMMA_SENSITIVITY_FIGURE_PATH)


def print_terminal_summary(
    N_asli: float,
    incidence_rate: float,
    N_efektif: float,
    N: float,
    S0: float,
    I0: float,
    R0: float,
    warning_result: dict[str, float],
    elapsed_time: float,
) -> None:
    """Menampilkan ringkasan simulasi utama di terminal."""
    infected_maksimum = warning_result["infected_maksimum"]
    hari_puncak = warning_result["hari_puncak"]
    hari_siaga = warning_result["hari_siaga"]

    print("=== Simulasi SIR DBD Jawa Barat ===")
    print(f"Tahun simulasi          : {YEAR_SIMULATION}")
    print(f"Penduduk asli Jawa Barat: {N_asli:,.0f}")
    print(f"Incidence Rate 2024     : {incidence_rate:.2f} per 100.000 penduduk")
    print(f"Populasi efektif        : {N_efektif:,.2f}")
    print(f"N simulasi              : {N:,.2f}")
    print(f"Nilai awal S0           : {S0:,.2f}")
    print(f"Nilai awal I0           : {I0:,.2f}")
    print(f"Nilai awal R0           : {R0:,.2f}")
    print(f"Beta                    : {BETA}")
    print(f"Gamma                   : {GAMMA:.6f}")
    print(f"h                       : {H}")
    print(f"t_max                   : {T_MAX} hari")
    print(f"Infected maksimum       : {infected_maksimum:,.2f}")
    print(f"Hari puncak             : {hari_puncak:g}")
    print(f"Hari siaga              : {hari_siaga:g}")
    print(f"Waktu komputasi         : {elapsed_time:.6f} detik")
    print()
    print(
        f"Puncak wabah DBD diprediksi mencapai {infected_maksimum:,.2f} "
        f"jiwa pada hari ke-{hari_puncak:g}."
    )
    print(f"STATUS SIAGA: Intervensi disarankan mulai hari ke-{hari_siaga:g}.")


def main() -> None:
    """Menjalankan seluruh proses untuk kebutuhan output laporan BAB V."""
    try:
        OUTPUT_FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_TABLES_DIR.mkdir(parents=True, exist_ok=True)

        data = load_processed_dataset()
        yearly_summary = load_yearly_summary(data)
        yearly_summary.to_csv(HISTORICAL_SUMMARY_OUTPUT_PATH, index=False)

        N_asli, incidence_rate, N_efektif, N, S0, I0, R0 = get_simulation_initial_values(
            data, YEAR_SIMULATION
        )
        save_parameter_table(N_asli, incidence_rate, N_efektif, N, S0, I0, R0)

        simulation_df, elapsed_time = run_simulation(N, S0, I0, R0, BETA, GAMMA, H, T_MAX)
        simulation_df.to_csv(SIR_OUTPUT_PATH, index=False)

        warning_result = calculate_early_warning(simulation_df, WARNING_WINDOW)
        save_main_summary(
            N_asli,
            incidence_rate,
            N_efektif,
            N,
            S0,
            I0,
            R0,
            warning_result,
            elapsed_time,
        )

        plot_sir(simulation_df, SIR_FIGURE_PATH)
        plot_case_trend(yearly_summary, CASE_TREND_FIGURE_PATH)

        run_stability_test(N, S0, I0, R0)
        run_beta_sensitivity_test(N, S0, I0, R0)
        run_gamma_sensitivity_test(N, S0, I0, R0)

        print_terminal_summary(
            N_asli,
            incidence_rate,
            N_efektif,
            N,
            S0,
            I0,
            R0,
            warning_result,
            elapsed_time,
        )

    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
    except Exception as error:
        print(f"Terjadi error yang tidak terduga: {error}")


if __name__ == "__main__":
    main()
