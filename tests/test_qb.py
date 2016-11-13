from ds.qb import QueryBuilder

def helper_get_login_builder():
    builder = QueryBuilder()
    builder.host = "192.168.1.250"
    builder.port = 5000
    builder.cgi_path = "/webapi/auth.cgi"
    builder.api = "SYNO.API.Auth"
    builder.version = 2
    builder.method = "login"
    return builder


def test_build_query_with_one_param():
    login_url = '''http://192.168.1.250:5000/webapi/auth.cgi?api=SYNO.API.Auth&version=2&method=login&account=ABCD'''
    builder = helper_get_login_builder()
    builder.param["account"] = "ABCD"
    assert builder.build_get() == login_url


def test_build_query_with_multiple_params():
    login_url = '''http://192.168.1.250:5000/webapi/auth.cgi?api=SYNO.API.Auth&version=2&method=login&account=ABCD&password=aaaaa'''
    builder = helper_get_login_builder()
    builder.param["account"] = "ABCD"
    builder.param["password"] = "aaaaa"
    assert builder.build_get() == login_url


def test_build_query_with_params_and_sid():
    login_url = '''http://192.168.1.250:5000/webapi/auth.cgi?api=SYNO.API.Auth&version=2&method=login&account=ABCD&_sid=abcdef'''
    builder = helper_get_login_builder()
    builder.sid = "abcdef"
    builder.param["account"] = "ABCD"
    assert builder.build_get() == login_url


def test_build_post_query_with_one_param():
    login_url = '''http://192.168.1.250:5000/webapi/auth.cgi'''
    post_data = '''api=SYNO.API.Auth&version=2&method=login&account=ABCD'''
    builder = helper_get_login_builder()
    builder.param["account"] = "ABCD"
    assert builder.build_post() == (login_url, post_data)


def test_build_post_query_with_multiple_params():
    login_url = '''http://192.168.1.250:5000/webapi/auth.cgi'''
    post_data = '''api=SYNO.API.Auth&version=2&method=login&account=ABCD&password=aaaaa'''
    builder = helper_get_login_builder()
    builder.param["account"] = "ABCD"
    builder.param["password"] = "aaaaa"
    assert builder.build_post() == (login_url, post_data)


def test_build_query_with_params_and_sid():
    login_url = '''http://192.168.1.250:5000/webapi/auth.cgi'''
    post_data = '''api=SYNO.API.Auth&version=2&method=login&account=ABCD&_sid=abcdef'''
    builder = helper_get_login_builder()
    builder.sid = "abcdef"
    builder.param["account"] = "ABCD"
    assert builder.build_post() == (login_url, post_data)
