# Prediksi Penyebaran Penyakit DBD di Jawa Barat Menggunakan Model SIR dan Metode Euler

Mini project Analisis Numerik untuk mensimulasikan penyebaran penyakit Demam Berdarah Dengue (DBD) di Jawa Barat menggunakan model SIR dan Metode Euler. Simulasi utama memakai data tahun 2024 karena tahun tersebut memiliki total kasus tertinggi pada rentang 2016-2024.

## Struktur Folder

```text
dbd-sir-euler-jabar/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── outputs/
│   ├── figures/
│   └── tables/
├── src/
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

## Dataset

Dataset yang digunakan terdiri dari data kasus DBD, data penduduk, dan data kematian akibat DBD di Jawa Barat pada rentang 2016-2024. Dataset utama program berada di:

```text
data/processed/dataset_harian_estimasi_dbd_jabar_2016_2024_agregat.csv
```

Catatan: dataset harian merupakan hasil estimasi dari data tahunan 2016-2024, bukan data observasi harian aktual.

## Instalasi

```bash
pip install -r requirements.txt
```

## Cara Menjalankan Program

Dari folder utama project, jalankan:

```bash
python -m src.main
```

atau:

```bash
python src/main.py
```

## Output

Program akan menghasilkan:

- `outputs/tables/hasil_simulasi_sir_2024.csv`
- `outputs/tables/ringkasan_hasil_simulasi.csv`
- `outputs/figures/grafik_sir_2024.png`
- `outputs/figures/grafik_tren_kasus_2016_2024.png`

Output terminal menampilkan total populasi, nilai awal S0, I0, R0, parameter beta, gamma, h, t_max, puncak infeksi maksimum, hari puncak infeksi, dan hari status siaga.

## Model SIR

Model SIR membagi populasi menjadi tiga kompartemen:

- `S` atau Susceptible: populasi yang rentan terinfeksi.
- `I` atau Infected: populasi yang sedang terinfeksi.
- `R` atau Recovered: populasi yang sembuh.

Persamaan model:

```text
dS/dt = -beta S I / N
dI/dt = beta S I / N - gamma I
dR/dt = gamma I
```

## Metode Euler

Metode Euler digunakan untuk menghampiri solusi numerik model SIR secara diskrit per hari:

```text
S(r+1) = S(r) + h(-beta S(r) I(r) / N)
I(r+1) = I(r) + h(beta S(r) I(r) / N - gamma I(r))
R(r+1) = R(r) + h(gamma I(r))
```

Parameter default simulasi:

- `beta = 0.30`
- `gamma = 1/7`
- `h = 1`
- `t_max = 150`
