#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Package tests
"""

import unittest
import shutil
import tempfile
import subprocess
import os
import re

from pyrepo import RepoImporter, Command, Host, git_command
from test_utils import makeGitSourceRepo

class GitCommandTestCase(unittest.TestCase):
    """
    Tests the `Command` class.
    """ 

    def setUp(self):
        """
        Setup a temporary Git repository and directory to clone into.
        Ensure tearDown removes these directories.
        """
        self.repo_dir = tempfile.mkdtemp() # repo on local filesystem
        makeGitSourceRepo(self.repo_dir)   # make a few test commits
        self.target = tempfile.mkdtemp()   # clone/create into this dir
        self.git = git_command

    def tearDown(self):
        """Teardown after each test"""
        shutil.rmtree(self.repo_dir)
        shutil.rmtree(self.target)

    def test_clone(self):
        self.git.clone(self.repo_dir, self.target)
        repo_file = os.path.join(self.target, "TESTFILE.txt")
        self.assertTrue(os.path.isfile(repo_file))
        with open(repo_file) as f:
            self.assertTrue('Version 1' in f.read())

    # TODO: test update once sync to commit implemented
    # TODO: test does not perform non-ff updates

    def test_update_already_updated(self):
        self.git.clone(self.repo_dir, self.target)
        (stdout, stderr) = self.git.update(self.target)
        self.assertEqual('Already up-to-date.\n', 
                         stdout.decode('utf-8'))

    # def test_tags(self):
    #     self.git.clone(self.repo_dir, self.target)
    #     tags = self.git.tag_list(cwd=self.target)
    #     expected_tags = ["master", "v0.0.2", "v0.0.3"]
    #     self.assertEqual(set(expected_tags), set(tags))


# TODO: test importer with different host and command sets
class RepoImporterTestCase(unittest.TestCase):

    def setUp(self):
        self.importer = RepoImporter()
        pass

    def test_github_import_name(self):
        import_path = "github.com/dghubble/python-role"
        (command, url) = self.importer.resolve(import_path)
        self.assertEqual("git", command.name)
        self.assertEqual("https://github.com/dghubble/python-role", 
            url)

    def test_bitbucket_import_name(self):
        import_path = "bitbucket.org/dghubble/role-template"
        (command, url) = self.importer.resolve(import_path)
        self.assertEqual("git", command.name)
        self.assertEqual("https://bitbucket.org/dghubble/role-template", 
            url)

if __name__ == '__main__':
    unittest.main()





