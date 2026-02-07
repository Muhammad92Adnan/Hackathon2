"""
Application configuration management.

This module loads and validates environment variables for the application.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        DATABASE_URL: PostgreSQL connection string for Neon database
        BETTER_AUTH_SECRET: Shared secret for JWT token verification (min 32 chars)
        JWT_ALGORITHM: Algorithm for JWT encoding/decoding (default: HS256)
        JWT_EXPIRATION_HOURS: Token validity period in hours (default: 24)
        CORS_ORIGINS: Comma-separated list of allowed CORS origins
        HOST: Server host address (default: 0.0.0.0)
        PORT: Server port (default: 8000)
    """

    # Database Configuration
    DATABASE_URL: str

    # JWT Configuration
    BETTER_AUTH_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # CORS Configuration
    CORS_ORIGINS: str = "http://localhost:3000"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """
        Parse CORS_ORIGINS string into list of URLs.

        Returns:
            List of allowed origin URLs
        """
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    def validate_secret(self) -> None:
        """
        Validate that BETTER_AUTH_SECRET meets minimum length requirement.

        Raises:
            ValueError: If secret is shorter than 32 characters
        """
        if len(self.BETTER_AUTH_SECRET) < 32:
            raise ValueError(
                "BETTER_AUTH_SECRET must be at least 32 characters long. "
                "Generate one with: openssl rand -base64 32"
            )


# Global settings instance
settings = Settings()

# Validate settings on module load
settings.validate_secret()
