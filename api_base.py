
import json
import regex
import requests




class ApiError(Exception):
    def __init__(self, http_error: int, json_content: dict, description: str):
        super().__init__(description)
        self.code = http_error
        self.data = json_content
        self.description = description


def url_encode(string: str, ignore = "") -> str:
    ign = ignore.replace('\\', '\\\\').replace(']', '\\]').replace('/', '\\/')
    return regex.sub(r"([^\w{}])".format(ign), lambda x: ''.join(f"%{c:0>2X}" for c in x[0].encode('utf-8')), string)  



class AbstractApi:
    def __init__(self, host: str, username: str, token: str):
        self._host = host
        self._username = username
        self._token = token
        self._init()

    def _init(self):
        pass

    def host(self, endpoint: str = '/'):
        return regex.sub(r"\/+$", '', self._host) + regex.sub(r"^\/+", '/', '/' + endpoint)
    
    def username(self):
        return self._username

    def raw_invoke_request(self, method: str, path: str, data: dict, headers: dict) -> requests.Response:
        res = requests.request(method, self.host(path),
                               headers = {'Authorization': 'Token {}'.format(self._token), **headers},
                               data = data)
        return res


class AbstractApiMethod:
    def __init__(self, api: AbstractApi, path: str):
        self._api = api
        self._path = path

    def invoke_request(self, method: str, 
                       path_args: dict = {},
                       data: dict = {},
                       headers: dict = {}) -> requests.Response:
        path = self._path.format(**path_args, username = self._api.username())
        return self._api.raw_invoke_request(method, path, data, headers)



