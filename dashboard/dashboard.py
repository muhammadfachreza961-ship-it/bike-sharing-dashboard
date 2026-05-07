import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Konfigurasi halaman
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Memuat data
BASE_DIR = os.path.dirname(__file__)
try:
    df = pd.read_csv(os.path.join(BASE_DIR, "main_data.csv"))
    if "dteday" in df.columns:
        df["dteday"] = pd.to_datetime(df["dteday"])
except Exception as e:
    st.error(f"Gagal memuat data: {e}")
    st.stop()

st.title("Bike Sharing Dashboard 🚲")

# Sidebar - Filter
st.sidebar.header("Filter Data")

# 1. Validasi Input Tanggal
try:
    min_date = df["dteday"].min()
    max_date = df["dteday"].max()

    date_range = st.sidebar.date_input(
        "Pilih Rentang Tanggal",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    if len(date_range) == 2:
        start_date, end_date = date_range
        main_df = df[(df["dteday"] >= pd.to_datetime(start_date)) & 
                     (df["dteday"] <= pd.to_datetime(end_date))]
    else:
        st.info("Silakan pilih rentang tanggal lengkap (Start Date dan End Date) di sidebar.")
        st.stop()
except Exception:
    st.error("Terjadi kesalahan pada filter tanggal.")
    st.stop()

# 2. Filter Musim (Dibuat agar selalu tersedia dan aman)
if "season" in df.columns:
    # Kita ambil daftar musim unik dari dataframe asli agar pilihan tetap ada 
    # meskipun filter tanggal mengubah isi data
    list_musim = sorted(df["season"].unique())
    
    selected_season = st.sidebar.multiselect(
        "Pilih Musim",
        options=list_musim,
        default=list_musim  # Secara default terpilih semua
    )
    
    # Validasi: Jika user mengosongkan semua musim, berikan peringatan
    if not selected_season:
        st.sidebar.warning("Pilih minimal satu musim untuk menampilkan data.")
        st.stop() # Dashboard berhenti di sini sampai user memilih musim kembali
    
    # Filter dataframe berdasarkan pilihan musim
    main_df = main_df[main_df["season"].isin(selected_season)]

# --- Bagian Visualisasi (Tetap Sama) ---

st.subheader("Ringkasan Data")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", f"{main_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Penyewaan", f"{main_df['cnt'].mean():.2f}")
with col3:
    st.metric("Maksimum Penyewaan", f"{main_df['cnt'].max():,}")

if "weathersit" in main_df.columns:
    st.subheader("Pengaruh Kondisi Cuaca terhadap Penyewaan")
    weather_avg = main_df.groupby("weathersit")["cnt"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=weather_avg.index, y=weather_avg.values, palette="viridis", ax=ax)
    ax.set_title("Rata-rata Penyewaan Berdasarkan Kondisi Cuaca")
    ax.set_xlabel("Kondisi Cuaca (1: Cerah, 4: Buruk)")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

if "hr" in main_df.columns and "workingday" in main_df.columns:
    st.subheader("Pola Penyewaan: Hari Kerja vs Hari Libur")
    hourly_pattern = main_df.groupby(["hr", "workingday"])["cnt"].mean().reset_index()
    hourly_pattern["workingday"] = hourly_pattern["workingday"].map({1: "Hari Kerja", 0: "Hari Libur"})
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=hourly_pattern, x="hr", y="cnt", hue="workingday", marker="o", ax=ax)
    ax.set_title("Perbandingan Rata-rata Penyewaan per Jam")
    ax.set_xlabel("Jam (0-23)")
    ax.set_ylabel("Rata-rata Jumlah Penyewaan")
    ax.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig)
    
    st.info("""
    **Insight:**
    - Pada **Hari Kerja**, puncak penyewaan terjadi pada jam sibuk (08:00 dan 17:00-18:00).
    - Pada **Hari Libur**, puncak penyewaan cenderung stabil di tengah hari (11:00-15:00).
    """)