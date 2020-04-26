'''
FILE_WORKER is a class provide all functionalities to process an uploaded file
'''
# import regex library 
import re 
# use nltk library to process stem and stop word
import nltk
import ssl

#Dowload nltk data
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download("stopwords")
nltk.download("wordnet")

#import nltk lemmatizer
from nltk.stem import WordNetLemmatizer  
# import NLTK stopwords
from nltk.corpus import stopwords 


class FileWorker:
    lemmatizer = WordNetLemmatizer()
    stop_word_list = set(stopwords.words('english'))
    '''
        each file_worker contains:
        @param original_text: the content before processing
        @param stop_word: 1 if enable, 0 otherwise
    '''
    def __init__(self, original_text, stop_word):
        self.original_text = original_text
        self.stop_word = stop_word

    def get_top_25_words(self):
        '''
        return a list contains top 10 words and their frequencies
        '''
        word_frequency = dict()  # map word -> frequency

        # extract words from original_text 
        word_list = re.findall(r'\w+', self.original_text)
        # convert words to lower case
        word_list = list(map(lambda w: w.lower(), word_list))
        # convert to stem form
        word_list = self.convert_to_stem(word_list)
        
        if self.stop_word == 1:
            word_list = self.exclude_stop_word(word_list)
        
        # count word frequency
        for word in word_list:
            word_frequency[word] = word_frequency.get(word, 0) + 1
        
        # sort the list of word by their frequency, break tie by the string word
        sorted_word_list = list(word_frequency.items())
        sorted_word_list.sort(key=lambda item: (item[1], item[0]), reverse=True)

        top_25_words = sorted_word_list[:25]
        return top_25_words

    def convert_to_stem(self, word_list):
        '''
        converting all “equivalent forms” of listed verbs to their corresponding “stem.”
        '''
        for i in range(len(word_list)):
            word_list[i] = self.lemmatizer.lemmatize(word_list[i], pos="v")
        return word_list
    
    def exclude_stop_word(self, word_list):
        '''
        return a new word list which does not contains stopword
        '''
        return [word for word in word_list if word not in self.stop_word_list]



