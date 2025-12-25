"""
Unit tests for the validator module.

This module contains comprehensive tests for all validation functions
including input validation, type checking, and error handling.
"""

import pytest
from validator import (
    validate_input,
    validate_number,
    validate_string,
    validate_list,
    validate_dict,
    ValidationError
)


class TestValidateInput:
    """Tests for the validate_input function."""

    def test_validate_input_with_valid_data(self):
        """Test validation with valid input data."""
        valid_data = {"key": "value", "number": 42}
        result = validate_input(valid_data)
        assert result is True

    def test_validate_input_with_none(self):
        """Test validation with None input."""
        with pytest.raises(ValidationError):
            validate_input(None)

    def test_validate_input_with_empty_dict(self):
        """Test validation with empty dictionary."""
        with pytest.raises(ValidationError):
            validate_input({})

    def test_validate_input_with_invalid_type(self):
        """Test validation with invalid input type."""
        with pytest.raises(ValidationError):
            validate_input("not a dict")


class TestValidateNumber:
    """Tests for the validate_number function."""

    def test_validate_number_with_valid_integer(self):
        """Test validation with valid integer."""
        assert validate_number(42) is True

    def test_validate_number_with_valid_float(self):
        """Test validation with valid float."""
        assert validate_number(3.14) is True

    def test_validate_number_with_zero(self):
        """Test validation with zero."""
        assert validate_number(0) is True

    def test_validate_number_with_negative(self):
        """Test validation with negative number."""
        assert validate_number(-100) is True

    def test_validate_number_with_string(self):
        """Test validation with string input."""
        with pytest.raises(ValidationError):
            validate_number("42")

    def test_validate_number_with_none(self):
        """Test validation with None."""
        with pytest.raises(ValidationError):
            validate_number(None)

    def test_validate_number_with_min_constraint(self):
        """Test validation with minimum value constraint."""
        assert validate_number(50, min_value=10) is True
        with pytest.raises(ValidationError):
            validate_number(5, min_value=10)

    def test_validate_number_with_max_constraint(self):
        """Test validation with maximum value constraint."""
        assert validate_number(50, max_value=100) is True
        with pytest.raises(ValidationError):
            validate_number(150, max_value=100)

    def test_validate_number_with_both_constraints(self):
        """Test validation with both min and max constraints."""
        assert validate_number(50, min_value=10, max_value=100) is True
        with pytest.raises(ValidationError):
            validate_number(5, min_value=10, max_value=100)
        with pytest.raises(ValidationError):
            validate_number(150, min_value=10, max_value=100)


