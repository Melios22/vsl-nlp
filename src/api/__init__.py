"""
API Package
===========

FastAPI application for Vietnamese NLP and Sign Language conversion.
Contains web API endpoints and data models.
"""

from .main import app
from .models import AnalysisResponse, SignLanguageResponse, TextRequest

__all__ = ["app", "TextRequest", "AnalysisResponse", "SignLanguageResponse"]
