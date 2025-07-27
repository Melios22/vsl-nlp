"""
Vietnamese Sign Language NLP API
================================

Main FastAPI application for Vietnamese text processing and sign language conversion.
This API provides endpoints for POS tagging and converting Vietnamese text to
Vietnamese Sign Language (VSL) representation.

Features:
- Vietnamese POS tagging using UndertheSea
- Vietnamese to Sign Language conversion with linguistic accuracy
- RESTful API with automatic documentation
- Health monitoring and system information
"""

import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from ..core.sign_language_converter import VietnameseSignLanguageConverter
from ..core.tagger import UndertheSeaPOSTagger
from .models import AnalysisResponse, SignLanguageResponse, TextRequest


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager - initializes models on startup.

    This function runs before the application starts and after it shuts down.
    It initializes the singleton instances of our NLP components.
    """

    # Initialize singletons - they handle their own initialization
    tagger = UndertheSeaPOSTagger.get_instance()
    sign_converter = VietnameseSignLanguageConverter.get_instance()

    # Check if components loaded successfully
    if not tagger or not tagger.is_initialized:
        print("[-] Failed to load POS Tagger.")

    if not sign_converter or not sign_converter.is_initialized:
        print("[-] Failed to load Sign Language Converter.")

    print("[+] API is ready.")
    yield

    # Cleanup on shutdown
    print("[!] Shutting down Vietnamese NLP API...")


# Create FastAPI application instance
app = FastAPI(
    title="Vietnamese Sign Language NLP API",
    description="API for Vietnamese text processing and Sign Language conversion",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory for serving web interface
static_path = Path(__file__).parent.parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


def validate_text_input(text: str) -> str:
    """
    Validate and clean text input from user requests.

    Args:
        text: Raw text input from user

    Returns:
        str: Cleaned text ready for processing

    Raises:
        HTTPException: If text is empty or invalid
    """
    text = text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Please provide text input!")
    return text


def check_component_initialization(component, component_name: str):
    """
    Check if a NLP component is properly initialized.

    Args:
        component: The component instance to check
        component_name: Human-readable name for error messages

    Raises:
        HTTPException: If component is not initialized
    """
    if not component.is_initialized:
        raise HTTPException(status_code=500, detail=f"Error loading {component_name}!")


@app.get("/")
async def read_root():
    """Serve the main HTML interface page."""
    return FileResponse(str(static_path / "index.html"))


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_text(request: TextRequest):
    """
    Analyze Vietnamese text with POS tagging.

    This endpoint performs Part-of-Speech tagging on Vietnamese text using UndertheSea.
    It returns detailed analysis including word tags, statistics, and processing metrics.

    Args:
        request: TextRequest containing the text to analyze

    Returns:
        AnalysisResponse: Results with POS tags and statistics
    """
    try:
        text = validate_text_input(request.text)
        pos_tagger = UndertheSeaPOSTagger.get_instance()
        check_component_initialization(pos_tagger, "POS Tagger")

        # Measure processing time
        start_time = time.time()
        tagged_words = pos_tagger.tag_sentence(text)
        processing_time = time.time() - start_time

        # Calculate statistics
        tag_counts = {}
        for _, tag in tagged_words:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

        return AnalysisResponse(
            success=True,
            results=tagged_words,
            statistics={
                "total_words": len(tagged_words),
                "unique_tags": len(tag_counts),
                "processing_time": round(processing_time, 2),
                "words_per_second": (
                    round(len(tagged_words) / processing_time, 1)
                    if processing_time > 0
                    else 0
                ),
                "tag_distribution": tag_counts,
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@app.post("/api/convert-sign-language", response_model=SignLanguageResponse)
async def convert_to_sign_language(request: TextRequest):
    """
    Convert Vietnamese text to Sign Language representation.

    This endpoint converts Vietnamese text to Vietnamese Sign Language (VSL)
    using linguistic principles. It performs POS tagging first, then applies
    grammar restructuring and sign language conversion rules.

    Args:
        request: TextRequest containing the text to convert

    Returns:
        SignLanguageResponse: VSL conversion with detailed analysis
    """
    try:
        text = validate_text_input(request.text)

        # Get singleton instances
        pos_tagger = UndertheSeaPOSTagger.get_instance()
        sign_converter = VietnameseSignLanguageConverter.get_instance()

        # Check initialization
        check_component_initialization(pos_tagger, "POS Tagger")
        check_component_initialization(sign_converter, "Sign Language Converter")

        # Measure processing time
        start_time = time.time()

        # Step 1: POS tagging
        pos_tagged_words = pos_tagger.tag_sentence(text)

        # Step 2: Convert to sign language
        sign_result = sign_converter.convert_to_sign_language(pos_tagged_words)

        # Add processing time to results
        processing_time = time.time() - start_time
        sign_result["structure_analysis"]["processing_time"] = round(processing_time, 2)

        return SignLanguageResponse(
            success=True,
            original_sentence=sign_result["original_sentence"],
            pos_analysis=pos_tagged_words,
            sign_language_sequence=sign_result["sign_language_sequence"],
            structure_analysis=sign_result["structure_analysis"],
            pos_structure=sign_result["pos_analysis"],
            word_details=sign_result.get("word_details", []),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint for monitoring system status.

    Returns:
        dict: System health status and component availability
    """
    pos_tagger = UndertheSeaPOSTagger.get_instance()
    sign_converter = VietnameseSignLanguageConverter.get_instance()

    return {
        "status": "healthy",
        "pos_tagger_loaded": pos_tagger is not None and pos_tagger.is_initialized,
        "sign_converter_loaded": sign_converter is not None
        and sign_converter.is_initialized,
        "version": "2.0.0",
    }


@app.get("/api/sign-dictionary-info")
async def get_sign_dictionary_info():
    """
    Get information about the sign language conversion system.

    Returns detailed information about the VSL converter including
    dictionary size, conversion strategies, and grammar rules.

    Returns:
        dict: Sign language system information
    """
    try:
        sign_converter = VietnameseSignLanguageConverter.get_instance()
        check_component_initialization(sign_converter, "Sign Language Converter")
        return sign_converter.get_sign_dictionary_info()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting converter info: {str(e)}"
        )


@app.get("/api/examples")
async def get_examples():
    """
    Get example Vietnamese sentences for testing the API.

    Returns:
        dict: List of example sentences in Vietnamese
    """
    examples = [
        "Tôi đang học Công nghệ Thông tin tại Đại học Khoa học Tự nhiên.",
        "Hôm nay trời đẹp, chúng ta đi dạo công viên nhé.",
        "Việt Nam là một đất nước xinh đẹp và giàu truyền thống.",
        "Sinh viên trường Đại học Khoa học Tự Nhiên rất năng động.",
        "Hà Nội là thủ đô của Việt Nam.",
    ]
    return {"examples": examples}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
