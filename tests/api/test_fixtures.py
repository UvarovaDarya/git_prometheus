import pytest


@pytest.mark.check
def test_change_name(user):
    assert user.name == 'Daria'


@pytest.mark.check
def test_change_second_name(user):
    assert user.second_name == 'Uvarova'