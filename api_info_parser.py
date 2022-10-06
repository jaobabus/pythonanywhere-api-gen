
import json
import regex
import enum



class Method:
    def __init__(self, name: str, path_format: str, arguments: list, defaults: dict):
        self.api_name = name
        self.path = path_format
        self.arguments = arguments
        self.defaults = defaults

    def to_json(self):
        return {
            'path':      self.path,
            'arguments': self.arguments,
            'defaults':  self.defaults,
        }
    
    @staticmethod
    def from_json(self, json_data: dict):
        self.path      = json_data['path']
        self.arguments = json_data['arguments']
        self.defaults  = json_data['defaults']

class ParserContext:
    class State(enum.Enum):
        Initialized      = 0
        FoundHeader      = 1
        FoundPath        = 2
        FoundTableHeader = 3
        FoundMethod      = 4
    
    def __init__(self):
        self.state = ParserContext.State.Initialized
        self.last_api: dict = None
        self.current_captures: dict = None
        
    def get_last_api_data(self, path: str, default = None):
        path = map(lambda x: int(x) if regex.match(r"\d+", x) else x, path.split('.'))
        data = self.last_api
        for key in path:
            if key in data:
                data = data[key]
            elif str(key) in data:
                data = data[str(key)]
            else:
                return default
        return data
        
    
_parser_parse_line_regex = r"""^
{0}(?<header>\w+){0}
{0}(?<query_arg>(?<query_arg_name>\w+)\=(?<query_arg_value>\{\w+\})){0}
{0}(?<query>\?(?&query_arg)(&(?&query_arg))*){0}
{0}(?<path_arg>\{\w+\}){0}
{0}(?<path>((\/\w+|\/?(?&path_arg)))+\/?(?&query)?){0}
{0}(?<tableheader>Method\tDescription\tParameters){0}
{0}(?<httpmth>GET|POST|PUT|HEAD|DELETE|PATCH){0}
{0}(?<data_parameter>\w+( \w+)?){0}
{0}(?<data_parameters>(POST parameters?\: )?(?<data_params>(?&data_parameter)(, (?&data_params))?)){0}
{0}(?<query_parameter>\w+( \w+)?){0}
{0}(?<query_parameters>(POST parameters?\: )?(?<query_params>(?&query_parameter)(, (?&query_params))?)){0}
{0}(?<parameters>(Query parameters?\: (?&query_parameters))|(?&data_parameters)|\(no parameters\)){0}
{0}(?<method>(?&httpmth)\t(?<mthdescription>[^\t]*)\t(?&parameters)){0}
{0}(?<body>(?&header)|(?&path)|(?&method)|(?&tableheader)|){0}
{0}"""

