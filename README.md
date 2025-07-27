# Vietnamese Sign Language (VSL) NLP System

A Vietnamese Natural Language Processing system that converts Vietnamese text to Vietnamese Sign Language (VSL) representation using proper linguistic principles.

## What is this project?

This system analyzes Vietnamese text and converts it to Vietnamese Sign Language format by:

1. **POS Tagging**: Analyzing Vietnamese text grammar using UndertheSea library
2. **Grammar Restructuring**: Converting Vietnamese SVO (Subject-Verb-Object) structure to VSL SOV (Subject-Object-Verb) structure  
3. **Sign Language Conversion**: Mapping Vietnamese words to sign language representations using a curated dictionary

## What is it meant to do?

- **Process Vietnamese text** with accurate grammatical analysis
- **Convert to VSL format** following proper sign language grammar rules
- **Provide detailed analysis** of the conversion process
- **Serve results via REST API** for integration with other applications

### Example Conversion:
```
Input (Vietnamese):  "Tôi đang học tiếng Việt"
Output (VSL):        "TÔI TIẾNG VIỆT HỌC ĐANG"
Structure:           Subject → Object → Verb → Adverb
```

## Important Note: Dictionary

**The current VSL dictionary (`src/data/sign_language_dictionary.txt`) is for demonstration purposes only.**

- Contains ~90 basic Vietnamese-VSL word mappings as examples
- **Should be replaced** with a comprehensive, linguistically accurate VSL dictionary for production use
- **Recommendations**:
  - Consult certified Vietnamese Sign Language experts
  - Use validated VSL dictionaries from recognized institutions
  - Expand vocabulary based on your specific use case
  - Regular updates and validation by VSL community

The system will fall back to POS tags for words not found in the dictionary.rocessing system that converts Vietnamese text to Vietnamese Sign Language (VSL) representation using proper linguistic principles.

## How to Run

### Prerequisites
```bash
pip install -r requirements.txt
```

### Normal Execution

#### Option 1: Production Mode (Recommended)
```bash
python main.py
```

### Docker Execution

#### Using Docker Compose (Recommended)
```bash
docker-compose up --build
```

#### Using Docker directly
```bash
# Build the image
docker build -t vsl-nlp .

# Run the container
docker run -p 8000:8000 vsl-nlp
```

### Access the Application
- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## � Dependencies

### Core Dependencies
- **FastAPI** (0.112.2) - Web framework for the API
- **Uvicorn** (0.35.0) - ASGI server
- **Pydantic** (2.11.7) - Data validation and settings management
- **UndertheSea** (6.8.4) - Vietnamese NLP library for POS tagging

### Full Dependencies List
See `requirements.txt` for complete list of dependencies including versions.

### System Requirements
- **Python**: 3.8 or higher
- **Memory**: ~100MB baseline + model loading
- **Platform**: Linux, macOS, Windows

## API Endpoints

- `POST /api/analyze` - POS tagging for Vietnamese text
- `POST /api/convert-sign-language` - Convert Vietnamese to VSL
- `GET /api/health` - System health check
- `GET /api/sign-dictionary-info` - VSL system information

---

**Note**: This system provides linguistic representation of Vietnamese Sign Language. For actual sign language learning, consult certified VSL instructors.

