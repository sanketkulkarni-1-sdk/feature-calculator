"""
Utility helper functions for feature calculator.

This module provides common utility functions used throughout the feature calculator
to support feature engineering, data transformation, and calculation operations.
"""

from typing import Any, Dict, List, Optional, Union
import logging


logger = logging.getLogger(__name__)


def validate_input(value: Any, expected_type: type, nullable: bool = False) -> bool:
    """
    Validate that an input value matches the expected type.
    
    Args:
        value: The value to validate
        expected_type: The expected type of the value
        nullable: Whether None values are acceptable
        
    Returns:
        bool: True if validation passes, False otherwise
    """
    if value is None:
        return nullable
    return isinstance(value, expected_type)


def safe_divide(numerator: Union[int, float], denominator: Union[int, float], 
                default: Union[int, float] = 0) -> Union[int, float]:
    """
    Safely divide two numbers, returning a default value if division by zero occurs.
    
    Args:
        numerator: The numerator
        denominator: The denominator
        default: The default value to return if denominator is zero
        
    Returns:
        Union[int, float]: The result of division or the default value
    """
    try:
        if denominator == 0:
            logger.warning("Division by zero detected, returning default value")
            return default
        return numerator / denominator
    except (TypeError, ValueError) as e:
        logger.error(f"Error during division: {e}")
        return default


def normalize_values(values: List[Union[int, float]]) -> List[float]:
    """
    Normalize a list of numeric values to a 0-1 range.
    
    Args:
        values: List of numeric values to normalize
        
    Returns:
        List[float]: Normalized values in range [0, 1]
        
    Raises:
        ValueError: If values list is empty or contains non-numeric types
    """
    if not values:
        raise ValueError("Cannot normalize empty list")
    
    try:
        min_val = min(values)
        max_val = max(values)
        range_val = max_val - min_val
        
        if range_val == 0:
            return [0.5] * len(values)
        
        return [(v - min_val) / range_val for v in values]
    except TypeError:
        raise ValueError("All values must be numeric")


def merge_dictionaries(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge multiple dictionaries into a single dictionary.
    
    Later dictionaries take precedence in case of key conflicts.
    
    Args:
        *dicts: Variable number of dictionaries to merge
        
    Returns:
        Dict[str, Any]: Merged dictionary
    """
    result = {}
    for d in dicts:
        if isinstance(d, dict):
            result.update(d)
    return result


def filter_by_condition(data: List[Dict[str, Any]], 
                       key: str, 
                       condition_func) -> List[Dict[str, Any]]:
    """
    Filter a list of dictionaries based on a condition function.
    
    Args:
        data: List of dictionaries to filter
        key: The dictionary key to apply the condition to
        condition_func: A callable that takes a value and returns bool
        
    Returns:
        List[Dict[str, Any]]: Filtered list of dictionaries
    """
    return [item for item in data if key in item and condition_func(item[key])]


def calculate_statistics(values: List[Union[int, float]]) -> Dict[str, float]:
    """
    Calculate basic statistics for a list of numeric values.
    
    Args:
        values: List of numeric values
        
    Returns:
        Dict[str, float]: Dictionary containing mean, min, max, and sum
        
    Raises:
        ValueError: If values list is empty
    """
    if not values:
        raise ValueError("Cannot calculate statistics for empty list")
    
    return {
        'mean': sum(values) / len(values),
        'min': min(values),
        'max': max(values),
        'sum': sum(values),
        'count': len(values)
    }


def retry_on_exception(func, max_retries: int = 3, delay: float = 1.0) -> Any:
    """
    Execute a function with retry logic on exception.
    
    Args:
        func: Callable to execute
        max_retries: Maximum number of retry attempts
        delay: Delay in seconds between retries
        
    Returns:
        Any: The result of the function
        
    Raises:
        Exception: The last exception if all retries are exhausted
    """
    import time
    
    last_exception = None
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            last_exception = e
            if attempt < max_retries - 1:
                logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s")
                time.sleep(delay)
    
    logger.error(f"Failed after {max_retries} attempts")
    raise last_exception
