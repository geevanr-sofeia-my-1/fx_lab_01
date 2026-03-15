"""Project-specific exceptions."""


class FXLabError(Exception):
    """Base project exception."""


class ConfigError(FXLabError):
    """Raised when configuration loading or validation fails."""
