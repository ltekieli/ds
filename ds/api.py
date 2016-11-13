import json
import random
import string
import urllib2
from qb import QueryBuilder


def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get(url):
    api_response = urllib2.urlopen(url).read()
    return json.loads(api_response)


def post(url, request):
    req = urllib2.Request(url, request)
    api_response = urllib2.urlopen(req).read()
    return json.loads(api_response)


class LoginFailed(Exception):
    pass


class LogoutFailed(Exception):
    pass


class FetchFailed(Exception):
    pass


class CreateFailed(Exception):
    pass


class DeleteFailed(Exception):
    pass


class Response:
    def __init__(self, response):
        for key in response:
            setattr(self, key, response[key])


class Api(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def _get_builder(self):
        builder = QueryBuilder()
        builder.host = self._host
        builder.port = self._port
        return builder


class AuthApi(Api):
    def __init__(self, host, port):
        super(AuthApi, self).__init__(host, port)
        self._session_name = id_generator()

    def _get_builder(self):
        builder = super(AuthApi, self)._get_builder()
        builder.cgi_path = "/webapi/auth.cgi"
        builder.api = "SYNO.API.Auth"
        builder.version = 2
        builder.param["session"] = self._session_name
        return builder

    def login(self, account, password):
        builder = self._get_builder()
        builder.method = "login"
        builder.param["account"] = account
        builder.param["passwd"] = password
        request = builder.build_get()
        try:
            response = Response(get(request))
            return response.data["sid"]
        except Exception:
            raise LoginFailed()

    def logout(self):
        builder = self._get_builder()
        builder.method = "logout"
        request = builder.build_get()
        try:
            response = Response(get(request))
            return response.success
        except Exception:
            raise LogoutFailed()


class TaskApi(Api):
    def __init__(self, host, port, sid):
        super(TaskApi, self).__init__(host, port)
        self._sid = sid

    def _get_builder(self):
        builder = super(TaskApi, self)._get_builder()
        builder.cgi_path = "/webapi/DownloadStation/task.cgi"
        builder.api = "SYNO.DownloadStation.Task"
        builder.version = 1
        builder.sid = self._sid
        return builder

    def list(self):
        builder = self._get_builder()
        builder.param["additional"] = "detail,transfer"
        builder.method = "list"
        request = builder.build_get()
        try:
            response = Response(get(request))
            return response
        except Exception:
            raise FetchFailed()

    def create(self, uri):
        builder = self._get_builder()
        builder.method = "create"
        builder.param["uri"] = uri
        (url, request) = builder.build_post()
        try:
            response = Response(post(url, request))
            return response
        except Exception:
            raise CreateFailed()

    def delete(self, name):
        ids = []
        for task in self.list().data['tasks']:
            if name in task['title']:
                ids.append(task['id'])
        return self._delete(",".join(ids))

    def _delete(self, id):
        builder = self._get_builder()
        builder.method = "delete"
        builder.param["id"] = id
        request = builder.build_get()
        try:
            response = Response(get(request))
            return response
        except Exception:
            raise DeleteFailed()


class Session:
    def __init__(self, host, port, username, password):
        self.auth_api = AuthApi(host, port)
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def __enter__(self):
        self.id = self.auth_api.login(self.username, self.password)
        self.task_api = TaskApi(self.host, self.port, self.id)
        return self

    def __exit__(self, type, value, traceback):
        self.auth_api.logout()
