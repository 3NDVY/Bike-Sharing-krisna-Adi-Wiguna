# -*- coding: utf-8 -*-
"""Dashboard.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16t-J7mQSg9DnaqPhncsL5C2BHcCOmi_A
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

sns.set(style='dark')

st.header("Data Bike Sharing :fire:")
def by_season_df(df):
    byseason_df = df.groupby(by="weathersit").instant.nunique().reset_index()
    byseason_df.rename(columns={"instant": "sum"}, inplace=True)
    byseason_df

    return byseason_df

def by_working_df(df):
    byworkingday_df = day_df.groupby(by="workingday").instant.nunique().reset_index()
    byworkingday_df.rename(columns={"instant": "sum"}, inplace=True)
    byworkingday_df

    return byworkingday_df

def sidebar(df):
    df["dteday"] = pd.to_datetime(df["dteday"])
    min_date = df["dteday"].min()
    max_date = df["dteday"].max()
    with st.sidebar:
        # Menambahkan logo perusahaan
        st.image("https://th.bing.com/th/id/OIP.VARWOmMVOINqLTlIc1AGZgHaFM?rs=1&pid=ImgDetMain")

        def on_change():
            st.session_state.date = date

        date = st.date_input(
            label="Rentang Waktu",
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date],
            on_change=on_change
        )

    return date

# Dataset
day_df = pd.read_csv("Dashboard/dashboard.csv")

date = sidebar(day_df)
if len(date) == 2:
    main_df = day_df[(day_df["dteday"] >= str(date[0])) & (day_df["dteday"] <= str(date[1]))]
else:
  main_df = day_df[
      (day_df["dteday"] >= str(st.session_state.date[0])) & (day_df["dteday"] <= str(st.session_state.date[1]))]

by_season_df = by_season_df(main_df)
by_working_df = by_working_df(main_df)

st.header("Bike Sharing Dashboard :bike:")

# Pengaruh cuaca terhadap penggunaan sepeda
st.subheader("Berdasarkan musim/cuaca")
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    x="weathersit",
    y="sum",
    data=by_season_df.sort_values(by="sum", ascending=False)
)
ax.set_title("Pengaruh cuaca terhadap Penggunaan Sepeda", loc="center", fontsize=15)
ax.set_ylabel("jumlah Pengguna")
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Temperatur
st.subheader("Berdasarkan Temperatur")
fig, ax = plt.subplots(figsize=(16, 8))
sns.regplot(x=day_df["atemp"], y=day_df["cnt"])
ax.set_title("Pengaruh Temperatur Terhadap Penggunaan Sepeda", loc="center", fontsize=15)
ax.set_ylabel("Jumlah Pengguna")
ax.set_xlabel("Temperatur")
st.pyplot(fig)

# Feeling Temperatur
st.subheader("Berdasarkan feeling Temperatur")
fig, ax = plt.subplots(figsize=(16, 8))
sns.regplot(x=day_df["atemp"], y=day_df["cnt"])
ax.set_title("Pengaruh Feelings Temperatur terhadap penggunaan Sepeda", loc="center", fontsize=15)
ax.set_ylabel("Jumlah Pengguna")
ax.set_xlabel("Feels Temperatur")
st.pyplot(fig)

# pengguna sepeda berdasarkan hari kerja dan hari libur
st.subheader("Berdasarkan hari kerja dan hari libur")
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    x="workingday",
    y="sum",
    data= by_working_df.sort_values(by="workingday", ascending=False),
    ax=ax
)
ax.set_title("Penggunaan Sepeda saat hari kerja dan hari libur", loc="center", fontsize=15)
ax.set_ylabel("Jumlah Pengguna")
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)


st.caption('Copyright (C) 2024, Krisna Adi Wiguna')
