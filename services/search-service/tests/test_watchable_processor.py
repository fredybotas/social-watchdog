from libcore.types.watchable_notification import WatchableNotification
from search_service import WatchableProcessor
from libcore.types import Watchable, WatchableProcessorType
import pytest
from datetime import timedelta, datetime
from unittest.mock import MagicMock


@pytest.fixture
def watchable_stub():
    return Watchable(
        id="aaa",
        provider_user_id="provid_u_id",
        effective_chat_id="eff_chat_id",
        subreddit="all",
        watch="Heart rate zones",
        processor_type=WatchableProcessorType.STRICT,
        created_at=datetime.utcnow(),
    )


@pytest.fixture
def submission_stub(request):
    fake = MagicMock()
    fake.submission_id = "aaa"
    fake.created_utc = request.param
    fake.title = "TestTitle"
    fake.selftext = "TestText"
    fake.shortlink = "link"
    return fake


@pytest.fixture
def matcher_false_mock():
    mock = MagicMock()
    mock.match = MagicMock(return_value=False)
    return mock


@pytest.fixture
def matcher_true_mock():
    mock = MagicMock()
    mock.match = MagicMock(return_value=True)
    return mock


@pytest.mark.parametrize(
    "submission_stub",
    [(datetime.utcnow() - timedelta(days=1)).timestamp()],
    indirect=True,
)
def test_old_submission_should_not_be_processed(
    watchable_stub, submission_stub, matcher_false_mock
):
    sut = WatchableProcessor(
        default_matcher=matcher_false_mock, strict_matcher=matcher_false_mock
    )
    notification = sut.get_notification_if_appropriate(watchable_stub, submission_stub)
    assert notification is None


@pytest.mark.parametrize(
    "submission_stub",
    [(datetime.utcnow() + timedelta(days=1)).timestamp()],
    indirect=True,
)
def test_newer_submission_should_be_processed(
    watchable_stub, submission_stub, matcher_true_mock
):
    sut = WatchableProcessor(
        default_matcher=matcher_true_mock, strict_matcher=matcher_true_mock
    )
    notification = sut.get_notification_if_appropriate(watchable_stub, submission_stub)
    assert notification is not None


@pytest.mark.parametrize(
    "submission_stub",
    [(datetime.utcnow() + timedelta(days=1)).timestamp()],
    indirect=True,
)
def test_newer_submission_should_call_matcher(
    watchable_stub, submission_stub, matcher_false_mock
):
    sut = WatchableProcessor(
        default_matcher=matcher_false_mock, strict_matcher=matcher_false_mock
    )
    _ = sut.get_notification_if_appropriate(watchable_stub, submission_stub)
    matcher_false_mock.match.assert_called_once_with(
        watchable_stub, "TestTitle TestText"
    )


@pytest.mark.parametrize(
    "submission_stub",
    [(datetime.utcnow() + timedelta(days=1)).timestamp()],
    indirect=True,
)
def test_newer_submission_should_return_none_on_matcher(
    watchable_stub, submission_stub, matcher_false_mock
):
    sut = WatchableProcessor(
        default_matcher=matcher_false_mock, strict_matcher=matcher_false_mock
    )
    notification = sut.get_notification_if_appropriate(watchable_stub, submission_stub)
    assert not notification


@pytest.mark.parametrize(
    "submission_stub",
    [(datetime.utcnow() + timedelta(days=1)).timestamp()],
    indirect=True,
)
def test_newer_submission_matched(watchable_stub, submission_stub, matcher_true_mock):
    sut = WatchableProcessor(
        default_matcher=matcher_true_mock, strict_matcher=matcher_true_mock
    )
    notification = sut.get_notification_if_appropriate(watchable_stub, submission_stub)
    assert notification.title == "TestTitle"
    assert notification.url == "link"
    assert notification.watchable_id == "aaa"
