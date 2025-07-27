"""
Pydantic Models for API Request/Response
=======================================

This module defines the data models used for API requests and responses.
Using Pydantic for automatic validation, serialization, and documentation.

Models:
- TextRequest: Input text for processing
- AnalysisResponse: POS tagging results
- SignLanguageResponse: Sign language conversion results
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    """
    Request model for text input.

    Used by endpoints that process Vietnamese text.
    """

    text: str = Field(..., description="Vietnamese text to process", min_length=1)

    class Config:
        json_schema_extra = {"example": {"text": "Tôi đang học tiếng Việt"}}


class AnalysisResponse(BaseModel):
    """
    Response model for POS tagging analysis.

    Contains the results of Vietnamese text analysis including
    POS tags and statistical information.
    """

    success: bool = Field(..., description="Whether the analysis was successful")
    results: Optional[List[tuple]] = Field(
        None, description="List of (word, POS_tag) tuples"
    )
    statistics: Optional[Dict] = Field(None, description="Analysis statistics")
    error: Optional[str] = Field(None, description="Error message if failed")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "results": [("Tôi", "PRON"), ("đang", "ADV"), ("học", "VERB")],
                "statistics": {
                    "total_words": 3,
                    "unique_tags": 3,
                    "processing_time": 0.05,
                },
            }
        }


class SignLanguageResponse(BaseModel):
    """
    Response model for sign language conversion.

    Contains the complete sign language conversion results including
    original text, POS analysis, converted sequence, and detailed analysis.
    """

    success: bool = Field(..., description="Whether the conversion was successful")
    original_sentence: Optional[str] = Field(
        None, description="Original Vietnamese sentence"
    )
    pos_analysis: Optional[List[tuple]] = Field(None, description="POS tagging results")
    sign_language_sequence: Optional[List[str]] = Field(
        None, description="Sign language word sequence"
    )
    structure_analysis: Optional[Dict] = Field(
        None, description="Conversion structure analysis"
    )
    pos_structure: Optional[Dict] = Field(None, description="POS structure breakdown")
    word_details: Optional[List[Dict]] = Field(
        None, description="Detailed word-by-word information"
    )
    error: Optional[str] = Field(None, description="Error message if failed")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "original_sentence": "Tôi đang học tiếng Việt",
                "pos_analysis": [("Tôi", "PRON"), ("đang", "ADV"), ("học", "VERB")],
                "sign_language_sequence": ["TÔI", "TIẾNG", "VIỆT", "HỌC"],
                "structure_analysis": {"word_count": 5, "conversion_applied": True},
            }
        }
