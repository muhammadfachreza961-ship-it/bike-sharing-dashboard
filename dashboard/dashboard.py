import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# ======================
# LOAD DATA
# ======================
df = pd.read_csv("dashboard/main_data.csv")

st.title("🚲 Bike Sharing Dashboard")

st.subheader("Preview Data")
st.dataframe(df.head())

st.subheader("Kolom Dataset")
st.write(df.columns)

# ======================
# CEK KOLOM CNT
# ======================
if "cnt" not in df.columns:
    st.error("Kolom 'cnt' tidak ditemukan di dataset!")
    st.stop()

# ======================
# BASIC STATISTICS
# ======================
st.subheader("Statistik Penyewaan")
st.write(df["cnt"].describe())

# ======================
# GROUPING AMAN (FLEXIBLE)
# ======================

# Coba cari kolom waktu yang umum
time_col = None
for col in ["hr", "hour", "mnth", "dteday", "date"]:
    if col in df.columns:
        time_col = col
        break

st.subheader("Analisis Time-based")

if time_col is None:
    st.warning("Tidak ditemukan kolom waktu (hr/hour/mnth/dteday). Menggunakan index.")
    df["index"] = df.index
    grouped = df.groupby("index")["cnt"].mean()
    x_label = "index"
else:
    # Jika datetime
    if time_col in ["dteday", "date"]:
        df[time_col] = pd.to_datetime(df[time_col])
        df["hour"] = df[time_col].dt.hour
        grouped = df.groupby("hour")["cnt"].mean()
        x_label = "hour"
    else:
        grouped = df.groupby(time_col)["cnt"].mean()
        x_label = time_col

# ======================
# VISUALISASI
# ======================
fig, ax = plt.subplots()
grouped.plot(kind="bar", ax=ax)
ax.set_title(f"Rata-rata Penyewaan berdasarkan {x_label}")
ax.set_xlabel(x_label)
ax.set_ylabel("Jumlah Penyewaan")

st.pyplot(fig)

# ======================
# HEATMAP CORRELATION (SAFE)
# ======================
st.subheader("Korelasi Data")

numeric_df = df.select_dtypes(include=["number"])

if numeric_df.shape[1] > 1:
    fig2, ax2 = plt.subplots()
    sns.heatmap(numeric_df.corr(), annot=False, cmap="coolwarm", ax=ax2)
    st.pyplot(fig2)
else:
    st.info("Tidak cukup data numerik untuk korelasi")