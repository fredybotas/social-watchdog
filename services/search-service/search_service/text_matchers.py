import spacy
import math
from libcore.types import Watchable


class Matcher:
    def __init__(self) -> None:
        self.nlp = spacy.load("en_core_web_sm")

    def match(self, watchable: Watchable, doc_str: str) -> bool:
        raise NotImplementedError()


class StrictMatcher(Matcher):
    def match(self, watchable: Watchable, doc_str: str) -> bool:
        matcher = spacy.matcher.Matcher(self.nlp.vocab)
        matcher.add(
            "Matcher",
            [[{"LOWER": token} for token in watchable.watch.lower().split(" ")]],
        )
        doc = self.nlp(doc_str)
        return len(matcher(doc)) > 0


class DefaultMatcher(Matcher):
    def match(self, watchable: Watchable, doc_str: str) -> bool:
        matches_count = 0
        tokens_to_match = watchable.watch.lower().split(" ")
        threshold = math.ceil(len(tokens_to_match) / 2)
        for token in tokens_to_match:
            matcher = spacy.matcher.Matcher(self.nlp.vocab)
            matcher.add(
                "Matcher",
                [[{"LOWER": token}]],
            )
            doc = self.nlp(doc_str)
            matches_count += 1 if len(matcher(doc)) > 0 else 0
        return matches_count >= threshold
