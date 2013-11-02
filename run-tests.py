#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Project: Implementation of the Lemke-Howson algorithm for finding MNE
# Author:  Petr Zemek <s3rvac@gmail.com>, 2009
#

"""Runs all project unit tests."""


import sys


def main():
    """Runs all project unit tests."""
    try:
        # These imports must be here because of possible
        # SyntaxError and AttributeError exceptions in different
        # versions of python (this program needs python 2.5)
        import unittest
        import src.tests

        # Gather all tests
        allTests = [src.tests.suite()]

        # Run them
        runner = unittest.TextTestRunner()
        runner.run(unittest.TestSuite(allTests))
    except AttributeError:
        sys.stderr.write('Need python 2.5 to run this program.\n')
    except SyntaxError:
        sys.stderr.write('Need python 2.5 to run this program.\n')


if __name__ == '__main__':
    main()
