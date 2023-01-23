import trafilatura
import re
import pprint
from  openpyxl import load_workbook
import selenium

def get_text(url):
    """returns the text found in a given url"""
    source = trafilatura.fetch_url(url)
    text = trafilatura.extract(source)
    return text

# some function definitions for the split_into_sentences() function.
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
digits = "([0-9])"

search_items = ['sugar','sugary', 'sweets', 'sweetened', 'sweetener','soda','sucrose','fructose', 'glycemic index', 'glycemic load', 'processed', 'refined', 'fiber', 'whole grain', 'whole-grain', 
'fruit', 'vegetable', 'saturated fat', 'unsaturated fat', 'low-fat', 'low fat', 'red meat', 'processed meat', 'obese', 'obesity', 'weight', 'abdominal fat', 'belly fat', 'body mass index', 'bmi', 
'adiposity', 'exercis', 'activ', 'sedentary', 'hypertension', 'blood pressure', 'blood pressure', 'dyslipidemia',  'triglyceride', 'cholesterol', 'ldl', 'hdl', 'age', 'old', 'history', 'genetic', 'ethnicit']


# Split the input text into sentences.
def split_into_sentences(text):
    """Splits a text into sentences. Returns a list containing those sentences."""
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    if "..." in text: text = text.replace("...","<prd><prd><prd>")
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

# Custom dictionary class for having multiple values for one key.
class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)


text = get_text('https://www.uptodate.com/contents/type-2-diabetes-overview-beyond-the-basics')

sentences = split_into_sentences(text)

lower_case_sentences = []
for sentence in sentences:
    lower_case_sentences.append(sentence.lower())

search_results = {}

for sentence in lower_case_sentences:
    for search_item in search_items:
        if search_item in sentence:
            search_results.setdefault(search_item, []).append([True, sentence])

# print out the results in a readbale format.
pprint.pprint(search_results)

