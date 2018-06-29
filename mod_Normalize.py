import string
import re
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
            'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

tanda_baca = ['.',',',';',':','-,','...','?','!','(',')','[',']','{','}','<','>','"','/','\'','#','-','@']
remove_charac = ['—','…']

class normalize():
    def enterNormalize(self, text):
        norm_enter = text.replace("\n", " ")
        return norm_enter

    def lowerNormalize(self, text):
        norm_lower = text.lower()
        return norm_lower

    def repeatcharNormalize(self, text):
        for i in range(len(tanda_baca)):
            karakter_long = 5
            while karakter_long>=2:
                karakter = tanda_baca[i]*karakter_long
                text = text.replace(karakter, tanda_baca[i])
                karakter_long -= 1

        for i in range(len(alphabet)):
            charac_long = 5
            while charac_long>=3:
                char = alphabet[i]*charac_long
                text = text.replace(char, alphabet[i])
                charac_long -= 1
        return text

    def spacecharNormalize(self, text):
        table = str.maketrans({key: " " for key in string.punctuation})
        return text.translate(table)

    def ellipsisNormalize(self, text):
        text = text.replace('…',' …')
        text = text.replace(' …',' ')
        return text