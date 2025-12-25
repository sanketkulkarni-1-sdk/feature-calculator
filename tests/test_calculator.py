import unittest
from calculator import Calculator


class TestCalculator(unittest.TestCase):
    """Unit tests for the Calculator module."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.calc = Calculator()

    def test_add_positive_numbers(self):
        """Test addition of two positive numbers."""
        result = self.calc.add(5, 3)
        self.assertEqual(result, 8)

    def test_add_negative_numbers(self):
        """Test addition of negative numbers."""
        result = self.calc.add(-5, -3)
        self.assertEqual(result, -8)

    def test_add_mixed_numbers(self):
        """Test addition of positive and negative numbers."""
        result = self.calc.add(10, -4)
        self.assertEqual(result, 6)

    def test_add_zero(self):
        """Test addition with zero."""
        result = self.calc.add(0, 5)
        self.assertEqual(result, 5)

    def test_subtract_positive_numbers(self):
        """Test subtraction of two positive numbers."""
        result = self.calc.subtract(10, 3)
        self.assertEqual(result, 7)

    def test_subtract_negative_numbers(self):
        """Test subtraction with negative numbers."""
        result = self.calc.subtract(-5, -3)
        self.assertEqual(result, -2)

    def test_subtract_result_negative(self):
        """Test subtraction resulting in a negative number."""
        result = self.calc.subtract(3, 10)
        self.assertEqual(result, -7)

    def test_subtract_zero(self):
        """Test subtraction with zero."""
        result = self.calc.subtract(5, 0)
        self.assertEqual(result, 5)

    def test_multiply_positive_numbers(self):
        """Test multiplication of two positive numbers."""
        result = self.calc.multiply(4, 5)
        self.assertEqual(result, 20)

    def test_multiply_negative_numbers(self):
        """Test multiplication of negative numbers."""
        result = self.calc.multiply(-4, -5)
        self.assertEqual(result, 20)

    def test_multiply_mixed_signs(self):
        """Test multiplication with mixed positive and negative numbers."""
        result = self.calc.multiply(-4, 5)
        self.assertEqual(result, -20)

    def test_multiply_by_zero(self):
        """Test multiplication by zero."""
        result = self.calc.multiply(5, 0)
        self.assertEqual(result, 0)

    def test_multiply_by_one(self):
        """Test multiplication by one."""
        result = self.calc.multiply(7, 1)
        self.assertEqual(result, 7)

    def test_divide_positive_numbers(self):
        """Test division of two positive numbers."""
        result = self.calc.divide(10, 2)
        self.assertEqual(result, 5.0)

    def test_divide_negative_numbers(self):
        """Test division of negative numbers."""
        result = self.calc.divide(-10, -2)
        self.assertEqual(result, 5.0)

    def test_divide_mixed_signs(self):
        """Test division with mixed positive and negative numbers."""
        result = self.calc.divide(-10, 2)
        self.assertEqual(result, -5.0)

    def test_divide_by_zero(self):
        """Test division by zero raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

    def test_divide_with_remainder(self):
        """Test division with remainder."""
        result = self.calc.divide(7, 2)
        self.assertAlmostEqual(result, 3.5)

    def test_power(self):
        """Test power operation."""
        result = self.calc.power(2, 3)
        self.assertEqual(result, 8)

    def test_power_zero_exponent(self):
        """Test power with zero exponent."""
        result = self.calc.power(5, 0)
        self.assertEqual(result, 1)

    def test_power_negative_exponent(self):
        """Test power with negative exponent."""
        result = self.calc.power(2, -2)
        self.assertAlmostEqual(result, 0.25)

    def test_square_root(self):
        """Test square root operation."""
        result = self.calc.square_root(16)
        self.assertEqual(result, 4.0)

    def test_square_root_zero(self):
        """Test square root of zero."""
        result = self.calc.square_root(0)
        self.assertEqual(result, 0.0)

    def test_square_root_negative(self):
        """Test square root of negative number raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.square_root(-4)

    def test_modulo(self):
        """Test modulo operation."""
        result = self.calc.modulo(10, 3)
        self.assertEqual(result, 1)

    def test_modulo_by_zero(self):
        """Test modulo by zero raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.modulo(10, 0)

    def test_absolute_value_positive(self):
        """Test absolute value of positive number."""
        result = self.calc.absolute(5)
        self.assertEqual(result, 5)

    def test_absolute_value_negative(self):
        """Test absolute value of negative number."""
        result = self.calc.absolute(-5)
        self.assertEqual(result, 5)

    def test_absolute_value_zero(self):
        """Test absolute value of zero."""
        result = self.calc.absolute(0)
        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
