from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import os
ser_path = os.path.join(os.getcwd(),'NLP/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz')
jar_path = os.path.join(os.getcwd(),'NLP/stanford-ner-2014-06-16/stanford-ner.jar')
st = StanfordNERTagger(ser_path,jar_path,encoding = 'utf-8')
def classify_text(text):
    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)
    propernouns_company = [word for word,pos in classified_text if pos =='ORGANIZATION'] #Puts all organizations
    if len(propernouns_company) < 1: #If there are no organizations
        propernouns = [word for word, pos, in classified_text if pos != 'O'] #Outputs all except non Pronouns
    else:
        propernouns = propernouns_company #If there are organizatiosn put those in
    non_delimited = "" #Converts delimiter to a | as opposed to a Comma to avoid messing with CSV values
    for i in propernouns: 
        non_delimited += i + "|"
    return non_delimited
