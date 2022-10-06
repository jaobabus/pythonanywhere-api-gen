import api_base


class AlwaysOn(AbstractApi):
    class ById(AbstractApi):
        class Restart(AbstractApi):
            def post(id: str, command: str, description: str, enabled: str):
                """
                always_on.by_id.restart
                > POST /api/v0/user/{username}/always_on/{id}/restart/
                Endpoints for always-on tasks
                """
                return self.invoke_request('POST',
                                           {'id':id},
                                           {'command': command, 'description': description, 'enabled': enabled})
        
        def get(id: str):
            """
            always_on.by_id
            > GET /api/v0/user/{username}/always_on/{id}/
            Return information about an always-on task.
            """
            return self.invoke_request('GET',
                                       {'id':id},
                                       {})
        
        def put(id: str, command: str, description: str, enabled: str):
            """
            always_on.by_id
            > PUT /api/v0/user/{username}/always_on/{id}/
            Endpoints for always-on tasks
            """
            return self.invoke_request('PUT',
                                       {'id':id},
                                       {'command': command, 'description': description, 'enabled': enabled})
        
        def patch(id: str, command: str, description: str, enabled: str):
            """
            always_on.by_id
            > PATCH /api/v0/user/{username}/always_on/{id}/
            Endpoints for always-on tasks
            """
            return self.invoke_request('PATCH',
                                       {'id':id},
                                       {'command': command, 'description': description, 'enabled': enabled})
        
        def delete(id: str):
            """
            always_on.by_id
            > DELETE /api/v0/user/{username}/always_on/{id}/
            Stop and delete an always-on task
            """
            return self.invoke_request('DELETE',
                                       {'id':id},
                                       {})
    
    def get():
        """
        always_on
        > GET /api/v0/user/{username}/always_on/
        List all of your always-on tasks
        """
        return self.invoke_request('GET',
                                   {},
                                   {})
    
    def post(command: str, description: str, enabled: str):
        """
        always_on
        > POST /api/v0/user/{username}/always_on/
        Create and start a new always-on task
        """
        return self.invoke_request('POST',
                                   {},
                                   {'command': command, 'description': description, 'enabled': enabled})



class Consoles(AbstractApi):
    class SharedWithYou(AbstractApi):
        def get():
            """
            consoles.shared_with_you
            > GET /api/v0/user/{username}/consoles/shared_with_you/
            View consoles shared with you.
            """
            return self.invoke_request('GET',
                                       {},
                                       {})
    class ById(AbstractApi):
        class GetLatestOutput(AbstractApi):
            def get(id: str):
                """
                consoles.by_id.get_latest_output
                > GET /api/v0/user/{username}/consoles/{id}/get_latest_output/
                Get the most recent output from the console (approximately 500 characters).
                """
                return self.invoke_request('GET',
                                           {'id':id},
                                           {})
        class SendInput(AbstractApi):
            def post(id: str, input: str):
                """
                consoles.by_id.send_input
                > POST /api/v0/user/{username}/consoles/{id}/send_input/
                "type" into the console. Add a "\n" for return.
                """
                return self.invoke_request('POST',
                                           {'id':id},
                                           {'input': input})
        
        def get(id: str):
            """
            consoles.by_id
            > GET /api/v0/user/{username}/consoles/{id}/
            Return information about a console instance.
            """
            return self.invoke_request('GET',
                                       {'id':id},
                                       {})
        
        def delete(id: str):
            """
            consoles.by_id
            > DELETE /api/v0/user/{username}/consoles/{id}/
            Kill a console.
            """
            return self.invoke_request('DELETE',
                                       {'id':id},
                                       {})
    
    def get():
        """
        consoles
        > GET /api/v0/user/{username}/consoles/
        List all your consoles
        """
        return self.invoke_request('GET',
                                   {},
                                   {})
    
    def post(executable: str, arguments: str, working_directory: str):
        """
        consoles
        > POST /api/v0/user/{username}/consoles/
        Create a new console object (NB does not actually start the process. Only connecting to the console in a browser will do that).
        """
        return self.invoke_request('POST',
                                   {},
                                   {'executable': executable, 'arguments': arguments, 'working_directory': working_directory})



class Cpu(AbstractApi):
    def get():
        """
        cpu
        > GET /api/v0/user/{username}/cpu/
        Returns information about cpu usage in json format:
        {
            "daily_cpu_limit_seconds": <int>,
            "next_reset_time": <isoformat>,
            "daily_cpu_total_usage_seconds": <float>
        }
        """
        return self.invoke_request('GET',
                                   {},
                                   {})



class DefaultPython3Version(AbstractApi):
    def get():
        """
        default_python3_version
        > GET /api/v0/user/{username}/default_python3_version/
        Returns information about user's current and available default Python 3 version in json format:
        {
            "default_python3_version": <str>,
            "available_python3_versions": [<str>],
        }
        """
        return self.invoke_request('GET',
                                   {},
                                   {})
    
    def patch():
        """
        default_python3_version
        > PATCH /api/v0/user/{username}/default_python3_version/
        Sets default Python 3 version for user.
        """
        return self.invoke_request('PATCH',
                                   {},
                                   {})



class DefaultPythonVersion(AbstractApi):
    def get():
        """
        default_python_version
        > GET /api/v0/user/{username}/default_python_version/
        Returns information about user's current and available default Python version in json format:
        {
            "default_python_version": <str>,
            "available_python_versions": [<str>],
        }
        """
        return self.invoke_request('GET',
                                   {},
                                   {})
    
    def patch():
        """
        default_python_version
        > PATCH /api/v0/user/{username}/default_python_version/
        Sets default Python version for user.
        """
        return self.invoke_request('PATCH',
                                   {},
                                   {})



