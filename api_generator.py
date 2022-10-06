

from api_info_parser import Parser, test as _test
import regex
import json
from copy import copy
import os




_api_method_init_define_template = "def _init(self):\n"
_api_class_define_template = "class {name}(AbstractApi):\n"
_api_method_class_define_template = "class _{name}(AbstractApiMethod):\n"
_api_method_func_define_templae = "def {name}(self, {args}) -> requests.Response:\n"
_api_method_invoke_template = "self.invoke_request('{method}',\n{nop:27}{{{path_args}}},\n{nop:27}{data})\n"
_api_method_description_template = '"""' """
{api_name}
> {method} {path}
{description}
{params}
""" '"""\n'

# { # Api
#   'name': <Api name>,
#   'groups': [
#     { # Api group
#       'path': <Group path>,
#       'path_args': [ <Path argument: str> ],
#       'query_args': { <Query argument: name:value> },
#       'methods': [
#         { # Group Method
#           'method': <http method, allows GET, PUT, POST, PATCH, DELETE>,
#           'query_params': [ <parameters: str>, ... ],
#           'data_params': [ <parameters: str>, ... ],
#           'description': <description>,
#           'raw_params': <raw text in params>
#         }
#       ]
#     }, ...
#   ]
# }


def add_tab(source: str, tab: int|str):
    if isinstance(tab, int):
        return add_tab(source, ' ' * tab)
    elif isinstance(tab, str):
        return '\n'.join(f"{s and tab}{s}" for s in source.split('\n'))
    else:
        raise TypeError("Unsupported tab type({})".format(str(type(tab))))


def generate_method(path: str, path_args: list, api_name: str, method: dict, path_seq: list):
    #         { # Group Method
    #           'method': <http method, allows GET, PUT, POST, PATCH, DELETE>,
    #           'query_params': [ <parameters: str>, ... ],
    #           'data_params': [ <parameters: str>, ... ],
    #           'description': <description>,
    #           'raw_params': <raw text in params>
    #         }
    out = ""
    name = f"by_{path_seq[-1][1:-1]}" if path_seq[0].startswith('{') else path_seq[-1]
    args = ', '.join(f"{k}: str" for k in [*path_args, *method['query_params'], *method['data_params']])
    out += _api_method_func_define_templae.format(nop = '', name = method['method'].lower(), args = args)
    body = _api_method_description_template.format(nop = '',
                                                   api_name = '.'.join(path_seq),
                                                   method = method['method'],
                                                   path = path,
                                                   description = method['description'],
                                                   params = method['raw_params'])
    body += "return " + _api_method_invoke_template.format(nop = '',
                                                           method = method['method'],
                                                           path_args = ', '.join(f"'{k}':{k}" 
                                                                                 for k in (path_args + method['query_params'])),
                                                           data = '{' + ', '.join(f"'{k}': {k}"
                                                                                  for k in method['data_params']) + '}')
    out += add_tab(body, 4)
    return out
    

def generate_group(group: dict, path_seq: list, api_name: str):
    #     { # Api group
    #       'path': <Group path>,
    #       'path_args': [ <Path argument: str> ],
    #       'query_args': { <Query argument: name:value> },
    #       'methods': [
    #         { # Group Method
    #           'method': <http method, allows GET, PUT, POST, PATCH, DELETE>,
    #           'query_params': [ <parameters: str>, ... ],
    #           'data_params': [ <parameters: str>, ... ],
    #           'description': <description>,
    #           'raw_params': <raw text in params>
    #         }
    #       ]
    #     }, ...    
    methods_tree = {}
    
    for method in group['methods']:
        methods_tree[method['method']] = generate_method(group['path'], 
                                                         [k for k in group['path_args'] if k != 'username'], 
                                                          api_name, method, path_seq)

    return methods_tree

def generate_api(api: dict):
    # { # Api
    #   'name': <Api name>,
    #   'groups': [
    #     { # Api group
    #       'path': <Group path>,
    #       'path_args': [ <Path argument: str> ],
    #       'query_args': { <Query argument: name:value> },
    #       'methods': [
    #         { # Group Method
    #           'method': <http method, allows GET, PUT, POST, PATCH, DELETE>,
    #           'query_params': [ <parameters: str>, ... ],
    #           'data_params': [ <parameters: str>, ... ],
    #           'description': <description>,
    #           'raw_params': <raw text in params>
    #         }
    #       ]
    #     }, ...
    #   ]
    # }    
    groups_tree = {}
    def get_ref(path: list|str, default_set = {}):
        if isinstance(path, list):
            ref = groups_tree
            for key in path:
                if key not in ref:
                    ref[key] = copy(default_set)
                ref = ref[key]
            return ref
        if isinstance(path, str):
            return get_ref(path.split('.'))

    for group in api['groups']:
        path = regex.sub(r"\{(\w+)\}", lambda x: f"by_{x[1]}", group['path'])
        seq = regex.match(r"(\/\w+)+", path)[0].split('/')[1:]
        ref = get_ref(seq)
        ref['_group'] = generate_group(group, seq, api['name'])
        ref['_meta'] = group
    
    def add_inits(name: str, group: dict):
        init = ""
        for k, v in group.items():
            if k.startswith('_'): continue
            add_inits(k, v)
            if '_group' in v:
                up = regex.sub(r"^(\w)|_(\w)", lambda x: (x[1] or x[2]).upper(), k)
                init += add_tab("self.{name} = self._{cls_name}(self, \"{path}\")\n".format(name = k, 
                                                                                         cls_name = up, 
                                                                                         path = v['_meta']['path']), 4)
        if init:
            group['_init'] = _api_method_init_define_template.format(nop = '') + init
    add_inits("", get_ref('api.v0.user.by_username'))
    get_ref('api.v0.user.by_username')['_meta'] = api
    return get_ref('api.v0.user.by_username')

def generate_apis(apis: list):
    out = generate_api({'name': 'Api', 
                        'groups': [
                            group
                            for api in apis for group in api['groups']
                        ]})
    return out


def _format_api(api: dict):
    out = ""
    methods = ""
    group, init = "", ""
    if '_meta' in api:
        api.pop('_meta')
    if '_group' in api:
        group = '\n'.join(api.pop('_group').values())
    if '_init' in api:
        init = api.pop('_init')
    for k, v in api.items():
        template = _api_method_class_define_template
        cls_name = regex.sub(r"^(\w)|_(\w)", lambda x: (x[1] or x[2]).upper(), k)
        cls = template.format(name=cls_name)
        out += cls + add_tab(_format_api(v), 4)
    return "{}{}{}{}\n".format(out, init, init and '\n', group)

def format_api(api: dict):
    head = "\nfrom api_base import AbstractApi, AbstractApiMethod\nimport requests\n\n\n"
    return head + _api_class_define_template.format(name = api['_meta']['name']) + add_tab(_format_api(api), 4)


if __name__ == '__main__' or 1:
    api = generate_apis(Parser().parse(_test))
    print(json.dumps(api, indent=2))
    open("api.py", 'w').write(format_api(api))
        



