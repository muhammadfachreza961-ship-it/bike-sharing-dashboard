# 🚲 Bike Sharing Dashboard

Dashboard ini dibuat menggunakan Streamlit untuk menganalisis pola penyewaan sepeda berdasarkan dataset Bike Sharing tahun 2011–2012. Proyek ini bertujuan untuk menjawab beberapa pertanyaan bisnis terkait tren penggunaan sepeda, pola waktu penyewaan, serta pengaruh faktor eksternal seperti cuaca.

---

# 🎯 Tujuan Analisis

Beberapa pertanyaan utama yang dijawab dalam proyek ini:

1. Bagaimana tren jumlah penyewaan sepeda per bulan selama tahun 2011–2012?
2. Pada jam berapa terjadi puncak penyewaan sepeda berdasarkan rata-rata jumlah penyewaan antara hari kerja (weekday) dan hari libur (weekend) selama 2011–2012?
3. Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda?

---

# ⚙️ Setup Environment

## 1. Clone Repository

```bash
git clone https://github.com/username/bike-sharing-dashboard.git
cd bike-sharing-dashboard
```

---

## 2. Membuat Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### MacOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

Pastikan file **requirements.txt** berada di root project, lalu jalankan:

```bash
pip install -r requirements.txt
```

---

# ▶️ Menjalankan Dashboard

Jalankan perintah berikut untuk membuka dashboard:

```bash
streamlit run dashboard.py
```

Setelah itu, dashboard akan terbuka otomatis di browser.

---

# 📊 Fitur Dashboard

Dashboard ini memiliki beberapa fitur utama:

* 📈 Visualisasi tren penyewaan sepeda per bulan
* ⏰ Perbandingan pola penyewaan berdasarkan jam (weekday vs weekend)
* 🌦️ Analisis pengaruh kondisi cuaca terhadap jumlah penyewaan
* 🎛️ Fitur interaktif (filter data berdasarkan parameter tertentu seperti tanggal, musim, atau cuaca)

---

# 📦 Struktur Folder

```text
bike-sharing-dashboard/
│
├── dashboard.py
├── requirements.txt
├── README.md
├── data/
│   └── main_data.csv
```

---

# 📌 Catatan Penting

* Gunakan Python versi 3.8 atau lebih baru
* Disarankan menggunakan virtual environment untuk menghindari konflik library
* Pastikan semua dependencies sudah terinstall sebelum menjalankan dashboard
* Jika terjadi error, periksa kembali path file dataset dan versi library

---

# 👨‍💻 Author

Muhammad Fachreza Aldava Sinaga
Submission Analisis Data - Dicoding

---
