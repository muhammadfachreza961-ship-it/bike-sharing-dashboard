import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "main_data.csv")
st.set_page_config(page_title="Bike Sharing Analysis Dashboard", layout="wide")

st.markdown("""
    <style>
    div[data-baseweb="popover"] {
        transform: translate3d(0px, 40px, 0px) !important;
    }
    section[data-testid="stSidebar"] > div {
        overflow-y: auto;
        padding-bottom: 300px; 
    }
    </style>
    """, unsafe_allow_html=True)
import os


@st.cache_data
def load_data():
    # Menggunakan csv_path yang sudah didefinisikan secara absolut
    if not os.path.exists(csv_path):
        st.error(f"File tidak ditemukan di: {csv_path}")
        st.stop()
        
    df_day = pd.read_csv(csv_path)
    df_day["dteday"] = pd.to_datetime(df_day["dteday"])
    return df_day

try:
    main_df = load_data()
except Exception as e:
    st.error(f"Gagal memuat data: {e}")
    st.stop()

st.sidebar.header("Filter Eksplorasi")

# 1. Filter Rentang Waktu
min_date, max_date = main_df["dteday"].min(), main_df["dteday"].max()
date_range = st.sidebar.date_input(
    "Pilih Rentang Waktu",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# 2. Filter Kondisi Cuaca (Mengambil label unik langsung dari data)
weather_col = "weather_condition" if "weather_condition" in main_df.columns else "weathersit"
weather_options = sorted(main_df[weather_col].unique())
selected_weather = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca:",
    options=weather_options,
    default=weather_options
)

# 3. Filter Tipe Hari (Working Day / Holiday)
workingday_col = "workingday"
day_options = sorted(main_df[workingday_col].unique())
selected_day = st.sidebar.multiselect(
    "Pilih Tipe Hari:",
    options=day_options,
    default=day_options
)

# --- LOGIKA FILTERING DATA ---
# Filter Tanggal
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
    df_filtered = main_df[(main_df["dteday"] >= pd.to_datetime(start_date)) & 
                          (main_df["dteday"] <= pd.to_datetime(end_date))]
else:
    df_filtered = main_df

# Filter Cuaca dan Tipe Hari
df_filtered = df_filtered[
    (df_filtered[weather_col].isin(selected_weather)) & 
    (df_filtered[workingday_col].isin(selected_day))
]

# --- MAIN PAGE ---
st.title("Bike Sharing Analysis Dashboard 🚲")

# Metrics Section
y_col = "total_count" if "total_count" in main_df.columns else "cnt"
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Penyewaan", f"{df_filtered[y_col].sum():,}")
with col2:
    avg_val = int(df_filtered[y_col].mean()) if not df_filtered.empty else 0
    st.metric("Rata-rata Penyewaan", f"{avg_val:,}")

st.divider()

# Visualisasi 1: Cuaca
st.subheader("1. Pengaruh Kondisi Cuaca terhadap Penyewaan")
if not df_filtered.empty:
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.barplot(
        x=weather_col, 
        y=y_col, 
        data=df_filtered, 
        palette="viridis", 
        ax=ax1, 
        estimator='mean',
        order=weather_options # Menjaga urutan agar konsisten
    )
    ax1.set_ylabel("Rata-rata Penyewaan")
    ax1.set_xlabel("Kondisi Cuaca")
    st.pyplot(fig1)
else:
    st.warning("Tidak ada data untuk filter yang dipilih.")

# Visualisasi 2: Hari Kerja vs Libur
st.subheader("2. Distribusi Penyewaan: Hari Kerja vs Hari Libur")
if not df_filtered.empty:
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.boxplot(
        x=workingday_col, 
        y=y_col, 
        data=df_filtered, 
        palette="rocket", 
        ax=ax2,
        order=day_options
    )
    ax2.set_ylabel("Jumlah Penyewaan")
    ax2.set_xlabel("Tipe Hari")
    st.pyplot(fig2)
    
    with st.expander("Lihat Insight"):
        st.write(f"Data yang ditampilkan mencakup **{len(df_filtered)}** hari hasil filtrasi.")
        st.write("Kondisi cuaca yang cerah dan hari kerja tetap menjadi penyumbang volume penyewaan paling stabil.")