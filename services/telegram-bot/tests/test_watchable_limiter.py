from telegram_bot import WatchableLimiter
from unittest.mock import MagicMock
import pytest


@pytest.fixture
def watchable_repo_mock():
    mock = MagicMock()
    mock.get_all = MagicMock(return_value=["a", "b", "c"])
    return mock


def test_limiter_calls_repo(watchable_repo_mock):
    sut = WatchableLimiter(watchable_repo_mock)
    test_user_id = "USER_ID"

    sut.should_allow_create(test_user_id)

    watchable_repo_mock.get_all.assert_called_once_with(
        {"provider_user_id": test_user_id}
    )


def test_limiter_allow_under_limit(watchable_repo_mock):
    sut = WatchableLimiter(watchable_repo_mock, limit=4)
    test_user_id = "USER_ID"

    assert sut.should_allow_create(test_user_id)


def test_limiter_allow_limit_exceeded(watchable_repo_mock):
    sut = WatchableLimiter(watchable_repo_mock, limit=3)
    test_user_id = "USER_ID"

    assert not sut.should_allow_create(test_user_id)
