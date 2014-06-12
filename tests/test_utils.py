#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Utilities to aid in testing.
"""

import subprocess
import os

from pyrepo import git_command

def makeGitSourceRepo(directory):
    """
    Setup a testing Git repository with some test commits and tags.
    :param str directory: directory in which a test Git repo should be 
        created
    """
    test_file = 'TESTFILE.txt'
    with open(os.path.join(directory, test_file), 'w') as f:
        f.write('Version 0')
    git_command.init(directory)
    subprocess.Popen(
        "git config user.name 'Tester'".split(),
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        cwd=directory).communicate()
    subprocess.Popen(
        "git config user.email 'test@test.com'".split(),
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        cwd=directory).communicate()
    git_command.add(test_file, dir=directory)
    git_command.commit('Initial', dir=directory)
    with open(os.path.join(directory, test_file), 'w') as f:
        f.write('Version 1')
    git_command.add(test_file, dir=directory)
    git_command.commit('Release', dir=directory)
