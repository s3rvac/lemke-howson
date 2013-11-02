#!/usr/bin/env python
# vim:fileencoding=utf8
#
# Project: Implementation of the Lemke-Howson algorithm for finding MNE
# Author:  Petr Zemek <s3rvac@gmail.com>, 2009
#

"""Runs a program which computes MNE in the given 2-player game
using the Lemke-Howson algorithm.
"""


import sys


def main():
    try:
        # These imports must be here because of possible
        # SyntaxError exceptions in different versions of python
        # (this program needs python 2.5)
        import src.io
        import src.lh

        # Check program arguments (there should be none)
        if len(sys.argv) > 1:
            stream = sys.stderr
            if sys.argv[1] in ['-h', '--help']:
                stream = sys.stdout
            src.io.printHelp(stream)
            return 1

        # Obtain input matrices from the standard input
        m1, m2 = src.io.parseInputMatrices(sys.stdin.read())

        # Compute the equilibirum
        eq = src.lh.lemkeHowson(m1, m2)

        # Print both matrices and the result
        src.io.printGameInfo(m1, m2, eq, sys.stdout)

        return 0
    except SyntaxError:
        sys.stderr.write('Need python 2.5 to run this program.\n')
    except Exception, e:
        sys.stderr.write('Error: ' + e.message + '\n')
        return 1


if __name__ == '__main__':
    main()
