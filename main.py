#!/usr/bin/env python3
"""
Main application entry point for the Feature Calculator.
Provides an interactive CLI calculator for mathematical operations.
"""

import sys
from typing import Optional, Tuple


class Calculator:
    """Interactive CLI Calculator for mathematical operations."""
    
    def __init__(self):
        """Initialize the calculator."""
        self.last_result: Optional[float] = None
        self.operations = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y if y != 0 else self._division_error(),
            '**': lambda x, y: x ** y,
            '%': lambda x, y: x % y if y != 0 else self._modulo_error(),
        }
    
    def _division_error(self) -> None:
        """Handle division by zero error."""
        raise ValueError("Cannot divide by zero")
    
    def _modulo_error(self) -> None:
        """Handle modulo by zero error."""
        raise ValueError("Cannot perform modulo with zero")
    
    def calculate(self, num1: float, operator: str, num2: float) -> float:
        """
        Perform a calculation.
        
        Args:
            num1: First number
            operator: Operation to perform (+, -, *, /, **, %)
            num2: Second number
            
        Returns:
            Result of the calculation
            
        Raises:
            ValueError: If operator is not supported or division/modulo by zero
        """
        if operator not in self.operations:
            raise ValueError(f"Unsupported operator: {operator}")
        
        try:
            result = self.operations[operator](num1, num2)
            self.last_result = result
            return result
        except Exception as e:
            raise ValueError(f"Calculation error: {str(e)}")
    
    def get_last_result(self) -> Optional[float]:
        """Get the last calculation result."""
        return self.last_result
    
    @staticmethod
    def parse_input(user_input: str) -> Tuple[float, str, float]:
        """
        Parse user input for calculator operation.
        
        Format: "number operator number" (e.g., "5 + 3")
        
        Args:
            user_input: Raw user input string
            
        Returns:
            Tuple of (num1, operator, num2)
            
        Raises:
            ValueError: If input format is invalid
        """
        parts = user_input.strip().split()
        
        if len(parts) < 3:
            raise ValueError("Invalid input format. Use: number operator number")
        
        try:
            num1 = float(parts[0])
            operator = parts[1]
            num2 = float(parts[2])
            return num1, operator, num2
        except ValueError as e:
            raise ValueError(f"Invalid input: {str(e)}")
    
    def display_help(self) -> None:
        """Display help information."""
        help_text = """
╔════════════════════════════════════════════════════════════╗
║           Feature Calculator - Interactive CLI             ║
╚════════════════════════════════════════════════════════════╝

Supported Operations:
  +   : Addition
  -   : Subtraction
  *   : Multiplication
  /   : Division
  **  : Exponentiation
  %   : Modulo (remainder)

Usage:
  Enter calculations in the format: number operator number
  Examples:
    5 + 3
    10 - 2
    4 * 7
    15 / 3
    2 ** 3
    10 % 3

Commands:
  help  : Display this help message
  last  : Show the last calculation result
  quit  : Exit the calculator

        """
        print(help_text)


def main() -> None:
    """Main application loop for interactive CLI calculator."""
    calculator = Calculator()
    
    print("\n" + "="*60)
    print("Welcome to Feature Calculator!")
    print("Type 'help' for usage information or 'quit' to exit.")
    print("="*60 + "\n")
    
    while True:
        try:
            user_input = input("calc> ").strip()
            
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() == 'quit':
                print("\nThank you for using Feature Calculator. Goodbye!")
                sys.exit(0)
            
            elif user_input.lower() == 'help':
                calculator.display_help()
                continue
            
            elif user_input.lower() == 'last':
                last_result = calculator.get_last_result()
                if last_result is not None:
                    print(f"Last result: {last_result}")
                else:
                    print("No previous calculation result available.")
                continue
            
            # Parse and perform calculation
            num1, operator, num2 = Calculator.parse_input(user_input)
            result = calculator.calculate(num1, operator, num2)
            print(f"Result: {result}")
            
        except ValueError as e:
            print(f"Error: {str(e)}")
        except KeyboardInterrupt:
            print("\n\nCalculator interrupted. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
