import streamlit as st
import tensorflow 
import pandas as pd
import numpy as np
def main():
    st.title("Bahasa Indonesia - Bahasa Madura")
    
    corpus = pd.read_csv("https://raw.githubusercontent.com/Kaffin190176/file_tugas/main/dataset%20full.csv")

    Bahasa_Indonesia = corpus['Indonesia']
    Bahasa_Madura = corpus['Madura']

    def case_folding(text):
        text= str(text).lower()
        return text
    Bahasa_Indonesia = Bahasa_Indonesia.apply(case_folding)
    Bahasa_Madura = Bahasa_Madura.apply(case_folding)


    import string

    def remove_punctuation(text):
        text = text.replace(' ’ ', "'")
        text = text.replace('?', '')
        text = text.replace('!', '')
        text = text.replace('.', '')
        text = text.replace(',', '')
        text = text.replace(':', '')
        text = text.replace(';', '')
        text = text.replace('/', '')
        text = text.replace('"', '')
        return text

    # Apply the modified function to the Series
    Bahasa_Indonesia = Bahasa_Indonesia.apply(remove_punctuation)
    Bahasa_Madura = Bahasa_Madura.apply(remove_punctuation)



    def tokenize_with_unicode(text):
        # Use word_tokenize from nltk to tokenize the text
        text = text.split()
        return text

    # Apply the modified function to the Series
    Bahasa_Madura = Bahasa_Madura.apply(tokenize_with_unicode)
    Bahasa_Indonesia = Bahasa_Indonesia.apply(tokenize_with_unicode)


    from tensorflow.keras.preprocessing.sequence import pad_sequences


        

    #membuat kosakata kata ke index dan index ke kata
    def create_vocab(sentences):
        word_to_index = {}
        index_to_word = {}
        for sentence in sentences:
            for word in sentence:
                if word not in word_to_index:
                    index = len(word_to_index)
                    word_to_index[word] = index
                    index_to_word[index] = word
        vocab_size = len(word_to_index)
        return word_to_index, index_to_word, vocab_size

    # Vocabulary creation for Madurese
    word_to_index_BM, index_to_word_BM, vocab_size_BM = create_vocab(Bahasa_Madura)

    # Vocabulary creation for Indonesia
    word_to_index_BI, index_to_word_BI, vocab_size_BI = create_vocab(Bahasa_Indonesia)
    # Convert kalimat menjadi integer
    def sentences_to_sequences(sentences, word_to_index):
        return [[word_to_index[word] for word in sentence] for sentence in sentences]
    integer_sequences_BM = sentences_to_sequences(Bahasa_Madura, word_to_index_BM)
    integer_sequences_BI = sentences_to_sequences(Bahasa_Indonesia, word_to_index_BI)

    #menghitung kalimat terpanjang masing-masing sentence

    max_sequence_length_BM = max(len(sequence) for sequence in integer_sequences_BM)
    max_sequence_length_BI = max(len(sequence) for sequence in integer_sequences_BI)
    max_sequence_length = max(max_sequence_length_BM, max_sequence_length_BI)
    # mencari panjang sentence


    # Pad sequences
    padded_sequences_BM = pad_sequences(integer_sequences_BM, maxlen=max_sequence_length, padding='post')
    padded_sequences_BI = pad_sequences(integer_sequences_BI, maxlen=max_sequence_length, padding='post')

    from tensorflow.keras.models import load_model



    def load_my_model():
        model = load_model("D:\Skripsi\web\id_mad64200.h5")  # Ganti dengan path sesuai lokasi file model Anda
        return model

    model = load_my_model()







    def predict_mad(input_text):
        input_text = input_text.lower()
        input_text = remove_punctuation(input_text)
        input_tok= tokenize_with_unicode(input_text)
        predicted_sentence = []
        not_in_word_to_index_BI = []
        for index in input_tok:
            if index in word_to_index_BI:
                predicted_sentence.append(word_to_index_BI[index])
            else:
                predicted_sentence.append(0)
                not_in_word_to_index_BI.append(index)
        padd_seq =pad_sequences([predicted_sentence],maxlen=max_sequence_length, padding='post')

        predict_seq=model.predict([padd_seq , padd_seq])
        predict =[index_to_word_BM[np.argmax(word)] for word in predict_seq[0] ]
        pred_set = ' '. join(predict).split('<pad>')[0]
        return pred_set.replace(index_to_word_BM[0],''), not_in_word_to_index_BI




    text = st.text_input('Masukkan Kata Bahasa Indonesia : ',key="indo")


    pred_set, not_in_word_to_index_BI = predict_mad(text)
    not_in_word_to_index_BM_text = ' '.join(not_in_word_to_index_BI)

    # Mengatur tata letak untuk menampilkan dua output berdampingan
    col1, col2 = st.columns(2)  # Membagi layout menjadi dua kolom


    # Output terjemahan

    with col1:
        st.write('Terjemahan :')
        st.text_area('', value=pred_set, height=200,key="indo1")

    # Output kata tidak ada dalam data
    with col2:
        st.write('Kata ini tidak ada dalam data:')
        st.text_area('', value=not_in_word_to_index_BM_text, height=200,key="indo2")


if __name__ == "__main__":
    main()