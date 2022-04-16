
import glove.util as util
import pytest
import pytest_mock
from uuid import UUID


@pytest.fixture()
def fake_current_ids():
    return ["a1a1a1a1", "b2b2b2b2", "c3c3c3c3"]


@pytest.fixture()
def fake_get_subject_ids(mocker, fake_current_ids):
    mocker.patch(
        "glove.util.get_subject_ids",
        return_value=fake_current_ids,
    )

@pytest.fixture()
def deterministic_uuid4(mocker):
    mocker.patch(
        "glove.util.uuid4",
        side_effect=[
            UUID("00000000-0000-0000-0000-0000a1a1a1a1"),
            UUID("00000000-0000-0000-0000-0000b2b2b2b2"),
            UUID("00000000-0000-0000-0000-0000c3c3c3c3"),
        ]
    )


def test_not_same_id_twice(fake_get_subject_ids):
    assert util.generate_subject_id() != util.generate_subject_id()


def test_avoid_collision(fake_get_subject_ids, fake_current_ids):
    _id = util.generate_subject_id()
    assert _id not in fake_current_ids