class DefaultSaveAndRunPythonVersion(AbstractApi):
    def get():
        """
        default_save_and_run_python_version
        > GET /api/v0/user/{username}/default_save_and_run_python_version/
        Returns information about user's current and available Python version used for the "Run" button in the editor, in json format:
        {
            "default_save_and_run_python_version": <str>,
            "available_python_versions": [<str>],
        }
        """
        return self.invoke_request('GET',
                                   {},
                                   {})
    
    def patch():
        """
        default_save_and_run_python_version
        > PATCH /api/v0/user/{username}/default_save_and_run_python_version/
        Sets Python version used for the "Run" button in the editor.
        """
        return self.invoke_request('PATCH',
                                   {},
                                   {})



class Files(AbstractApi):
    class PathbyPath(AbstractApi):
        def get(path: str):
            """
            files.pathby_path
            > GET /api/v0/user/{username}/files/path{path}
            
            """
            return self.invoke_request('GET',
                                       {'path':path},
                                       {})
        
        def post(path: str):
            """
            files.pathby_path
            > POST /api/v0/user/{username}/files/path{path}
            Uploads a file to the specified file path. Contents should be in a multipart-encoded file with the name "content". The attached filename is ignored. If the directories in the given path do not exist, they will be created. Any file already present at the specified path will be overwritten. Returns 201 on success if a file has been created, or 200 if an existing file has been updated.
            """
            return self.invoke_request('POST',
                                       {'path':path},
                                       {})
        
        def delete(path: str):
            """
            files.pathby_path
            > DELETE /api/v0/user/{username}/files/path{path}
            Deletes the file at the specified path. This method can be used to delete log files that are not longer required. Returns 204 on success.
            """
            return self.invoke_request('DELETE',
                                       {'path':path},
                                       {})
    class Sharing(AbstractApi):
        def get(path: str):
            """
            files.sharing
            > GET /api/v0/user/{username}/files/sharing/?path={path}
            Check sharing status for a path. Returns 404 if path not currently shared.
            """
            return self.invoke_request('GET',
                                       {'path':path},
                                       {})
        
        def delete(path: str):
            """
            files.sharing
            > DELETE /api/v0/user/{username}/files/sharing/?path={path}
            Stop sharing a path. Returns 204 on successful unshare.
            """
            return self.invoke_request('DELETE',
                                       {'path':path},
                                       {})
    class Tree(AbstractApi):
        def get(path: str):
            """
            files.tree
            > GET /api/v0/user/{username}/files/tree/?path={path}
            Returns a list of the contents of a directory, and its subdirectories as a list. Paths ending in slash/ represent directories. Limited to 1000 results.
            """
            return self.invoke_request('GET',
                                       {'path':path},
                                       {})



class Schedule(AbstractApi):
    class ById(AbstractApi):
        def get(id: str):
            """
            schedule.by_id
            > GET /api/v0/user/{username}/schedule/{id}/
            Return information about a scheduled task.
            """
            return self.invoke_request('GET',
                                       {'id':id},
                                       {})
        
        def put(id: str, command: str, enabled: str, interval: str, hour: str, minute: str, description: str):
            """
            schedule.by_id
            > PUT /api/v0/user/{username}/schedule/{id}/
            Endpoints for scheduled tasks
            """
            return self.invoke_request('PUT',
                                       {'id':id},
                                       {'command': command, 'enabled': enabled, 'interval': interval, 'hour': hour, 'minute': minute, 'description': description})
        
        def patch(id: str, command: str, enabled: str, interval: str, hour: str, minute: str, description: str):
            """
            schedule.by_id
            > PATCH /api/v0/user/{username}/schedule/{id}/
            Endpoints for scheduled tasks
            """
            return self.invoke_request('PATCH',
                                       {'id':id},
                                       {'command': command, 'enabled': enabled, 'interval': interval, 'hour': hour, 'minute': minute, 'description': description})
        
        def delete(id: str):
            """
            schedule.by_id
            > DELETE /api/v0/user/{username}/schedule/{id}/
            Delete an scheduled task
            """
            return self.invoke_request('DELETE',
                                       {'id':id},
                                       {})
    
    def get():
        """
        schedule
        > GET /api/v0/user/{username}/schedule/
        List all of your scheduled tasks
        """
        return self.invoke_request('GET',
                                   {},
                                   {})
    
    def post(command: str, enabled: str, interval: str, hour: str, minute: str, description: str):
        """
        schedule
        > POST /api/v0/user/{username}/schedule/
        Create a new scheduled task
        """
        return self.invoke_request('POST',
                                   {},
                                   {'command': command, 'enabled': enabled, 'interval': interval, 'hour': hour, 'minute': minute, 'description': description})



class Students(AbstractApi):
    class ByStudent(AbstractApi):
        def delete(student: str):
            """
            students.by_student
            > DELETE /api/v0/user/{username}/students/{student}/
            
            """
            return self.invoke_request('DELETE',
                                       {'student':student},
                                       {})
    
    def get():
        """
        students
        > GET /api/v0/user/{username}/students/
        Returns a list of students of the current user
        {
            "students": [
                {"username": <string>},
                {"username": <string>},
                ...
            ]
        }
        """
        return self.invoke_request('GET',
                                   {},
                                   {})



class SystemImage(AbstractApi):
    def get():
        """
        system_image
        > GET /api/v0/user/{username}/system_image/
        Returns information about user's current and available system images in json format:
        {
            "system_image": <str>,
            "available_system_images": [<str>],
        }
        """
        return self.invoke_request('GET',
                                   {},
                                   {})
    
    def patch():
        """
        system_image
        > PATCH /api/v0/user/{username}/system_image/
        Sets system image for user.
        """
        return self.invoke_request('PATCH',
                                   {},
                                   {})

