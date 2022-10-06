
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

    def host(self, endpoint: str = '/'):
        return regex.sub(r"\/+$", '', self._host) + regex.sub(r"^\/+", '/', '/' + endpoint)

    def raw_invoke_request(self, method: str, path: str, data: dict, headers: dict) -> requests.Response:
        endpoint = regex.sub(r"\/+$", '', self.endpoint) + regex.sub(r"^\/*", '/', path.format(username=self._username))
        res = requests.request(method, endpoint,
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
                       headers: dict = {}) -> dict:
        path = self._path.format(**path_args)
        res = self._api.raw_invoke_request(method, path, data, headers)
        try:
            return res.json()
        except json.JSONDecodeError as e:
            raise RuntimeError("Not a json", res.status_code, e)          

    def GET(self, *args, **kwargs):
        return get(*args, **kwargs)
    def PUT(self, *args, **kwargs):
        return put(*args, **kwargs)
    def POST(self, *args, **kwargs):
        return post(*args, **kwargs)
    def PATCH(self, *args, **kwargs):
        return patch(*args, **kwargs)
    def DELETE(self, *args, **kwargs):
        return delete(*args, **kwargs)

    def get(self, *args, **kwargs):
        raise NotImplementedError()
    def put(self, *args, **kwargs):
        raise NotImplementedError()
    def post(self, *args, **kwargs):
        raise NotImplementedError()
    def patch(self, *args, **kwargs):
        raise NotImplementedError()
    def delete(self, *args, **kwargs):
        raise NotImplementedError()






