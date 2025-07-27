"""
Vietnamese Sign Language NLP Application
========================================

Main entry point for the Vietnamese Sign Language Natural Language Processing system.
This application provides a web API for Vietnamese text analysis and sign language conversion.

Usage:
    python main.py                    # Start development server
    python -m uvicorn main:app       # Alternative startup method

Environment Variables:
    HOST: Server host (default: 0.0.0.0)
    PORT: Server port (default: 8000)
"""

import os
import sys
from pathlib import Path

# Add src directory to Python path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

if __name__ == "__main__":
    import uvicorn

    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    print("=" * 50)
    print(f"Starting server at http://{host}:{port}")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)

    # Import the app after setting up the path
    from src.api.main import app

    # Start the server
    uvicorn.run(
        app,  # Use app object directly
        host=host,
        port=port,
        reload=False,  # Disable reload to avoid import string issues
        log_level="info",
    )
