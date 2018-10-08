import pytest
# from types import ModuleType,
# import inspect


StationId = 1


@pytest.fixture(scope="module")
def esp3k5():
    """ import file """
    import esp3k5
    return esp3k5.Esp3k5(StationId)


def test_generate_dummy_data(esp3k5):
    """ 테스트 파일이 import 되었는지 확인 """
    print(type(esp3k5))
    assert esp3k5 != None
    # assert pytest.Module.classnamefilter(esp3k5, "esp3k5")


def test_unittest2():
    """ 테스트 케이스 검사 """
    assert 1 == 1


def test_unittest3():
    assert 1 == 1
