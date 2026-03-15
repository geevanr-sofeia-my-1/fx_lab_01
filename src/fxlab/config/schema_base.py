"""Base configuration schema helpers."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class FXLabBaseModel(BaseModel):
    """Base pydantic model with deterministic serialization defaults."""

    model_config = ConfigDict(extra="forbid", frozen=True)
