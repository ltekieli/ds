from collections import OrderedDict
import urllib.request, urllib.parse, urllib.error


class QueryBuilder:
    def __init__(self):
        self._param = dict()
        self._sid = None

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, val):
        self._host = val

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, val):
        self._port = val

    @property
    def cgi_path(self):
        return self._cgi_path

    @cgi_path.setter
    def cgi_path(self, val):
        self._cgi_path = val

    @property
    def api(self):
        return self._api

    @api.setter
    def api(self, val):
        self._api = val

    @property
    def sid(self):
        return self._sid

    @sid.setter
    def sid(self, val):
        self._sid = val

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, val):
        self._version = val

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, val):
        self._method = val

    @property
    def param(self):
        return self._param

    @param.setter
    def param(self, val):
        self._param = val

    def _build(self):
        url = "http://" + self.host + ":" + str(self.port) + self.cgi_path

        query = OrderedDict()
        query['api'] = self.api
        query['version'] = self.version
        query['method'] = self.method
        query.update(self.param)

        if self.sid:
            query['_sid'] = self.sid

        return (url, urllib.parse.urlencode(query))

    def build_get(self):
        url, data = self._build()
        return url + "?" + data

    def build_post(self):
        return self._build()
