"""
Core NLP Components
==================

Core natural language processing components for Vietnamese text analysis
and sign language conversion.

Components:
- tagger: Vietnamese POS tagging using UndertheSea
- sign_language_converter: Vietnamese to VSL conversion
"""

from .sign_language_converter import VietnameseSignLanguageConverter
from .tagger import UndertheSeaPOSTagger

__all__ = ["UndertheSeaPOSTagger", "VietnameseSignLanguageConverter"]
