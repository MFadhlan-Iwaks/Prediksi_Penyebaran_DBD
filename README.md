# Prediksi Penyebaran Penyakit DBD di Jawa Barat Menggunakan Model SIR dan Metode Euler

Mini project mata kuliah Analisis Numerik untuk memprediksi dinamika penyebaran penyakit Demam Berdarah Dengue (DBD) di Jawa Barat. Program menggunakan model SIR dan Metode Euler, lalu memakai puncak infeksi sebagai dasar sistem peringatan dini.

## Tujuan Project

- Memprediksi tren penyebaran kasus DBD di Jawa Barat.
- Mengimplementasikan Metode Euler untuk memperoleh solusi numerik model SIR.
- Menentukan status siaga berdasarkan puncak infeksi hasil simulasi.
- Menyediakan tabel dan grafik untuk kebutuhan analisis BAB V laporan.

## Struktur Folder

```text
Prediksi_Penyebaran_DBD/
|-- data/
|   |-- raw/
|   `-- processed/
|-- notebooks/
|-- outputs/
|   |-- figures/
|   `-- tables/
|-- src/
|-- requirements.txt
|-- README.md
|-- .gitignore
`-- LICENSE
```

## Dataset

Dataset utama berada di:

```text
data/processed/dataset_harian_estimasi_dbd_jabar_2016_2024_agregat.csv
```

Dataset pendukung ringkasan tahunan berada di:

```text
data/processed/ringkasan_tahunan_dbd_jabar_2016_2024.csv
```

Data 2016-2024 digunakan sebagai data historis. Simulasi utama menggunakan tahun 2024 sebagai baseline karena tahun tersebut memiliki total kasus tertinggi pada rentang data.

Catatan penting: dataset harian merupakan hasil estimasi dari data tahunan 2016-2024, bukan data observasi harian aktual.

## Populasi Efektif Simulasi

Jumlah penduduk asli Jawa Barat tetap dibaca dari dataset, tetapi tidak langsung digunakan sebagai `N` utama pada model SIR. Program menggunakan pendekatan populasi efektif berbasis incidence rate DBD tahun 2024:

```text
N_efektif = (IR / 100000) x jumlah penduduk asli
```

Incidence Rate 2024 yang digunakan adalah `119.69` per 100.000 penduduk. Pendekatan ini digunakan agar simulasi tidak mengasumsikan seluruh penduduk Jawa Barat sebagai populasi rentan aktif.

Dengan pendekatan ini:

- `jumlah_penduduk_asli` digunakan sebagai dasar perhitungan.
- `N_efektif` digunakan sebagai populasi simulasi model SIR.
- `I0` dan `R0` tetap diambil dari rekomendasi dataset tahun 2024.
- `S0` dihitung ulang dengan rumus `S0 = N_efektif - I0 - R0`.

## Model SIR

Model SIR membagi populasi menjadi tiga kompartemen:

- `S` atau Susceptible: populasi rentan.
- `I` atau Infected: populasi terinfeksi.
- `R` atau Recovered: populasi sembuh.

Persamaan model:

```text
dS/dt = -beta S I / N
dI/dt = beta S I / N - gamma I
dR/dt = gamma I
```

## Metode Euler

Metode Euler digunakan untuk menghampiri perubahan S, I, dan R secara diskrit:

```text
S(r+1) = S(r) + h(-beta S(r) I(r) / N)
I(r+1) = I(r) + h(beta S(r) I(r) / N - gamma I(r))
R(r+1) = R(r) + h(gamma I(r))
```

Simulasi dilakukan secara harian dengan `h = 1` hari untuk skenario utama.

## Parameter Simulasi Utama

- `tahun_simulasi = 2024`
- `beta = 0.30`
- `gamma = 1/7`
- `h = 1`
- `t_max = 150`
- `warning_window = 14`
- `incidence_rate_2024 = 119.69`

Nilai awal `I0` dan `R0` diambil dari dataset tahun 2024. Nilai `N` model SIR menggunakan populasi efektif, sedangkan `S0` dihitung dari `N_efektif - I0 - R0`.

## Output Program

Output data historis:

- `outputs/tables/ringkasan_tahunan_dbd_jabar_2016_2024.csv`
- `outputs/figures/grafik_tren_kasus_2016_2024.png`

Output parameter dan simulasi utama:

- `outputs/tables/parameter_simulasi_2024.csv`
- `outputs/tables/hasil_simulasi_sir_2024.csv`
- `outputs/tables/ringkasan_hasil_simulasi.csv`
- `outputs/figures/grafik_sir_2024.png`

Output uji stabilitas step size:

- `outputs/tables/hasil_uji_stabilitas_h.csv`
- `outputs/figures/grafik_uji_stabilitas_h.png`

Output uji sensitivitas parameter:

- `outputs/tables/hasil_uji_sensitivitas_beta.csv`
- `outputs/figures/grafik_uji_sensitivitas_beta.png`
- `outputs/tables/hasil_uji_sensitivitas_gamma.csv`
- `outputs/figures/grafik_uji_sensitivitas_gamma.png`

## Uji Stabilitas h

Uji stabilitas dilakukan dengan membandingkan:

- `h = 1`
- `h = 0.5`

Program menyimpan infected maksimum, hari puncak, hari siaga, waktu komputasi, selisih infected maksimum dari `h = 1`, dan selisih hari puncak dari `h = 1`.

## Uji Sensitivitas Beta dan Gamma

Skenario beta:

- `beta = 0.20`
- `beta = 0.30`
- `beta = 0.40`

Skenario gamma:

- `gamma = 1/5`
- `gamma = 1/7`
- `gamma = 1/10`

Uji ini digunakan untuk melihat pengaruh laju transmisi dan laju kesembuhan terhadap puncak infeksi.

## Catatan Galat

Program tidak menghitung galat terhadap solusi eksak karena solusi analitik dan data observasi harian aktual tidak tersedia. Sebagai gantinya, evaluasi stabilitas numerik dilakukan dengan membandingkan hasil simulasi `h = 1` dan `h = 0.5`.

## Instalasi

```bash
pip install -r requirements.txt
```

## Cara Menjalankan Program

Jalankan dari root project:

```bash
python src/main.py
```

Program akan membuat folder output secara otomatis jika belum tersedia.
