# -*- coding: utf-8 -*-
# coding: utf-8

from nltk.stem import PorterStemmer
from nltk import ngrams
from nltk.tokenize import word_tokenize

slang_BOW = {}
keys = ["ama", "ga", "mulu", "gk", "tp", "gak", "engga", "g", "bs", "yg", "lbh",
        "krn", "byk", "karna", "emang", "skrg", "utk", "ancur", "ampe", "bgt", "ok", "blm",
        "jg", "brp", "tdk", "krena", "pke", "uda", "gitu", "pas", "lg", "tlg", "dlm", "sdh",
        "ndak", "dr", "aja", "tetep", "cuman", "gmn", "gw", "gue", "blg", "cm", "knp", "hrs", "klo",
        "skr", "pake", "bnyk", "bangetz", "gokil", "lgsg", "jgn", "kl", "jng", "trims", "pkai",
        "dpake", "lgsung", "tob", "neh", "trs", "sm", "demen", "masi", "bete", "jancok", "kl", "koq",
        "gembel", "suwun", "bwt", "kagak", "asik", "sblm", "bbrp", "smpe", "msh", "dpt", "bgs",
        "mesen", "nyari", "tlong", "lmyn", "bener", "byr", "tlp", "cpt", "kasi", "guoblok"]

values = ["sama", "tidak", "melulu", "tidak", "tapi", "tidak", "tidak", "tidak", "bisa", "yang", "lebih",
          "karena", "banyak", "karena", "memang", "sekarang", "untuk", "hancur", "sampai", "sekali", "oke", "belum",
          "juga", "berapa", "tidak", "karena", "pakai", "sudah", "gitu", "saat", "lagi", "tolong", "dalam", "sudah",
          "tidak", "dari", "saja", "tetap", "cuma", "gimana", "aku", "aku", "bilang", "cuma", "kenapa", "harus", "kalau",
          "sekarang", "pakai", "banyak", "sekali", "gila", "langsung", "jangan", "kl", "jangan", "terima kasih", "pakai",
          "dipakai", "langsung", "bagus", "nih", "terus", "sama", "suka", "masih", "sedih", "jelek", "kalau", "kok",
          "melarat", "terima kasih", "buat", "tidak", "asyik", "sebelum", "beberapa", "sampai", "masih", "dapat", "bagus",
          "pesan", "cari", "tolong", "lumayan", "benar", "bayar", "telpon", "cepat", "kasih", "bodoh"]
for index in range(len(keys)):
    slang_BOW[keys[index]] = values[index]

class NormalizeSlangWord():

    def get_ngrams(self, review, n):
        n_grams = ngrams(word_tokenize(review), n)
        return [' '.join(grams) for grams in n_grams]

    def tokenization(self, reviews):
        single_unigrams = self.get_ngrams(reviews, 1)
        return single_unigrams

    def slang_word_normalization(self, unigrams):
        unigram  = self.tokenization(unigrams)
        #print(unigram)
        for index in range(len(unigram)):
            #print(unigram[index])
            if unigram[index] in slang_BOW.keys():
                unigram[index] = slang_BOW[unigram[index]]
        return " ".join(unigram)