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
[found_words] = googlesheet.get_columns('Behave!B5:B')

input_words = """
    unorthodox
    Irgun,
    Zionist
    extortion,
    captive
    score
    wreak havoc
"""

input_words = str_to_list(input_words)
print("input_words:", input_words)

new_words = ", ".join([w for w in input_words if w not in found_words])
print("new_words:", new_words)

if new_words:
    searched_words = crew.search_words(new_words)

    values = [[word['word'], word['meaning_eng'], word['meaning_native']] for word in searched_words]
    googlesheet.append_data('Behave!B4', values)