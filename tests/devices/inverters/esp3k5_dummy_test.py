import pytest


@pytest.fixture(scope="module")
def dummy():
    from devices.inverters import esp3k5_dummy
    return esp3k5_dummy


def test_import_dummy_check(dummy):
    # print(dummy.__name__)
    assert "esp3k5_dummy" in dummy.__name__
