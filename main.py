import streamlit as st
import pandas as pd
import joblib
import os

# Judul Aplikasi
st.title("Prediksi Harga Rumah")

# Pengenalan Aplikasi
st.write("""
**Prediksi Harga Rumah**  
Selamat datang di aplikasi *Prediksi Harga Rumah*! Aplikasi ini menggunakan model *Artificial Intelligence (AI)* untuk memprediksi harga rumah di wilayah Boston berdasarkan berbagai kriteria yang Anda masukkan. Model ini dibangun dengan memanfaatkan data historis dan sejumlah faktor penting seperti luas lahan, jumlah kamar, usia rumah, tingkat pajak properti, dan banyak lagi.

Masukkan data sesuai kriteria yang tersedia di bawah, dan temukan estimasi harga rumah Anda dengan cepat dan mudah!
""")

# Path relatif ke file model
model_path = "housing_model.pkl"  # Pastikan file ini ada di direktori yang sama dengan main.py

if not os.path.exists(model_path):
    st.error(f"File model tidak ditemukan di: {model_path}. Pastikan file sudah diunggah ke direktori yang sesuai.")
    st.stop()

# Muat Model
try:
    model = joblib.load(model_path)
    st.success("Model berhasil dimuat!")
except Exception as e:
    st.error(f"Error saat memuat model: {e}")
    st.stop()

# Fungsi untuk mendapatkan input dari pengguna
def get_user_input():
    try:
        ZN = st.number_input("Masukkan persentase lahan zonasi perumahan untuk lot besar (0-100):", min_value=0, max_value=100, step=1)
        INDUS = st.number_input("Masukkan persentase lahan untuk bisnis non-ritel (0-100):", min_value=0, max_value=100, step=1)
        RM = st.number_input("Masukkan jumlah kamar:", min_value=1, step=1)
        AGE = st.number_input("Masukkan usia rumah (0-100):", min_value=0, max_value=100, step=1)
        TAX = st.number_input("Masukkan tarif pajak properti per $10.000:", min_value=0, step=1)
        PTRATIO = st.number_input("Masukkan rasio pelajar-guru di sekolah sekitar:", min_value=0, step=1)
        B = st.number_input("Masukkan proporsi rasio etnis berkulit hitam per 1000 orang:", min_value=0, step=1)
        LSTAT = st.number_input("Masukkan persentase populasi berstatus sosial-ekonomi rendah:", min_value=0, step=1)
        CRIM = st.number_input("Masukkan tingkat kriminalitas per kapita (jumlah kejahatan per penduduk):", min_value=0, step=1)
        CHAS = st.selectbox("Apakah properti berada dekat sungai?", options=[0, 1], format_func=lambda x: "Ya" if x == 1 else "Tidak")
        NOX = st.number_input("Masukkan konsentrasi nitrogen oksida (NOx) per 10 juta:", min_value=0, step=1)
        DIS = st.number_input("Masukkan jarak rata-rata ke pusat pekerjaan (dalam mil):", min_value=0, step=1)
        RAD = st.number_input("Masukkan indeks aksesibilitas ke jalan bebas hambatan:", min_value=0, step=1)

        user_data = pd.DataFrame({
            'ZN': [ZN],
            'INDUS': [INDUS],
            'RM': [RM],
            'AGE': [AGE],
            'TAX': [TAX],
            'PTRATIO': [PTRATIO],
            'B': [B],
            'LSTAT': [LSTAT],
            'CRIM': [CRIM],
            'CHAS': [CHAS],
            'NOX': [NOX],
            'DIS': [DIS],
            'RAD': [RAD]
        })
        return user_data
    except Exception as e:
        st.error(f"Error saat menerima input pengguna: {e}")
        return None

# Input Pengguna
user_input = get_user_input()

if user_input is not None:
    st.write("Data Input Pengguna:")
    st.dataframe(user_input)

    # Normalisasi Data
    try:
        mean = pd.Series([12, 18, 6, 68, 400, 18, 356, 12, 0, 0, 0, 4, 5], 
                         index=['ZN', 'INDUS', 'RM', 'AGE', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'CRIM', 'CHAS', 'NOX', 'DIS', 'RAD'])
        std = pd.Series([7, 7, 1, 28, 100, 2, 50, 7, 1, 1, 1, 2, 3], 
                        index=['ZN', 'INDUS', 'RM', 'AGE', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'CRIM', 'CHAS', 'NOX', 'DIS', 'RAD'])

        user_input_normalized = (user_input - mean) / std
        st.write("Data setelah normalisasi:")
        st.dataframe(user_input_normalized)

        # Prediksi Harga
        predicted_price = model.predict(user_input_normalized)
        
        # Pastikan predicted_price adalah angka tunggal
        st.success(f"Prediksi harga rumah: ${float(predicted_price[0]):,.2f}")

    except Exception as e:
        st.error(f"Error saat melakukan prediksi: {e}")
