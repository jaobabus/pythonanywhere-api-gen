
from test import Host, Username, Token
from api import Api


api = Api(Host, Username, Token)

def test_AlwaysOn_ById_restart():
    res = api.always_on.get()
    assert res.status_code == 200






