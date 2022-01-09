"""
Module to check requirements for used and unused packages.
"""
import os
import time
from datetime import datetime
import pandas as pd
from .parse_tree_freeze import parse_tree_freeze


class CheckProj:
    """
    Class used to check if requirements are used in a project.
    Steps:
        1. Then checks IMPORT statements of files in modules
        2. Then updates whether a requirement was used
        3. Exports to a csv (requirements.csv)
            a. 0 = not used
            b. 1 = used
        4. If an import is used but not in requirements.txt
            it is added to not_in_requirements.txt
            1 column.
            All packages in the file are used.
    Inputs:
        base = lint_dir directory of the project
    """

    def __init__(self, lint_dir):
        self.now = str(time.mktime(datetime.now().timetuple()))[:-2]
        self.lint_dir = lint_dir
        self.proj = os.path.dirname(lint_dir)
        self.req = parse_tree_freeze(self.proj)
        self.not_in_req = pd.Series(name='pkg')

    def parse_project_file(self, imports):
        """
        Checks each individual file for the used and unused packages
        Changes used from 0 to 1 if used.
        If it is used once then we should not remove it once iteration is over

        :param imports: pandas Series fille with the import statments
        """
        # removes excess words only keep package name
        pkgs = imports.str.split(" ", expand=True)[1]
        # account for imports like from django.db import blah
        pkgs = pkgs.str.split('.', expand=True)[0]
        # from .lint import Lint would cause an error because nothing there
        # ["", "lint"]
        # this gets rid of those blank imports
        pkgs = pkgs[pkgs != ""]
        pkgs.reset_index(drop=True)
        req_pkgs = pkgs[pkgs.isin(self.req.index)]
        if req_pkgs.any():
            # where this index matches in the requirements df change it to 1
            self.req.at[req_pkgs, 'used'] = 1
        else:
            # ~ is a bitwise not in python means not in requirements below
            not_req_pkgs = pkgs[~pkgs.isin(self.req.index)]
            not_req_pkgs = not_req_pkgs.rename('pkg')
            # if there is nothing then it just appends nothing so nothing happens
            self.not_in_req = self.not_in_req.append(not_req_pkgs, ignore_index=True)
            # make a huge series. we'll drop duplicates at the end b4 exporting

    def loop_dir(self, directory):
        """
        Recursively look through directories
        This is pretty pointless I just thought
        there was too much indentation

        :param directory: directory name
        """
        for file_or_dir in os.listdir(directory):
            self.route_file_dir(directory, file_or_dir)

    def check_if_empty_file(self, f_name):
        """
        completelely empty files returns an error
        This checks for the empty files or empty imports before parsing
        :param  f_name: filename
        """
        with open(f_name, 'r') as file:
            lines = [line for line in file]
            lines = pd.Series(lines)
            # checks for any empty files
            # empty files causes crashes
            if lines.any():
                lines = lines.str.strip()
                # import statement starts with import
                i_import = lines[lines.str.startswith('import')]
                # import statement starts with from
                f_import = lines[lines.str.startswith('from')]
                # all import statments
                a_imports = i_import.append(f_import)
                # checks for any blank imports
                # no lines that start with import or from
                if a_imports.any():
                    self.parse_project_file(a_imports)

    def route_file_dir(self, parent_dir, file_or_dir):
        """
        :param file_or_dir: file or directory name
        :param parent_dir: parent directory name
        """
        # full file path
        parent_w_child = os.path.join(parent_dir, file_or_dir)
        if len(file_or_dir.split(".")) == 1:  # if it's a directory
            # 'proj'.split(".") => ['proj'] => len == 1
            self.loop_dir(parent_w_child)
        elif file_or_dir.split(".")[1] == 'py':  # it's a py file
            # 'check.py'.split(".") => ['Check', 'py'] => len == 2
            self.check_if_empty_file(parent_w_child)
        else:  # it's a reg  file
            pass

    def export(self):
        """
        Creates two files
        requirements-now.csv:
            contains all the packages from the requirements and 0 if not used 1 if used
        not_in_requirements-now.csv:
            IMPORT statements that were not declared in requirement.txt but were used
        """
        req_csv = os.path.join(self.lint_dir, 'requirements-'+self.now+'.csv')
        print('exporting to ' + req_csv)
        self.req.to_csv(req_csv)
        not_req_csv = os.path.join(self.lint_dir, 'not_in_requirements-'+self.now+'.csv')
        self.not_in_req.drop_duplicates(keep='first', inplace=True)
        print('exporting to ' + not_req_csv)
        self.not_in_req.to_csv(not_req_csv, index=False)

    def run(self):
        """
        Main function to run program
        Loops through all the directories
        """
        print('checking for unused requirements')
        proj_files = [x for x in os.listdir(self.proj) if x not in ['lint_dir']]
        for file_or_dir in proj_files:
            self.route_file_dir(self.proj, file_or_dir)

        self.export()
        print('check done')
