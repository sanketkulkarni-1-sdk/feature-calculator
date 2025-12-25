"""
Validator module for feature calculator.

This module provides validation functionality for feature calculations,
ensuring input data integrity and correctness.
"""

from typing import Any, Dict, List, Optional, Union
from abc import ABC, abstractmethod


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class Validator(ABC):
    """
    Abstract base class for validators.
    
    Provides a common interface for implementing validation logic
    for different types of data and features.
    """
    
    @abstractmethod
    def validate(self, data: Any) -> bool:
        """
        Validate the provided data.
        
        Args:
            data: The data to validate.
            
        Returns:
            bool: True if data is valid, False otherwise.
            
        Raises:
            ValidationError: If validation fails with details.
        """
        pass
    
    @abstractmethod
    def get_error_message(self) -> str:
        """
        Get the error message from the last validation attempt.
        
        Returns:
            str: Description of validation error or empty string if valid.
        """
        pass


class NumericValidator(Validator):
    """Validator for numeric data."""
    
    def __init__(self, min_value: Optional[float] = None, 
                 max_value: Optional[float] = None,
                 allow_none: bool = False):
        """
        Initialize numeric validator.
        
        Args:
            min_value: Minimum allowed value (inclusive).
            max_value: Maximum allowed value (inclusive).
            allow_none: Whether to allow None values.
        """
        self.min_value = min_value
        self.max_value = max_value
        self.allow_none = allow_none
        self._error_message = ""
    
    def validate(self, data: Any) -> bool:
        """
        Validate that data is numeric and within specified bounds.
        
        Args:
            data: The data to validate.
            
        Returns:
            bool: True if valid, False otherwise.
        """
        if data is None:
            if self.allow_none:
                self._error_message = ""
                return True
            self._error_message = "Value cannot be None"
            return False
        
        try:
            value = float(data)
        except (ValueError, TypeError):
            self._error_message = f"Value '{data}' is not numeric"
            return False
        
        if self.min_value is not None and value < self.min_value:
            self._error_message = f"Value {value} is less than minimum {self.min_value}"
            return False
        
        if self.max_value is not None and value > self.max_value:
            self._error_message = f"Value {value} is greater than maximum {self.max_value}"
            return False
        
        self._error_message = ""
        return True
    
    def get_error_message(self) -> str:
        """Get the last validation error message."""
        return self._error_message


class StringValidator(Validator):
    """Validator for string data."""
    
    def __init__(self, min_length: int = 0, max_length: Optional[int] = None,
                 allowed_values: Optional[List[str]] = None,
                 allow_none: bool = False):
        """
        Initialize string validator.
        
        Args:
            min_length: Minimum string length.
            max_length: Maximum string length.
            allowed_values: List of allowed values (None = any value allowed).
            allow_none: Whether to allow None values.
        """
        self.min_length = min_length
        self.max_length = max_length
        self.allowed_values = allowed_values
        self.allow_none = allow_none
        self._error_message = ""
    
    def validate(self, data: Any) -> bool:
        """
        Validate that data is a string meeting specified criteria.
        
        Args:
            data: The data to validate.
            
        Returns:
            bool: True if valid, False otherwise.
        """
        if data is None:
            if self.allow_none:
                self._error_message = ""
                return True
            self._error_message = "Value cannot be None"
            return False
        
        if not isinstance(data, str):
            self._error_message = f"Value must be string, got {type(data).__name__}"
            return False
        
        if len(data) < self.min_length:
            self._error_message = f"String length {len(data)} is less than minimum {self.min_length}"
            return False
        
        if self.max_length is not None and len(data) > self.max_length:
            self._error_message = f"String length {len(data)} is greater than maximum {self.max_length}"
            return False
        
        if self.allowed_values is not None and data not in self.allowed_values:
            self._error_message = f"Value '{data}' not in allowed values: {self.allowed_values}"
            return False
        
        self._error_message = ""
        return True
    
    def get_error_message(self) -> str:
        """Get the last validation error message."""
        return self._error_message


class DictValidator(Validator):
    """Validator for dictionary data with schema validation."""
    
    def __init__(self, required_keys: Optional[List[str]] = None,
                 validators: Optional[Dict[str, Validator]] = None):
        """
        Initialize dictionary validator.
        
        Args:
            required_keys: List of required keys in the dictionary.
            validators: Dictionary mapping keys to Validator instances.
        """
        self.required_keys = required_keys or []
        self.validators = validators or {}
        self._error_message = ""
    
    def validate(self, data: Any) -> bool:
        """
        Validate that data is a dictionary with required keys and valid values.
        
        Args:
            data: The data to validate.
            
        Returns:
            bool: True if valid, False otherwise.
        """
        if not isinstance(data, dict):
            self._error_message = f"Value must be dictionary, got {type(data).__name__}"
            return False
        
        # Check required keys
        for key in self.required_keys:
            if key not in data:
                self._error_message = f"Required key '{key}' missing from dictionary"
                return False
        
        # Validate values using provided validators
        for key, validator in self.validators.items():
            if key in data:
                if not validator.validate(data[key]):
                    self._error_message = f"Invalid value for key '{key}': {validator.get_error_message()}"
                    return False
        
        self._error_message = ""
        return True
    
    def get_error_message(self) -> str:
        """Get the last validation error message."""
        return self._error_message


class ListValidator(Validator):
    """Validator for list data with item validation."""
    
    def __init__(self, item_validator: Optional[Validator] = None,
                 min_length: int = 0, max_length: Optional[int] = None):
        """
        Initialize list validator.
        
        Args:
            item_validator: Validator to apply to each list item.
            min_length: Minimum list length.
            max_length: Maximum list length.
        """
        self.item_validator = item_validator
        self.min_length = min_length
        self.max_length = max_length
        self._error_message = ""
    
    def validate(self, data: Any) -> bool:
        """
        Validate that data is a list with valid items.
        
        Args:
            data: The data to validate.
            
        Returns:
            bool: True if valid, False otherwise.
        """
        if not isinstance(data, list):
            self._error_message = f"Value must be list, got {type(data).__name__}"
            return False
        
        if len(data) < self.min_length:
            self._error_message = f"List length {len(data)} is less than minimum {self.min_length}"
            return False
        
        if self.max_length is not None and len(data) > self.max_length:
            self._error_message = f"List length {len(data)} is greater than maximum {self.max_length}"
            return False
        
        # Validate each item if validator provided
        if self.item_validator:
            for i, item in enumerate(data):
                if not self.item_validator.validate(item):
                    self._error_message = f"Invalid item at index {i}: {self.item_validator.get_error_message()}"
                    return False
        
        self._error_message = ""
        return True
    
    def get_error_message(self) -> str:
        """Get the last validation error message."""
        return self._error_message
