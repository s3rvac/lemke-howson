# vim:fileencoding=utf8
#
# Project: Implementation of the Lemke-Howson algorithm for finding MNE
# Author:  Petr Zemek <s3rvac@gmail.com>, 2009
#

import unittest
import sys

from .. import rational as r


class RationalTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCreateRationalFrom2CreatesCorrectRational(self):
        a = r.Rational(2)
        self.assertEqual(2, a.nom())
        self.assertEqual(1, a.denom())

    def testCreateRationalFromThreeSlashFourCreatesCorrectRational(self):
        a = r.Rational(3, 4)
        self.assertEqual(3, a.nom())
        self.assertEqual(4, a.denom())

    def testCreateRationalFromMinus2CreatesNegativeRational(self):
        a = r.Rational(-2)
        self.assertEqual(-2, a.nom())
        self.assertEqual(1, a.denom())

    def testCreateRationalFromMinus5Minus6CreatesNegativeRational(self):
        a = r.Rational(-5, -6)
        self.assertEqual(5, a.nom())
        self.assertEqual(6, a.denom())

    def testCreateRationalFrom7Minus6CreatesNegativeRational(self):
        a = r.Rational(7, -6)
        self.assertEqual(-7, a.nom())
        self.assertEqual(6, a.denom())

    def testCreateRational5Slash10WillBeTransformedInto1Slash2(self):
        a = r.Rational(5, 10)
        self.assertEqual(1, a.nom())
        self.assertEqual(2, a.denom())

    def testCreateRationalMinus10Slash10WillBeTransformedInto1Slash1(self):
        a = r.Rational(-10, 10)
        self.assertEqual(-1, a.nom())
        self.assertEqual(1, a.denom())

    def testCreateRational10SlashMinus10WillBeTransformedInto1Slash1(self):
        a = r.Rational(10, -10)
        self.assertEqual(-1, a.nom())
        self.assertEqual(1, a.denom())

    def testCreateRationalMinus12SlashMinus4WillBeTransformedInto3Slash1(self):
        a = r.Rational(-12, -4)
        self.assertEqual(3, a.nom())
        self.assertEqual(1, a.denom())

    def testCreateRationalFromOtherRationalBothRationalsAreEqual(self):
        a = r.Rational(-12, -4)
        b = r.Rational(a)
        self.assertEqual(a, b)

    def testValueErrorIsRaisedWhenCreatingRationalFromOtherRationalAndBIsNotOne(self):
        try:
            a = r.Rational(-12, -4)
            b = r.Rational(a, 2)
        except ValueError:
            pass
        else:
            self.fail('ValueError should have been thrown.')

    def testValueErrorIsRaisedIfZeroDenominatorIsPassedToConstructor(self):
        try:
            a = r.Rational(1, 0)
        except ValueError:
            pass
        else:
            self.fail('ValueError should have been thrown.')

    def testRecipFrom1Slash1ReturnUnchangedResult(self):
        a = r.Rational(1)
        self.assertEqual(a, a.recip())

    def testRecipFrom1Slash4ReturnCorrectResult(self):
        a = r.Rational(1, 4)
        self.assertEqual(r.Rational(4), a.recip())

    def testRecipFromMinus1Slash4ReturnCorrectResult(self):
        a = r.Rational(-1, 4)
        self.assertEqual(r.Rational(-4), a.recip())

    def testAdd1Slash1To1Slash1CreatesCorrectRational(self):
        a = r.Rational(1, 1)
        b = r.Rational(1, 1)
        c = a + b
        self.assertEqual(2, c.nom())
        self.assertEqual(1, c.denom())

    def testAddMinus3Slash2To4SlashMinus5CreatesCorrectRational(self):
        a = r.Rational(-3, 2)
        b = r.Rational(4, -5)
        c = a + b
        self.assertEqual(-23, c.nom())
        self.assertEqual(10, c.denom())

    def testAdd4To3Slash2CreatesCorrectRational(self):
        a = r.Rational(3, 2)
        b = a + 4
        self.assertEqual(11, b.nom())
        self.assertEqual(2, b.denom())

    def testAdd3Slash2To4CreatesCorrectRational(self):
        a = r.Rational(3, 2)
        b = 4 + a
        self.assertEqual(11, b.nom())
        self.assertEqual(2, b.denom())

    def testMul3Slash2To4Slash5CreatesCorrectRational(self):
        a = r.Rational(3, 2)
        b = r.Rational(4, 5)
        c = a * b
        self.assertEqual(6, c.nom())
        self.assertEqual(5, c.denom())

    def testMulMinus3Slash2To4Slash5CreatesCorrectRational(self):
        a = r.Rational(-3, 2)
        b = r.Rational(4, 5)
        c = a * b
        self.assertEqual(-6, c.nom())
        self.assertEqual(5, c.denom())

    def testMul2Slash7With3CreatesCorrectRational(self):
        a = r.Rational(3, 7)
        b = a * 3
        self.assertEqual(9, b.nom())
        self.assertEqual(7, b.denom())

    def testMul3With3Slash7CreatesCorrectRational(self):
        a = r.Rational(3, 7)
        b = 3 * a
        self.assertEqual(9, b.nom())
        self.assertEqual(7, b.denom())

    def testDiv3Slash2With4Slash5CreatesCorrectRational(self):
        a = r.Rational(3, 2)
        b = r.Rational(4, 5)
        c = a / b
        self.assertEqual(15, c.nom())
        self.assertEqual(8, c.denom())

    def testDivMinus3Slash2With4Slash5CreatesCorrectRational(self):
        a = r.Rational(-3, 2)
        b = r.Rational(4, 5)
        c = a / b
        self.assertEqual(-15, c.nom())
        self.assertEqual(8, c.denom())

    def testDivMinus3Slash2WithMinus4Slash5CreatesCorrectRational(self):
        a = r.Rational(-3, 2)
        b = r.Rational(-4, 5)
        c = a / b
        self.assertEqual(15, c.nom())
        self.assertEqual(8, c.denom())

    def testDiv2Slash7With3CreatesCorrectRational(self):
        a = r.Rational(3, 7)
        b = a / 3
        self.assertEqual(1, b.nom())
        self.assertEqual(7, b.denom())

    def testDiv3With2Slash7CreatesCorrectRational(self):
        a = r.Rational(3, 7)
        b = 3 / a
        self.assertEqual(1, b.nom())
        self.assertEqual(7, b.denom())

    def testAbsFromPositiveRationalIsTheSameRational(self):
        a = r.Rational(3, 7)
        self.assertEqual(a, abs(a))

    def testAbsFromZeroRationalIsTheSameRational(self):
        a = r.Rational(0)
        self.assertEqual(a, abs(a))

    def testAbsFromNegativeRationalIsTheSameRationalWithPositiveNominator(self):
        a = r.Rational(-3, 7)
        self.assertEqual(r.Rational(3, 7), abs(a))

    def testMinus1Slash3IsMinus1Slash3(self):
        a = r.Rational(1, 3)
        self.assertEqual(r.Rational(-1, 3), -a)

    def testMinusMinus1Slash3Is1Slash3(self):
        a = r.Rational(-1, 3)
        self.assertEqual(r.Rational(1, 3), -a)

    def testMinus0Slash1Is0Slash1(self):
        a = r.Rational(0)
        self.assertEqual(a, -a)

    def testStrOnPositiveRationalReturnsCorrectString(self):
        a = r.Rational(3, 4)
        self.assertEqual('3/4', str(a))

    def testStrOnNegativeRationalReturnsCorrectString(self):
        a = r.Rational(-3, 4)
        self.assertEqual('-3/4', str(a))

    def testReprReturnsTheSameResultAsStr(self):
        a = r.Rational(3, 4)
        self.assertEqual(str(a), repr(a))

    def testTwoSameRationalNumbersAreEqual(self):
        a = r.Rational(3, 4)
        b = r.Rational(3, 4)
        self.assertTrue(a == b)
        self.assertTrue(not (a != b))

    def testTwoDifferentRationalNumbersAreNotEqual(self):
        a = r.Rational(2, 4)
        b = r.Rational(3, 7)
        self.assertTrue(a != b)
        self.assertTrue(not (a == b))

    def test3Slash1IsEqualTo3(self):
        a = r.Rational(3, 1)
        self.assertEqual(a, 3)

    def test3IsEqualTo3Slash1(self):
        a = r.Rational(3, 1)
        self.assertEqual(3, a)

    def test3Slash2IsNotEqualTo3(self):
        a = r.Rational(3, 2)
        self.assertNotEqual(a, 3)

    def test3IsNotEqualTo3Slash2(self):
        a = r.Rational(3, 2)
        self.assertNotEqual(3, a)

    def test1Slash3IsLowerOrEqualToSelf(self):
        a = r.Rational(1, 3)
        self.assertTrue(a <= a)

    def test1Slash3IsHigherOrEqualToSelf(self):
        a = r.Rational(1, 3)
        self.assertTrue(a >= a)

    def test1Slash3IsLowerOrEqualTo1Slash2(self):
        a = r.Rational(1, 3)
        b = r.Rational(1, 2)
        self.assertTrue(a <= b)

    def test1Slash3IsLowerThan1Slash2(self):
        a = r.Rational(1, 3)
        b = r.Rational(1, 2)
        self.assertTrue(a < b)

    def test1Slash2IsHigherOrEqualTo1Slash3(self):
        a = r.Rational(1, 2)
        b = r.Rational(1, 3)
        self.assertTrue(a >= b)

    def test1Slash2IsHigherThan1Slash3(self):
        a = r.Rational(1, 2)
        b = r.Rational(1, 3)
        self.assertTrue(a > b)

    def test5Slash3IsLowerOrEqualTo5Slash2(self):
        a = r.Rational(5, 3)
        b = r.Rational(5, 2)
        self.assertTrue(a <= b)

    def test5Slash3IsLowerThan5Slash2(self):
        a = r.Rational(5, 3)
        b = r.Rational(5, 2)
        self.assertTrue(a < b)

    def test5Slash2IsHigherOrEqualTo5Slash3(self):
        a = r.Rational(5, 2)
        b = r.Rational(5, 3)
        self.assertTrue(a >= b)

    def test5Slash2IsHigherThan5Slash3(self):
        a = r.Rational(5, 2)
        b = r.Rational(5, 3)
        self.assertTrue(a > b)

    def test5Slash3IsLowerOrEqualTo7Slash2(self):
        a = r.Rational(5, 3)
        b = r.Rational(7, 2)
        self.assertTrue(a <= b)

    def test5Slash3IsLowerThan7Slash2(self):
        a = r.Rational(5, 3)
        b = r.Rational(7, 2)
        self.assertTrue(a < b)

    def test7Slash2IsHigherOrEqualTo5Slash3(self):
        a = r.Rational(7, 2)
        b = r.Rational(5, 3)
        self.assertTrue(a >= b)

    def test7Slash2IsHigherThan5Slash3(self):
        a = r.Rational(7, 2)
        b = r.Rational(5, 3)
        self.assertTrue(a > b)

    def test0Slash1IsLowerOrEqualTo4Slash3(self):
        a = r.Rational(0)
        b = r.Rational(4, 3)
        self.assertTrue(a <= b)

    def test0Slash1IsLowerThan4Slash3(self):
        a = r.Rational(0)
        b = r.Rational(4, 3)
        self.assertTrue(a < b)

    def test4Slash3IsHigherOrEqualTo0Slash1(self):
        a = r.Rational(4, 3)
        b = r.Rational(0)
        self.assertTrue(a >= b)

    def test4Slash3IsHigherThan0Slash1(self):
        a = r.Rational(4, 3)
        b = r.Rational(0)
        self.assertTrue(a > b)

    def testMinus5Slash3IsLowerOrEqualTo7Slash2(self):
        a = r.Rational(-5, 3)
        b = r.Rational(7, 2)
        self.assertTrue(a <= b)

    def testMinus5Slash3IsLowerThan7Slash2(self):
        a = r.Rational(-5, 3)
        b = r.Rational(7, 2)
        self.assertTrue(a < b)

    def test5Slash3IsHigherOrEqualToMinus7Slash2(self):
        a = r.Rational(5, 3)
        b = r.Rational(-7, 2)
        self.assertTrue(a >= b)

    def test5Slash3IsHigherThanMinus7Slash2(self):
        a = r.Rational(5, 3)
        b = r.Rational(-7, 2)
        self.assertTrue(a > b)

    def test1IsLowerOrEqualTo5Slash3(self):
        a = 1
        b = r.Rational(5, 3)
        self.assertTrue(a <= b)

    def test1IsLowerThan5Slash3(self):
        a = 1
        b = r.Rational(5, 3)
        self.assertTrue(a < b)

    def test5Slash3IsLowerOrEqualTo5(self):
        a = r.Rational(5, 3)
        b = 5
        self.assertTrue(a <= b)

    def test5Slash3IsLowerThan5(self):
        a = r.Rational(5, 3)
        b = 5
        self.assertTrue(a < b)

    def testMinus3IsLowerOrEqualTo0Slash1(self):
        a = -3
        b = r.Rational(0)
        self.assertTrue(a <= b)

    def testMinus3IsLowerThan0Slash1(self):
        a = -3
        b = r.Rational(0)
        self.assertTrue(a < b)

    def testMinus5Slash1IsLowerOrEqualTo6(self):
        a = r.Rational(-5, 1)
        b = 6
        self.assertTrue(a <= b)

    def testMinus5Slash1IsLowerThan6(self):
        a = r.Rational(-5, 1)
        b = 6
        self.assertTrue(a < b)

    def testMinus6Slash1IsLowerOrEqualToMinus5(self):
        a = r.Rational(-6, 1)
        b = -5
        self.assertTrue(a <= b)

    def testMinus6Slash1IsLowerThanMinus5(self):
        a = r.Rational(-6, 1)
        b = -5
        self.assertTrue(a < b)


class FromTextTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def scenarioValidTextReturnsValidResult(self, text, expRational):
        self.assertEqual(r.fromText(text), expRational)

    def testSinglePositiveNumberReturnsValidResult(self):
        self.scenarioValidTextReturnsValidResult('1', r.Rational(1))

    def testSingleNegativeReturnsValidResult(self):
        self.scenarioValidTextReturnsValidResult('-450', r.Rational(-450))

    def testFullPositiveRationalReturnsValidResult(self):
        self.scenarioValidTextReturnsValidResult('1/2', r.Rational(1, 2))

    def testFullNegativeRationalReturnsValidResult(self):
        self.scenarioValidTextReturnsValidResult('-3/7', r.Rational(-3, 7))

    def testFullRationalIsNormalizedReturnsValidResult(self):
        self.scenarioValidTextReturnsValidResult('4/8', r.Rational(1, 2))

    def testRedundantWhiteSpaceAreRemoved(self):
        self.scenarioValidTextReturnsValidResult('  3	/	4 ', r.Rational(3, 4))

    def scenarioInvalidRationalReprErrorIsRaisedOnInvalidText(self, text):
        try:
            a = r.fromText(text)
        except r.InvalidRationalReprError:
            pass
        else:
            self.fail('InvalidRationalReprError should have been thrown.')

    def testInvalidRationalReprErrorIsRaisedOnEmptyText(self):
        self.scenarioInvalidRationalReprErrorIsRaisedOnInvalidText('')

    def testInvalidRationalReprErrorIsRaisedOnInvalidSingleNumber(self):
        self.scenarioInvalidRationalReprErrorIsRaisedOnInvalidText('#')

    def testInvalidRationalReprErrorIsRaisedOnMissingDenomAfterSlash(self):
        self.scenarioInvalidRationalReprErrorIsRaisedOnInvalidText('5/')

    def testInvalidRationalReprErrorIsRaisedOnMissingNom(self):
        self.scenarioInvalidRationalReprErrorIsRaisedOnInvalidText('/5')

    def testInvalidRationalReprErrorIsRaisedOnInvalidDenom(self):
        self.scenarioInvalidRationalReprErrorIsRaisedOnInvalidText('1/a')

    def testInvalidRationalReprErrorIsRaisedOnNegativeDenom(self):
        self.scenarioInvalidRationalReprErrorIsRaisedOnInvalidText('1/-5')


def suite():
    """Returns a test suite that contains all tests from this module."""
    return unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])


def test():
    """Runs all unit tests for this module."""
    runner = unittest.TextTestRunner()
    runner.run(suite())


if __name__ == '__main__':
    test()
