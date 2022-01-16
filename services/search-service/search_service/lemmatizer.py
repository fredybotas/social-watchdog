import spacy
from typing import List


class Lemmatizer:
    def __init__(self) -> None:
        self.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

    def lemmatize(self, doc_str: str) -> List[str]:
        return [token.lemma_ for token in self.nlp(doc_str)]
