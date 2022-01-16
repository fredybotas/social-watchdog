from dataclasses import dataclass


@dataclass
class Submission:
    id: str
    url: str
    created_timestamp: int
    title: str
    text: str