class TestValidateString:
    """Tests for the validate_string function."""

    def test_validate_string_with_valid_string(self):
        """Test validation with valid string."""
        assert validate_string("hello") is True

    def test_validate_string_with_empty_string(self):
        """Test validation with empty string."""
        with pytest.raises(ValidationError):
            validate_string("")

    def test_validate_string_with_whitespace_only(self):
        """Test validation with whitespace-only string."""
        with pytest.raises(ValidationError):
            validate_string("   ")

    def test_validate_string_with_non_string(self):
        """Test validation with non-string input."""
        with pytest.raises(ValidationError):
            validate_string(123)

    def test_validate_string_with_none(self):
        """Test validation with None."""
        with pytest.raises(ValidationError):
            validate_string(None)

    def test_validate_string_with_min_length(self):
        """Test validation with minimum length constraint."""
        assert validate_string("hello", min_length=3) is True
        with pytest.raises(ValidationError):
            validate_string("hi", min_length=3)

    def test_validate_string_with_max_length(self):
        """Test validation with maximum length constraint."""
        assert validate_string("hello", max_length=10) is True
        with pytest.raises(ValidationError):
            validate_string("hello world", max_length=5)

    def test_validate_string_with_pattern(self):
        """Test validation with regex pattern."""
        assert validate_string("test@example.com", pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$") is True
        with pytest.raises(ValidationError):
            validate_string("invalid-email", pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")


class TestValidateList:
    """Tests for the validate_list function."""

    def test_validate_list_with_valid_list(self):
        """Test validation with valid list."""
        assert validate_list([1, 2, 3]) is True

    def test_validate_list_with_empty_list(self):
        """Test validation with empty list."""
        assert validate_list([]) is True

    def test_validate_list_with_non_list(self):
        """Test validation with non-list input."""
        with pytest.raises(ValidationError):
            validate_list("not a list")

    def test_validate_list_with_none(self):
        """Test validation with None."""
        with pytest.raises(ValidationError):
            validate_list(None)

    def test_validate_list_with_min_length(self):
        """Test validation with minimum length constraint."""
        assert validate_list([1, 2, 3], min_length=2) is True
        with pytest.raises(ValidationError):
            validate_list([1], min_length=2)

    def test_validate_list_with_max_length(self):
        """Test validation with maximum length constraint."""
        assert validate_list([1, 2, 3], max_length=5) is True
        with pytest.raises(ValidationError):
            validate_list([1, 2, 3, 4, 5, 6], max_length=5)

    def test_validate_list_with_element_type(self):
        """Test validation with element type constraint."""
        assert validate_list([1, 2, 3], element_type=int) is True
        with pytest.raises(ValidationError):
            validate_list([1, "two", 3], element_type=int)

    def test_validate_list_with_mixed_types_allowed(self):
        """Test validation allows mixed types when no element_type specified."""
        assert validate_list([1, "two", 3.0]) is True


class TestValidateDict:
    """Tests for the validate_dict function."""

    def test_validate_dict_with_valid_dict(self):
        """Test validation with valid dictionary."""
        assert validate_dict({"key": "value"}) is True

    def test_validate_dict_with_empty_dict(self):
        """Test validation with empty dictionary."""
        assert validate_dict({}) is True

    def test_validate_dict_with_non_dict(self):
        """Test validation with non-dict input."""
        with pytest.raises(ValidationError):
            validate_dict("not a dict")

    def test_validate_dict_with_none(self):
        """Test validation with None."""
        with pytest.raises(ValidationError):
            validate_dict(None)

    def test_validate_dict_with_required_keys(self):
        """Test validation with required keys constraint."""
        data = {"name": "John", "age": 30}
        assert validate_dict(data, required_keys=["name", "age"]) is True
        with pytest.raises(ValidationError):
            validate_dict(data, required_keys=["name", "age", "email"])

    def test_validate_dict_with_allowed_keys(self):
        """Test validation with allowed keys constraint."""
        data = {"name": "John", "age": 30}
        assert validate_dict(data, allowed_keys=["name", "age", "email"]) is True
        with pytest.raises(ValidationError):
            validate_dict(data, allowed_keys=["name"])

    def test_validate_dict_with_key_types(self):
        """Test validation with key type constraints."""
        data = {"name": "John", "age": 30}
        schema = {"name": str, "age": int}
        assert validate_dict(data, key_types=schema) is True
        with pytest.raises(ValidationError):
            validate_dict({"name": "John", "age": "thirty"}, key_types=schema)


class TestValidationError:
    """Tests for the ValidationError exception."""

    def test_validation_error_is_exception(self):
        """Test that ValidationError is an Exception."""
        assert issubclass(ValidationError, Exception)

    def test_validation_error_with_message(self):
        """Test ValidationError with custom message."""
        message = "Invalid input provided"
        error = ValidationError(message)
        assert str(error) == message

    def test_validation_error_can_be_caught(self):
        """Test that ValidationError can be caught."""
        with pytest.raises(ValidationError) as exc_info:
            validate_string(None)
        assert isinstance(exc_info.value, ValidationError)


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_validate_number_with_very_large_number(self):
        """Test validation with very large number."""
        large_number = 10**308
        assert validate_number(large_number) is True

    def test_validate_number_with_very_small_number(self):
        """Test validation with very small number."""
        small_number = 10**-308
        assert validate_number(small_number) is True

    def test_validate_string_with_unicode_characters(self):
        """Test validation with Unicode characters."""
        assert validate_string("こんにちは") is True
        assert validate_string("مرحبا") is True

    def test_validate_string_with_special_characters(self):
        """Test validation with special characters."""
        assert validate_string("!@#$%^&*()") is True

    def test_validate_list_with_nested_structures(self):
        """Test validation with nested lists and dicts."""
        nested = [1, [2, 3], {"key": "value"}]
        assert validate_list(nested) is True

    def test_validate_dict_with_nested_structures(self):
        """Test validation with nested dicts."""
        nested = {"outer": {"inner": {"deep": "value"}}}
        assert validate_dict(nested) is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
