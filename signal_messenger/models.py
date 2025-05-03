"""Data models for the Signal Messenger Python API."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class LoggingConfig(BaseModel):
    """Logging configuration model."""

    level: str = ""
    Level: str = ""

    def __init__(self, **data):
        """Initialize the logging configuration model.

        This handles both 'level' and 'Level' fields from the API.
        """
        super().__init__(**data)
        if not self.level and self.Level:
            self.level = self.Level


class Configuration(BaseModel):
    """API configuration model."""

    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    Logging: Optional[LoggingConfig] = None

    def __init__(self, **data):
        """Initialize the configuration model.

        This handles both 'logging' and 'Logging' fields from the API.
        """
        super().__init__(**data)
        if not self.logging.level and self.Logging:
            self.logging = self.Logging


class Capabilities(BaseModel):
    """API capabilities model."""

    model_config = ConfigDict(extra="allow")


class About(BaseModel):
    """API information model."""

    build: int
    capabilities: Dict[str, List[str]] = Field(default_factory=dict)
    mode: str
    version: str
    versions: List[str]


class AccountSettings(BaseModel):
    """Account settings model."""

    trust_mode: str
