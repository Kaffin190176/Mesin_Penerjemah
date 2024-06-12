import streamlit as st

# Fungsi untuk menambahkan huruf ke dalam input teks
def add_letter(letter):
    text_input_value = st.session_state.text_input_value
    st.session_state.text_input_value = text_input_value + letter

# Fungsi utama Streamlit
def main():
    st.title("Keyboard Virtual untuk Streamlit")

    # Buat variabel untuk menyimpan nilai input teks
    if 'text_input_value' not in st.session_state:
        st.session_state.text_input_value = ""

    # Tampilkan input teks
    text_input_value = st.session_state.text_input_value
    text_input = st.text_input("Masukkan Teks", value=text_input_value)

    # Tambahkan tombol-tombol untuk setiap huruf
    st.write("Tombol Keyboard:")
    letters = 'abcdefghijklmnopqrstuvwxyz'
    for letter in letters:
        st.button(letter, on_click=add_letter, args=(letter,))

if __name__ == "__main__":
    main()