class Parser:
    def __init__(self):
        self.context = ParserContext()
        self.parsed = []
        
        self._parser_parse_line = regex.compile(_parser_parse_line_regex + "(?&body)$")
        self._parser_parse_line_M = regex.compile(_parser_parse_line_regex + "(?&body)$")
        self._parser_is_method = regex.compile(_parser_parse_line_regex + "(?&httpmth)")        
        
    def parse(self, text: str):
        # <header>
        #  (<path>
        #   <tableheader>
        #   <method>+
        #  )+
        
        self.parsed = []
        State = ParserContext.State
        warnings = {
            'header': {
                State.FoundPath: lambda ctx: "Api no body, name: '{}', path: '{}'".format(ctx.get_last_api_data('name', '<None>'),
                                                                                           ctx.get_last_api_data('groups.-1.path', '<None>')),
                State.FoundTableHeader: lambda ctx: "Api group '{}' no methods, skip".format(ctx.get_last_api_data('groups.-1.name', '<None>')),
            },
            'path': {
                State.FoundPath: lambda ctx: "Group no table? path: '{}'".format(ctx.get_last_api_data('groups.-1.path', '<None>')),
            },
            'tableheader': {
                State.FoundTableHeader: lambda ctx: "Dublicate 'table-header'?",
            }
        }
        errors = {
            'header': {
                State.FoundHeader: lambda ctx: "Empty Api? '{}' -> '{}'".format(ctx.get_last_api_data('name'),
                                                                                ctx.current_captures['header'][0]),        
            },
            'tableheader': {
                State.Initialized: lambda ctx: "Expected 'header'",
            },
            'method': {
                State.FoundPath: lambda ctx: "Unexpected 'table-header'",
                State.Initialized: lambda ctx: "Expected 'header'",
            },
            'path': {
                State.Initialized: lambda ctx: "Expected 'header'",
            },
        }
        
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
        
        def do(context: ParserContext, line: str):
            captures = context.current_captures
            if captures['header']:
                if self.context.state is not State.Initialized:
                    self._process_last_api()
                self.context.state = ParserContext.State.FoundHeader
                self.context.last_api = { 'name': captures['header'][0], 'groups': [] }
            
            elif captures['path']:
                args = [x[1:-1] for x in captures['path_arg']]
                self.context.state = ParserContext.State.FoundPath
                self.context.last_api['groups'].append({ 'path': captures['path'][0], 'path_args': args, 'query_args': {}, 'methods': [] })
                if captures['query']:
                    for key, value in zip(captures['query_arg_name'], captures['query_arg_value']):
                        self.context.last_api['groups'][-1]['query_args'].update({ key: value[1:-1] })
            
            elif captures['tableheader']:
                self.context.state = ParserContext.State.FoundTableHeader
            
            elif captures['method']:
                args = captures['parameters'][0]
                self.context.state = ParserContext.State.FoundMethod
                self.context.last_api['groups'][-1]['methods'].append(
                { 
                    'method': captures['httpmth'][0],
                    'description': captures['mthdescription'][0],
                    'query_params': captures['query_parameter'],
                    'data_params': captures['data_parameter'],
                })
        
        def raw_do(context: ParserContext, line: str):
            for key, value in warnings.items():
                if self.context.state in value and context.current_captures[key]:
                    print("last state = {state}\n>> {index: >4}:{line}\n  Warning: {err}\n".format(index = index + 1, line = line, err = value[self.context.state](self.context), state = self.context.state))
            for key, value in errors.items():
                if self.context.state in value and context.current_captures[key]:
                    print("last state = {state}\n>> {index: >4}:{line}\n  Error: {err}\n".format(index = index + 1, line = line, err = value[self.context.state](self.context), state = self.context.state))
            return do(context, line)            
        
        def raw_parse(line: str, rex: regex.Pattern):
            match = regex.match(rex, line)
            if match is None:
                return None
            else:
                return match.capturesdict()
        
        skip_until, skip_cb = None, None
        lines = text.split('\n')
        for index, line in enumerate(lines):
            if skip_until is not None:
                if index < skip_until:
                    continue
                else:
                    skip_cb(self.context, line)
                    skip_until, skip_cb = None, None
                    continue
            
            captures = raw_parse(line, self._parser_parse_line)
            if captures is None:
                if self._parser_is_method.match(line) and lines[index + 1].strip().startswith('{'):
                    for i in range(index + 1, len(lines)):
                        def reparse(ctx: ParserContext, line: str):
                            captures = raw_parse(line, self._parser_parse_line_M)
                            if captures is None:
                                raise RuntimeError("Error parse line '{}'".format(line))
                            ctx.current_captures = captures
                            return raw_do(ctx, line)
                                
                        current_line = lines[i].strip()                            
                        if current_line.endswith('}'):
                            skip_until = i + 1
                            skip_cb = (lambda index, i:
                                           lambda ctx, line: reparse(ctx, '\n'.join(lines[index : i + 1])
                                                                          + '\t' + lines[i + 1])
                                      )(index, i)
                            break
                if skip_until is None:
                    raise RuntimeError("Error parse line '{}'".format(line))
                else:
                    continue
            
            self.context.current_captures = captures
            raw_do(self.context, line)
            
                
        return self.parsed
        
    def _process_last_api(self):
        self.parsed.append(self.context.last_api)
        self.context.last_api = None








