#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Repository tests.
"""

import os
import shutil
import tempfile
import unittest

from pyrepo import (Repository, RepoImporter, git_command, 
    ImportPathError, hg_command)
from test_utils import makeGitSourceRepo

class InitRepositoryTestCase(unittest.TestCase):

    def test_init_command_and_url(self):
        command = git_command
        url = "https://github.com/dghubble/pyrepo"
        repo = Repository(command=command, url=url)
        self.assertEqual(command.name, repo.command.name)
        self.assertEqual(url, repo.url)
        self.assertEqual(None, repo.import_path)

    def test_init_import_path(self):
        import_path = "github.com/dghubble/pyrepo"
        repo = Repository(import_path=import_path)
        self.assertEqual(git_command.name, repo.command.name)
        expected_url = "https://github.com/dghubble/pyrepo"
        self.assertEqual(expected_url, repo.url)
        self.assertEqual(import_path, repo.import_path)

    def test_init_prefer_command(self):
        """
        When the `import_path` must be resolved, but a command was
        given directly, prefer the command argument to the resolved
        command.
        """
        command = hg_command
        import_path = "github.com/dghubble/pyrepo"
        repo = Repository(command=command, import_path=import_path)
        self.assertEqual(command.name, repo.command.name)

    def test_init_prefer_url(self):
        """
        When the `import_path` must be resolved, but a url was
        given directly, prefer the url argument over the resolved url.
        """
        url = "https://preferred_url"
        import_path = "github.com/dghubble/pyrepo"
        repo = Repository(url=url, import_path=import_path)
        self.assertEqual(url, repo.url)

    def test_init_invalid_import_path(self):
        # general invalid path
        self.assertRaises(ImportPathError, Repository, 
            import_path="://invalid_path")
        # path matches no host start patterns
        self.assertRaises(ImportPathError, Repository, 
            import_path="gggiiitthub.com/")
        # path matches a host's start, but not pattern
        self.assertRaises(ImportPathError, Repository, 
            import_path="github.com/missingproj")
        self.assertRaises(ImportPathError, Repository, 
            import_path="github.com/missingproj/")
        self.assertRaises(ImportPathError, Repository, 
            import_path="bitbucket.org/missingproj")
        self.assertRaises(ImportPathError, Repository, 
            import_path="bitbucket.org/missingproj/")

    def test_init_missing_arguments(self):
        # missing url, missing import_path to resolve url
        self.assertRaises(ValueError, Repository,
            command=git_command)
        # missing command, missing import_path to resolve url
        self.assertRaises(ValueError, Repository,
            url="https://github.com/dghubble/pyrepo")
        # missing arguments for resolving command and url
        self.assertRaises(ValueError, Repository)


class RepositoryTestCase(unittest.TestCase):
    """
    Tests the `Repository` class.
    """

    def setUp(self):
        """
        Setup a temporary Git repository and directory to clone into.
        Ensure tearDown removes these directories.
        """
        self.repo_dir = tempfile.mkdtemp() # repo on local filesystem
        makeGitSourceRepo(self.repo_dir)   # make a few test commits
        self.target = tempfile.mkdtemp()   # clone/create into this dir
        self.repo = Repository(command=git_command, url=self.repo_dir)

    def tearDown(self):
        """Teardown after each test"""
        shutil.rmtree(self.repo_dir)
        shutil.rmtree(self.target)

    def test_clone(self):
        self.repo.clone(self.target)
        repo_file = os.path.join(self.target, "TESTFILE.txt")
        self.assertTrue(os.path.isfile(repo_file))
        with open(repo_file) as f:
            self.assertTrue('Version 1' in f.read())

    def test_update_already_updated(self):
        self.repo.clone(self.target)
        (stdout, stderr) = self.repo.update(self.target)
        self.assertEqual('Already up-to-date.\n', 
                         stdout.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
