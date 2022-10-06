

from api_info_parser import Parser, test as _test
import regex
import json
from copy import copy
import os




_api_class_define_template = "class {name}(AbstractApi):\n"
_api_method_class_define_template = "class {name}(AbstractApiMethod):\n"
_api_method_func_define_templae = "def {name}({args}):\n"
_api_method_invoke_template = "self.invoke_request('{method}',\n{nop:27}{{{path_args}}},\n{nop:27}{data})\n"
_api_method_description_template = '"""' """
{api_name}
> {method} {path}
{description}
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
#           'description': <description>
#         }
#       ]
#     }, ...
#   ]
# }


def add_tab(source: str, tab: int|str):
    if isinstance(tab, int):
        return ' '*tab + ('\n' + ' '*tab).join(source.split('\n')).strip() + '\n'
    elif isinstance(tab, str):
        return tab + ('\n' + tab).join(source.split('\n')).strip() + '\n'
    else:
        raise TypeError("Unsupported tab type({})".format(str(type(tab))))

def generate_method(path: str, path_args: list, api_name: str, method: dict, path_seq: list):
    #         { # Group Method
    #           'method': <http method, allows GET, PUT, POST, PATCH, DELETE>,
    #           'query_params': [ <parameters: str>, ... ],
    #           'data_params': [ <parameters: str>, ... ],
    #           'description': <description>
    #         }
    out = ""
    name = f"by_{path_seq[-1][1:-1]}" if path_seq[0].startswith('{') else path_seq[-1]
    args = ', '.join(f"{k}: str" for k in [*path_args, *method['query_params'], *method['data_params']])
    out += _api_method_func_define_templae.format(nop = '', name = method['method'].lower(), args = args)
    body = _api_method_description_template.format(nop = '',
                                                   api_name = '.'.join(path_seq),
                                                   method = method['method'],
                                                   path = path,
                                                   description = method['description'])
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
    #           'description': <description>
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
    #           'description': <description>
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
        norm_path = regex.sub(r"\{(\w+)\}", lambda x: f"by_{x[1]}", group['path'])
        path = norm_path[norm_path.index(api['name'].lower()) - 1:]
        seq = regex.match(r"(\/[\w\{\}]+)+", path)[0].split('/')[1:]
        get_ref(seq)['_group'] = generate_group(group, seq, api['name'])
    
    return groups_tree

def generate_apis(apis: list):
    return [generate_api(api) for api in apis]

def format_api(api: dict):
    out = ""
    group = ""
    if '_group' in api:
        group = '\n'.join(api.pop('_group').values())
    for k, v in api.items():
        cls = _api_class_define_template.format(name=regex.sub(r"^(\w)|_(\w)", lambda x: (x[1] or x[2]).upper(), k))
        out += cls + add_tab(format_api(v), 4)
    return out + '\n' + group
            
        

def format_apis(apis: list):
    return 'import api_base\n\n\n' + '\n\n'.join(format_api(api) for api in apis)



if __name__ == '__main__' or 1:
    apis = generate_apis(Parser().parse(_test))
    print(json.dumps(apis, indent=2))
    open("api.py", 'w').write(format_apis(apis))
    if os.path.exists("./test.py"):
        from test import Host, Token, Username