test = r"""
Always_On
/api/v0/user/{username}/always_on/
Method	Description	Parameters
GET	List all of your always-on tasks	(no parameters)
POST	Create and start a new always-on task	command, description, enabled
/api/v0/user/{username}/always_on/{id}/
Method	Description	Parameters
GET	Return information about an always-on task.	(no parameters)
PUT	Endpoints for always-on tasks	command, description, enabled
PATCH	Endpoints for always-on tasks	command, description, enabled
DELETE	Stop and delete an always-on task	(no parameters)
/api/v0/user/{username}/always_on/{id}/restart/
Method	Description	Parameters
POST	Endpoints for always-on tasks	command, description, enabled
Consoles
/api/v0/user/{username}/consoles/
Method	Description	Parameters
GET	List all your consoles	(no parameters)
POST	Create a new console object (NB does not actually start the process. Only connecting to the console in a browser will do that).	executable, arguments, working_directory
/api/v0/user/{username}/consoles/shared_with_you/
Method	Description	Parameters
GET	View consoles shared with you.	(no parameters)
/api/v0/user/{username}/consoles/{id}/
Method	Description	Parameters
GET	Return information about a console instance.	(no parameters)
DELETE	Kill a console.	(no parameters)
/api/v0/user/{username}/consoles/{id}/get_latest_output/
Method	Description	Parameters
GET	Get the most recent output from the console (approximately 500 characters).	(no parameters)
/api/v0/user/{username}/consoles/{id}/send_input/
Method	Description	Parameters
POST	"type" into the console. Add a "\n" for return.	POST parameter: input
Cpu
/api/v0/user/{username}/cpu/
Method	Description	Parameters
GET	Returns information about cpu usage in json format:
{
    "daily_cpu_limit_seconds": <int>,
    "next_reset_time": <isoformat>,
    "daily_cpu_total_usage_seconds": <float>
}
(no parameters)
Default_Python3_Version
/api/v0/user/{username}/default_python3_version/
Method	Description	Parameters
GET	Returns information about user's current and available default Python 3 version in json format:
{
    "default_python3_version": <str>,
    "available_python3_versions": [<str>],
}
(no parameters)
PATCH	Sets default Python 3 version for user.	(no parameters)
Default_Python_Version
/api/v0/user/{username}/default_python_version/
Method	Description	Parameters
GET	Returns information about user's current and available default Python version in json format:
{
    "default_python_version": <str>,
    "available_python_versions": [<str>],
}
(no parameters)
PATCH	Sets default Python version for user.	(no parameters)
Default_Save_And_Run_Python_Version
/api/v0/user/{username}/default_save_and_run_python_version/
Method	Description	Parameters
GET	Returns information about user's current and available Python version used for the "Run" button in the editor, in json format:
{
    "default_save_and_run_python_version": <str>,
    "available_python_versions": [<str>],
}
(no parameters)
PATCH	Sets Python version used for the "Run" button in the editor.	(no parameters)
Files
/api/v0/user/{username}/files/path{path}
Method	Description	Parameters
GET		(no parameters)
POST	Uploads a file to the specified file path. Contents should be in a multipart-encoded file with the name "content". The attached filename is ignored. If the directories in the given path do not exist, they will be created. Any file already present at the specified path will be overwritten. Returns 201 on success if a file has been created, or 200 if an existing file has been updated.	(no parameters)
DELETE	Deletes the file at the specified path. This method can be used to delete log files that are not longer required. Returns 204 on success.	(no parameters)
/api/v0/user/{username}/files/sharing/
Method	Description	Parameters
POST	Start sharing a file. Returns 201 on success, or 200 if file was already shared.	POST parameter: path
/api/v0/user/{username}/files/sharing/?path={path}
Method	Description	Parameters
GET	Check sharing status for a path. Returns 404 if path not currently shared.	Query parameter: path
DELETE	Stop sharing a path. Returns 204 on successful unshare.	Query parameter: path
/api/v0/user/{username}/files/tree/?path={path}
Method	Description	Parameters
GET	Returns a list of the contents of a directory, and its subdirectories as a list. Paths ending in slash/ represent directories. Limited to 1000 results.	Query parameter: path
Schedule
/api/v0/user/{username}/schedule/
Method	Description	Parameters
GET	List all of your scheduled tasks	(no parameters)
POST	Create a new scheduled task	command, enabled, interval, hour, minute, description
/api/v0/user/{username}/schedule/{id}/
Method	Description	Parameters
GET	Return information about a scheduled task.	(no parameters)
PUT	Endpoints for scheduled tasks	command, enabled, interval, hour, minute, description
PATCH	Endpoints for scheduled tasks	command, enabled, interval, hour, minute, description
DELETE	Delete an scheduled task	(no parameters)
Students
/api/v0/user/{username}/students/
Method	Description	Parameters
GET	Returns a list of students of the current user
{
    "students": [
        {"username": <string>},
        {"username": <string>},
        ...
    ]
}
(no parameters)
/api/v0/user/{username}/students/{student}/
Method	Description	Parameters
DELETE		(no parameters)
System_Image
/api/v0/user/{username}/system_image/
Method	Description	Parameters
GET	Returns information about user's current and available system images in json format:
{
    "system_image": <str>,
    "available_system_images": [<str>],
}
(no parameters)
PATCH	Sets system image for user.	(no parameters)
Webapps
/api/v0/user/{username}/webapps/
Method	Description	Parameters
GET	List all webapps	(no parameters)
POST	Create a new webapp with manual configuration. Use (for example) "python36" to specify Python 3.6.	POST parameters: domain_name, python_version
/api/v0/user/{username}/webapps/{domain_name}/
Method	Description	Parameters
GET	Return information about a web app's configuration	(no parameters)
PUT	Modify configuration of a web app. (NB a reload is usually required to apply changes).	python_version, source_directory, virtualen v_path, force_https, password_protection_enabled, password_protection_username, password_protection_password
PATCH	Modify configuration of a web app. (NB a reload is usually required to apply changes).	python_version, source_directory, virtual env_path, force_https, password_protection_enabled, password_protection_username, password_protection_password
DELETE	Delete the webapp. This will take the site offline. Config is backed up in /var/www, and your code is not touched.	(no parameters)
/api/v0/user/{username}/webapps/{domain_name}/disable/
Method	Description	Parameters
POST	Disable the webapp.	POST parameters: none
/api/v0/user/{username}/webapps/{domain_name}/enable/
Method	Description	Parameters
POST	Enable the webapp.	POST parameters: none
/api/v0/user/{username}/webapps/{domain_name}/reload/
Method	Description	Parameters
POST	Reload the webapp to reflect changes to configuration and/or source code on disk.	POST parameters: none
/api/v0/user/{username}/webapps/{domain_name}/ssl/
Method	Description	Parameters
GET	Get and set TLS/HTTPS info. POST parameters to the right are incorrect, use `cert` and `private_key` when posting.	(no parameters)
POST	Get and set TLS/HTTPS info. POST parameters to the right are incorrect, use `cert` and `private_key` when posting.	python_version, source_directory, virtualenv_path, force_https, password_protection_enabled, password_protection_username, password_protection_passw ord
DELETE	Get and set TLS/HTTPS info. POST parameters to the right are incorrect, use `cert` and `private_key` when posting.	(no parameters)
/api/v0/user/{username}/webapps/{domain_name}/static_files/
Method	Description	Parameters
GET	List all the static files mappings for a domain.	(no parameters)
POST	Create a new static files mapping. (webapp restart required)	url, path
/api/v0/user/{username}/webapps/{domain_name}/static_files/{id}/
Method	Description	Parameters
GET	Get URL and path of a particular mapping.	(no parameters)
PUT	Modify a static files mapping. (webapp restart required)	url, path
PATCH	Modify a static files mapping. (webapp restart required)	url, path
DELETE	Remove a static files mapping. (webapp restart required)	(no parameters)
/api/v0/user/{username}/webapps/{domain_name}/static_headers/
Method	Description	Parameters
GET	List all the static headers for a domain.	(no parameters)
POST	Create a new static header. (webapp restart required)	url, name, value
/api/v0/user/{username}/webapps/{domain_name}/static_headers/{id}/
Method	Description	Parameters
GET	Get URL, name and value of a particular header.	(no parameters)
PUT	Modify a static header. (webapp restart required)	url, name, value
PATCH	Modify a static header. (webapp restart required)	url, name, value
DELETE	Remove a static header. (webapp restart required)	(no parameters)
"""


if __name__ == '__main__':
    parsed = Parser().parse(test)
    print(json.dumps(parsed, indent=2))


