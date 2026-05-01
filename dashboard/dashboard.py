import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Bike Sharing Dashboard 🚲")

# Load data
df = pd.read_csv("dashboard/main_data.csv")

# Tampilkan data
st.subheader("Sample Data")
st.write(df.head())

# Analisis jam
st.subheader("Rata-rata Penyewaan per Jam")
hourly = df.groupby("hr")["cnt"].mean()

fig, ax = plt.subplots()
sns.lineplot(x=hourly.index, y=hourly.values, ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig)

# Analisis cuaca
st.subheader("Pengaruh Cuaca terhadap Penyewaan")
weather = df.groupby("weathersit")["cnt"].mean()

fig2, ax2 = plt.subplots()
sns.barplot(x=weather.index, y=weather.values, ax=ax2)
st.pyplot(fig2)