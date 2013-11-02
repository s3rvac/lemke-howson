# vim:fileencoding=utf8
#
# Project: Implementation of the Lemke-Howson algorithm for finding MNE
# Author:  Petr Zemek <s3rvac@gmail.com>, 2009
#

import unittest
import sys

from .. import matrix
from .. import rational as r


class MatrixTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def scenarioGetNumRowsAndColsReturnsCorrectNumber(self, rows, cols):
        m = matrix.Matrix(rows, cols)
        self.assertEqual(rows, m.getNumRows())
        self.assertEqual(cols, m.getNumCols())

    def testGetNumRowsAndColsReturnsCorrectNumber11(self):
        self.scenarioGetNumRowsAndColsReturnsCorrectNumber(1, 1)

    def testGetNumRowsAndColsReturnsCorrectNumber24(self):
        self.scenarioGetNumRowsAndColsReturnsCorrectNumber(2, 4)

    def testGetNumRowsAndColsReturnsCorrectNumber55(self):
        self.scenarioGetNumRowsAndColsReturnsCorrectNumber(5, 5)

    def scenarioValueErrorIsThrownOnInvalidMatrixDimension(self, rows, cols):
        try:
            matrix.Matrix(rows, cols)
        except ValueError:
            pass
        else:
            self.fail('ValueError should have been thrown.')

    def testValueErrorIsThrownOnNegativeRows(self):
        self.scenarioValueErrorIsThrownOnInvalidMatrixDimension(-1, 4)

    def testValueErrorIsThrownOnNegativeCols(self):
        self.scenarioValueErrorIsThrownOnInvalidMatrixDimension(4, -1)

    def testValueErrorIsThrownOnZeroRows(self):
        self.scenarioValueErrorIsThrownOnInvalidMatrixDimension(0, 3)

    def testValueErrorIsThrownOnZeroCols(self):
        self.scenarioValueErrorIsThrownOnInvalidMatrixDimension(3, 0)

    def scenarioMatrixElementsAreInitializedToZeroAfterMatrixCreation(self, rows, cols):
        m = matrix.Matrix(rows, cols)
        for i in xrange(1, rows + 1):
            for j in xrange(1, cols + 1):
                self.assertEqual(0, m.getItem(i, j))

    def testMatrixElementsAreInitializedToZeroAfterMatrixCreation11(self):
        self.scenarioMatrixElementsAreInitializedToZeroAfterMatrixCreation(1, 1)

    def testMatrixElementsAreInitializedToZeroAfterMatrixCreation19(self):
        self.scenarioMatrixElementsAreInitializedToZeroAfterMatrixCreation(1, 9)

    def testMatrixElementsAreInitializedToZeroAfterMatrixCreation91(self):
        self.scenarioMatrixElementsAreInitializedToZeroAfterMatrixCreation(9, 2)

    def scenarioIndexErrorIsThrownWhenAccessingNonExistingElement(self, m, i, j):
        try:
            m.getItem(i, j)
        except IndexError:
            pass
        else:
            self.fail('IndexError should have been thrown.')

    def testIndexErrorIsThrownWhenAccesingNegativeRow(self):
        m = matrix.Matrix(3, 3)
        self.scenarioIndexErrorIsThrownWhenAccessingNonExistingElement(m, -1, 1)

    def testIndexErrorIsThrownWhenAccesingNegativeCol(self):
        m = matrix.Matrix(3, 3)
        self.scenarioIndexErrorIsThrownWhenAccessingNonExistingElement(m, 1, -1)

    def testIndexErrorIsThrownWhenAccesingTooHighRow(self):
        m = matrix.Matrix(3, 3)
        self.scenarioIndexErrorIsThrownWhenAccessingNonExistingElement(m, 10, 1)

    def testIndexErrorIsThrownWhenAccesingTooHighCol(self):
        m = matrix.Matrix(3, 3)
        self.scenarioIndexErrorIsThrownWhenAccessingNonExistingElement(m, 1, 10)

    def scenarioGetElementReturnsCorrectValueAfterThatElementIsSet(self, m, i, j, v):
        m.setItem(i, j, v)
        self.assertEqual(v, m.getItem(i, j))

    def testGetElementReturnsCorrectValueAfterThatElementIsSet11(self):
        m = matrix.Matrix(1, 1)
        self.scenarioGetElementReturnsCorrectValueAfterThatElementIsSet(m, 1, 1, 5)

    def testGetElementReturnsCorrectValueAfterThatElementIsSet19(self):
        m = matrix.Matrix(1, 9)
        self.scenarioGetElementReturnsCorrectValueAfterThatElementIsSet(m, 1, 7, 3)

    def testGetElementReturnsCorrectValueAfterThatElementIsSet33(self):
        m = matrix.Matrix(3, 3)
        self.scenarioGetElementReturnsCorrectValueAfterThatElementIsSet(m, 3, 3, 4)

    def scenarioIndexErrorIsThrownWhenSettingNonExistingElement(self, m, i, j):
        try:
            m.setItem(i, j, 5)
        except IndexError:
            pass
        else:
            self.fail('IndexError should have been thrown.')

    def testIndexErrorIsThrownWhenAccesingNegativeRow(self):
        m = matrix.Matrix(3, 3)
        self.scenarioIndexErrorIsThrownWhenSettingNonExistingElement(m, -1, 1)

    def testIndexErrorIsThrownWhenAccesingNegativeCol(self):
        m = matrix.Matrix(3, 3)
        self.scenarioIndexErrorIsThrownWhenSettingNonExistingElement(m, 1, -1)

    def testIndexErrorIsThrownWhenAccesingTooHighRow(self):
        m = matrix.Matrix(3, 3)
        self.scenarioIndexErrorIsThrownWhenSettingNonExistingElement(m, 10, 1)

    def testIndexErrorIsThrownWhenAccesingTooHighCol(self):
        m = matrix.Matrix(3, 3)
        self.scenarioIndexErrorIsThrownWhenSettingNonExistingElement(m, 1, 10)

    def scenarioReprReturnsCorrectResult(self, m, expRes):
        self.assertEqual(expRes, repr(m))

    def testReprReturnsCorrectResult11(self):
        m = matrix.Matrix(1, 1)
        m.setItem(1, 1, 5)
        res = "5\n"
        self.scenarioReprReturnsCorrectResult(m, res)

    def testReprReturnsCorrectResult23(self):
        m = matrix.Matrix(2, 3)
        m.setItem(1, 1, 3)
        m.setItem(1, 3, 5)
        m.setItem(2, 2, 4)
        m.setItem(2, 3, 5)
        res = "3 0 5\n0 4 5\n"
        self.scenarioReprReturnsCorrectResult(m, res)

    def testTwoSameMatricesAreEqual(self):
        m = matrix.Matrix(2, 3)
        self.assertEqual(m, m)

    def testTwoMatricesWithSameDimensionsAndValuesAreEqual(self):
        m1 = matrix.Matrix(2, 3)
        m1.setItem(2, 2, 4)
        m2 = matrix.Matrix(2, 3)
        m2.setItem(2, 2, 4)
        self.assertEqual(m1, m2)

    def testTwoMatricesWithSameDimensionsAndDifferentValuesAreNotEqual(self):
        m1 = matrix.Matrix(2, 3)
        m1.setItem(2, 2, 3)
        m2 = matrix.Matrix(2, 3)
        m2.setItem(2, 2, 5)
        self.assertNotEqual(m1, m2)

    def testTwoMatricesWithDifferentNumberOfRowsAreNotEqual(self):
        m1 = matrix.Matrix(2, 3)
        m2 = matrix.Matrix(4, 3)
        self.assertNotEqual(m1, m2)

    def testTwoMatricesWithDifferentNumberOfColsAreNotEqual(self):
        m1 = matrix.Matrix(2, 5)
        m2 = matrix.Matrix(2, 3)
        self.assertNotEqual(m1, m2)

    def testTwoMatricesWithSameDimensionsAndValuesButInDifferentTypesAreEqual(self):
        m1 = matrix.Matrix(2, 3)
        m1.setItem(2, 2, 4)
        m2 = matrix.Matrix(2, 3)
        m2.setItem(2, 2, r.Rational(4))
        self.assertEqual(m1, m2)


class MatrixFromTextTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def scenarioCorrectMatrixIsReturned(self, inpText, expText):
        m = matrix.fromText(inpText)
        self.assertEqual(expText, repr(m))

    def testCreate11Matrix(self):
        text = '5\n'
        self.scenarioCorrectMatrixIsReturned(text, text)

    def testCreate41Matrix(self):
        text = '1\n4\n8\n12\n'
        self.scenarioCorrectMatrixIsReturned(text, text)

    def testCreate33Matrix(self):
        text = '1 2 3\n4 5 6\n7 8 9\n'
        self.scenarioCorrectMatrixIsReturned(text, text)

    def testCreate22MatrixNegativeNumbers(self):
        text = '1 -2\n-4 6\n'
        self.scenarioCorrectMatrixIsReturned(text, text)

    def testCreate22MatrixRedundantWhitespace(self):
        inpText = '  5	7 \n	444      8\n'
        expText = '5 7\n444 8\n'
        self.scenarioCorrectMatrixIsReturned(inpText, expText)

    def testCreate22MatrixLastNewLineIsMissing(self):
        inpText = '2 2\n1 1'
        expText = inpText + '\n'
        self.scenarioCorrectMatrixIsReturned(inpText, expText)

    def scenarioInvalidMatrixReprErrorIsRaisesOnInvalidMatrix(self, inpText):
        try:
            m = matrix.fromText(inpText)
        except matrix.InvalidMatrixReprError:
            pass
        else:
            self.fail('InvalidMatrixReprError should have been thrown.')

    def testInvalidMatrixReprErrorIsRaisedOnInvalidMatrixEmptyString(self):
        text = ''
        self.scenarioInvalidMatrixReprErrorIsRaisesOnInvalidMatrix(text)

    def testInvalidMatrixReprErrorIsRaisedOnInvalidMatrixMissingColumn(self):
        text = '1 2 3\n1 4\n'
        self.scenarioInvalidMatrixReprErrorIsRaisesOnInvalidMatrix(text)

    def testInvalidMatrixReprErrorIsRaisedOnInvalidMatrixEmptyLine(self):
        text = '1\n\n1\n'
        self.scenarioInvalidMatrixReprErrorIsRaisesOnInvalidMatrix(text)


def suite():
    """Returns a test suite that contains all tests from this module."""
    return unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])


def test():
    """Runs all unit tests for this module."""
    runner = unittest.TextTestRunner()
    runner.run(suite())


if __name__ == '__main__':
    test()
