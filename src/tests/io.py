# vim:fileencoding=utf8
#
# Project: Implementation of the Lemke-Howson algorithm for finding MNE
# Author:  Petr Zemek <s3rvac@gmail.com>, 2009
#

import unittest
import sys
import tempfile

from .. import io
from .. import matrix as m
from .. import rational as r


class ParseInputMatricesTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def scenarioValidMatricesAreParsedCorrectly(self, text, expM1, expM2):
        m1, m2 = io.parseInputMatrices(text)
        self.assertEqual(repr(expM1), repr(m1))
        self.assertEqual(repr(expM2), repr(m2))

    def testParseTwo11Matrices(self):
        text = '1\n\n1\n'
        expM1 = m.fromText('1\n')
        expM2 = m.fromText('1\n')
        self.scenarioValidMatricesAreParsedCorrectly(text, expM1, expM2)

    def testParseTwo11MatricesRedundantNewLines(self):
        text = '1\n\n1\n\n\n\n'
        expM1 = m.fromText('1\n')
        expM2 = m.fromText('1\n')
        self.scenarioValidMatricesAreParsedCorrectly(text, expM1, expM2)

    def testParseTwo33Matrices(self):
        text = '1 2 3\n4 5 6\n7 8 9\n\n9 8 7\n6 5 4\n3 2 1\n'
        expM1 = m.fromText('1 2 3\n4 5 6\n7 8 9\n')
        expM2 = m.fromText('9 8 7\n6 5 4\n3 2 1\n')
        self.scenarioValidMatricesAreParsedCorrectly(text, expM1, expM2)

    def scenarioValueErrorIsRaisedOnInvalidText(self, text):
        try:
            io.parseInputMatrices(text)
        except ValueError:
            pass
        else:
            self.fail('ValueError should have been thrown.')

    def testValueErrorIsRaisedOnEmptyText(self):
        self.scenarioValueErrorIsRaisedOnInvalidText('')

    def testValueErrorIsRaisedOnSingleNewLine(self):
        self.scenarioValueErrorIsRaisedOnInvalidText('\n')

    def testValueErrorIsRaisedOnInvalidFirstMatrix(self):
        self.scenarioValueErrorIsRaisedOnInvalidText('x\n\n1\n')

    def testValueErrorIsRaisedOnInvalidSecondMatrix(self):
        self.scenarioValueErrorIsRaisedOnInvalidText('1\n\nx')

    def testValueErrorIsRaisedOnMissingSecondMatrix(self):
        self.scenarioValueErrorIsRaisedOnInvalidText('1\n\n')

    def testValueErrorIsRaisedOnMissingExtraNewLine(self):
        self.scenarioValueErrorIsRaisedOnInvalidText('1\n1\n')

    def testValueErrorIsRaisedOnRedundantCharactes(self):
        self.scenarioValueErrorIsRaisedOnInvalidText('1\n\n1\n\nfgh\n\n')

    def testValueErrorIsRaisedOnDifferentNumberOfRows(self):
        self.scenarioValueErrorIsRaisedOnInvalidText('1 2\n3 4\n5 6\n\n4 5\n6 7\n')

    def testValueErrorIsRaisedOnDifferentNumberOfCols(self):
        self.scenarioValueErrorIsRaisedOnInvalidText('1 2 3\n4 5 6\n\n4 5\n6 7\n')


class PrintEquilibriumTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def scenarioEquilibriumIsPrintedCorrectly(self, eq, expEqText):
        class StreamStub(object):
            def __init__(self):
                self.data = ''
            def write(self, data):
                self.data += data
        stream = StreamStub()
        io.printEquilibrium(eq, stream)
        self.assertEqual(expEqText, stream.data)

    def testEquilibriumWithMoreThanOneStrategyForBothPlayersIsPrintedAsIs(self):
        eq = ((r.Rational(1, 2), r.Rational(1, 2)),
              (r.Rational(1, 2), r.Rational(1, 2)))
        self.scenarioEquilibriumIsPrintedCorrectly(eq, '((1/2, 1/2), (1/2, 1/2))')

    def testEquilibriumWithOneStrategyForAPlayerHasCommaRemoved(self):
        eq = ((r.Rational(1, 2),), (r.Rational(1, 2),))
        self.scenarioEquilibriumIsPrintedCorrectly(eq, '((1/2), (1/2))')

    def test1Slash1IsReplacedWith1(self):
        eq = ((r.Rational(1, 1),), (r.Rational(1, 2), r.Rational(1, 2)))
        self.scenarioEquilibriumIsPrintedCorrectly(eq, '((1), (1/2, 1/2))')

    def test0Slash1IsReplacedWith1(self):
        eq = ((r.Rational(0, 1),), (r.Rational(1, 2), r.Rational(1, 2)))
        self.scenarioEquilibriumIsPrintedCorrectly(eq, '((0), (1/2, 1/2))')


def suite():
    """Returns a test suite that contains all tests from this module."""
    return unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])


def test():
    """Runs all unit tests for this module."""
    runner = unittest.TextTestRunner()
    runner.run(suite())


if __name__ == '__main__':
    test()
