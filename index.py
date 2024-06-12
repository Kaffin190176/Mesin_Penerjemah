import streamlit as st
import mad_ind
import ind_mad

def main():
    st.sidebar.title("Mesin Penerjemah ")
    selected_page = st.sidebar.radio("Pilih Bahasa", ["Bahasa Madura - Bahasa Indonesia", "Bahasa Indonesia - Bahasa Madura"])

    if selected_page == "Bahasa Madura - Bahasa Indonesia":
        mad_ind.main()
    elif selected_page == "Bahasa Indonesia - Bahasa Madura":
        ind_mad.main()

if __name__ == "__main__":
    main()

#streamlit run D:\Skripsi\web\index.py