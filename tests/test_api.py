import json
import pytest

from mock import patch, Mock

from ds import *


@patch('ds.api.urllib.request.urlopen')
def test_login_success(mock_urlopen):
    mock_urlopen.return_value.read.return_value = json.dumps({'data': {'sid': 'w65edxZ6uuIx.1560MPN622801'}, 'success': True})
    auth_api = AuthApi("192.168.1.250", 5000)
    auth_api.login("user", "blabla")
    assert "method=login" in mock_urlopen.call_args[0][0]
    assert "account=user" in mock_urlopen.call_args[0][0]
    assert "passwd=blabla" in mock_urlopen.call_args[0][0]


@patch('ds.api.urllib.request.urlopen')
def test_login_fail(mock_urlopen):
    with pytest.raises(LoginFailed):
        mock_urlopen.return_value.read.return_value = json.dumps({'success': False})
        auth_api = AuthApi("192.168.1.250", 5000)
        auth_api.login("user", "blabla")


@patch('ds.api.urllib.request.urlopen')
def test_logout_success(mock_urlopen):
    mock_urlopen.return_value.read.return_value = json.dumps({'success': True})
    auth_api = AuthApi("192.168.1.250", 5000)
    assert auth_api.logout()
    assert "method=logout" in mock_urlopen.call_args[0][0]


@patch('ds.api.urllib.request.urlopen')
def test_logout_fail(mock_urlopen):
    mock_urlopen.return_value.read.return_value = json.dumps({'success': False, 'error': 400})
    auth_api = AuthApi("192.168.1.250", 5000)
    assert not auth_api.logout()


@patch('ds.api.urllib.request.urlopen')
def test_logout_throws(mock_urlopen):
    with pytest.raises(LogoutFailed):
        mock_urlopen.return_value.read.return_value = json.dumps({})
        auth_api = AuthApi("192.168.1.250", 5000)
        assert not auth_api.logout()
