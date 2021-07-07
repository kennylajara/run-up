# cython: language_level=3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


# Built-in
from abc import ABC, abstractmethod
from collections.abc import KeysView
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
import zipfile

# 3rd party
import click
import pyximport  # type: ignore

pyximport.install()

# Own
from runup.db cimport RunupDB
from runup.utils cimport vCall, vInfo, vResponse


cdef class Interpreter:
    """Interpreters' abstract class."""

    def __init__(
        self,
        context: Path,
        bint verbose,
        char* version,
        required_parameters: List[str],
        valid_parameters: Dict[str, Any],
    ):
        """Set interpreter variables."""
        self._context:Path = context
        self._required_parameters:List[str] = required_parameters
        self._valid_parameters:Dict[str, Any] = valid_parameters
        self._verbose:bint = verbose
        self._version = version

    cpdef bint create_backup(self, yaml_config, project):
        """Create a new backup."""
        raise NotImplementedError()

    # @abstractmethod
    def restore_backup(
        self,
        yaml_config: Dict[str, Any],
        backup_id: str,
        location: str,
        job: int,
        force: bool,
    ) -> Optional[bool]:
        """Restore the specified backup."""
        raise NotImplementedError()

    # @abstractmethod
    def set_environment(self) -> bool:
        """Create the backup enviroment."""
        raise NotImplementedError()

    # @abstractmethod
    def missing_parameter(self, yaml_config: Dict[str, Any]) -> Optional[str]:
        """Find the required parameters missing on YAML file"""
        raise NotImplementedError()

    # @abstractmethod
    def validate_parameters(
        self, search_area: Union[Dict[Any, Any], List[Any]], prefix: str = ""
    ) -> Optional[str]:
        """Finds the parameters in YAML file not accepted by the interpreter"""
        result: Optional[str] = None
        valid_parameters: KeysView[str] = self._valid_parameters.keys()
        full_key: str = ""

        if prefix != "":
            prefix = str(f"{prefix}.")
            vInfo(self._verbose, f"New prefix `{prefix}`")

        if type(search_area) == list:
            vInfo(self._verbose, "`search_area` is a list")
            for value in search_area:
                vInfo(self._verbose, f"Testing parameter `{value}`")
                if f"{prefix}*" in valid_parameters:
                    vInfo(self._verbose, f"`{value}` has been found as `{prefix}*`")
                    full_key = str(f"{prefix}*")
                elif f"{prefix}{value}" in valid_parameters:
                    full_key = str(f"{prefix}{value}")
                    vInfo(
                        self._verbose, f"`{value}` has been found as `{prefix}{value}`"
                    )

                if len(full_key) > 0:
                    vInfo(
                        self._verbose,
                        f"The value of parameter `{full_key}` is type {type(value)}",
                    )
                    if type(value) == self._valid_parameters[full_key]:
                        vInfo(
                            self._verbose,
                            f"`{type(value)}` is a valid type for parameter `{full_key}`",
                        )
                    else:
                        click.echo(
                            f"`{value}` expected to be type `{self._valid_parameters[full_key]}` "
                            + f"but received `{type(value)}`"
                        )
                        return full_key
                else:
                    vInfo(self._verbose, f"`{value}` is not a valid parameter")
                    return full_key

        elif type(search_area) == dict:
            vInfo(self._verbose, "`search_area` is a dict")
            for key, values in search_area.items():
                vInfo(self._verbose, f"Testing parameter `{key}`")
                if f"{prefix}*" in valid_parameters:
                    vInfo(self._verbose, f"`{key}` has been found as `{prefix}*`")
                    full_key = str(f"{prefix}*")
                elif f"{prefix}{key}" in valid_parameters:
                    full_key = str(f"{prefix}{key}")
                    vInfo(self._verbose, f"`{key}` has been found as `{prefix}{key}`")

                if len(full_key) > 0:
                    vInfo(
                        self._verbose,
                        f"The value of parameter `{prefix}{key}` is type {type(values)}",
                    )
                    if type(values) == self._valid_parameters[full_key]:
                        vInfo(
                            self._verbose,
                            f"`{type(values)}` is a valid type for parameter `{prefix}{key}`",
                        )
                    else:
                        click.echo(
                            f"`{key}` expected to be type `{self._valid_parameters[full_key]}` "
                            + f"but received `{type(values)}`"
                        )
                        return full_key

                    if type(values) == dict or type(values) == list:
                        vInfo(self._verbose, f"Analysing subparameters of `{key}`")
                        vCall(self._verbose, "Interpreter:validate_parameters")
                        next_prefix: str = str(
                            f"{prefix}*"
                            if f"{prefix}*" in valid_parameters
                            else f"{prefix}{key}"
                        )
                        result = self.validate_parameters(values, next_prefix)
                        vResponse(
                            self._verbose, "Interpreter:validate_parameters", result
                        )
                        if result is not None:
                            vInfo(self._verbose, f"`{key}` has an invalid subparameter")
                            return result
                else:
                    vInfo(self._verbose, f"`{key}` is not a valid parameter")
                    return full_key

        else:
            raise TypeError(
                f"`search_area` expected to be dict or list, `{type(search_area)}` received."
            )

        return None


