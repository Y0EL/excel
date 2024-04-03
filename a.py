import streamlit as st
import pandas as pd
import re

def process_data(file):
    # Baca file excel
    df = pd.read_excel(file)

    # Identifikasi data
    st.write("File diidentifikasi:")
    st.write(df)

    # Cari data 'No. Pesanan', 'No. Resi', 'Nomor Referensi SKU', 'Nama Variasi', dan tambahan 'Keterangan Gudang'
    if 'No. Pesanan' in df.columns and 'No. Resi' in df.columns and 'Nomor Referensi SKU' in df.columns and 'Nama Variasi' in df.columns:
        # Membuat data pada 'No. Pesanan' menjadi Descending
        df.sort_values(by='No. Pesanan', ascending=False, inplace=True)
        df.reset_index(drop=True, inplace=True)  # Reset index agar nomor urut sesuai dengan urutan baris

        # Extract SKU from 'Nomor Referensi SKU'
        df['SKU'] = df['Nomor Referensi SKU'].apply(lambda x: re.split(r'[^\w]+', str(x))[0])

        # Combine Warna & Size from 'Nama Variasi'
        df['Warna & Size'] = df['Nama Variasi'].apply(lambda x: str(x))

        # Renaming columns
        df.rename(columns={'No. Pesanan': 'No. Order', 'No. Resi': 'Nomor Resi'}, inplace=True)

        # Buat Kolom 'Keterangan Gudang' dengan nilai kosong
        df['Keterangan Gudang'] = ''

        # Urutkan kolom sesuai dengan urutan yang diminta
        df = df[['No. Order', 'Nomor Resi', 'SKU', 'Warna & Size', 'Keterangan Gudang']]

        try:
            # Membuat file excel baru
            new_file = "processed_data.xlsx"
            df.to_excel(new_file, index=False)
            st.success(f"File hasil pengolahan disimpan sebagai {new_file}")
            st.write(df)  # Menampilkan dataframe hasil pengolahan
        except Exception as e:
            st.error(f"Terjadi kesalahan saat menyimpan file Excel: {str(e)}")
    else:
        st.error("Kolom yang diperlukan tidak ditemukan dalam file.")

# Tampilan Streamlit
st.title("Pengolahan Data Excel")
file = st.file_uploader("Upload file Excel", type=["xls", "xlsx"])

if file is not None:
    process_data(file)
