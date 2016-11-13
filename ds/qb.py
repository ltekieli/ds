from collections import OrderedDict
import urllib

class QueryBuilder:
    def __init__(self):
        self._param = dict()
        self._sid = None

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def cgi_path(self):
        return self._cgi_path

    @property
    def api(self):
        return self._api

    @property
    def sid(self):
        return self._sid

    @property
    def version(self):
        return self._version

    @property
    def method(self):
        return self._method

    @property
    def param(self):
        return self._param

    def _build(self):
        url = "http://" + self.host + ":" + str(self.port) + self.cgi_path

        query = OrderedDict()
        query['api'] = self.api
        query['version'] = self.version
        query['method'] = self.method
        query.update(self.param)

        if self.sid:
            query['_sid'] = self.sid

        return (url, urllib.urlencode(query))

    def build_get(self):
        url, data = self._build()
        return url + "?" + data

    def build_post(self):
        return self._build()
