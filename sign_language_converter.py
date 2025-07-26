import re
from pathlib import Path
from typing import Dict, List, Tuple


class VietnameseSignLanguageConverter:
    """
    Lớp chuyển đổi câu tiếng Việt sang cấu trúc ngôn ngữ ký hiệu.
    Ngôn ngữ ký hiệu có cấu trúc ngữ pháp khác với tiếng nói,
    thường theo thứ tự: CHỦ NGỮ - TÍNH TỪ - TÂN NGỮ - ĐỘNG TỪ

    Implements Singleton pattern để đảm bảo chỉ có một instance duy nhất.
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            cls._instance = super(VietnameseSignLanguageConverter, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Khởi tạo converter với các quy tắc chuyển đổi"""
        # Chỉ khởi tạo một lần duy nhất
        if VietnameseSignLanguageConverter._initialized:
            return

        print("[+] Initializing Vietnamese Sign Language Converter...")
        self.is_initialized = True
        VietnameseSignLanguageConverter._initialized = True

        # Load từ điển từ file
        self.sign_dictionary = self._load_dictionary_from_file()

        # Từ loại quan trọng để sắp xếp lại câu
        self.important_pos = {
            "NOUN": "noun",
            "PROPN": "proper_noun",
            "VERB": "verb",
            "ADJ": "adjective",
            "PRON": "pronoun",
            "NUM": "number",
            "ADV": "adverb",
        }

        print(f"[+] Loaded {len(self.sign_dictionary)} words from dictionary")
        print("[+] Vietnamese Sign Language Converter initialized successfully.")

    def _load_dictionary_from_file(
        self, dictionary_file: str = "sign_language_dictionary.txt"
    ) -> Dict[str, str]:
        """
        Load từ điển từ file txt.

        Args:
            dictionary_file: Path to dictionary file

        Returns:
            Dictionary mapping Vietnamese words to sign language words
        """
        dictionary = {}
        file_path = Path(__file__).parent / dictionary_file

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()

                    # Skip empty lines and comments
                    if not line or line.startswith("#"):
                        continue

                    # Parse line: vietnamese_word = SIGN_WORD
                    if "=" in line:
                        parts = line.split("=", 1)
                        if len(parts) == 2:
                            vietnamese_word = parts[0].strip()
                            sign_word = parts[1].strip()

                            if vietnamese_word and sign_word:
                                dictionary[vietnamese_word] = sign_word
                            else:
                                print(
                                    f"[!] Warning: Empty word or sign on line {line_num}: {line}"
                                )
                        else:
                            print(
                                f"[!] Warning: Invalid format on line {line_num}: {line}"
                            )
                    else:
                        print(f"[!] Warning: No '=' found on line {line_num}: {line}")

        except FileNotFoundError:
            print(
                f"[!] Warning: Dictionary file '{dictionary_file}' not found. Using empty dictionary."
            )
            print("[!] Please create the dictionary file or check the path.")
        except Exception as e:
            print(f"[!] Error loading dictionary: {e}")
            print("[!] Using empty dictionary.")

        return dictionary

    def reload_dictionary(self, dictionary_file: str = "sign_language_dictionary.txt"):
        """
        Reload từ điển từ file (useful for updating dictionary without restarting)

        Args:
            dictionary_file: Path to dictionary file
        """
        print("[+] Reloading dictionary...")
        old_count = len(self.sign_dictionary)
        self.sign_dictionary = self._load_dictionary_from_file(dictionary_file)
        new_count = len(self.sign_dictionary)
        print(f"[+] Dictionary reloaded: {old_count} -> {new_count} words")

    def convert_to_sign_language(self, pos_tagged_words: List[Tuple[str, str]]) -> Dict:
        """
        Chuyển đổi câu đã được gán nhãn POS sang cấu trúc ngôn ngữ ký hiệu

        Args:
            pos_tagged_words: Danh sách tuple (từ, nhãn_POS)

        Returns:
            Dict chứa cấu trúc ngôn ngữ ký hiệu và thông tin phân tích
        """
        if not self.is_initialized:
            return {"error": "Sign Language Converter is not initialized"}

        # Phân loại từ theo loại
        categorized_words = self._categorize_words(pos_tagged_words)

        # Sắp xếp lại theo cấu trúc ngôn ngữ ký hiệu
        reordered_structure = self._reorder_for_sign_language(categorized_words)

        # Chuyển đổi từ vựng sang ký hiệu
        sign_sequence = self._convert_vocabulary(reordered_structure)

        # Tạo cấu trúc phân tích
        analysis = self._create_analysis(
            pos_tagged_words, categorized_words, sign_sequence
        )

        return {
            "original_sentence": " ".join([word for word, _ in pos_tagged_words]),
            "sign_language_sequence": sign_sequence,
            "structure_analysis": analysis,
            "pos_analysis": categorized_words,
        }

    def _categorize_words(self, pos_tagged_words: List[Tuple[str, str]]) -> Dict:
        """Phân loại từ theo các nhóm từ loại"""
        categories = {
            "subjects": [],  # Chủ ngữ
            "objects": [],  # Tân ngữ
            "verbs": [],  # Động từ
            "adjectives": [],  # Tính từ
            "adverbs": [],  # Trạng từ
            "numbers": [],  # Số từ
            "pronouns": [],  # Đại từ
            "prepositions": [],  # Giới từ
            "others": [],  # Khác
        }

        for word, pos in pos_tagged_words:
            word_lower = word.lower()

            if pos == "PRON":
                categories["pronouns"].append((word, pos))
            elif pos in ["NOUN", "PROPN"]:
                # Phân biệt chủ ngữ và tân ngữ dựa vào vị trí
                if len(categories["subjects"]) == 0 and len(categories["verbs"]) == 0:
                    categories["subjects"].append((word, pos))
                else:
                    categories["objects"].append((word, pos))
            elif pos == "VERB":
                categories["verbs"].append((word, pos))
            elif pos == "ADJ":
                categories["adjectives"].append((word, pos))
            elif pos == "ADV":
                categories["adverbs"].append((word, pos))
            elif pos == "NUM":
                categories["numbers"].append((word, pos))
            elif pos == "ADP":
                categories["prepositions"].append((word, pos))
            else:
                categories["others"].append((word, pos))

        return categories

    def _reorder_for_sign_language(
        self, categorized_words: Dict
    ) -> List[Tuple[str, str]]:
        """
        Sắp xếp lại từ theo cấu trúc ngôn ngữ ký hiệu:
        CHỦ NGỮ - TÍNH TỪ - TÂN NGỮ - ĐỘNG TỪ - TRẠNG TỪ
        """
        reordered = []

        # 1. Đại từ và chủ ngữ
        reordered.extend(categorized_words["pronouns"])
        reordered.extend(categorized_words["subjects"])

        # 2. Tính từ (mô tả chủ ngữ)
        reordered.extend(categorized_words["adjectives"])

        # 3. Số từ
        reordered.extend(categorized_words["numbers"])

        # 4. Tân ngữ
        reordered.extend(categorized_words["objects"])

        # 5. Động từ
        reordered.extend(categorized_words["verbs"])

        # 6. Trạng từ
        reordered.extend(categorized_words["adverbs"])

        # 7. Giới từ và khác
        reordered.extend(categorized_words["prepositions"])
        reordered.extend(categorized_words["others"])

        return reordered

    def _convert_vocabulary(self, word_sequence: List[Tuple[str, str]]) -> List[str]:
        """Chuyển đổi từ vựng sang ký hiệu"""
        sign_sequence = []

        for word, pos in word_sequence:
            word_lower = word.lower()

            # Xử lý từ ghép
            normalized_word = word_lower.replace(" ", "_")

            # Tìm trong từ điển ký hiệu
            if normalized_word in self.sign_dictionary:
                sign_sequence.append(self.sign_dictionary[normalized_word])
            else:
                # Nếu không tìm thấy, giữ nguyên nhưng viết hoa
                sign_sequence.append(word.upper())

        return sign_sequence

    def _create_analysis(
        self,
        original_words: List[Tuple[str, str]],
        categorized: Dict,
        sign_sequence: List[str],
    ) -> Dict:
        """Tạo phân tích cấu trúc câu"""
        return {
            "word_count": len(original_words),
            "sign_count": len(sign_sequence),
            "structure_changes": {
                "subjects": len(categorized["subjects"]),
                "verbs": len(categorized["verbs"]),
                "objects": len(categorized["objects"]),
                "adjectives": len(categorized["adjectives"]),
                "others": len(categorized["others"]),
            },
            "reorder_applied": True,
            "vocabulary_mapped": len(
                [
                    s
                    for s in sign_sequence
                    if not s.isupper() or s in self.sign_dictionary.values()
                ]
            ),
        }

    def get_sign_dictionary_info(self) -> Dict:
        """Lấy thông tin về từ điển ký hiệu"""
        # Automatically categorize words based on common patterns
        categories = {
            "pronouns": [],
            "verbs": [],
            "adjectives": [],
            "nouns": [],
            "time_words": [],
            "question_words": [],
            "numbers": [],
            "others": [],
        }

        # Common word lists for categorization
        pronouns = [
            "tôi",
            "mình",
            "em",
            "bạn",
            "anh",
            "chị",
            "cô",
            "họ",
            "chúng_ta",
            "chúng_tôi",
        ]
        verbs = [
            "là",
            "có",
            "không",
            "đi",
            "đến",
            "về",
            "tới",
            "ăn",
            "uống",
            "ngủ",
            "làm",
            "học",
            "đọc",
            "viết",
            "nói",
            "nghe",
            "nhìn",
            "thấy",
            "yêu",
            "thích",
            "ghét",
            "mua",
            "bán",
            "cho",
            "lấy",
        ]
        adjectives = [
            "đẹp",
            "xấu",
            "tốt",
            "lớn",
            "nhỏ",
            "cao",
            "thấp",
            "dài",
            "ngắn",
            "rộng",
            "hẹp",
            "nóng",
            "lạnh",
            "ấm",
            "mát",
            "vui",
            "buồn",
            "giận",
            "hạnh_phúc",
        ]
        time_words = [
            "hôm_nay",
            "ngày_mai",
            "hôm_qua",
            "sáng",
            "trưa",
            "chiều",
            "tối",
            "tuần",
            "tháng",
            "năm",
        ]
        question_words = ["gì", "ai", "đâu", "khi_nào", "như_thế_nào", "tại_sao"]
        numbers = [
            "một",
            "hai",
            "ba",
            "bốn",
            "năm",
            "sáu",
            "bảy",
            "tám",
            "chín",
            "mười",
        ]

        for word in self.sign_dictionary.keys():
            if word in pronouns:
                categories["pronouns"].append(word)
            elif word in verbs:
                categories["verbs"].append(word)
            elif word in adjectives:
                categories["adjectives"].append(word)
            elif word in time_words:
                categories["time_words"].append(word)
            elif word in question_words:
                categories["question_words"].append(word)
            elif word in numbers:
                categories["numbers"].append(word)
            else:
                categories["nouns"].append(word)

        return {
            "total_entries": len(self.sign_dictionary),
            "categories": {
                "pronouns": len(categories["pronouns"]),
                "verbs": len(categories["verbs"]),
                "adjectives": len(categories["adjectives"]),
                "nouns": len(categories["nouns"]),
                "time_words": len(categories["time_words"]),
                "question_words": len(categories["question_words"]),
                "numbers": len(categories["numbers"]),
            },
            "sample_words": {
                "pronouns": categories["pronouns"][:5],
                "verbs": categories["verbs"][:5],
                "adjectives": categories["adjectives"][:5],
                "nouns": categories["nouns"][:5],
            },
            "dictionary_source": "sign_language_dictionary.txt",
            "note": "Dictionary can be updated by editing the sign_language_dictionary.txt file",
        }

    @classmethod
    def get_instance(cls):
        """
        Lấy singleton instance của Vietnamese Sign Language Converter.

        Returns:
            VietnameseSignLanguageConverter: Singleton instance
        """
        return cls()


if __name__ == "__main__":
    # Test converter - using singleton
    converter = VietnameseSignLanguageConverter.get_instance()

    # Test với câu mẫu
    test_pos_tagged = [
        ("Tôi", "PRON"),
        ("đang", "ADV"),
        ("học", "VERB"),
        ("tiếng", "NOUN"),
        ("Việt", "PROPN"),
        ("tại", "ADP"),
        ("trường", "NOUN"),
        ("đại", "ADJ"),
        ("học", "NOUN"),
    ]

    result = converter.convert_to_sign_language(test_pos_tagged)

    print("\n=== DEMO: Vietnamese to Sign Language ===")
    print(f"Original: {result['original_sentence']}")
    print(f"Sign Language: {' - '.join(result['sign_language_sequence'])}")
    print(f"Structure Analysis: {result['structure_analysis']}")

    # Test singleton pattern
    print("\n[Singleton Test]")
    converter1 = VietnameseSignLanguageConverter()
    converter2 = VietnameseSignLanguageConverter.get_instance()
    print(f"converter1 is converter2: {converter1 is converter2}")
    print(f"Same instance ID: {id(converter1) == id(converter2)}")
