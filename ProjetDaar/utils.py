#from pdfminer.high_level import extract_text
#import docx2txt
import nltk

import re
import subprocess

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')









def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)


def extract_text_from_docx(docx_path):
    txt = docx2txt.process(docx_path)
    if txt:
        return txt.replace('\t', ' ')
    return None

def extract(doc):
    if "pdf" in doc:
       return extract_text_from_pdf(doc)
    else:
        return extract_text_from_docx(doc)






def extract_names(txt):
    person_names = []
    i=0
    for sent in nltk.sent_tokenize(txt,language="french"):
        if(i==0):
            person_names=re.findall("[A-Z]+\s[A-Z]+", sent)
            if len(person_names)==1:
                return person_names
            else:
                i+=1
        #print(sent)
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent,language="french"))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                person_names.append(
                    ' '.join(chunk_leave[0] for chunk_leave in chunk.leaves())
                )

    return person_names

def extract_phone_number(resume_text):
    PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')

    phone = re.findall(PHONE_REG, resume_text)

    if phone:
        number = ''.join(phone[0])

        if resume_text.find(number) >= 0 and len(number) < 16:
            return number
    return None


def extract_emails(resume_text):
    EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
    return re.findall(EMAIL_REG, resume_text)



def text_json(text):
    dict={"name":extract_names(text)[0],"Telephone":extract_phone_number(text),"Email":extract_emails(text)[0],"content":text}
    return json.dumps(dict)