cdef class Interpreter_1(Interpreter):
    """Interpreter that implements the rules for YAML version 1.0"""

    def __init__(self, context: Path, verbose: bool):
        super(Interpreter_1, self).__init__(
            context=context,
            required_parameters=[
                # 'version', # Already validated to get the right interpreter
                "project",
                "project.*",  # `project` needs to have ANY value - not empty
                "project.*.include",
                "project.*.include.*",
            ],
            valid_parameters={
                # 'fieldname': type,
                "version": str,
                "project": dict,
                "project.*": dict,
                # 'project.*.cron': str,
                # 'project.*.encrypt': list,
                # 'project.*.encrypt.*': str,
                "project.*.exclude": list,
                "project.*.exclude.*": str,
                "project.*.include": list,
                "project.*.include.*": str,
                # 'project.*.password': str,
            },
            verbose=verbose,
            version= b'1',
        )

    cpdef bint create_backup(self, yaml_config, project):
        """Create a new backup"""

        initiated: bool = self._validate_prev_init(yaml_config)
        if not initiated:
            return False
        
        backup_list: List[str] = []
        working_directories: Dict[str, str]

        # Make context relative
        context: str = str(self._context)
        if not context.endswith(os.sep):
            context += os.sep

        # Select project(s) to backup
        if project == "":
            backup_list = yaml_config["project"].keys()
        else:
            backup_list.append(project)
        
        # Create each backup
        for backup in backup_list:

            working_directories = {}
            vCall(self._verbose, "Interpreter_1:_working_directories")
            working_directories.update(
                self._working_directories(yaml_config["project"][backup])
            )
            vResponse(
                self._verbose,
                "Interpreter_1:_working_directories",
                working_directories,
            )

            # Create DB backup
            db: RunupDB = RunupDB(self._context, self._verbose)
            vCall(self._verbose, "RunupDB:insert_job")
            job_id: bool = db.insert_job(backup)
            vResponse(self._verbose, "RunupDB:insert_job", job_id)
            
            # Zip File
            with zipfile.ZipFile(f"{context}.runup/jobs/{job_id}", "w") as my_zip:

                for path_from_pwd, path_from_yaml_file in working_directories.items():

                    vCall(self._verbose, "RunupDB:insert_file")
                    inserted_new: bool = db.insert_file(
                        job_id, 
                        bytes(path_from_pwd, 'utf-8'),
                        path_from_yaml_file
                    )
                    vResponse(self._verbose, "RunupDB:insert_file", inserted_new)
                    
                    if inserted_new:
                        vInfo(self._verbose, f"Zipping file: {path_from_pwd}")
                        my_zip.write(path_from_pwd, path_from_yaml_file)
                    else:
                        vInfo(self._verbose, f"Not zipping file: {path_from_pwd}")

        return True

    def restore_backup(
        self,
        yaml_config: Dict[str, Any],
        project: str,
        location: str,
        job: int,
        force: bool,
    ) -> Optional[bool]:
        """Restore a backup"""

        initiated: bool = self._validate_prev_init(yaml_config)
        if not initiated:
            return None

        if project != "":
            projects = [project]
        else:
            projects = yaml_config["project"].keys()

        # Make context relative
        context: str = str(self._context)
        if not context.endswith(os.sep):
            context += os.sep

        for project_name in projects:

            # Read DB backup
            db: RunupDB = RunupDB(self._context, self._verbose)
            vCall(self._verbose, "RunupDB:select_job")
            job_data = db.select_job(job, project_name)
            vResponse(self._verbose, "RunupDB:select_job", job_data)

            if len(job_data) == 0:
                click.secho(
                    f'The project "{project_name}" is not part of the job {job}.',
                    fg="red",
                )
                continue

            if not force:
                confirmation: str = ""
                while confirmation not in ["yes", "y", "no", "n"]:
                    confirmation = input(
                        f'Are you sure you want to restore the project "{project_name}"? [Y/n] '
                    )
                    confirmation = confirmation.lower()

                if confirmation == "n" or confirmation == "no":
                    continue

            # Dictionary with location of data.
            # ------------------------------------------------------
            # The key is the id of the job where the file is located
            # and the value is another dictionary where its key is
            # the path of the destination file and the value is the
            # path of the file in the job.
            restoration_source: Dict[str, Dict[str, str]] = {}

            for (
                job_if_original,
                path_if_original,
                job_if_copy,
                path_if_copy,
            ) in job_data:
                if job_if_copy is not None:
                    if job_if_copy not in restoration_source:
                        restoration_source[job_if_copy] = {}
                    restoration_source[job_if_copy][path_if_original] = path_if_copy
                else:
                    if job_if_original not in restoration_source:
                        restoration_source[job_if_original] = {}
                    restoration_source[job_if_original][
                        path_if_original
                    ] = path_if_original

            for job_id, file_dict in restoration_source.items():
                with zipfile.ZipFile(f"{context}.runup/jobs/{job_id}") as myzip:
                    for dst, src in file_dict.items():

                        while src.startswith("./"):
                            src = src[2:]

                        while dst.startswith("./"):
                            dst = dst[2:]
                        dst = str(f"{location.strip('/')}/{dst}")

                        # Try to get File info
                        try:
                            src_info = myzip.getinfo(src)
                        # If is an empty directory
                        except KeyError:
                            dst = f"{context}{dst}"
                            if not os.path.exists(dst):
                                os.mkdir(dst)
                        # else
                        else:
                            src_info.filename = dst
                            myzip.extract(src_info)

            click.secho(
                f'A backup for the project "{project_name}" has been restored.',
                fg="green",
            )

        return True

    def missing_parameter(
        self, yaml_config: Dict[str, Any], search_area: Optional[List[str]] = None
    ) -> Optional[str]:
        """Analyse a parameter to confirm if is missing or not"""

        if search_area is None:
            search_area = self._required_parameters

        for parameter in search_area:
            vInfo(self._verbose, f"Analysing parameter `{parameter}`")
            vCall(self._verbose, "Interpreter_1:missing_parameter_part")
            missing_part: Optional[str] = self.missing_parameter_part(
                yaml_config, parameter
            )
            vResponse(
                self._verbose, "Interpreter_1:missing_parameter_part", missing_part
            )
            if missing_part:
                vInfo(self._verbose, f"missing parameter part `{missing_part}`")
                return missing_part

        return None

    def missing_parameter_part(
        self, search_area: Dict, parameter: str
    ) -> Optional[str]:
        """Analyse each part of a parameter looking for missing parts."""

        if "." not in parameter:
            vInfo(
                self._verbose, f"Parameter `{parameter}` doesn't have sub-paramenters"
            )
            if parameter == "*":
                if search_area is not None and len(search_area) > 0:
                    vInfo(
                        self._verbose,
                        f"YAML file cointains {len(search_area)} parameters.",
                    )
                    return None
                elif search_area is not None:
                    vInfo(self._verbose, "YAML file cointains no parameters.")
                    return "*"
                else:
                    vInfo(self._verbose, "YAML file cointains no parameters.")
                    return None
            elif parameter not in search_area.keys():
                vInfo(
                    self._verbose,
                    f"Single parameter `{parameter}` not found in search area",
                )
                return parameter
        else:
            vInfo(self._verbose, f"Parameter `{parameter}` have sub-paramenters")
            missing: Optional[str] = None

            parts = parameter.split(".", 1)
            vInfo(
                self._verbose,
                f"Search `{parts[0]}` in search_area {list(search_area.keys())}",
            )
            if (parts[0] == "*" and len(search_area) > 0) or parts[
                0
            ] in search_area.keys():
                vInfo(
                    self._verbose, f"Parameter part `{parts[0]}` found in search area."
                )

                if parts[0] != "*":
                    vCall(self._verbose, "Interpreter_1:missing_parameter_part")
                    missing = self.missing_parameter_part(
                        search_area[parts[0]], parts[1]
                    )
                    vResponse(
                        self._verbose, "Interpreter_1:missing_parameter_part", missing
                    )
                else:
                    for element in search_area.keys():
                        vCall(self._verbose, "Interpreter_1:missing_parameter_part")
                        missing = self.missing_parameter_part(
                            search_area[element], parts[1]
                        )
                        vResponse(
                            self._verbose,
                            "Interpreter_1:missing_parameter_part",
                            missing,
                        )
                        if missing is not None:
                            break

                if missing is None:
                    return None
                elif missing == "*":
                    if parameter.endswith(".*"):
                        return f"*{parameter[0:-2]}"
                    else:
                        return f"*.{parameter}"
                else:
                    return f"{parameter}"
            else:
                vInfo(
                    self._verbose,
                    f"Parameter part `{parts[0]}` not found in search area",
                )
                return parts[0]

        return None

    def set_environment(self) -> bool:
        """
        Create the backup enviroment.

        Creates a directory `.runup` at context level. In it
        creates a `.version` that only contains a number `1`
        and creates a SQLite database named `runup.db`.
        """

        vInfo(self._verbose, "Setting environment.")

        # Create the directory `.runup`
        if not os.path.exists(f"{self._context}/.runup"):
            os.mkdir(f"{self._context}/.runup")
            vInfo(self._verbose, f"Created directory {self._context}/.runup")
        else:
            vInfo(
                self._verbose, f"The directory `{self._context}/.runup` already exists."
            )
            click.echo("RunUp is already initiated.")
            return False

        # Create file `.version`
        # TODO: Convert this into a function the `version.pyx` file.
        with open(f"{str(self._context)}/.runup/.version", "w") as file:
            file.write(self._version.decode())
        vInfo(self._verbose, f"Created file `{self._context}/.runup/.version`")

        # Create the directory `.runup`
        if not os.path.exists(f"{self._context}/.runup/jobs"):
            os.mkdir(f"{self._context}/.runup/jobs")
            vInfo(self._verbose, f"Created directory `{self._context}/.runup/jobs`")
        else:
            vInfo(
                self._verbose,
                f"The directory `{self._context}/.runup/jobs` already exists.",
            )
            click.echo("RunUp is already initiated.")
            return False

        # Create database
        RunupDB(self._context, self._verbose).create_database()

        if self._verbose:
            click.echo("-" * 10)

        return True

    def validate_parameters(
        self, yaml_config: Union[Dict[Any, Any], List[Any]], prefix: str = ""
    ) -> Optional[str]:
        return super().validate_parameters(yaml_config, prefix)

    def _validate_prev_init(self, yaml_config: Dict[str, Any]):
        """Validate RunUp has been previously initialized."""

        if not os.path.exists(f"{self._context}/.runup"):
            click.echo("RunUp has not been initialized.")
            return False

        for project in yaml_config["project"].keys():
            vCall(self._verbose, "RunupDB.insert_backup")
            db = RunupDB(self._context, self._verbose)
            db.insert_backup(project)
            vResponse(self._verbose, "RunupDB.insert_backup", None)

        return True

    cdef _working_directories(self, config: Dict[str, Any]): # -> Dict[str, str]:
        """Select the working directories based on the `include` and `exclude` on the YAML file."""

        # cdef char* filepath

        tmp_bytes:bytes
        directories: Dict[str, str] = {}
        exclude_list: List[str] = []
        exclude_list_slash: List[str] = []
        include_dict: Dict[str, str] = {}

        for inc in config["include"]:
            inc_os = inc.replace("/", os.sep)
            include_dict[os.path.join(self._context, inc_os)] = inc.replace(os.sep, "/")

        if "exclude" in config:
            exclude_list = [
                os.path.join(self._context, exc.replace("/", os.sep))
                for exc in config["exclude"]
            ]
            for element in exclude_list:
                if element.endswith(os.sep):
                    exclude_list_slash.append(element)
                else:
                    exclude_list_slash.append(element + os.sep)

        exclude_tuple_slash: Tuple = tuple(exclude_list_slash)

        for include_str in include_dict.keys():
            if os.path.isfile(include_str):
                vInfo(
                    self._verbose,
                    f"`{include_str}` is a file. Including it into workspace.",
                )
                directories[include_str] = os.path.relpath(
                    include_str, self._context
                ).replace(os.sep, "/")
            else:
                # traverse root directory as root, and list directories as _ and files as files
                for root, _, files in os.walk(include_str):
                    if (
                        not (root + os.sep).startswith(exclude_tuple_slash)
                        and root not in exclude_list
                        and ".runup" not in root.split(os.sep)
                    ):
                        vInfo(
                            self._verbose,
                            f"Including directory `{root}` into workspace.",
                        )
                        # directories[root] = include_dict[root]
                        if len(files) == 0:
                            vInfo(
                                self._verbose,
                                f"Including empty directory `{root}` into workspace",
                            )
                            directories[root] = os.path.relpath(
                                root, self._context
                            ).replace(os.sep, "/")
                        else:
                            for file in files:

                                filepath:str = root + os.sep + file
                                
                                if filepath in exclude_list or file in [
                                    b"runup.yml",
                                    b"runup.yaml",
                                ]:
                                    vInfo(
                                        self._verbose,
                                        f"Ignoring file `{filepath}` from workspace.",
                                    )
                                else:
                                    vInfo(
                                        self._verbose,
                                        f"Including file `{filepath}` into workspace.",
                                    )
                                    directories[filepath] = os.path.relpath(
                                        filepath, self._context
                                    ).replace(os.sep, "/")
                    else:
                        vInfo(
                            self._verbose, f"Ignoring directory `{root}` from workspace"
                        )

        return directories
