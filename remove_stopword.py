from nltk import ngrams
from nltk.tokenize import word_tokenize

stopword = ["dan", "dengan", "serta", "atau", "tetapi", "namun", "sedangkan", "sebaliknya", "melainkan", "hanya",
            "bahkan", "malah", "lagipula", "apalagi", "jangankan", "kecuali", "hanya", "lalu", "kemudian", "selanjutnya",
            "yaitu", "yakni", "bahwa", "adalah", "ialah", "jadi", "sebab", "karena", "kalau", "jikalau", "jika", "bila",
            "apalagi", "asal", "agar", "supaya", "ketika", "sewaktu", "sebelum", "sesudah", "tatkala", "sampai", "hingga",
            "sehingga", "untuk", "guna", "seperti", "sebagai", "laksana"]

class RemoveStopWord():

    def get_ngrams(self, review, n):
        n_grams = ngrams(word_tokenize(review), n)
        return [' '.join(grams) for grams in n_grams]

    def tokenization(self, reviews):
        single_unigrams = self.get_ngrams(reviews, 1)
        return single_unigrams

    def remove_stop_word(self, unigrams):
        unigram  = self.tokenization(unigrams)
        #print(unigram)
        for index in range(len(unigram)):
            #print(unigram[index])
            if unigram[index] in stopword:
                unigram[index] = ""
        return " ".join(unigram)