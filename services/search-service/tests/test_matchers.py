from libcore.types import Watchable, WatchableProcessorType
from search_service import DefaultMatcher, StrictMatcher
import pytest
from datetime import datetime


@pytest.fixture
def watchable_stub():
    return Watchable(
        id="aaa",
        provider_user_id="provid_u_id",
        effective_chat_id="eff_chat_id",
        subreddit="all",
        watch="Heart rate zones",
        processor_type=WatchableProcessorType.DEFAULT,
        created_at=datetime.utcnow(),
    )


def test_strict_matcher_should_match(watchable_stub):
    sut = StrictMatcher()
    assert sut.match(watchable_stub, "Heart rate zones test text.")


def test_strict_matcher_should_not_match(watchable_stub):
    sut = StrictMatcher()
    assert not sut.match(watchable_stub, "Heart zones test text.")


def test_default_matcher_should_match(watchable_stub):
    sut = DefaultMatcher()
    assert sut.match(watchable_stub, "Heart :D zones test text")


def test_default_matcher_should_not_match(watchable_stub):
    sut = DefaultMatcher()
    assert not sut.match(watchable_stub, "Heart test text.")
