"""
Basic usage examples for the Feature Calculator SDK.

This module demonstrates common operations with the calculator.
"""

from feature_calculator import Calculator


def basic_arithmetic_operations():
    """Demonstrate basic arithmetic operations."""
    calc = Calculator()
    
    # Addition
    result = calc.add(10, 5)
    print(f"10 + 5 = {result}")
    
    # Subtraction
    result = calc.subtract(10, 3)
    print(f"10 - 3 = {result}")
    
    # Multiplication
    result = calc.multiply(7, 6)
    print(f"7 * 6 = {result}")
    
    # Division
    result = calc.divide(20, 4)
    print(f"20 / 4 = {result}")


def chained_operations():
    """Demonstrate chaining multiple operations."""
    calc = Calculator()
    
    # Start with a value and chain operations
    result = calc.add(10, 5)      # 15
    result = calc.multiply(result, 2)  # 30
    result = calc.subtract(result, 5)  # 25
    
    print(f"Chained result: (10 + 5) * 2 - 5 = {result}")


def working_with_decimals():
    """Demonstrate working with decimal numbers."""
    calc = Calculator()
    
    # Decimal operations
    result = calc.add(3.14, 2.86)
    print(f"3.14 + 2.86 = {result}")
    
    result = calc.divide(10.0, 3.0)
    print(f"10.0 / 3.0 = {result:.2f}")


def error_handling():
    """Demonstrate error handling."""
    calc = Calculator()
    
    try:
        # This will raise an error
        result = calc.divide(10, 0)
    except ZeroDivisionError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    """Run all examples."""
    print("=" * 50)
    print("Basic Arithmetic Operations")
    print("=" * 50)
    basic_arithmetic_operations()
    
    print("\n" + "=" * 50)
    print("Chained Operations")
    print("=" * 50)
    chained_operations()
    
    print("\n" + "=" * 50)
    print("Working with Decimals")
    print("=" * 50)
    working_with_decimals()
    
    print("\n" + "=" * 50)
    print("Error Handling")
    print("=" * 50)
    error_handling()


if __name__ == "__main__":
    main()
