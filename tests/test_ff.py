import unittest
from ipynb.ff import FiniteField


class TestFiniteField(unittest.TestCase):
    def test_ne(self):
        a = FiniteField(2, 31)
        b = FiniteField(2, 31)
        c = FiniteField(15, 31)
        self.assertEqual(a, b)
        self.assertTrue(a != c)
        self.assertFalse(a != b)

    def test_add(self):
        a = FiniteField(2, 31)
        b = FiniteField(15, 31)
        self.assertEqual(a + b, FiniteField(17, 31))
        a = FiniteField(17, 31)
        b = FiniteField(21, 31)
        self.assertEqual(a + b, FiniteField(7, 31))

    def test_sub(self):
        a = FiniteField(29, 31)
        b = FiniteField(4, 31)
        self.assertEqual(a - b, FiniteField(25, 31))
        a = FiniteField(15, 31)
        b = FiniteField(30, 31)
        self.assertEqual(a - b, FiniteField(16, 31))

    def test_mul(self):
        a = FiniteField(24, 31)
        b = FiniteField(19, 31)
        self.assertEqual(a * b, FiniteField(22, 31))

    def test_rmul(self):
        a = FiniteField(24, 31)
        b = 2
        self.assertEqual(b * a, a + a)

    def test_pow(self):
        a = FiniteField(17, 31)
        self.assertEqual(a**3, FiniteField(15, 31))
        a = FiniteField(5, 31)
        b = FiniteField(18, 31)
        self.assertEqual(a**5 * b, FiniteField(16, 31))

    def test_div(self):
        a = FiniteField(3, 31)
        b = FiniteField(24, 31)
        self.assertEqual(a / b, FiniteField(4, 31))
        a = FiniteField(17, 31)
        self.assertEqual(a**-3, FiniteField(29, 31))
        a = FiniteField(4, 31)
        b = FiniteField(11, 31)
        self.assertEqual(a**-4 * b, FiniteField(13, 31))
