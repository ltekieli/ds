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

    def build(self):
        query = "http://" + self.host + ":" + str(self.port) + self.cgi_path + "?api=" + \
            self.api + "&version=" + str(self.version) + "&method=" + self.method
        for k, v in self.param.iteritems():
            query += "&{}={}".format(k, v)
        if self.sid:
            query += "&_sid=" + self.sid
        return query
