import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

sns.set(style='dark')

st.subheader("Data")

# Fungsi untuk memproses data berdasarkan cuaca
def by_season_df(df):
    byseason_df = df.groupby(by="weathersit").instant.nunique().reset_index()
    byseason_df.rename(columns={"instant": "sum"}, inplace=True)
    return byseason_df  # Pastikan fungsi mengembalikan dataframe

# Fungsi untuk memproses data berdasarkan hari kerja
def by_working_df(df):
    byworkingday_df = df.groupby(by="workingday").instant.nunique().reset_index()
    byworkingday_df.rename(columns={"instant": "sum"}, inplace=True)
    return byworkingday_df  # Pastikan fungsi mengembalikan dataframe

# Sidebar untuk rentang tanggal
def sidebar(df):
    df["dteday"] = pd.to_datetime(df["dteday"])
    min_date = df["dteday"].min()
    max_date = df["dteday"].max()

    # Inisialisasi session_state jika belum ada
    if 'date' not in st.session_state:
        st.session_state.date = [min_date, max_date]

    with st.sidebar:
        # Menambahkan logo perusahaan
        st.image("https://w7.pngwing.com/pngs/837/372/png-transparent-bicycle-cycling-mountain-bike-bicycle.png")

        # Fungsi untuk mengubah rentang tanggal
        def on_change():
            st.session_state.date = date

        # Input rentang waktu dengan date_input
        date = st.date_input(
            label="Rentang Waktu",
            min_value=min_date,
            max_value=max_date,
            value=st.session_state.date,
            on_change=on_change
        )

    return date

# Memuat dataset
day_df = pd.read_csv("dashboard.csv")

# Mendapatkan rentang waktu dari sidebar
date = sidebar(day_df)
if len(date) == 2:
    main_df = day_df[(day_df["dteday"] >= pd.to_datetime(date[0])) & (day_df["dteday"] <= pd.to_datetime(date[1]))]
else:
    main_df = day_df[(day_df["dteday"] >= pd.to_datetime(st.session_state.date[0])) & (day_df["dteday"] <= pd.to_datetime(st.session_state.date[1]))]

# Mengolah data berdasarkan cuaca dan hari kerja
by_season_df = by_season_df(main_df)
by_working_df = by_working_df(main_df)

# Header Dashboard
st.header("Bike Sharing Dashboard :bike:")

# Pengaruh cuaca terhadap penggunaan sepeda
st.subheader("Bike Sharing berdasarkan musim")
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    x="weathersit",
    y="sum",
    data=by_season_df.sort_values(by="sum", ascending=False)
)
ax.set_title("Pengaruh Cuaca terhadap Penggunaan Sepeda", loc="center", fontsize=15)
ax.set_ylabel("Jumlah Pengguna")
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Pengaruh Temperatur terhadap penggunaan sepeda
st.subheader("Berdasarkan Temperatur")
fig, ax = plt.subplots(figsize=(16, 8))
sns.regplot(x=day_df["atemp"], y=day_df["cnt"])
ax.set_title("Pengaruh Temperatur Terhadap Penggunaan Sepeda", loc="center", fontsize=15)
ax.set_ylabel("Jumlah Pengguna")
ax.set_xlabel("Temperatur")
st.pyplot(fig)

# Pengaruh Feels Temperatur terhadap penggunaan sepeda
st.subheader("Berdasarkan Feelings Temperatur")
fig, ax = plt.subplots(figsize=(16, 8))
sns.regplot(x=day_df["atemp"], y=day_df["cnt"])
ax.set_title("Pengaruh Feelings Temperatur terhadap Penggunaan Sepeda", loc="center", fontsize=15)
ax.set_ylabel("Jumlah Pengguna")
ax.set_xlabel("Feels Temperatur")
st.pyplot(fig)

# Penggunaan sepeda berdasarkan hari kerja dan hari libur
st.subheader("Penggunaan Sepeda berdasarkan hari kerja dan hari libur")
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    x="workingday",
    y="sum",
    data=by_working_df.sort_values(by="workingday", ascending=False),
    ax=ax
)
ax.set_title("Penggunaan Sepeda saat Hari Kerja dan Hari Libur", loc="center", fontsize=15)
ax.set_ylabel("Jumlah Pengguna")
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Menampilkan nama pembuat dashboard
st.caption('Krisna Adi Wiguna')
