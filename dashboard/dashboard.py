import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
# ======================
# CONFIG
# ======================
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# ======================
# LOAD DATA
# ======================
BASE_DIR = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(BASE_DIR, "main_data.csv"))

if "dteday" in df.columns:
    df["dteday"] = pd.to_datetime(df["dteday"])

# ======================
# TITLE
# ======================
st.title("🚲 Bike Sharing Dashboard")

# ======================
# MAPPING KATEGORI
# ======================
season_map = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

weather_map = {
    1: "Cerah",
    2: "Berawan",
    3: "Hujan Ringan",
    4: "Buruk"
}

if "season" in df.columns:
    df["season_label"] = df["season"].map(season_map)

if "weathersit" in df.columns:
    df["weather_label"] = df["weathersit"].map(weather_map)

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.header("Filter Data")

# Date filter
if "dteday" in df.columns:
    min_date = df["dteday"].min()
    max_date = df["dteday"].max()

    date_range = st.sidebar.date_input(
        "Pilih Rentang Tanggal",
        [min_date, max_date]
    )

    df = df[
        (df["dteday"] >= pd.to_datetime(date_range[0])) &
        (df["dteday"] <= pd.to_datetime(date_range[1]))
    ]

# Season filter (TEXT)
if "season_label" in df.columns:
    season = st.sidebar.selectbox(
        "Pilih Musim",
        options=sorted(df["season_label"].dropna().unique())
    )
    df = df[df["season_label"] == season]

# ======================
# KPI METRICS
# ======================
st.subheader("📊 Ringkasan Data")

col1, col2, col3 = st.columns(3)

col1.metric("Total Penyewaan", int(df["cnt"].sum()))
col2.metric("Rata-rata Penyewaan", int(df["cnt"].mean()))
col3.metric("Maksimum Penyewaan", int(df["cnt"].max()))

# ======================
# PREVIEW DATA
# ======================
st.subheader("Preview Data")
st.dataframe(df.head())

# ======================
# STATISTIK
# ======================
st.subheader("Statistik Penyewaan")
st.write(df["cnt"].describe())

# ======================
# PERTANYAAN 1: CUACA
# ======================
if "weather_label" in df.columns:
    st.subheader("🌤 Pengaruh Cuaca terhadap Penyewaan")

    weather_avg = df.groupby("weather_label")["cnt"].mean().sort_values(ascending=False)

    st.dataframe(weather_avg)

    fig1, ax1 = plt.subplots()
    sns.barplot(x=weather_avg.index, y=weather_avg.values, ax=ax1)

    ax1.set_title("Rata-rata Penyewaan Berdasarkan Cuaca")
    ax1.set_xlabel("Cuaca")
    ax1.set_ylabel("Rata-rata Penyewaan")

    st.pyplot(fig1)

    st.success(
        f"Cuaca dengan penyewaan tertinggi adalah {weather_avg.idxmax()} "
        f"({weather_avg.max():.0f} rata-rata penyewaan)"
    )

# ======================
# PERTANYAAN 2: BULAN
# ======================
if "mnth" in df.columns:
    st.subheader("📅 Tren Penyewaan per Bulan")

    monthly = df.groupby("mnth")["cnt"].mean()

    fig2, ax2 = plt.subplots()
    ax2.plot(monthly.index, monthly.values, marker="o")

    ax2.set_title("Rata-rata Penyewaan per Bulan")
    ax2.set_xlabel("Bulan")
    ax2.set_ylabel("Rata-rata Penyewaan")

    st.pyplot(fig2)

# ======================
# PERTANYAAN 3: JAM
# ======================
if "hr" in df.columns and "workingday" in df.columns:
    st.subheader("⏰ Pola Penyewaan per Jam")

    weekday = df[df["workingday"] == 1]
    weekend = df[df["workingday"] == 0]

    weekday_hour = weekday.groupby("hr")["cnt"].mean()
    weekend_hour = weekend.groupby("hr")["cnt"].mean()

    fig3, ax3 = plt.subplots()

    ax3.plot(weekday_hour.index, weekday_hour.values, label="Weekday")
    ax3.plot(weekend_hour.index, weekend_hour.values, label="Weekend")

    ax3.set_title("Pola Penyewaan per Jam")
    ax3.set_xlabel("Jam")
    ax3.set_ylabel("Rata-rata Penyewaan")
    ax3.legend()

    st.pyplot(fig3)

    st.subheader("📌 Insight Jam Puncak")

    st.write(f"Weekday peak: jam {weekday_hour.idxmax()} dengan rata-rata {weekday_hour.max():.0f}")
    st.write(f"Weekend peak: jam {weekend_hour.idxmax()} dengan rata-rata {weekend_hour.max():.0f}")

# ======================
# KORELASI
# ======================
st.subheader("📈 Korelasi Data")

numeric_df = df.select_dtypes(include=["number"])

if numeric_df.shape[1] > 1:
    fig4, ax4 = plt.subplots()
    sns.heatmap(numeric_df.corr(), cmap="coolwarm", ax=ax4)

    st.pyplot(fig4)
else:
    st.info("Tidak cukup data numerik untuk korelasi")