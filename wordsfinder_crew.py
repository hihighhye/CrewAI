from pydantic import BaseModel
from typing import List
from crewai import Crew, Agent, Task
import json


class Words(BaseModel):
        word: str
        pronunciation: str
        meaning_eng: str
        meaning_native: str

class WordList(BaseModel):
    words: List[Words]

class WordsFinderCrew:
    def __init__(self, native_lang):   
        self.native_lang = native_lang

        self.agent = Agent(
            role="Searching the meaning of words",
            goal="Find the meaning of given words in English and given native language.",
            backstory="""
                You are finding the meaning of English words in dictionaries for people studying English.
                These are essential elements that you should find.
                - word :
                    The given word. Use lowercase letters.
                - pronunciation : 
                    The pronunciation of the words
                - meaning(English) : 
                    The meaning of given words in English dictionary
                    Each meaning should be provided with its grammatical category information(a./ad./v./n....).
                - meaning(native) :
                    What the words mean in native language
                    (in other words, how the words can translate in native language)

                e.g.
                    - word : succinct
                    - pronunciation : /səkˈsɪŋkt/
                    - meaning(English) : a. (especially of something written or spoken) briefly and clearly expressed
                    - meaing(native) : 간결한

                The words will be given as a comma-separated list.
            """,
            verbose=True,
            allow_delegation=False,
        )

        self.task = Task(
            description="Find the meaning of given words in English and {native_lang} by searching dictionaries: {word_list}",
            agent=self.agent,
            expected_output="A List of Words Object",
            output_json=WordList,
        )

        self.crew = Crew(
            tasks=[
                self.task,
            ],
            agents=[
                self.agent,
            ],
            verbose=2,
            cache=True,
        )

    def search_words(self, word_list):
        result = self.crew.kickoff(
            inputs=dict(
                native_lang=self.native_lang,
                word_list=word_list,
            )
        )
        crewai_response = json.loads(result)
        return crewai_response['words']