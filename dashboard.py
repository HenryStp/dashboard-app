import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_month_df(df):
    month_df = df.groupby(by="mnth").agg({
    "cnt":"sum",
    "casual":"sum",
    "registered":"sum"
}).sort_values(by="cnt",ascending=True)
    month_df = month_df.reset_index()
    return month_df

def create_season_df(df):
    season_df = df.groupby(by="season").agg({
        "cnt": "sum"
    }).reset_index()
    
    season_mapping = {
        1: "Spring",
        2: "Summer",
        3: "Fall",
        4: "Winter"
    }
    season_df["season"] = season_df["season"].map(season_mapping)
    
    return season_df

def create_holiday_df (df):
    holiday_df = df.groupby(by="holiday").cnt.sum().sort_values(ascending=False).reset_index()
    return holiday_df

def create_hour_df (df):
    hour_df = df.groupby(by='hr').cnt.sum().sort_values(ascending=False).reset_index()
    return hour_df

day_df = pd.read_csv ("day.csv")
hour_df = pd.read_csv("hour.csv")

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/HenryStp/Semester-5/blob/main/sepeda.jpeg?raw=true")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df_1 = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

main_df_2 = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]

month_df = create_month_df(main_df_1)
season_df = create_season_df(main_df_1)
hour_df = create_hour_df(main_df_2)
holiday_df = create_holiday_df(main_df_1)

st.header('Bike Sharing Dashboard :sparkles:')
st.subheader('Monthly Order')

col1, col2, col3 = st.columns(3)

with col1:
    total_order = month_df.cnt.sum()
    st.metric("Total orders", value=total_order)

with col2:
    total_casual = month_df.casual.sum()
    st.metric("Casual User", value = total_casual)

with col3:
    total_registered = month_df.registered.sum()
    st.metric("Registered User", value = total_registered)


month_cnt = month_df.groupby("mnth").cnt.sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(month_cnt.index, month_cnt.values, color='skyblue', edgecolor='black')
ax.set_title("Total Peminjaman Sepeda per Bulan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Peminjaman (cnt)")

st.pyplot(fig)

st.subheader('Musim Favorit Bike Sharing')
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(season_df["season"], season_df["cnt"], color='skyblue', edgecolor='black')
ax.set_title("Total Peminjaman Sepeda per Musim")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Peminjaman (cnt)")

st.pyplot(fig)

st.subheader("Waktu Pemakaian Bike Sharing (jam)")

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x="hr", y="cnt", data=hour_df, color="skyblue", ax=ax)
ax.set_title("Tren Peminjaman Sepeda per Jam", fontsize=16)
ax.set_xlabel("Jam", fontsize=12)
ax.set_ylabel("Total Peminjaman (cnt)", fontsize=12)
plt.tight_layout()
st.pyplot(fig)

st.subheader("Holiday vs Workday")

labels = ['Workday', 'Holiday']
sizes = holiday_df["cnt"]
colors = ['#66b3ff', '#ff9999']
explode = (0.1, 0)


fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    sizes, 
    explode=explode, 
    labels=labels, 
    colors=colors, 
    autopct='%1.1f%%', 
    startangle=90, 
    shadow=True, 
    textprops={'fontsize': 12}
)

ax.legend(wedges, labels, title="Kategori", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

ax.set_title("Proporsi Peminjaman Sepeda: Hari Libur vs Bukan Hari Libur", fontsize=16)

st.pyplot(fig)