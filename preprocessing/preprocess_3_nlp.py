import string
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

from preprocessing.preprocess_2_features import *


# New Function for preprocessing text
def preprocess_text(sentence):
    """
    Function to clean description text, tokenize and lemmatize words
    """

    # List of extra stopwords we decided do not help create new genres
    extended_stop_words = ['able','access','across','also','always','another','away',
                        'back','become','best','better','big','box','bring','certain',
                        'clear','close','come','console','content','could','course','digital',
                        'dont','one','two','three','four','five','six','seven','eight','nine',
                        'ten','hundred','thousand','either','enjoy','enough','even','exclusive',
                        'extra','feature','franchise','full','fully','fun','game','gameplay',
                        'genre','get','give','go','good','great','great','greatest','happen',
                        'however','huge','ii','improve','include','increase','inside',
                        'interactive','introduce','instead','involve','know','large','last',
                        'later','launch','lead','let','level','like','little','look','long',
                        'main','may','meet','might','mix','modern','mode','much','must','nan',
                        'name','new','next','need','number','nintendo','official','offer',
                        'object','option','order','original','originally','others','part','pc',
                        'perfect','platform','play','playable','player','playstation','plus',
                        'possible','port','prepare','previous','progress','project','publish',
                        'put','reach','ready','remain','return','screen','scroll','second',
                        'first','third','see','sega','sequel','series','set','several','show',
                        'side','similar','since','small','something','sound','special','start',
                        'stat','state','stay','still','studio','super','take','switch','tell',
                        'test','th','though','throughout','title','together','top','try',
                        'ultimate','unique','update','upon','us','use','version','via','wait',
                        'want','wii','within','without','would','xbox','youll','youre','youve']

    ## define stopwords
    stop_words = stopwords.words('english')
    stop_words.extend(extended_stop_words)

    # Basic cleaning
    sentence = sentence.strip() ## remove whitespaces
    sentence = sentence.lower() ## lowercase
    sentence = ''.join(char for char in sentence if not char.isdigit()) ## remove numbers

    # Advanced cleaning

    # remove punctuation
    for punctuation in string.punctuation:
        sentence = sentence.replace(punctuation, '')

    # tokenize
    tokenized_sentence = word_tokenize(sentence)

    # remove stopwords
    tokenized_sentence_cleaned = [
        w for w in tokenized_sentence if not w in stop_words]


    noun_lemmatized = [
        WordNetLemmatizer().lemmatize(word, pos = "n")
        for word in tokenized_sentence_cleaned]

    lemmatized = [
        WordNetLemmatizer().lemmatize(word, pos = "v")
        for word in noun_lemmatized]

    cleaned_sentence = ' '.join(word for word in lemmatized)

    return cleaned_sentence


# Old function for preprocessing text
def preprocessing(sentence):
    """
    This is the old function, try ise preprocess_text
    """

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

def vectorize_text(data, column, min_df=0.02):
    """
    Vectorizes text for NLP topic creation
    Returns Vectorizer and vectorized descriptions
    """

    vectorizer = TfidfVectorizer(min_df=min_df)

    # Fit transform on clean text
    vectorized_descriptions = vectorizer.fit_transform(data[column])

    # Create dataframe of vectorized descriptions
    vectorized_descriptions = pd.DataFrame(
        vectorized_descriptions.toarray(),
        columns = vectorizer.get_feature_names_out())

    return vectorizer, vectorized_descriptions

def fit_lda(vectorized_sentence, num_topics):
    lda = LatentDirichletAllocation(n_components=num_topics, max_iter = 50, learning_method='online')
    lda.fit(vectorized_sentence)
    return lda

def nlp_topic(x, fitted_vectorizer, fitted_lda):
    """
    Determines which topic the description belongs to
    Should be used to add topic to a column in the training data
    """

    vectorised_x = fitted_vectorizer.transform(pd.Series(x))
    vec_x_array = fitted_lda.transform(vectorised_x)
    vec_list = vec_x_array[0].tolist()

    return vec_list.index(max(vec_list))


def print_topics(model, vectorizer):
    """
    Allows you to print topics to review performance
    """
    for idx, topic in enumerate(model.components_):
        print("Topic %d:" % (idx))
        print([(vectorizer.get_feature_names_out()[i], topic[i])
                        for i in topic.argsort()[:-10 - 1:-1]])



def create_nlp_topics_and_append(data, column_to_clean, origin_column, lda_components=30, total_features_to_make=None):
    """
    Requires preprocessed data
    Creates the NLP topics and adds them to the dataframe
    Returns a concatenated df with the new data
    """

    # Create dataframe of vectorized descriptions
    vectorizer, vectorized_descriptions = vectorize_text(data, column_to_clean)

    # Instantiate LDA model
    lda_model = LatentDirichletAllocation(n_components=lda_components, max_iter = 20, learning_method='online')

    # Fit the LDA on the vectorized documents
    lda_model.fit(vectorized_descriptions)

    # Creating topics column, and encoding into dara
    data['topic'] = data[column_to_clean].apply(nlp_topic, vectorizer = vectorizer, lda_model = lda_model)
    topics = pd.get_dummies(data['topic'])

    if total_features_to_make == None:
        pass
    else:
        topics = keep_x_OHE_columns(topics, total_features_to_make)


    # Creating final df to be split into training data
    concatenated_df = data.drop(columns=[origin_column, column_to_clean, 'topic'], axis=1)
    final_df = pd.concat((concatenated_df, topics), axis=1)

    return final_df

def topics_from_nlp(data, column_with_text, number_of_topics_to_keep=None, lda_components=30):
    """
    Preprocesses the data and creates NLP topics
    """

    data['clean_text'] = data[column_with_text].apply(preprocess_text)
    topics_nlp_df = create_nlp_topics_and_append(data, column_to_clean='clean_text',
                                                 origin_column=column_with_text, total_features_to_make=number_of_topics_to_keep,
                                                 lda_components=lda_components)

    return topics_nlp_df
