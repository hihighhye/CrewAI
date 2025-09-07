from pydantic import BaseModel
from typing import List
from crewai import Crew, Agent, Task
import json


class Phrase(BaseModel):
    english: str
    native: str

class TranslatorCrew:
    def __init__(self, native_lang):   
        self.native_lang = native_lang

        self.agent = Agent(
            role="Translator",
            goal="Translate given English sentence or phrase in given native language.",
            backstory="""
                You are translating English sentences or phrases for people studying English.
                Return the given English sentence and its translation in native language.
            """,
            verbose=True,
            allow_delegation=False,
        )

        self.task = Task(
            description="Translate given English sentence or phrase in {native_lang}: {phrase}",
            agent=self.agent,
            expected_output="An Phrase Object",
            output_json=Phrase,
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

    def translate(self, phrase):
        result = self.crew.kickoff(
            inputs=dict(
                native_lang=self.native_lang,
                phrase=phrase,
            )
        )
        crewai_response = json.loads(result)
        return crewai_response