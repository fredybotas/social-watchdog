import spacy
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
            [[{"LEMMA": token.lemma_} for token in self.nlp(watchable.watch)]],
        )
        doc = self.nlp(doc_str)
        return len(matcher(doc)) > 0


class DefaultMatcher(Matcher):
    def match(self, watchable: Watchable, doc_str: str) -> bool:
        matches_count = 0
        watchable_doc = self.nlp(watchable.watch)
        threshold = len(watchable_doc)  # math.ceil(len(watchable_doc) / 2)
        for token in watchable_doc:
            matcher = spacy.matcher.Matcher(self.nlp.vocab)
            matcher.add(
                "Matcher",
                [[{"LEMMA": token.lemma_}]],
            )
            doc = self.nlp(doc_str)
            matches_count += 1 if len(matcher(doc)) > 0 else 0
        return matches_count >= threshold
