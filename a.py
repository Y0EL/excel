import streamlit as st
import pandas as pd
import re

def identify_symbols(seller_sku):
    # Identifikasi simbol pemisah yang umum digunakan
    separators = re.findall(r'[:,-]', seller_sku)
    return set(separators)

def identify_colors(seller_sku):
    # Daftar warna dalam bahasa Indonesia
    indonesian_colors = ['hitam', 'putih', 'merah', 'biru', 'hijau', 'kuning', 'jingga', 'ungu', 'coklat', 'abu-abu']

    # Temukan kata-kata warna dalam seller_sku
    colors_found = [color for color in indonesian_colors if color in seller_sku.lower()]
    return set(colors_found)

def identify_sizes(seller_sku):
    # Temukan angka dengan panjang 2 digit dalam seller_sku
    sizes_found = re.findall(r'\b\d{2}\b', seller_sku)
    return set(sizes_found)

def process_data(file):
    # Baca file excel
    df = pd.read_excel(file)

    # Identifikasi data
    st.write("File diidentifikasi:")
    st.write(df)

    # Cari data 'orderNumber', 'trackingCode', dan 'sellerSku'
    if 'orderNumber' in df.columns and 'trackingCode' in df.columns and 'sellerSku' in df.columns:
        # Membuat data pada 'orderNumber' menjadi Descending
        df.sort_values(by='orderNumber', ascending=False, inplace=True)
        df.reset_index(drop=True, inplace=True)  # Reset index agar nomor urut sesuai dengan urutan baris

        # Extract information from 'sellerSku'
        df[['No. SKU', 'Warna', 'Size']] = df['sellerSku'].apply(lambda x: pd.Series(extract_info(x)))

        # Buat 6 Kolom menyamping bertuliskan 'No' , 'No. Resi' , 'SKU' , 'Warna' , 'Size' dan 'Ket. Gudang'
        df['No'] = df.index + 1  # Nomor berurutan sesuai dengan jumlah baris
        df['No. Resi'] = df['orderNumber'].astype(str)  # Konversi nomor resi ke string untuk mempertahankan format
        df['SKU'] = df['trackingCode']
        df['Ket. Gudang'] = ''

        # Urutkan kolom sesuai dengan urutan yang diminta
        df = df[['No', 'No. Resi', 'No. SKU', 'SKU', 'Warna', 'Size', 'Ket. Gudang']]

        # Membuat file excel baru
        new_file = "processed_data.xlsx"
        df.to_excel(new_file, index=False)

        st.success(f"File hasil pengolahan disimpan sebagai {new_file}")
    else:
        st.error("Kolom 'orderNumber', 'trackingCode', dan/atau 'sellerSku' tidak ditemukan dalam file.")

def extract_info(seller_sku):
    # Default values if no information found
    no_sku = ''
    warna = ''
    size = ''

    # Try to extract information from seller_sku using regular expressions
    match = re.match(r'([A-Za-z0-9]+)-([A-Za-z]+)-([A-Za-z0-9]+)', seller_sku)
    if match:
        no_sku = match.group(1)
        warna = match.group(2)
        size = match.group(3)
    return no_sku, warna, size

# Tampilan Streamlit
st.title("Pengolahan Data Excel")
file = st.file_uploader("Upload file Excel", type=["xls", "xlsx"])

if file is not None:
    process_data(file)
