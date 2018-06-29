import pandas as pd
import math
import matplotlib.pyplot as plt

import numpy as np
from scipy.cluster.vq import vq, kmeans, whiten
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from mod_Normalize import normalize
from normalize_slang_word import NormalizeSlangWord
from remove_stopword import RemoveStopWord
from sklearn.feature_extraction.text import TfidfVectorizer

def fetch_reviews():
    df = pd.read_csv('keluhan.csv')
    return df

def preprocessing(reviews_df):

    """ Inisiasi untuk class normalisasi kalimat """
    usenorm = normalize()

    """ Inisiasi untuk class normalisasi kata slang """
    slangnorm = NormalizeSlangWord()

    """ Inisiasi untuk class remove stop word """
    stopwordnorm = RemoveStopWord()

    for index in range(len(reviews_df.index)):

        # print(index, reviews_df.iloc[index]['COMMENT'])

        """ Pertama, normalisasi menghilangkan (ENTER) pada kalimat """
        reviews_df.at[index, 'Keluhan'] = usenorm.enterNormalize(reviews_df.iloc[index]['Keluhan'])

        """ Kedua, normalisasi merubah kalimat menjadi huruf kecil semua """
        reviews_df.at[index, 'Keluhan'] = usenorm.lowerNormalize(reviews_df.iloc[index]['Keluhan'])
        """ Ketiga, normalisasi merubah kalimat yang menggunakan character berlebihan misal Yahhhh menjadi Yah """
        reviews_df.at[index, 'Keluhan'] = usenorm.repeatcharNormalize(reviews_df.iloc[index]['Keluhan'])

        """ Ketiga, normalisasi menghapus tanda baca """
        reviews_df.at[index, 'Keluhan'] = usenorm.spacecharNormalize(reviews_df.iloc[index]['Keluhan'])

        """ Keempat, normalisasi menghapus tanda elipsis """
        reviews_df.at[index, 'Keluhan'] = usenorm.ellipsisNormalize(reviews_df.iloc[index]['Keluhan'])

        """ Kelima, normalisasi kata slang misalnya aq menjadi aku (masih belum lengkap) """
        reviews_df.at[index, 'Keluhan'] = slangnorm.slang_word_normalization(reviews_df.iloc[index]['Keluhan'])

        """ Keenam, menghapus stopword dalam kalimat """
        reviews_df.at[index, 'Keluhan'] = stopwordnorm.remove_stop_word(reviews_df.iloc[index]['Keluhan'])

        print(index, reviews_df.iloc[index]['Keluhan'])

    return reviews_df

def makeTFIdf(preprocessed_reviews_df):

    """ Inisiasi untuk class yang akan digunakan untuk membuat TF-IDF """
    tfidf = TfidfVectorizer(sublinear_tf=False, min_df=2, norm='l2', analyzer='word', encoding='latin-1', ngram_range=(1, 2),
                            stop_words=None)


    """ Merubah isi dari setiap dokumen yang ada di kolom COMMENT menjadi TF-IDF Vector """
    features = tfidf.fit_transform(preprocessed_reviews_df.Keluhan).toarray()
    print(features)
    features_name = tfidf.vocabulary_
    # print(len(features_name))
    # features_name1 = tfidf.get_feature_names()
    # print(len(features_name1))
    # for f in features_name1:
    #     print(f)

    # """ Variabel untuk labels dari tiap dokumen """
    # labels = preprocessed_reviews_df.SENTIMEN_ID

    return features


#end of tfidf numpy array

def kmeanscluster(fitur):
    centroid=((fitur[20],fitur[100]))
    km= kmeans(fitur,centroid)
    print(km)


def main():
    keluhan = fetch_reviews()
    preprocessed_keluhan = preprocessing(keluhan)
    tf_idf = makeTFIdf(preprocessed_keluhan)
    kmeanscluster(tf_idf)


if __name__ == '__main__':
    main()
