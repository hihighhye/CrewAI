import openai
import os
from dotenv import load_dotenv
import re
from wordsfinder_crew import WordsFinderCrew
from googlesheets_utils import GooglesheetUtils


def str_to_list(words):
    words = words.strip()
    words = re.sub(r'[ \t\r\f\v]{2,}', ' ', words)
    word_list = re.split(r'[,\n]+', words)
    word_list = [wd.strip() for wd in word_list]
    return word_list

load_dotenv()
os.environ['OPENAI_MODEL_NAME'] = 'gpt-4o-mini'

crew = WordsFinderCrew(native_lang="Korean")

googlesheet = GooglesheetUtils(spreadsheet_id='1hFNuCdmySJodQM5qsR5FJ6pkPLQc5DbXwP7h74pwTs8')
[found_words] = googlesheet.get_data('Behave!D5:D', majorDimension='COLUMNS')

input_words = """
    rudimentary
    pituitary
    henceforth
    suffice
    satiation
    downright
    norm
    violation
    besting
    specter
    demoted
    gloating
    resentment
    invidiousness
    paycheck
    habituate
    discrepancy
    bummer
    namely
    dwarf
    quaint
    beehive
    privation
    spasm
    deluge
    contingency
    monetary
    afterthought
    sated
    rundown
    inundate
    impending
    chute
    anthropology
    intermittent
    blip
    astronomical
    pickling
    propensity
    calibrated
    agitating
"""

cat1 = "Behave"
cat2 = "Chapter 2"

input_words = str_to_list(input_words)
print("input_words:", input_words)

new_words = [w for w in input_words if w not in found_words]
print("new_words:", new_words)

result = []
for word in new_words:
    try:
        searched_word = crew.search_words(word)
        result.append([cat1, cat2, searched_word['word'], searched_word['pronunciation'], searched_word['meaning_eng'], searched_word['meaning_native']])
    except Exception:
        result.append([cat1, cat2, word, '',"Cannot find the meaning.", ''])

googlesheet.append_data('Behave!B4', result)