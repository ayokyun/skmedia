import pytest


@pytest.fixture(scope="module")
def dummy():
    import esp3k5_dummy
    return esp3k5_dummy


def test_import_dummy_check(dummy):
    # print(dummy.__name__)
    assert dummy.__name__ == "esp3k5_dummy"
