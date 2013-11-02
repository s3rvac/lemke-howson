# vim:fileencoding=utf8
#
# Project: Implementation of the Lemke-Howson algorithm for finding MNE
# Author:  Petr Zemek <s3rvac@gmail.com>, 2009
#

import unittest
import sys

from .. import lh
from .. import matrix
from .. import rational as r


# Examples
EX1_M1 = matrix.fromText('2 0\n0 2\n')
EX1_M2 = matrix.fromText('0 2\n2 0\n')
EX2_M1 = matrix.fromText('1 3 0\n0 0 2\n2 1 1\n')
EX2_M2 = matrix.fromText('2 1 0\n1 3 1\n0 0 3\n')
EX3_M1 = matrix.fromText('1 2\n3 4\n5 6\n')
EX3_M2 = matrix.fromText('7 8\n9 10\n11 12\n')
EX4_M1 = matrix.fromText('3 1\n-1 2\n')
EX4_M2 = matrix.fromText('2 3\n4 1\n')
EX5_M1 = matrix.fromText('0 1\n')
EX5_M2 = matrix.fromText('2 3\n')
EX6_M1 = matrix.fromText('0\n1\n2\n3\n')
EX6_M2 = matrix.fromText('4\n5\n6\n7\n')
EX7_M1 = matrix.fromText('124 170 197\n146 253 114\n267 110 262\n')
EX7_M2 = matrix.fromText('270 194 100\n148 161 175\n163 260 268\n')
EX8_M1 = matrix.fromText('3 6 7\n3 8 9\n5 5 0\n')
EX8_M2 = matrix.fromText('2 7 8\n4 4 1\n6 2 3\n')
EX9_M1 = matrix.fromText('4 7\n8 1\n')
EX9_M2 = matrix.fromText('6 3\n2 9\n')
EX10_M1 = matrix.fromText('3 5 6\n6 1 5\n')
EX10_M2 = matrix.fromText('4 2 4\n2 4 1\n')

# itemFromStrFunc for creating tableaux from text,
# which creates rational numbers only from rational numbers
# (long numbers are created otherwise)
def tableauxItemFromStrFunc(str):
    n = r.fromText(str)
    if n.denom() == 1:
        return n.nom()
    else:
        return n


class NormalizeMatricesTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def scenarioMatricesAreProperlyNormalized(self, m1, m2, expM1, expM2):
        (normM1, normM2) = lh.normalizeMatrices(m1, m2)
        self.assertEqual(expM1, normM1)
        self.assertEqual(expM2, normM2)

    def testMatricesWithRowFullOfZerosWillNotContainRowFullOfZerosAfterNormalization(self):
        m1 = matrix.fromText('1 2 3\n0 0 0\n4 5 6\n')
        m2 = matrix.fromText('1 2 3\n0 0 0\n4 5 6\n')
        expM1 = matrix.fromText('2 3 4\n1 1 1\n5 6 7\n')
        expM2 = matrix.fromText('2 3 4\n1 1 1\n5 6 7\n')
        self.scenarioMatricesAreProperlyNormalized(m1, m2, expM1, expM2)

    def testMatricesWithColFullOfZerosWillNotContainRowFullOfZerosAfterNormalization(self):
        m1 = matrix.fromText('1 0 3\n1 0 6\n4 0 6\n')
        m2 = matrix.fromText('1 0 3\n1 0 6\n4 0 6\n')
        expM1 = matrix.fromText('2 1 4\n2 1 7\n5 1 7\n')
        expM2 = matrix.fromText('2 1 4\n2 1 7\n5 1 7\n')
        self.scenarioMatricesAreProperlyNormalized(m1, m2, expM1, expM2)

    def testMatricesWithNegativeItemsWillNotContainNegativeItemsAfterNormalization(self):
        m1 = matrix.fromText('1 0 -3\n-1 0 6\n-3 0 6\n')
        m2 = matrix.fromText('1 0 -4\n-1 0 6\n-3 0 6\n')
        expM1 = matrix.fromText('6 5 2\n4 5 11\n2 5 11\n')
        expM2 = matrix.fromText('6 5 1\n4 5 11\n2 5 11\n')
        self.scenarioMatricesAreProperlyNormalized(m1, m2, expM1, expM2)

    def testMatricesWithNonZeroAndPositiveItemsNothingIsAssed(self):
        m1 = matrix.fromText('1 4 3\n1 8 6\n4 3 6\n')
        m2 = matrix.fromText('1 3 3\n1 2 6\n4 1 7\n')
        self.scenarioMatricesAreProperlyNormalized(m1, m2, m1, m2)


class CreateTableauxTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def scenarioCreateCorrectTableaux(self, m1, m2, expTText):
        t = lh.createTableaux(m1, m2)
        expT = matrix.fromText(expTText)
        self.assertEqual(expT, t)

    def testEx1InitializesCorrectly(self):
        expTText = '-1 1  0  0 -2  0\n' +\
                   '-2 1  0  0  0 -2\n' +\
                   '-3 1  0 -2  0  0\n' +\
                   '-4 1 -2  0  0  0\n'
        self.scenarioCreateCorrectTableaux(EX1_M1, EX1_M2, expTText)

    def testEx2InitializesCorrectly(self):
        expTText = '-1 1  0  0  0 -1 -3  0\n' +\
                   '-2 1  0  0  0  0  0 -2\n' +\
                   '-3 1  0  0  0 -2 -1 -1\n' +\
                   '-4 1 -2 -1  0  0  0  0\n' +\
                   '-5 1 -1 -3  0  0  0  0\n' +\
                   '-6 1  0 -1 -3  0  0  0\n'
        self.scenarioCreateCorrectTableaux(EX2_M1, EX2_M2, expTText)

    def testEx3InitializesCorrectly(self):
        expTText = '-1 1  0  0   0  -1 -2\n' +\
                   '-2 1  0  0   0  -3 -4\n' +\
                   '-3 1  0  0   0  -5 -6\n' +\
                   '-4 1 -7 -9  -11  0  0\n' +\
                   '-5 1 -8 -10 -12  0  0\n'
        self.scenarioCreateCorrectTableaux(EX3_M1, EX3_M2, expTText)

    def scenarioValueErrorIsRaisedWhenMatricesDoNotHaveSameNumberOfRowsAndColumns(self, m1, m2):
        try:
            t = lh.createTableaux(m1, m2)
        except ValueError:
            pass
        else:
            self.fail('ValueError should have been thrown.')

    def testValueErrorIsRaisedWhenTheSecondMatrixHaveDifferentNumberOfRows(self):
        m1 = matrix.Matrix(3, 4)
        m2 = matrix.Matrix(2, 4)
        self.scenarioValueErrorIsRaisedWhenMatricesDoNotHaveSameNumberOfRowsAndColumns(m1, m2)

    def testValueErrorIsRaisedWhenTheSecondMatrixHaveDifferentNumberOfCols(self):
        m1 = matrix.Matrix(3, 4)
        m2 = matrix.Matrix(3, 5)
        self.scenarioValueErrorIsRaisedWhenMatricesDoNotHaveSameNumberOfRowsAndColumns(m1, m2)


class MakePivotingStepTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def scenarioMakePivotingStep(self, t, p1SCount, enterBasisVar, expLeftBasisVar, expT):
        lb = lh.makePivotingStep(t, p1SCount, enterBasisVar)
        self.assertEqual(expLeftBasisVar, lb)
        self.assertEqual(expT, t)

    def testEx1MakeFirstPivotingStep(self):
        t = lh.createTableaux(EX1_M1, EX1_M2)
        expTText = '-1  1   0   0  -2   0\n' +\
                   '-2  1   0   0   0  -2\n' +\
                   '-3  1   0  -2   0   0\n' +\
                   ' 1 1/2  0   0   0  -1/2\n'
        expT = matrix.fromText(expTText, itemFromStrFunc=tableauxItemFromStrFunc)
        self.scenarioMakePivotingStep(t, EX1_M1.getNumRows(), 1, -4, expT)

    def testEx1MakeSecondPivotingStep(self):
        origTText = '-1  1   0   0  -2   0\n' +\
                    '-2  1   0   0   0  -2\n' +\
                    '-3  1   0  -2   0   0\n' +\
                    ' 1 1/2  0   0   0  -1/2\n'
        t = matrix.fromText(origTText, itemFromStrFunc=tableauxItemFromStrFunc)
        expTText = '-1  1   0   0  -2   0\n' +\
                   ' 4 1/2  0 -1/2  0   0\n' +\
                   '-3  1   0  -2   0   0\n' +\
                   ' 1 1/2  0   0   0  -1/2\n'
        expT = matrix.fromText(expTText, itemFromStrFunc=tableauxItemFromStrFunc)
        self.scenarioMakePivotingStep(t, EX1_M1.getNumRows(), 4, -2, expT)

    def testEx2MakeFirstPivotingStep(self):
        t = lh.createTableaux(EX2_M1, EX2_M2)
        expTText = '-1 1   0  0    0 -1   -3  0\n' +\
                   '-2 1   0  0    0  0    0 -2\n' +\
                   '-3 1   0  0    0 -2   -1 -1\n' +\
                   ' 1 1/2 0 -1/2  0 -1/2  0  0\n' +\
                   '-5 1/2 0 -5/2  0  1/2  0  0\n' +\
                   '-6 1   0 -1   -3  0    0  0\n'
        expT = matrix.fromText(expTText, itemFromStrFunc=tableauxItemFromStrFunc)
        self.scenarioMakePivotingStep(t, EX2_M1.getNumRows(), 1, -4, expT)

    def testEx2MakeSecondPivotingStep(self):
        origTText = '-1 1   0  0    0 -1   -3  0\n' +\
                    '-2 1   0  0    0  0    0 -2\n' +\
                    '-3 1   0  0    0 -2   -1 -1\n' +\
                    ' 1 1/2 0 -1/2  0 -1/2  0  0\n' +\
                    '-5 1/2 0 -5/2  0  1/2  0  0\n' +\
                    '-6 1   0 -1   -3  0    0  0\n'
        t = matrix.fromText(origTText, itemFromStrFunc=tableauxItemFromStrFunc)
        expTText = '-1 1/2 0  0    1/2   0 -5/2 1/2\n' +\
                   '-2 1   0  0    0     0  0   -2\n' +\
                   ' 4 1/2 0  0   -1/2   0 -1/2 -1/2\n' +\
                   ' 1 1/2 0 -1/2  0 -1/2  0  0\n' +\
                   '-5 1/2 0 -5/2  0  1/2  0  0\n' +\
                   '-6 1   0 -1   -3  0    0  0\n'
        expT = matrix.fromText(expTText, itemFromStrFunc=tableauxItemFromStrFunc)
        self.scenarioMakePivotingStep(t, EX2_M1.getNumRows(), 4, -3, expT)

    def testEx2MakeThirdPivotingStep(self):
        origTText = '-1 1/2 0  0    1/2   0 -5/2 1/2\n' +\
                    '-2 1   0  0    0     0  0   -2\n' +\
                    ' 4 1/2 0  0   -1/2   0 -1/2 -1/2\n' +\
                    ' 1 1/2 0 -1/2  0 -1/2  0  0\n' +\
                    '-5 1/2 0 -5/2  0  1/2  0  0\n' +\
                    '-6 1   0 -1   -3  0    0  0\n'
        t = matrix.fromText(origTText, itemFromStrFunc=tableauxItemFromStrFunc)
        expTText = '-1 1/2 0  0    1/2   0 -5/2 1/2\n' +\
                   '-2 1   0  0    0     0  0   -2\n' +\
                   ' 4 1/2 0  0   -1/2   0 -1/2 -1/2\n' +\
                   ' 1 1/2 0 -1/2  0 -1/2  0  0\n' +\
                   '-5 1/2 0 -5/2  0  1/2  0  0\n' +\
                   ' 3 1/3 0 -1/3  0  0    0  -1/3\n'
        expT = matrix.fromText(expTText, itemFromStrFunc=tableauxItemFromStrFunc)
        self.scenarioMakePivotingStep(t, EX2_M1.getNumRows(), 3, -6, expT)

    def testEx2MakeFourthPivotingStep(self):
        origTText = '-1 3/4 0/1 -1/4 1/2 0/1 -5/2 0\n' +\
                    ' 6 1/2 0/1 -1/2 0/1 0/1 0/1 0/1\n' +\
                    ' 4 1/4 0/1 1/4 -1/2 0/1 -1/2 0\n' +\
                    ' 1 1/2 0/1 -1/2 0/1 -1/2 0/1 0/1\n' +\
                    '-5 1/2 0 -5/2 0/1 1/2 0/1 0/1\n' +\
                    ' 3 1/3 0/1 -1/3 0/1 0/1 0/1 -1/3\n'
        t = matrix.fromText(origTText, itemFromStrFunc=tableauxItemFromStrFunc)
        expTText = '-1 3/4  0/1 -1/4 1/2 0/1 -5/2 0\n' +\
                   ' 6 1/2  0/1 -1/2 0/1 0/1 0/1 0/1\n' +\
                   ' 4 1/4  0/1 1/4 -1/2 0/1 -1/2 0\n' +\
                   ' 1 2/5  0/1 0/1 0/1 -3/5  1/5   0/1\n' +\
                   ' 2 1/5  0/1 0/1 0/1  1/5 -2/5   0/1\n' +\
                   ' 3 4/15 0/1 0/1 0/1 -1/15 2/15 -1/3\n'
        expT = matrix.fromText(expTText, itemFromStrFunc=tableauxItemFromStrFunc)
        self.scenarioMakePivotingStep(t, EX2_M1.getNumRows(), 2, -5, expT)

    def testEx8MakeSeventhPivotingStep(self):
        origTText = '-1 4/25 0/1  3/5   6/25   0    0/1 -8/5\n' +\
                    ' 5 2/25 0/1 -1/5   3/25   0    0/1 -9/5\n' +\
                    ' 4 3/25 0/1  1/5  -8/25   0/1  0/1  9/5\n' +\
                    '-6 3/4  0    0   -15/2   -5/4  3/2  0\n' +\
                    ' 2 1/4  0    0   -19/10  -7/20  1/10 0\n' +\
                    ' 1 0    0    0     4/5    1/5  -1/5  0\n'
        t = matrix.fromText(origTText, itemFromStrFunc=tableauxItemFromStrFunc)
        expTText = '-1 4/25 0 3/5 6/25 0 0 -8/5\n' +\
                   ' 5 2/25 0 -1/5 3/25 0 0 -9/5\n' +\
                   ' 4 3/25 0 1/5 -8/25 0 0 9/5\n' +\
                   ' 3 1/10 0/1 0/1 0/1 -1/6 1/5 -2/15\n' +\
                   ' 2 3/50 0/1 0/1 0 -1/30 -7/25 19/75\n' +\
                   ' 1 2/25 0/1 0/1 0 1/15 -1/25 -8/75\n'
        expT = matrix.fromText(expTText, itemFromStrFunc=tableauxItemFromStrFunc)
        self.scenarioMakePivotingStep(t, EX8_M1.getNumRows(), 3, -6, expT)

    def testEx8MakeEighthPivotingStep(self):
        origTText = '-1 4/25 0 3/5 6/25 0 0 -8/5\n' +\
                    ' 5 2/25 0 -1/5 3/25 0 0 -9/5\n' +\
                    ' 4 3/25 0 1/5 -8/25 0 0 9/5\n' +\
                    ' 3 1/10 0/1 0/1 0/1 -1/6 1/5 -2/15\n' +\
                    ' 2 3/50 0/1 0/1 0 -1/30 -7/25 19/75\n' +\
                    ' 1 2/25 0/1 0/1 0 1/15 -1/25 -8/75\n'
        t = matrix.fromText(origTText, itemFromStrFunc=tableauxItemFromStrFunc)
        expTText = '-1 4/45 0/1 7/9 2/15 0/1 8/9 0\n' +\
                   ' 6 2/45 0/1 -1/9 1/15 0/1 -5/9 0/1\n' +\
                   ' 4 1/5 0/1 0/1 -1/5 0/1 -1/1 0\n' +\
                   ' 3 1/10 0 0 0 -1/6 1/5 -2/15\n' +\
                   ' 2 3/50 0 0 0 -1/30 -7/25 19/75\n' +\
                   ' 1 2/25 0 0 0 1/15 -1/25 -8/75\n'
        expT = matrix.fromText(expTText, itemFromStrFunc=tableauxItemFromStrFunc)
        self.scenarioMakePivotingStep(t, EX8_M1.getNumRows(), 6, 5, expT)

    def testEx8MakeNinthPivotingStep(self):
        origTText = '-1 4/45 0/1 7/9 2/15 0/1 8/9 0\n' +\
                   ' 6 2/45 0/1 -1/9 1/15 0/1 -5/9 0/1\n' +\
                   ' 4 1/5 0/1 0/1 -1/5 0/1 -1/1 0\n' +\
                   ' 3 1/10 0 0 0 -1/6 1/5 -2/15\n' +\
                   ' 2 3/50 0 0 0 -1/30 -7/25 19/75\n' +\
                   ' 1 2/25 0 0 0 1/15 -1/25 -8/75\n'
        t = matrix.fromText(origTText, itemFromStrFunc=tableauxItemFromStrFunc)
        expTText = '-1 4/45 0 7/9 2/15 0 8/9 0\n' +\
                   '6 2/45 0 -1/9 1/15 0 -5/9 0\n' +\
                   '4 1/5 0 0 -1/5 0 -1 0\n' +\
                   '3 1/7 0/1 -5/7 0/1 -4/21 0 1/21\n' +\
                   '-5 3/14 0/1 -25/7 0/1 -5/42 0/1 19/21\n' +\
                   '1 1/14 0/1 1/7 0/1 1/14 0 -1/7\n'
        expT = matrix.fromText(expTText, itemFromStrFunc=tableauxItemFromStrFunc)
        self.scenarioMakePivotingStep(t, EX8_M1.getNumRows(), -5, 2, expT)

    def testEx8MakeTenthPivotingStep(self):
        origTText = '-1 4/45 0 7/9 2/15 0 8/9 0\n' +\
                    '6 2/45 0 -1/9 1/15 0 -5/9 0\n' +\
                    '4 1/5 0 0 -1/5 0 -1 0\n' +\
                    '3 1/7 0/1 -5/7 0/1 -4/21 0 1/21\n' +\
                    '-5 3/14 0/1 -25/7 0/1 -5/42 0/1 19/21\n' +\
                    '1 1/14 0/1 1/7 0/1 1/14 0 -1/7\n'
        t = matrix.fromText(origTText, itemFromStrFunc=tableauxItemFromStrFunc)
        expTText = '-1 2/5 0/1 0 3/5 0/1 -3/1 -7/1\n' +\
                   '-2 2/5 0/1 0/1 3/5 0/1 -5/1 -9/1\n' +\
                   '4 1/5 0 0 -1/5 0 -1 0\n' +\
                   '3 1/7 0 -5/7 0 -4/21 0 1/21\n' +\
                   '-5 3/14 0 -25/7 0 -5/42 0 19/21\n' +\
                   '1 1/14 0 1/7 0 1/14 0 -1/7\n'
        expT = matrix.fromText(expTText, itemFromStrFunc=tableauxItemFromStrFunc)
        self.scenarioMakePivotingStep(t, EX8_M1.getNumRows(), -2, 6, expT)

    def testEx8MakeEleventhPivotingStep(self):
        origTText = '-1 2/5 0/1 0 3/5 0/1 -3/1 -7/1\n' +\
                    '-2 2/5 0/1 0/1 3/5 0/1 -5/1 -9/1\n' +\
                    '4 1/5 0 0 -1/5 0 -1 0\n' +\
                    '3 1/7 0 -5/7 0 -4/21 0 1/21\n' +\
                    '-5 3/14 0 -25/7 0 -5/42 0 19/21\n' +\
                    '1 1/14 0 1/7 0 1/14 0 -1/7\n'
        t = matrix.fromText(origTText, itemFromStrFunc=tableauxItemFromStrFunc)
        expTText = '-1 2/5 0 0 3/5 0 -3 -7\n' +\
                   '-2 2/5 0 0 3/5 0 -5 -9\n' +\
                   '4 1/5 0 0 -1/5 0 -1 0\n' +\
                   '3 1/6 -1/3 -2/3 0/1 -1/6 0/1 0\n' +\
                   '-5 2/3 -19/3 -8/3 0/1 1/3 0/1 0\n' +\
                   '-6 1/2 -7/1 1/1 0/1 1/2 0/1 0/1\n'
        expT = matrix.fromText(expTText, itemFromStrFunc=tableauxItemFromStrFunc)
        self.scenarioMakePivotingStep(t, EX8_M1.getNumRows(), -6, 1, expT)

    def scenarioValueErrorIsRaisedOnPreconditionViolation(self, t, p1SCount, enterBasisVar):
        try:
            t = lh.makePivotingStep(t, p1SCount, enterBasisVar)
        except ValueError:
            pass
        else:
            self.fail('ValueError should have been thrown.')

    def testValueErrorIsRaisedWhenEnterBasisVarHasTooLowValue(self):
        t = lh.createTableaux(EX1_M1, EX1_M2)
        self.scenarioValueErrorIsRaisedOnPreconditionViolation(t, EX1_M1.getNumRows(), -5)

    def testValueErrorIsRaisedWhenEnterBasisVarHasZeroValue(self):
        t = lh.createTableaux(EX1_M1, EX1_M2)
        self.scenarioValueErrorIsRaisedOnPreconditionViolation(t, EX1_M1.getNumRows(), 0)

    def testValueErrorIsRaisedWhenEnterBasisVarHasTooHighValue(self):
        t = lh.createTableaux(EX1_M1, EX1_M2)
        self.scenarioValueErrorIsRaisedOnPreconditionViolation(t, EX1_M1.getNumRows(), t.getNumRows() + 1)

    def testValueErrorIsRaisedWhenP1SCountIsLowerThanZero(self):
        t = lh.createTableaux(EX1_M1, EX1_M2)
        self.scenarioValueErrorIsRaisedOnPreconditionViolation(t, -1, t.getNumRows() + 1)

    def testValueErrorIsRaisedWhenP1SCountIsEqualToNumberOfRows(self):
        t = lh.createTableaux(EX1_M1, EX1_M2)
        self.scenarioValueErrorIsRaisedOnPreconditionViolation(t, t.getNumRows(), t.getNumRows() + 1)


class GetEquilibirumTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def scenarioTestGetEquilibrium(self, t, p1SCount, expEq):
        eq = lh.getEquilibrium(t, p1SCount)
        self.assertEqual(expEq, eq)

    def testGetEquilibrium22(self):
        tText = '3 1/3 0 0 0 0\n' +\
                '4 2/3 0 0 0 0\n' +\
                '1 3/4 0 0 0 0\n' +\
                '2 1/4 0 0 0 0\n'
        t = matrix.fromText(tText, tableauxItemFromStrFunc)
        expEq = ((r.Rational(3, 4), r.Rational(1, 4)),
                 (r.Rational(1, 3), r.Rational(2, 3)))
        self.scenarioTestGetEquilibrium(t, 2, expEq)

    def testGetEquilibriumEx2(self):
        tText = '5 3/10 0 0 0 0\n' +\
                '6 1/2  0 0 0 0\n' +\
                '4 1/10 0 0 0 0\n' +\
                '1 2/5  0 0 0 0\n' +\
                '2 1/5  0 0 0 0\n' +\
                '3 4/15 0 0 0 0\n'
        t = matrix.fromText(tText, tableauxItemFromStrFunc)
        expEq = ((r.Rational(2, 5), r.Rational(1, 5), r.Rational(4, 15)),
                 (r.Rational(1, 10), r.Rational(3, 10), r.Rational(1, 2)))
        self.scenarioTestGetEquilibrium(t, 3, expEq)

    def testGetEquilibriumNegativeNumberInSecondColumn(self):
        tText = '3 1/3 0 0 0 0\n' +\
                '4 -2/3 0 0 0 0\n' +\
                '1 3/4 0 0 0 0\n' +\
                '2 1/4 0 0 0 0\n'
        t = matrix.fromText(tText, tableauxItemFromStrFunc)
        expEq = ((r.Rational(3, 4), r.Rational(1, 4)),
                 (r.Rational(1, 3), r.Rational(0)))
        self.scenarioTestGetEquilibrium(t, 2, expEq)

    def testGetEquilibriumNegativeNumbersInFirstColumn(self):
        tText = '-3 1/3 0 0 0 0\n' +\
                '4 2/3 0 0 0 0\n' +\
                '-1 3/4 0 0 0 0\n' +\
                '2 1/4 0 0 0 0\n'
        t = matrix.fromText(tText, tableauxItemFromStrFunc)
        expEq = ((r.Rational(0), r.Rational(1, 4)),
                 (r.Rational(0), r.Rational(2, 3)))
        self.scenarioTestGetEquilibrium(t, 2, expEq)

    def scenarioValueErrorIsRaisedOnPreconditionsViolations(self, t, p1SCount):
        try:
            eq = lh.getEquilibrium(t, p1SCount)
        except ValueError:
            pass
        else:
            self.fail('ValueError should have been thrown.')

    def testValueErrorIsRaisedOnP1SCountHigherThanTableauxNumRows(self):
        tText = '3 1/3 0 0 0 0\n' +\
                '4 2/3 0 0 0 0\n' +\
                '1 3/4 0 0 0 0\n' +\
                '2 1/4 0 0 0 0\n'
        t = matrix.fromText(tText, tableauxItemFromStrFunc)
        self.scenarioValueErrorIsRaisedOnPreconditionsViolations(t, t.getNumRows() + 1)

    def testValueErrorIsRaisedOnP1SCountEqualThanTableauxNumRows(self):
        tText = '3 1/3 0 0 0 0\n' +\
                '4 2/3 0 0 0 0\n' +\
                '1 3/4 0 0 0 0\n' +\
                '2 1/4 0 0 0 0\n'
        t = matrix.fromText(tText, tableauxItemFromStrFunc)
        self.scenarioValueErrorIsRaisedOnPreconditionsViolations(t, t.getNumRows())

    def testValueErrorIsRaisedOnP1SCountLowerThanZero(self):
        tText = '3 1/3 0 0 0 0\n' +\
                '4 2/3 0 0 0 0\n' +\
                '1 3/4 0 0 0 0\n' +\
                '2 1/4 0 0 0 0\n'
        t = matrix.fromText(tText, tableauxItemFromStrFunc)
        self.scenarioValueErrorIsRaisedOnPreconditionsViolations(t, -1)

    def testValueErrorIsRaisedOnTooHighNumberInFirstColumn(self):
        tText = '3 1/3 0 0 0 0\n' +\
                '4 2/3 0 0 0 0\n' +\
                '9 3/4 0 0 0 0\n' +\
                '2 1/4 0 0 0 0\n'
        t = matrix.fromText(tText, tableauxItemFromStrFunc)
        self.scenarioValueErrorIsRaisedOnPreconditionsViolations(t, 2)

    def testValueErrorIsRaisedOnZeroNumberInFirstColumn(self):
        tText = '3 1/3 0 0 0 0\n' +\
                '0 2/3 0 0 0 0\n' +\
                '1 3/4 0 0 0 0\n' +\
                '2 1/4 0 0 0 0\n'
        t = matrix.fromText(tText, tableauxItemFromStrFunc)
        self.scenarioValueErrorIsRaisedOnPreconditionsViolations(t, 2)

    def testValueErrorIsRaisedOnTooLowNegativeNumberInFirstColumn(self):
        tText = ' 3 1/3 0 0 0 0\n' +\
                ' 4 2/3 0 0 0 0\n' +\
                '-9 3/4 0 0 0 0\n' +\
                ' 2 1/4 0 0 0 0\n'
        t = matrix.fromText(tText, tableauxItemFromStrFunc)
        self.scenarioValueErrorIsRaisedOnPreconditionsViolations(t, 2)

    def testValueErrorIsRaisedWhenThereIsNotEveryIndexInFirstColumn(self):
        tText = ' 3 1/3 0 0 0 0\n' +\
                ' 1 2/3 0 0 0 0\n' +\
                '-1 3/4 0 0 0 0\n' +\
                ' 2 1/4 0 0 0 0\n'
        t = matrix.fromText(tText, tableauxItemFromStrFunc)
        self.scenarioValueErrorIsRaisedOnPreconditionsViolations(t, 2)

class NormalizeEquilibirumTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def scenarioNormalizationOfValidEquilibriumReturnsCorrectResult(self, eq, expEq):
        self.assertEqual(expEq, lh.normalizeEquilibrium(eq))

    def testNormalizeAlreadyNormalizedEquilibriumDoesNotChangeIt(self):
        eq = ((r.Rational(1, 2), r.Rational(1, 2)), (r.Rational(1, 4), r.Rational(3, 4)))
        self.scenarioNormalizationOfValidEquilibriumReturnsCorrectResult(eq, eq)

    def testNormalizeUnnormalizedEquilibriumReturnsNormalizedResult(self):
        eq = ((r.Rational(2, 5), r.Rational(1, 5), r.Rational(4, 15)),
                 (r.Rational(1, 10), r.Rational(3, 10), r.Rational(1, 2)))
        expEq = ((r.Rational(6, 13), r.Rational(3, 13), r.Rational(4, 13)),
                 (r.Rational(1, 9), r.Rational(3, 9), r.Rational(5, 9)))
        self.scenarioNormalizationOfValidEquilibriumReturnsCorrectResult(eq, expEq)

    def scenarioValueErrorIsRaisedOnPreconditionsViolations(self, eq):
        try:
            normEq = lh.normalizeEquilibrium(eq)
        except ValueError:
            pass
        else:
            self.fail('ValueError should have been thrown.')

    def testValueErrorIsRaisedOnEmptyEquilibrium(self):
        eq = ()
        self.scenarioValueErrorIsRaisedOnPreconditionsViolations(eq)

    def testValueErrorIsRaisedOnEquilibriumWithThreeTuplesEquilibrium(self):
        eq = ((r.Rational(1, 2)), (r.Rational(1, 2)), (r.Rational(1, 2)))
        self.scenarioValueErrorIsRaisedOnPreconditionsViolations(eq)

    def testValueErrorIsRaisedOnEquilibriumWithEmptyMixedStrategy(self):
        eq = ((), ())
        self.scenarioValueErrorIsRaisedOnPreconditionsViolations(eq)


class LemkeHowsonTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def scenarioValidRun(self, m1, m2, expEq):
        eq = lh.lemkeHowson(m1, m2)
        self.assertEqual(expEq, eq)

    def testMatrix11ValidRun(self):
        m1 = matrix.fromText('1\n')
        m2 = matrix.fromText('1\n')
        expEq = ((r.Rational(1, 1), ), (r.Rational(1, 1),))
        self.scenarioValidRun(m1, m2, expEq)

    def testEx1ValidRun(self):
        expEq = ((r.Rational(1, 2), r.Rational(1, 2)),
                 (r.Rational(1, 2), r. Rational(1, 2)))
        self.scenarioValidRun(EX1_M1, EX1_M2, expEq)

    def testEx2ValidRun(self):
        expEq = ((r.Rational(6, 13), r.Rational(3, 13), r.Rational(4, 13)),
                 (r.Rational(1, 9), r.Rational(3, 9), r.Rational(5, 9)))
        self.scenarioValidRun(EX2_M1, EX2_M2, expEq)

    def testEx3ValidRun(self):
        expEq = ((r.Rational(0), r.Rational(0), r.Rational(1)),
                 (r.Rational(0), r. Rational(1)))
        self.scenarioValidRun(EX3_M1, EX3_M2, expEq)

    def testEx4ValidRun(self):
        expEq = ((r.Rational(3, 4), r.Rational(1, 4)),
                 (r.Rational(1, 5), r.Rational(4, 5)))
        self.scenarioValidRun(EX4_M1, EX4_M2, expEq)

    def testEx5ValidRun(self):
        expEq = ((r.Rational(1),),
                 (r.Rational(0), r.Rational(1)))
        self.scenarioValidRun(EX5_M1, EX5_M2, expEq)

    def testEx6ValidRun(self):
        expEq = ((r.Rational(0), r.Rational(0), r.Rational(0), r.Rational(1)),
                 (r.Rational(1),))
        self.scenarioValidRun(EX6_M1, EX6_M2, expEq)

    def testEx7ValidRun(self):
        expEq = ((r.Rational(0), r.Rational(0), r.Rational(1)),
                 (r.Rational(0), r.Rational(0), r.Rational(1)))
        self.scenarioValidRun(EX7_M1, EX7_M2, expEq)

    def testEx8ValidRun(self):
        expEq = ((r.Rational(0), r.Rational(0), r.Rational(1)),
                 (r.Rational(1), r.Rational(0), r.Rational(0)))
        self.scenarioValidRun(EX8_M1, EX8_M2, expEq)

    def testEx9ValidRun(self):
        expEq = ((r.Rational(7, 10), r.Rational(3, 10)),
                 (r.Rational(3, 5), r.Rational(2, 5)))
        self.scenarioValidRun(EX9_M1, EX9_M2, expEq)

    def testEx10ValidRun(self):
        expEq = ((r.Rational(1, 2), r.Rational(1, 2)),
                 (r.Rational(4, 7), r.Rational(3, 7), r.Rational(0)))
        self.scenarioValidRun(EX10_M1, EX10_M2, expEq)

    def scenarioValueErrorIsRaisedWhenMatricesHaveDifferentDimensions(self, m1, m2):
        try:
            lh.lemkeHowson(m1, m2)
        except ValueError:
            pass
        else:
            self.fail('ValueError should have been thrown.')

    def testValueErrorRaisedWhenTheFirstMatrixHaveDifferentNumberOfRowsThanTheSecondMatrix(self):
        m1 = matrix.fromText('1\n2\n')
        m2 = matrix.fromText('1\n')
        self.scenarioValueErrorIsRaisedWhenMatricesHaveDifferentDimensions(m1, m2)

    def testValueErrorRaisedWhenTheFirstMatrixHaveDifferentNumberOfColsThanTheSecondMatrix(self):
        m1 = matrix.fromText('1 4\n2 3\n')
        m2 = matrix.fromText('1\n2\n')
        self.scenarioValueErrorIsRaisedWhenMatricesHaveDifferentDimensions(m1, m2)


def suite():
    """Returns a test suite that contains all tests from this module."""
    return unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])


def test():
    """Runs all unit tests for this module."""
    runner = unittest.TextTestRunner()
    runner.run(suite())


if __name__ == '__main__':
    test()
