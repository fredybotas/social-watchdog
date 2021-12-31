from dataclasses import dataclass


@dataclass
class WatchableNotification:
    watchable_id: str
    title: str
    url: str
