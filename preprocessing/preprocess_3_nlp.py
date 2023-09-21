import string
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation






vectorizer = TfidfVectorizer(min_df=0.02)
lda_model = LatentDirichletAllocation(n_components=10, max_iter = 50, learning_method='online',)

def preprocessing(sentence):
    extended_stop_words = ['able','access','across','also','always','another','away','back',
                       'become','best','better','big','box','bring','certain','clear',
                       'close','come','console','content','could','course','digital',
                       'dont','one','two','three','four','five','six','seven','eight',
                       'nine','ten','hundred','thousand','either','enjoy','enough','even',
                       'exclusive','extra','feature','franchise','full','fully','fun',
                       'game','gameplay','genre','get','give','go','good','great','great',
                       'greatest','happen','however','huge','ii','improve','include',
                       'increase','inside','interactive','introduce','instead','involve',
                       'large','last','later','launch','lead','let','level','like','little',
                       'look','main','meet','might','mix','modern','mode','must','name',
                       'new','next','need','number','nintendo','official','offer','object',
                       'option','order','original','originally','others','part','pc',
                       'perfect','platform','playable','player','playstation','plus',
                       'possible','port','prepare','previous','progress','project','put',
                       'reach','ready','remain','return','screen','scroll','second','first',
                       'third','see','sega','sequel','series','set','several','show','side',
                       'similar','since','small','something','sound','special','start',
                       'stat','state','stay','still','studio','super','take','switch',
                       'tell','test','th','though','throughout','title','together','try',
                       'ultimate','unique','update','upon','us','use','version','via','wait',
                       'want','wii','within','without','would','xbox','youll','youre','youve']


    # Basic cleaning
    sentence = sentence.strip() ## remove whitespaces
    sentence = sentence.lower() ## lowercase
    sentence = ''.join(char for char in sentence if not char.isdigit()) ## remove numbers

    # Advanced cleaning
    for punctuation in string.punctuation:
        sentence = sentence.replace(punctuation, '') ## remove punctuation

    tokenized_sentence = word_tokenize(sentence) ## tokenize
    stop_words = stopwords.words('english') ## define stopwords
    stop_words.extend(extended_stop_words)

    tokenized_sentence_cleaned = [ ## remove stopwords
        w for w in tokenized_sentence if not w in stop_words
    ]


    noun_lemmatized = [
        WordNetLemmatizer().lemmatize(word, pos = "n")
        for word in tokenized_sentence_cleaned
    ]
    lemmatized = [
        WordNetLemmatizer().lemmatize(word, pos = "v")
        for word in noun_lemmatized
    ]

    cleaned_sentence = ' '.join(word for word in lemmatized)

    return cleaned_sentence

def fit_vectorizer(processed_sentence):
    vectorizer = TfidfVectorizer(min_df=0.02)
    vectorizer.fit(processed_sentence)
    vectorized_sentence = vectorizer.transform(processed_sentence)
    return vectorizer, vectorized_sentence

def fit_lda(vectorized_sentence):
    lda = LatentDirichletAllocation(n_components=10, max_iter = 50, learning_method='online')
    lda.fit(vectorized_sentence)
    return lda

def nlp_topic(x, fitted_vectorizer, fitted_lda):
    vectorised_x = fitted_vectorizer.transform(pd.Series(x))
    vec_x_array = fitted_lda.transform(vectorised_x)
    vec_list = vec_x_array[0].tolist()
    return vec_list.index(max(vec_list))
