import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Konfigurasi halaman
st.set_page_config(page_title="Bike Sharing Analysis Dashboard", layout="wide")

# --- LOAD DATA ---
# Memastikan data yang dimuat adalah data yang sudah dibersihkan
@st.cache_data
def load_data():
    # Menggunakan main_data.csv (hasil export dari notebook setelah cleaning)
    # Jika belum ada, pastikan notebook sudah dijalankan sampai tahap day_df.to_csv('main_data.csv')
    df_day = pd.read_csv("main_data.csv")
    df_day["dteday"] = pd.to_datetime(df_day["dteday"])
    return df_day

try:
    main_df = load_data()
except Exception as e:
    st.error(f"Gagal memuat data. Pastikan file 'main_data.csv' tersedia. Error: {e}")
    st.stop()

# --- SIDEBAR (Fitur Interaktif) ---
st.sidebar.image("https://raw.githubusercontent.com/dicodingacademy/dicoding_dataset/main/logo_dicoding.png")
st.sidebar.header("Filter Eksplorasi")

# Fitur Interaktif 1: Filter Rentang Tanggal
min_date = main_df["dteday"].min()
max_date = main_df["dteday"].max()

start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Filter dataframe berdasarkan input
filtered_df = main_df[(main_df["dteday"] >= pd.to_datetime(start_date)) & 
                       (main_df["dteday"] <= pd.to_datetime(end_date))]

# --- MAIN PAGE ---
st.title("Bike Sharing Analysis Dashboard 🚲")
st.markdown("Dashboard ini menampilkan hasil analisis data penyewaan sepeda berdasarkan pertanyaan bisnis.")

# Metric Row
col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = filtered_df["total_count"].sum()
    st.metric("Total Penyewaan", value=f"{total_rentals:,}")
with col2:
    avg_rentals = round(filtered_df["total_count"].mean(), 2)
    st.metric("Rata-rata Harian", value=avg_rentals)
with col3:
    max_rentals = filtered_df["total_count"].max()
    st.metric("Puncak Penyewaan", value=f"{max_rentals:,}")

st.divider()

# --- VISUALISASI 1: PENGARUH CUACA (Pertanyaan Bisnis 1) ---
st.subheader("1. Pengaruh Kondisi Cuaca terhadap Penyewaan")
fig, ax = plt.subplots(figsize=(10, 5))

# Karena sudah di-mapping di cleaning, label otomatis 'Clear', 'Misty', dll.
sns.barplot(
    x="weather_condition", 
    y="total_count", 
    data=filtered_df, 
    palette="viridis",
    ax=ax,
    estimator='mean'
)
ax.set_title("Rata-rata Penyewaan per Hari Berdasarkan Kondisi Cuaca", fontsize=15)
ax.set_xlabel(None)
ax.set_ylabel("Rata-rata Jumlah Penyewaan")
st.pyplot(fig)

with st.expander("Lihat Insight"):
    st.write(
        "Kondisi cuaca **Clear** (Cerah) menunjukkan angka penyewaan tertinggi. "
        "Terjadi penurunan signifikan saat cuaca memasuki kategori **Light Snow/Rain**. "
        "Hal ini membuktikan bahwa cuaca merupakan faktor penentu utama dalam keputusan pengguna."
    )

# --- VISUALISASI 2: POLA HARI KERJA VS LIBUR (Pertanyaan Bisnis 2) ---
# Catatan: Untuk visualisasi per jam yang akurat, idealnya menggunakan hour_df. 
# Jika hanya ada main_data.csv (harian), kita tampilkan perbandingan harian.
st.subheader("2. Perbandingan Penyewaan: Hari Kerja vs Hari Libur")
fig2, ax2 = plt.subplots(figsize=(10, 5))

sns.boxplot(
    x="workingday", 
    y="total_count", 
    data=filtered_df, 
    palette="rocket",
    ax=ax2
)
ax2.set_title("Distribusi Penyewaan: Hari Kerja vs Hari Libur", fontsize=15)
ax2.set_xlabel(None)
ax2.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig2)

with st.expander("Lihat Insight"):
    st.write(
        "Meskipun rata-rata penyewaan pada hari kerja dan hari libur tampak bersaing, "
        "hari kerja cenderung memiliki variansi yang lebih stabil. "
        "Hal ini menunjukkan adanya kelompok pengguna rutin (komuter) pada hari kerja."
    )

st.caption('Copyright (c) Muhammad Fachreza Aldava Sinaga 2024')