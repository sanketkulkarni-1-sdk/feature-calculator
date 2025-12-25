"""
Calculator module providing a main Calculator class for feature calculations.
"""


class Calculator:
    """
    A Calculator class for performing basic arithmetic and feature calculation operations.
    """

    def __init__(self):
        """Initialize the Calculator instance."""
        self.last_result = None

    def add(self, a, b):
        """
        Add two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            The sum of a and b
        """
        self.last_result = a + b
        return self.last_result

    def subtract(self, a, b):
        """
        Subtract two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            The difference of a and b
        """
        self.last_result = a - b
        return self.last_result

    def multiply(self, a, b):
        """
        Multiply two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            The product of a and b
        """
        self.last_result = a * b
        return self.last_result

    def divide(self, a, b):
        """
        Divide two numbers.

        Args:
            a: First number (dividend)
            b: Second number (divisor)

        Returns:
            The quotient of a and b

        Raises:
            ValueError: If attempting to divide by zero
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        self.last_result = a / b
        return self.last_result

    def power(self, base, exponent):
        """
        Raise a number to a power.

        Args:
            base: The base number
            exponent: The exponent

        Returns:
            The base raised to the exponent
        """
        self.last_result = base ** exponent
        return self.last_result

    def square_root(self, num):
        """
        Calculate the square root of a number.

        Args:
            num: The number to calculate the square root of

        Returns:
            The square root of the number

        Raises:
            ValueError: If the number is negative
        """
        if num < 0:
            raise ValueError("Cannot calculate square root of negative number")
        self.last_result = num ** 0.5
        return self.last_result

    def get_last_result(self):
        """
        Get the last calculated result.

        Returns:
            The last calculation result or None if no calculation has been performed
        """
        return self.last_result

    def reset(self):
        """Reset the last result to None."""
        self.last_result = None
