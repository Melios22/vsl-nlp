import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# from grammar_analyzer import get_grammar_analyzer2, initialize_grammar_analyzer
from sign_language_converter import VietnameseSignLanguageConverter
from tagger import UndertheSeaPOSTagger


@asynccontextmanager
async def lifespan(app: FastAPI):  # Initialize the model during startup
    # Initialize singletons - they will handle their own initialization
    tagger = UndertheSeaPOSTagger.get_instance()
    sign_converter = VietnameseSignLanguageConverter.get_instance()
    # grammar_analyzer = initialize_grammar_analyzer()

    if tagger and tagger.is_initialized:
        print("[+] POS Tagger loaded successfully!")
    else:
        print("[-] Failed to load POS Tagger.")

    if sign_converter and sign_converter.is_initialized:
        print("[+] Sign Language Converter loaded successfully!")
    else:
        print("[-] Failed to load Sign Language Converter.")

    # if grammar_analyzer and grammar_analyzer.is_initialized:
    #     print("[+] Grammar Analyzer loaded successfully!")
    # else:
    #     print("[-] Failed to load Grammar Analyzer.")

    print("[+] API is ready.")

    yield

    # Shutdown
    print("[!] Shutting down Vietnamese NLP API...")


app = FastAPI(
    title="Vietnamese NLP API",
    description="API for Vietnamese NLP: POS tagging and Sign Language conversion using UndertheSea",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS middleware để cho phép frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production nên chỉ định cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


class TextRequest(BaseModel):
    text: str


class AnalysisResponse(BaseModel):
    success: bool
    results: list = None
    statistics: dict = None
    error: str = None


class SignLanguageResponse(BaseModel):
    success: bool
    original_sentence: str = None
    pos_analysis: list = None
    sign_language_sequence: list = None
    structure_analysis: dict = None
    pos_structure: dict = None
    grammar_analysis: dict = None
    error: str = None


def get_pos_tagger():
    """Get the singleton POS tagger instance"""
    return UndertheSeaPOSTagger.get_instance()


def get_sign_language_converter():
    """Get the singleton sign language converter instance"""
    return VietnameseSignLanguageConverter.get_instance()


def validate_text_input(text: str) -> str:
    """Validate and clean text input"""
    text = text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Vui lòng nhập văn bản!")
    return text


def check_component_initialization(component, component_name: str):
    """Check if a component is properly initialized"""
    if not component.is_initialized:
        raise HTTPException(status_code=500, detail=f"Lỗi khi tải {component_name}!")


# def get_grammar_analyzer():
#     """Get the initialized grammar analyzer"""
#     return get_grammar_analyzer2()


@app.get("/")
async def read_root():
    """Serve the main HTML page"""
    return FileResponse("static/index.html")


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_text(request: TextRequest):
    """API endpoint để phân tích văn bản"""
    try:
        text = validate_text_input(request.text)
        pos_tagger = get_pos_tagger()
        check_component_initialization(pos_tagger, "POS Tagger")

        # Đo thời gian và thực hiện gán nhãn
        start_time = time.time()
        tagged_words = pos_tagger.tag_sentence(text)
        processing_time = time.time() - start_time

        # Tính thống kê
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
        raise HTTPException(status_code=500, detail=f"Lỗi khi phân tích: {str(e)}")


@app.post("/api/convert-sign-language", response_model=SignLanguageResponse)
async def convert_to_sign_language(request: TextRequest):
    """API endpoint để chuyển đổi văn bản sang ngôn ngữ ký hiệu"""
    try:
        text = validate_text_input(request.text)

        # Lấy components (singletons)
        pos_tagger = get_pos_tagger()
        sign_converter = get_sign_language_converter()
        # grammar_analyzer = get_grammar_analyzer()

        # Kiểm tra initialization
        check_component_initialization(pos_tagger, "POS Tagger")
        check_component_initialization(sign_converter, "Sign Language Converter")
        # check_component_initialization(grammar_analyzer, "Grammar Analyzer")

        # Đo thời gian xử lý
        start_time = time.time()

        # Bước 1: Thực hiện POS tagging
        pos_tagged_words = pos_tagger.tag_sentence(text)

        # Bước 2: Phân tích ngữ pháp
        # grammar_analysis = grammar_analyzer.get_detailed_analysis_report(pos_tagged_words)

        # Bước 3: Chuyển đổi sang ngôn ngữ ký hiệu
        sign_result = sign_converter.convert_to_sign_language(pos_tagged_words)

        # Thêm thời gian xử lý vào kết quả
        processing_time = time.time() - start_time
        sign_result["structure_analysis"]["processing_time"] = round(processing_time, 2)

        return SignLanguageResponse(
            success=True,
            original_sentence=sign_result["original_sentence"],
            pos_analysis=pos_tagged_words,
            sign_language_sequence=sign_result["sign_language_sequence"],
            structure_analysis=sign_result["structure_analysis"],
            pos_structure=sign_result["pos_analysis"],
            # grammar_analysis=grammar_analysis,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi chuyển đổi: {str(e)}")


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    pos_tagger = get_pos_tagger()
    sign_converter = get_sign_language_converter()
    # grammar_analyzer = get_grammar_analyzer()

    return {
        "status": "healthy",
        "pos_tagger_loaded": pos_tagger is not None and pos_tagger.is_initialized,
        "sign_converter_loaded": sign_converter is not None
        and sign_converter.is_initialized,
        # "grammar_analyzer_loaded": grammar_analyzer is not None and grammar_analyzer.is_initialized,
    }


# @app.get("/api/grammar-comparison")
# async def get_grammar_comparison():
#     """Get detailed grammar comparison between Vietnamese and Sign Language"""
#     try:
#         grammar_analyzer = get_grammar_analyzer()
#         if not grammar_analyzer.is_initialized:
#             raise HTTPException(
#                 status_code=500, detail="Grammar analyzer not initialized"
#             )

#         comparison = {
#             "vietnamese_grammar": grammar_analyzer.vietnamese_grammar,
#             "sign_language_grammar": grammar_analyzer.sign_language_grammar,
#             "conversion_rules": grammar_analyzer.conversion_rules,
#             "key_differences": [
#                 "Thứ tự từ: Tiếng Việt dùng SVO, ngôn ngữ ký hiệu dùng SOV",
#                 "Vị trí tính từ: Tiếng Việt đặt sau danh từ, ngôn ngữ ký hiệu nhóm với chủ ngữ",
#                 "Biểu đạt thời gian: Ngôn ngữ ký hiệu tập trung thời gian ở đầu/cuối câu",
#                 "Sử dụng không gian 3D để biểu đạt quan hệ địa lý và ngữ pháp",
#                 "Kết hợp biểu cảm mặt và cử chỉ cơ thể như một phần của ngữ pháp",
#             ],
#         }

#         return comparison
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"Error getting grammar comparison: {str(e)}"
#         )


@app.get("/api/sign-dictionary-info")
async def get_sign_dictionary_info():
    """Get information about the sign language dictionary"""
    try:
        sign_converter = get_sign_language_converter()
        check_component_initialization(sign_converter, "Sign Language Converter")
        return sign_converter.get_sign_dictionary_info()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting dictionary info: {str(e)}"
        )


@app.post("/api/reload-dictionary")
async def reload_sign_dictionary():
    """Reload the sign language dictionary from file"""
    try:
        sign_converter = get_sign_language_converter()
        check_component_initialization(sign_converter, "Sign Language Converter")

        old_count = len(sign_converter.sign_dictionary)
        sign_converter.reload_dictionary()
        new_count = len(sign_converter.sign_dictionary)

        return {
            "success": True,
            "message": f"Dictionary reloaded successfully",
            "old_count": old_count,
            "new_count": new_count,
            "change": new_count - old_count,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error reloading dictionary: {str(e)}"
        )


@app.get("/api/examples")
async def get_examples():
    """Get example sentences"""
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
