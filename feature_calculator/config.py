"""
Configuration management for Feature Calculator.

This module provides centralized configuration management for the Feature Calculator
application, including environment-specific settings, feature flags, and runtime
configurations.

Created: 2025-12-25 14:17:26 UTC
"""

import os
from typing import Any, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum


class Environment(Enum):
    """Supported environment types."""
    
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    
    host: str = os.getenv("DB_HOST", "localhost")
    port: int = int(os.getenv("DB_PORT", "5432"))
    username: str = os.getenv("DB_USERNAME", "admin")
    password: str = os.getenv("DB_PASSWORD", "")
    database: str = os.getenv("DB_NAME", "feature_calculator")
    pool_size: int = int(os.getenv("DB_POOL_SIZE", "10"))
    max_overflow: int = int(os.getenv("DB_MAX_OVERFLOW", "20"))
    echo: bool = os.getenv("DB_ECHO", "False").lower() == "true"
    
    def get_connection_string(self) -> str:
        """Generate database connection string."""
        return (
            f"postgresql://{self.username}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}"
        )


@dataclass
class FeatureFlags:
    """Feature flags for feature toggling."""
    
    enable_caching: bool = os.getenv("FEATURE_ENABLE_CACHING", "True").lower() == "true"
    enable_analytics: bool = os.getenv("FEATURE_ENABLE_ANALYTICS", "True").lower() == "true"
    enable_advanced_calculations: bool = os.getenv(
        "FEATURE_ENABLE_ADVANCED_CALC", "False"
    ).lower() == "true"
    enable_api_versioning: bool = os.getenv(
        "FEATURE_ENABLE_API_VERSIONING", "True"
    ).lower() == "true"
    debug_mode: bool = os.getenv("FEATURE_DEBUG_MODE", "False").lower() == "true"


@dataclass
class CacheConfig:
    """Caching configuration settings."""
    
    enabled: bool = os.getenv("CACHE_ENABLED", "True").lower() == "true"
    backend: str = os.getenv("CACHE_BACKEND", "redis")  # redis, memory, memcached
    host: str = os.getenv("CACHE_HOST", "localhost")
    port: int = int(os.getenv("CACHE_PORT", "6379"))
    ttl_seconds: int = int(os.getenv("CACHE_TTL", "3600"))
    max_entries: int = int(os.getenv("CACHE_MAX_ENTRIES", "10000"))


@dataclass
class LoggingConfig:
    """Logging configuration settings."""
    
    level: str = os.getenv("LOG_LEVEL", "INFO")  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    format: str = os.getenv(
        "LOG_FORMAT",
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    log_file: Optional[str] = os.getenv("LOG_FILE", None)
    log_dir: str = os.getenv("LOG_DIR", "logs")
    max_file_size: int = int(os.getenv("LOG_MAX_FILE_SIZE", "10485760"))  # 10MB
    backup_count: int = int(os.getenv("LOG_BACKUP_COUNT", "5"))


@dataclass
class APIConfig:
    """API configuration settings."""
    
    host: str = os.getenv("API_HOST", "0.0.0.0")
    port: int = int(os.getenv("API_PORT", "8000"))
    workers: int = int(os.getenv("API_WORKERS", "4"))
    timeout: int = int(os.getenv("API_TIMEOUT", "30"))
    rate_limit: int = int(os.getenv("API_RATE_LIMIT", "1000"))
    rate_limit_period: int = int(os.getenv("API_RATE_LIMIT_PERIOD", "3600"))
    cors_origins: list = field(
        default_factory=lambda: os.getenv("CORS_ORIGINS", "*").split(",")
    )
    enable_docs: bool = os.getenv("API_ENABLE_DOCS", "True").lower() == "true"


class Config:
    """
    Main configuration class that aggregates all configuration sections.
    
    This class manages environment-specific settings and provides a centralized
    access point for all configuration parameters.
    """
    
    def __init__(self, env: Optional[str] = None):
        """
        Initialize configuration with specified environment.
        
        Args:
            env: Environment name. If not provided, defaults to value from
                 ENVIRONMENT environment variable or "development".
        """
        self.environment = Environment(
            env or os.getenv("ENVIRONMENT", "development")
        )
        
        # Initialize configuration sections
        self.database = DatabaseConfig()
        self.features = FeatureFlags()
        self.cache = CacheConfig()
        self.logging = LoggingConfig()
        self.api = APIConfig()
        
        # Runtime settings
        self.debug = self.environment != Environment.PRODUCTION
        self.testing = self.environment == Environment.TESTING
        
        self._settings: Dict[str, Any] = {}
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a runtime configuration value.
        
        Args:
            key: Configuration key (supports dot notation for nested values).
            value: Configuration value.
        """
        self._settings[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a runtime configuration value.
        
        Args:
            key: Configuration key (supports dot notation for nested values).
            default: Default value if key is not found.
        
        Returns:
            Configuration value or default.
        """
        return self._settings.get(key, default)
    
    def update(self, settings: Dict[str, Any]) -> None:
        """
        Update multiple configuration values at once.
        
        Args:
            settings: Dictionary of configuration key-value pairs.
        """
        self._settings.update(settings)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary representation.
        
        Returns:
            Dictionary containing all configuration settings.
        """
        return {
            "environment": self.environment.value,
            "debug": self.debug,
            "testing": self.testing,
            "database": {
                "host": self.database.host,
                "port": self.database.port,
                "database": self.database.database,
                "pool_size": self.database.pool_size,
            },
            "features": {
                "enable_caching": self.features.enable_caching,
                "enable_analytics": self.features.enable_analytics,
                "enable_advanced_calculations": self.features.enable_advanced_calculations,
                "enable_api_versioning": self.features.enable_api_versioning,
                "debug_mode": self.features.debug_mode,
            },
            "cache": {
                "enabled": self.cache.enabled,
                "backend": self.cache.backend,
                "ttl_seconds": self.cache.ttl_seconds,
            },
            "logging": {
                "level": self.logging.level,
                "log_dir": self.logging.log_dir,
            },
            "api": {
                "host": self.api.host,
                "port": self.api.port,
                "workers": self.api.workers,
                "rate_limit": self.api.rate_limit,
            },
            "runtime_settings": self._settings,
        }


# Global configuration instance
_config: Optional[Config] = None


def get_config(env: Optional[str] = None) -> Config:
    """
    Get or create the global configuration instance.
    
    Args:
        env: Environment name. Only used when creating a new instance.
    
    Returns:
        Global Config instance.
    """
    global _config
    if _config is None:
        _config = Config(env)
    return _config


def reset_config() -> None:
    """Reset the global configuration instance (useful for testing)."""
    global _config
    _config = None


# Export commonly used items
__all__ = [
    "Config",
    "Environment",
    "DatabaseConfig",
    "FeatureFlags",
    "CacheConfig",
    "LoggingConfig",
    "APIConfig",
    "get_config",
    "reset_config",
]
