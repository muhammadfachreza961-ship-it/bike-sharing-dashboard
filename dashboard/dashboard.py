import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

BASE_DIR = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(BASE_DIR, "main_data.csv"))

if "dteday" in df.columns:
    df["dteday"] = pd.to_datetime(df["dteday"])

st.title("Bike Sharing Dashboard")

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

st.sidebar.header("Filter Data")

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

if "season_label" in df.columns:
    season = st.sidebar.selectbox(
        "Pilih Musim",
        options=sorted(df["season_label"].dropna().unique())
    )
    df = df[df["season_label"] == season]

if "weather_label" in df.columns:
    weather = st.sidebar.multiselect(
        "Pilih Cuaca",
        options=df["weather_label"].dropna().unique(),
        default=df["weather_label"].dropna().unique()
    )
    df = df[df["weather_label"].isin(weather)]

st.subheader("Ringkasan Data")

col1, col2, col3 = st.columns(3)

col1.metric("Total Penyewaan", int(df["cnt"].sum()))
col2.metric("Rata-rata Penyewaan", int(df["cnt"].mean()))
col3.metric("Maksimum Penyewaan", int(df["cnt"].max()))

st.subheader("Preview Data")
st.dataframe(df.head())

if "weather_label" in df.columns:
    st.subheader("Pengaruh Cuaca terhadap Penyewaan")

    weather_avg = df.groupby("weather_label")["cnt"].mean().sort_values(ascending=False)

    st.dataframe(weather_avg)

    fig1, ax1 = plt.subplots()
    sns.barplot(x=weather_avg.index, y=weather_avg.values, ax=ax1)

    ax1.set_title("Rata-rata Penyewaan Berdasarkan Cuaca")
    ax1.set_xlabel("Cuaca")
    ax1.set_ylabel("Rata-rata Penyewaan")

    st.pyplot(fig1)

    st.success(
        f"Cuaca tertinggi: {weather_avg.idxmax()} ({weather_avg.max():.0f})"
    )

if "hr" in df.columns:
    st.subheader("Pola Penyewaan Berdasarkan Jam")

    hour_avg = df.groupby("hr")["cnt"].mean()

    fig2, ax2 = plt.subplots()
    ax2.plot(hour_avg.index, hour_avg.values, marker="o")

    ax2.set_title("Rata-rata Penyewaan per Jam")
    ax2.set_xlabel("Jam")
    ax2.set_ylabel("Rata-rata Penyewaan")

    st.pyplot(fig2)

    st.success(
        f"Puncak terjadi jam {hour_avg.idxmax()} "
        f"dengan rata-rata {hour_avg.max():.0f}"
    )

if "hr" in df.columns and "workingday" in df.columns:
    st.subheader("Weekday vs Weekend")

    weekday = df[df["workingday"] == 1]
    weekend = df[df["workingday"] == 0]

    weekday_hour = weekday.groupby("hr")["cnt"].mean()
    weekend_hour = weekend.groupby("hr")["cnt"].mean()

    fig3, ax3 = plt.subplots()

    ax3.plot(weekday_hour.index, weekday_hour.values, label="Weekday")
    ax3.plot(weekend_hour.index, weekend_hour.values, label="Weekend")

    ax3.set_title("Perbandingan Penyewaan")
    ax3.set_xlabel("Jam")
    ax3.set_ylabel("Rata-rata")
    ax3.legend()

    st.pyplot(fig3)


st.subheader("Korelasi")

numeric_df = df.select_dtypes(include=["number"])

if numeric_df.shape[1] > 1:
    fig4, ax4 = plt.subplots()
    sns.heatmap(numeric_df.corr(), cmap="coolwarm", ax=ax4)
    st.pyplot(fig4)