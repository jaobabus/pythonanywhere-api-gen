
from api_base import AbstractApi, AbstractApiMethod
import requests


class Api(AbstractApi):
    class _AlwaysOn(AbstractApiMethod):
        class _ById(AbstractApiMethod):
            class _Restart(AbstractApiMethod):
                def post(self, id: str, command: str, description: str, enabled: str) -> requests.Response:
                    """
                    api.v0.user.by_username.always_on.by_id.restart
                    > POST /api/v0/user/{username}/always_on/{id}/restart/
                    Endpoints for always-on tasks
                    command, description, enabled
                    """
                    return self.invoke_request('POST',
                                               {'id':id},
                                               {'command': command, 'description': description, 'enabled': enabled})

            def _init(self):
                self.restart = self._Restart(self, "/api/v0/user/{username}/always_on/{id}/restart/")

            def get(self, id: str) -> requests.Response:
                """
                api.v0.user.by_username.always_on.by_id
                > GET /api/v0/user/{username}/always_on/{id}/
                Return information about an always-on task.
                (no parameters)
                """
                return self.invoke_request('GET',
                                           {'id':id},
                                           {})

            def put(self, id: str, command: str, description: str, enabled: str) -> requests.Response:
                """
                api.v0.user.by_username.always_on.by_id
                > PUT /api/v0/user/{username}/always_on/{id}/
                Endpoints for always-on tasks
                command, description, enabled
                """
                return self.invoke_request('PUT',
                                           {'id':id},
                                           {'command': command, 'description': description, 'enabled': enabled})

            def patch(self, id: str, command: str, description: str, enabled: str) -> requests.Response:
                """
                api.v0.user.by_username.always_on.by_id
                > PATCH /api/v0/user/{username}/always_on/{id}/
                Endpoints for always-on tasks
                command, description, enabled
                """
                return self.invoke_request('PATCH',
                                           {'id':id},
                                           {'command': command, 'description': description, 'enabled': enabled})

            def delete(self, id: str) -> requests.Response:
                """
                api.v0.user.by_username.always_on.by_id
                > DELETE /api/v0/user/{username}/always_on/{id}/
                Stop and delete an always-on task
                (no parameters)
                """
                return self.invoke_request('DELETE',
                                           {'id':id},
                                           {})

        def _init(self):
            self.by_id = self._ById(self, "/api/v0/user/{username}/always_on/{id}/")

        def get(self, ) -> requests.Response:
            """
            api.v0.user.by_username.always_on
            > GET /api/v0/user/{username}/always_on/
            List all of your always-on tasks
            (no parameters)
            """
            return self.invoke_request('GET',
                                       {},
                                       {})

        def post(self, command: str, description: str, enabled: str) -> requests.Response:
            """
            api.v0.user.by_username.always_on
            > POST /api/v0/user/{username}/always_on/
            Create and start a new always-on task
            command, description, enabled
            """
            return self.invoke_request('POST',
                                       {},
                                       {'command': command, 'description': description, 'enabled': enabled})

    class _Consoles(AbstractApiMethod):
        class _SharedWithYou(AbstractApiMethod):
            def get(self, ) -> requests.Response:
                """
                api.v0.user.by_username.consoles.shared_with_you
                > GET /api/v0/user/{username}/consoles/shared_with_you/
                View consoles shared with you.
                (no parameters)
                """
                return self.invoke_request('GET',
                                           {},
                                           {})

        class _ById(AbstractApiMethod):
            class _GetLatestOutput(AbstractApiMethod):
                def get(self, id: str) -> requests.Response:
                    """
                    api.v0.user.by_username.consoles.by_id.get_latest_output
                    > GET /api/v0/user/{username}/consoles/{id}/get_latest_output/
                    Get the most recent output from the console (approximately 500 characters).
                    (no parameters)
                    """
                    return self.invoke_request('GET',
                                               {'id':id},
                                               {})

            class _SendInput(AbstractApiMethod):
                def post(self, id: str, input: str) -> requests.Response:
                    """
                    api.v0.user.by_username.consoles.by_id.send_input
                    > POST /api/v0/user/{username}/consoles/{id}/send_input/
                    "type" into the console. Add a "\n" for return.
                    POST parameter: input
                    """
                    return self.invoke_request('POST',
                                               {'id':id},
                                               {'input': input})

            def _init(self):
                self.get_latest_output = self._GetLatestOutput(self, "/api/v0/user/{username}/consoles/{id}/get_latest_output/")
                self.send_input = self._SendInput(self, "/api/v0/user/{username}/consoles/{id}/send_input/")

            def get(self, id: str) -> requests.Response:
                """
                api.v0.user.by_username.consoles.by_id
                > GET /api/v0/user/{username}/consoles/{id}/
                Return information about a console instance.
                (no parameters)
                """
                return self.invoke_request('GET',
                                           {'id':id},
                                           {})

            def delete(self, id: str) -> requests.Response:
                """
                api.v0.user.by_username.consoles.by_id
                > DELETE /api/v0/user/{username}/consoles/{id}/
                Kill a console.
                (no parameters)
                """
                return self.invoke_request('DELETE',
                                           {'id':id},
                                           {})

        def _init(self):
            self.shared_with_you = self._SharedWithYou(self, "/api/v0/user/{username}/consoles/shared_with_you/")
            self.by_id = self._ById(self, "/api/v0/user/{username}/consoles/{id}/")

        def get(self, ) -> requests.Response:
            """
            api.v0.user.by_username.consoles
            > GET /api/v0/user/{username}/consoles/
            List all your consoles
            (no parameters)
            """
            return self.invoke_request('GET',
                                       {},
                                       {})

        def post(self, executable: str, arguments: str, working_directory: str) -> requests.Response:
            """
            api.v0.user.by_username.consoles
            > POST /api/v0/user/{username}/consoles/
            Create a new console object (NB does not actually start the process. Only connecting to the console in a browser will do that).
            executable, arguments, working_directory
            """
            return self.invoke_request('POST',
                                       {},
                                       {'executable': executable, 'arguments': arguments, 'working_directory': working_directory})

    class _Cpu(AbstractApiMethod):
        def get(self, ) -> requests.Response:
            """
            api.v0.user.by_username.cpu
            > GET /api/v0/user/{username}/cpu/
            Returns information about cpu usage in json format:
            {
                "daily_cpu_limit_seconds": <int>,
                "next_reset_time": <isoformat>,
                "daily_cpu_total_usage_seconds": <float>
            }
            (no parameters)
            """
            return self.invoke_request('GET',
                                       {},
                                       {})

    class _DefaultPython3Version(AbstractApiMethod):
        def get(self, ) -> requests.Response:
            """
            api.v0.user.by_username.default_python3_version
            > GET /api/v0/user/{username}/default_python3_version/
            Returns information about user's current and available default Python 3 version in json format:
            {
                "default_python3_version": <str>,
                "available_python3_versions": [<str>],
            }
            (no parameters)
            """
            return self.invoke_request('GET',
                                       {},
                                       {})

        def patch(self, ) -> requests.Response:
            """
            api.v0.user.by_username.default_python3_version
            > PATCH /api/v0/user/{username}/default_python3_version/
            Sets default Python 3 version for user.
            (no parameters)
            """
            return self.invoke_request('PATCH',
                                       {},
                                       {})

    class _DefaultPythonVersion(AbstractApiMethod):
        def get(self, ) -> requests.Response:
            """
            api.v0.user.by_username.default_python_version
            > GET /api/v0/user/{username}/default_python_version/
            Returns information about user's current and available default Python version in json format:
            {
                "default_python_version": <str>,
                "available_python_versions": [<str>],
            }
            (no parameters)
            """
            return self.invoke_request('GET',
                                       {},
                                       {})

        def patch(self, ) -> requests.Response:
            """
            api.v0.user.by_username.default_python_version
            > PATCH /api/v0/user/{username}/default_python_version/
            Sets default Python version for user.
            (no parameters)
            """
            return self.invoke_request('PATCH',
                                       {},
                                       {})

    class _DefaultSaveAndRunPythonVersion(AbstractApiMethod):
        def get(self, ) -> requests.Response:
            """
            api.v0.user.by_username.default_save_and_run_python_version
            > GET /api/v0/user/{username}/default_save_and_run_python_version/
            Returns information about user's current and available Python version used for the "Run" button in the editor, in json format:
            {
                "default_save_and_run_python_version": <str>,
                "available_python_versions": [<str>],
            }
            (no parameters)
            """
            return self.invoke_request('GET',
                                       {},
                                       {})

        def patch(self, ) -> requests.Response:
            """
            api.v0.user.by_username.default_save_and_run_python_version
            > PATCH /api/v0/user/{username}/default_save_and_run_python_version/
            Sets Python version used for the "Run" button in the editor.
            (no parameters)
            """
            return self.invoke_request('PATCH',
                                       {},
                                       {})

    class _Files(AbstractApiMethod):
        class _PathbyPath(AbstractApiMethod):
            def get(self, path: str) -> requests.Response:
                """
                api.v0.user.by_username.files.pathby_path
                > GET /api/v0/user/{username}/files/path{path}

                (no parameters)
                """
                return self.invoke_request('GET',
                                           {'path':path},
                                           {})

            def post(self, path: str) -> requests.Response:
                """
                api.v0.user.by_username.files.pathby_path
                > POST /api/v0/user/{username}/files/path{path}
                Uploads a file to the specified file path. Contents should be in a multipart-encoded file with the name "content". The attached filename is ignored. If the directories in the given path do not exist, they will be created. Any file already present at the specified path will be overwritten. Returns 201 on success if a file has been created, or 200 if an existing file has been updated.
                (no parameters)
                """
                return self.invoke_request('POST',
                                           {'path':path},
                                           {})

            def delete(self, path: str) -> requests.Response:
                """
                api.v0.user.by_username.files.pathby_path
                > DELETE /api/v0/user/{username}/files/path{path}
                Deletes the file at the specified path. This method can be used to delete log files that are not longer required. Returns 204 on success.
                (no parameters)
                """
                return self.invoke_request('DELETE',
                                           {'path':path},
                                           {})

        class _Sharing(AbstractApiMethod):
            def get(self, path: str) -> requests.Response:
                """
                api.v0.user.by_username.files.sharing
                > GET /api/v0/user/{username}/files/sharing/?path={path}
                Check sharing status for a path. Returns 404 if path not currently shared.
                Query parameter: path
                """
                return self.invoke_request('GET',
                                           {'path':path},
                                           {})

            def delete(self, path: str) -> requests.Response:
                """
                api.v0.user.by_username.files.sharing
                > DELETE /api/v0/user/{username}/files/sharing/?path={path}
                Stop sharing a path. Returns 204 on successful unshare.
                Query parameter: path
                """
                return self.invoke_request('DELETE',
                                           {'path':path},
                                           {})

        class _Tree(AbstractApiMethod):
            def get(self, path: str) -> requests.Response:
                """
                api.v0.user.by_username.files.tree
                > GET /api/v0/user/{username}/files/tree/?path={path}
                Returns a list of the contents of a directory, and its subdirectories as a list. Paths ending in slash/ represent directories. Limited to 1000 results.
                Query parameter: path
                """
                return self.invoke_request('GET',
                                           {'path':path},
                                           {})

        def _init(self):
            self.pathby_path = self._PathbyPath(self, "/api/v0/user/{username}/files/path{path}")
            self.sharing = self._Sharing(self, "/api/v0/user/{username}/files/sharing/?path={path}")
            self.tree = self._Tree(self, "/api/v0/user/{username}/files/tree/?path={path}")


    class _Schedule(AbstractApiMethod):
        class _ById(AbstractApiMethod):
            def get(self, id: str) -> requests.Response:
                """
                api.v0.user.by_username.schedule.by_id
                > GET /api/v0/user/{username}/schedule/{id}/
                Return information about a scheduled task.
                (no parameters)
                """
                return self.invoke_request('GET',
                                           {'id':id},
                                           {})

            def put(self, id: str, command: str, enabled: str, interval: str, hour: str, minute: str, description: str) -> requests.Response:
                """
                api.v0.user.by_username.schedule.by_id
                > PUT /api/v0/user/{username}/schedule/{id}/
                Endpoints for scheduled tasks
                command, enabled, interval, hour, minute, description
                """
                return self.invoke_request('PUT',
                                           {'id':id},
                                           {'command': command, 'enabled': enabled, 'interval': interval, 'hour': hour, 'minute': minute, 'description': description})

            def patch(self, id: str, command: str, enabled: str, interval: str, hour: str, minute: str, description: str) -> requests.Response:
                """
                api.v0.user.by_username.schedule.by_id
                > PATCH /api/v0/user/{username}/schedule/{id}/
                Endpoints for scheduled tasks
                command, enabled, interval, hour, minute, description
                """
                return self.invoke_request('PATCH',
                                           {'id':id},
                                           {'command': command, 'enabled': enabled, 'interval': interval, 'hour': hour, 'minute': minute, 'description': description})

            def delete(self, id: str) -> requests.Response:
                """
                api.v0.user.by_username.schedule.by_id
                > DELETE /api/v0/user/{username}/schedule/{id}/
                Delete an scheduled task
                (no parameters)
                """
                return self.invoke_request('DELETE',
                                           {'id':id},
                                           {})

        def _init(self):
            self.by_id = self._ById(self, "/api/v0/user/{username}/schedule/{id}/")

        def get(self, ) -> requests.Response:
            """
            api.v0.user.by_username.schedule
            > GET /api/v0/user/{username}/schedule/
            List all of your scheduled tasks
            (no parameters)
            """
            return self.invoke_request('GET',
                                       {},
                                       {})

        def post(self, command: str, enabled: str, interval: str, hour: str, minute: str, description: str) -> requests.Response:
            """
            api.v0.user.by_username.schedule
            > POST /api/v0/user/{username}/schedule/
            Create a new scheduled task
            command, enabled, interval, hour, minute, description
            """
            return self.invoke_request('POST',
                                       {},
                                       {'command': command, 'enabled': enabled, 'interval': interval, 'hour': hour, 'minute': minute, 'description': description})

    class _Students(AbstractApiMethod):
        class _ByStudent(AbstractApiMethod):
            def delete(self, student: str) -> requests.Response:
                """
                api.v0.user.by_username.students.by_student
                > DELETE /api/v0/user/{username}/students/{student}/

                (no parameters)
                """
                return self.invoke_request('DELETE',
                                           {'student':student},
                                           {})

        def _init(self):
            self.by_student = self._ByStudent(self, "/api/v0/user/{username}/students/{student}/")

        def get(self, ) -> requests.Response:
            """
            api.v0.user.by_username.students
            > GET /api/v0/user/{username}/students/
            Returns a list of students of the current user
            {
                "students": [
                    {"username": <string>},
                    {"username": <string>},
                    ...
                ]
            }
            (no parameters)
            """
            return self.invoke_request('GET',
                                       {},
                                       {})

    class _SystemImage(AbstractApiMethod):
        def get(self, ) -> requests.Response:
            """
            api.v0.user.by_username.system_image
            > GET /api/v0/user/{username}/system_image/
            Returns information about user's current and available system images in json format:
            {
                "system_image": <str>,
                "available_system_images": [<str>],
            }
            (no parameters)
            """
            return self.invoke_request('GET',
                                       {},
                                       {})

        def patch(self, ) -> requests.Response:
            """
            api.v0.user.by_username.system_image
            > PATCH /api/v0/user/{username}/system_image/
            Sets system image for user.
            (no parameters)
            """
            return self.invoke_request('PATCH',
                                       {},
                                       {})

    def _init(self):
        self.always_on = self._AlwaysOn(self, "/api/v0/user/{username}/always_on/")
        self.consoles = self._Consoles(self, "/api/v0/user/{username}/consoles/")
        self.cpu = self._Cpu(self, "/api/v0/user/{username}/cpu/")
        self.default_python3_version = self._DefaultPython3Version(self, "/api/v0/user/{username}/default_python3_version/")
        self.default_python_version = self._DefaultPythonVersion(self, "/api/v0/user/{username}/default_python_version/")
        self.default_save_and_run_python_version = self._DefaultSaveAndRunPythonVersion(self, "/api/v0/user/{username}/default_save_and_run_python_version/")
        self.schedule = self._Schedule(self, "/api/v0/user/{username}/schedule/")
        self.students = self._Students(self, "/api/v0/user/{username}/students/")
        self.system_image = self._SystemImage(self, "/api/v0/user/{username}/system_image/")


