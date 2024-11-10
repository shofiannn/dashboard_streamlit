import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

import csv
import os

def read_csv_file(file_path):
    """
    Membaca file CSV dan mengembalikan data sebagai list of dictionaries.
    
    :param file_path: Path ke file CSV
    :return: List of dictionaries yang berisi data dari file CSV
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} tidak ditemukan.")
    
    data = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    
    return data

# Contoh penggunaan
file_path = 'data_day.csv'
try:
    data = read_csv_file(file_path)
    print(data)
except FileNotFoundError as e:
    print(e)

day_df = pd.DataFrame(data)

st.header("Pengaruh Musim Terhadap Penyewaan Sepeda (Dalam Persentase)")

day_df['cnt'] = pd.to_numeric(day_df['cnt'], errors='coerce')  # Konversi 'cnt' menjadi numerik

# Menghitung persentase penyewaan per musim
persentase = day_df.groupby('season')['cnt'].sum() / day_df['cnt'].sum() * 100

# Membuat DataFrame untuk persentase
persentase_df = persentase.reset_index(name="persentase")

# Membuat Bar Plot
fig, ax = plt.subplots(figsize=(15, 8))  # Ukuran plot

# Plot persentase penyewaan sepeda berdasarkan musim
sns.barplot(x="season", y="persentase", data=persentase_df, palette='coolwarm', ax=ax)

# Menambahkan label dan judul
ax.set_ylabel("Persentase Sepeda yang Disewakan", fontsize=20)
ax.set_xlabel("Musim ", fontsize=20)
plt.xticks(persentase.index, ['Semi', 'Panas', 'Gugur', 'Salju'], fontsize=15)

# Menampilkan plot di Streamlit
st.pyplot(fig)

with st.expander("Penjelasan"):
    st.write(
        """
        Dari plot di atas, kita dapat melihat bahwa Musim Gugur adalah musim yang paling banyak diminati oleh pengguna sepeda dengan persentase lebih dari 30%.
        """
    )

# Kelompokkan data berdasarkan kolom 'yr' dan hitung total 'cnt' untuk setiap tahun
data_grouped = day_df.groupby('yr')['cnt'].sum()

# Buat pie chart
labels = data_grouped.index
sizes = data_grouped.values
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
explode = (0.1, 0)  # Hanya meledakkan potongan pertama (jika ada dua tahun)

fig, ax = plt.subplots()
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.pie(data_grouped, labels=['Tahun 2011', 'Tahun 2012'], autopct='%1.1f%%', startangle=90)

st.header('Total Penyewaan Sepeda di Tahun 2011 dan 2012')
st.pyplot(fig)

with st.expander("Penjelasan"):
    st.write(
        """
        Dari pie chart di atas, kita dapat melihat bahwa total penyewaan sepeda di tahun 2012 lebih tinggi daripada tahun 2011 dengan selisih yaitu 24,4 %
        """
    )
