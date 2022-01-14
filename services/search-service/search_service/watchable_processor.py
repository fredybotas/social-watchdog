from libcore.types import Watchable, WatchableNotification
from typing import Optional
from datetime import datetime
from libcore.types import WatchableProcessorType
from .text_matchers import StrictMatcher, DefaultMatcher


class WatchableProcessor:
    # TODO: Refactor matchers to be more generic
    def __init__(self, strict_matcher: StrictMatcher, default_matcher: DefaultMatcher) -> None:
        self.strict_matcher = strict_matcher
        self.default_matcher = default_matcher

    def get_notification_if_appropriate(
        self, watchable: Watchable, submission: any
    ) -> Optional[WatchableNotification]:
        submission_datetime = datetime.utcfromtimestamp(submission.created_utc)
        if submission_datetime < watchable.created_at:
            return None
        if not self._should_deliver_submission(watchable, submission.title + " " + submission.selftext):
            return None
        return WatchableNotification(
            watchable_id=watchable.id,
            title=submission.title,
            url=submission.shortlink,
        )

    def _should_deliver_submission(self, watchable: Watchable, text_to_match: str):
        # TODO: Refactor and do tests
        match watchable.processor_type:
            case WatchableProcessorType.DEFAULT:
                return self.default_matcher.match(watchable, text_to_match)
            case WatchableProcessorType.STRICT:
                return self.strict_matcher.match(watchable, text_to_match)
