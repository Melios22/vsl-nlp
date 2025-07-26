import json
from typing import Dict, List, Tuple


class GrammarAnalyzer:
    """
    Lớp phân tích sự khác biệt về cấu trúc ngữ pháp giữa Tiếng Việt và ngôn ngữ ký hiệu
    """

    def __init__(self):
        """Khởi tạo analyzer với các quy tắc ngữ pháp"""
        self.is_initialized = True

        # Cấu trúc ngữ pháp tiếng Việt (SVO - Subject-Verb-Object)
        self.vietnamese_grammar = {
            "word_order": "SVO",  # Chủ ngữ - Động từ - Tân ngữ
            "structure": [
                "Subject (Chủ ngữ)",
                "Verb (Động từ)",
                "Object (Tân ngữ)",
                "Adjective (Tính từ - sau danh từ)",
                "Adverb (Trạng từ - trước động từ)",
                "Preposition (Giới từ - trước danh từ)",
            ],
            "features": {
                "tenses": "Thì được biểu hiện qua trạng từ thời gian",
                "adjective_position": "Tính từ đứng sau danh từ",
                "question_formation": "Dùng từ nghi vấn ở cuối câu",
                "negation": "Dùng 'không' trước động từ",
            },
        }

        # Cấu trúc ngữ pháp ngôn ngữ ký hiệu (SOV - Subject-Object-Verb)
        self.sign_language_grammar = {
            "word_order": "SOV",  # Chủ ngữ - Tân ngữ - Động từ
            "structure": [
                "Subject (Chủ ngữ)",
                "Adjective (Tính từ - mô tả chủ ngữ)",
                "Object (Tân ngữ)",
                "Verb (Động từ)",
                "Time (Thời gian - đầu hoặc cuối câu)",
                "Question words (Từ hỏi - cuối câu)",
            ],
            "features": {
                "tenses": "Thời gian được biểu hiện bằng ký hiệu riêng",
                "adjective_position": "Tính từ đứng ngay sau chủ ngữ",
                "question_formation": "Từ nghi vấn ở cuối câu + biểu cảm",
                "negation": "Lắc đầu kèm theo ký hiệu phủ định",
                "spatial_grammar": "Sử dụng không gian 3D để biểu đạt",
                "non_manual_markers": "Biểu cảm mặt và cử chỉ cơ thể",
            },
        }

        # Quy tắc chuyển đổi cấu trúc
        self.conversion_rules = {
            "word_order_change": {
                "from": "Subject + Verb + Object",
                "to": "Subject + Object + Verb",
                "example_vi": "Tôi ăn cơm",
                "example_sign": "TÔI CƠM ĂN",
            },
            "adjective_movement": {
                "from": "Noun + Adjective",
                "to": "Subject + Adjective + Verb/Object",
                "example_vi": "Cô gái đẹp",
                "example_sign": "CÔ-GÁI ĐẸP",
            },
            "time_expression": {
                "from": "Scattered throughout sentence",
                "to": "Beginning or end of sentence",
                "example_vi": "Tôi đã ăn cơm rồi",
                "example_sign": "HÔM-QUA TÔI CƠM ĂN",
            },
        }

        print("[+] Grammar Analyzer initialized successfully.")

    def analyze_sentence_structure(
        self, pos_tagged_words: List[Tuple[str, str]]
    ) -> Dict:
        """
        Phân tích cấu trúc ngữ pháp của câu tiếng Việt
        """
        analysis = {
            "vietnamese_structure": self._analyze_vietnamese_structure(
                pos_tagged_words
            ),
            "sign_language_structure": self._predict_sign_structure(pos_tagged_words),
            "differences": self._compare_structures(pos_tagged_words),
            "conversion_applied": self._get_conversion_rules_applied(pos_tagged_words),
            "grammar_comparison": self._compare_grammar_features(),
        }

        return analysis

    def _analyze_vietnamese_structure(
        self, pos_tagged_words: List[Tuple[str, str]]
    ) -> Dict:
        """Phân tích cấu trúc ngữ pháp tiếng Việt"""
        structure = {
            "word_order": "SVO",
            "identified_components": {},
            "sentence_type": "declarative",  # default
            "complexity": len(pos_tagged_words),
        }

        # Xác định các thành phần câu
        for i, (word, pos) in enumerate(pos_tagged_words):
            if (
                pos in ["NOUN", "PROPN", "PRON"]
                and "subject" not in structure["identified_components"]
            ):
                structure["identified_components"]["subject"] = {
                    "word": word,
                    "position": i,
                }
            elif pos == "VERB" and "verb" not in structure["identified_components"]:
                structure["identified_components"]["verb"] = {
                    "word": word,
                    "position": i,
                }
            elif (
                pos in ["NOUN", "PROPN"]
                and "subject" in structure["identified_components"]
                and "object" not in structure["identified_components"]
            ):
                structure["identified_components"]["object"] = {
                    "word": word,
                    "position": i,
                }
            elif pos == "ADJ":
                if "adjectives" not in structure["identified_components"]:
                    structure["identified_components"]["adjectives"] = []
                structure["identified_components"]["adjectives"].append(
                    {"word": word, "position": i}
                )

        # Xác định loại câu
        if any(
            word.lower() in ["gì", "ai", "đâu", "khi", "nào", "sao", "thế", "nào"]
            for word, _ in pos_tagged_words
        ):
            structure["sentence_type"] = "interrogative"
        elif any(
            pos == "PUNCT" and word in ["!", "ạ", "ơi"]
            for word, pos in pos_tagged_words
        ):
            structure["sentence_type"] = "exclamatory"

        return structure

    def _predict_sign_structure(self, pos_tagged_words: List[Tuple[str, str]]) -> Dict:
        """Dự đoán cấu trúc ngôn ngữ ký hiệu"""
        structure = {
            "word_order": "SOV",
            "predicted_sequence": [],
            "reordering_applied": True,
        }

        # Sắp xếp lại theo SOV
        components = {
            "subjects": [],
            "objects": [],
            "verbs": [],
            "adjectives": [],
            "others": [],
        }

        for word, pos in pos_tagged_words:
            if pos == "PRON":
                components["subjects"].append(word)
            elif pos in ["NOUN", "PROPN"]:
                if not components["subjects"] and not components["verbs"]:
                    components["subjects"].append(word)
                else:
                    components["objects"].append(word)
            elif pos == "VERB":
                components["verbs"].append(word)
            elif pos == "ADJ":
                components["adjectives"].append(word)
            else:
                components["others"].append(word)

        # Tạo sequence theo SOV
        structure["predicted_sequence"].extend(components["subjects"])
        structure["predicted_sequence"].extend(components["adjectives"])
        structure["predicted_sequence"].extend(components["objects"])
        structure["predicted_sequence"].extend(components["verbs"])
        structure["predicted_sequence"].extend(components["others"])

        return structure

    def _compare_structures(self, pos_tagged_words: List[Tuple[str, str]]) -> Dict:
        """So sánh sự khác biệt cấu trúc"""
        differences = {
            "word_order_change": {
                "vietnamese": "SVO (Chủ-Động-Tân)",
                "sign_language": "SOV (Chủ-Tân-Động)",
                "impact": "Động từ di chuyển từ giữa xuống cuối câu",
            },
            "adjective_position": {
                "vietnamese": "Danh từ + Tính từ",
                "sign_language": "Chủ ngữ + Tính từ (liền kề)",
                "impact": "Tính từ được nhóm với chủ ngữ",
            },
            "temporal_markers": {
                "vietnamese": "Trạng từ thời gian rải rác",
                "sign_language": "Thời gian ở đầu/cuối câu",
                "impact": "Tập trung biểu đạt thời gian",
            },
            "spatial_reference": {
                "vietnamese": "Dùng từ ngữ mô tả vị trí",
                "sign_language": "Dùng không gian 3D trực tiếp",
                "impact": "Biểu đạt trực quan hơn",
            },
        }

        return differences

    def _get_conversion_rules_applied(
        self, pos_tagged_words: List[Tuple[str, str]]
    ) -> List[Dict]:
        """Lấy danh sách quy tắc chuyển đổi được áp dụng"""
        applied_rules = []

        # Kiểm tra có động từ và tân ngữ không
        has_verb = any(pos == "VERB" for _, pos in pos_tagged_words)
        has_object = (
            len([pos for _, pos in pos_tagged_words if pos in ["NOUN", "PROPN"]]) > 1
        )

        if has_verb and has_object:
            applied_rules.append(
                {
                    "rule": "SVO → SOV",
                    "description": "Chuyển động từ từ giữa xuống cuối câu",
                    "example": "Tôi ăn cơm → TÔI CƠM ĂN",
                }
            )

        # Kiểm tra có tính từ không
        has_adjective = any(pos == "ADJ" for _, pos in pos_tagged_words)
        if has_adjective:
            applied_rules.append(
                {
                    "rule": "Adjective positioning",
                    "description": "Nhóm tính từ với chủ ngữ",
                    "example": "Cô gái đẹp → CÔ-GÁI ĐẸP",
                }
            )

        return applied_rules

    def _compare_grammar_features(self) -> Dict:
        """So sánh các đặc điểm ngữ pháp"""
        comparison = {
            "word_order": {
                "vietnamese": self.vietnamese_grammar["word_order"],
                "sign_language": self.sign_language_grammar["word_order"],
                "difference": "Tiếng Việt dùng SVO, ngôn ngữ ký hiệu dùng SOV",
            },
            "adjective_placement": {
                "vietnamese": "Sau danh từ",
                "sign_language": "Ngay sau chủ ngữ",
                "difference": "Vị trí tính từ thay đổi để nhóm với chủ ngữ",
            },
            "question_formation": {
                "vietnamese": "Từ hỏi + nội dung câu hỏi",
                "sign_language": "Nội dung + từ hỏi + biểu cảm",
                "difference": "Ngôn ngữ ký hiệu kết hợp biểu cảm mặt",
            },
            "temporal_expression": {
                "vietnamese": "Trạng từ thời gian tự do",
                "sign_language": "Thời gian ở đầu/cuối + ký hiệu chuyên biệt",
                "difference": "Ngôn ngữ ký hiệu tập trung thời gian",
            },
        }

        return comparison

    def get_detailed_analysis_report(
        self, pos_tagged_words: List[Tuple[str, str]]
    ) -> Dict:
        """Tạo báo cáo phân tích chi tiết"""
        analysis = self.analyze_sentence_structure(pos_tagged_words)

        report = {
            "input_analysis": {
                "sentence": " ".join([word for word, _ in pos_tagged_words]),
                "word_count": len(pos_tagged_words),
                "pos_distribution": self._get_pos_distribution(pos_tagged_words),
            },
            "grammar_analysis": analysis,
            "conversion_summary": {
                "structural_changes": len(analysis["conversion_applied"]),
                "complexity_score": self._calculate_complexity_score(pos_tagged_words),
                "conversion_accuracy": "High",  # Could be calculated based on rules
            },
            "educational_insights": self._generate_educational_insights(analysis),
        }

        return report

    def _get_pos_distribution(self, pos_tagged_words: List[Tuple[str, str]]) -> Dict:
        """Phân bố các loại từ"""
        distribution = {}
        for _, pos in pos_tagged_words:
            distribution[pos] = distribution.get(pos, 0) + 1
        return distribution

    def _calculate_complexity_score(
        self, pos_tagged_words: List[Tuple[str, str]]
    ) -> float:
        """Tính điểm phức tạp của câu"""
        # Điểm dựa trên số từ, số loại POS, và cấu trúc
        word_count = len(pos_tagged_words)
        unique_pos = len(set(pos for _, pos in pos_tagged_words))

        complexity = (word_count * 0.3) + (unique_pos * 0.7)
        return round(complexity, 2)

    def _generate_educational_insights(self, analysis: Dict) -> List[str]:
        """Tạo insights giáo dục về sự khác biệt ngữ pháp"""
        insights = [
            "🔄 Thứ tự từ: Tiếng Việt (SVO) vs Ngôn ngữ ký hiệu (SOV)",
            "📍 Vị trí tính từ: Tiếng Việt đặt sau danh từ, ngôn ngữ ký hiệu nhóm với chủ ngữ",
            "⏰ Biểu đạt thời gian: Ngôn ngữ ký hiệu tập trung thời gian ở đầu/cuối câu",
            "🤲 Không gian 3D: Ngôn ngữ ký hiệu sử dụng không gian để biểu đạt quan hệ",
            "😊 Biểu cảm phi ngôn ngữ: Ngôn ngữ ký hiệu kết hợp biểu cảm mặt và cử chỉ",
        ]

        return insights


# Global analyzer instance
grammar_analyzer = None


def initialize_grammar_analyzer():
    """Khởi tạo grammar analyzer"""
    global grammar_analyzer
    if grammar_analyzer is None:
        print("[+] Initializing Grammar Analyzer...")
        grammar_analyzer = GrammarAnalyzer()
    return grammar_analyzer


def get_grammar_analyzer2():
    """Lấy grammar analyzer instance"""
    global grammar_analyzer
    if grammar_analyzer is None:
        grammar_analyzer = initialize_grammar_analyzer()
    return grammar_analyzer


if __name__ == "__main__":
    # Test analyzer
    analyzer = GrammarAnalyzer()

    test_pos_tagged = [
        ("Tôi", "PRON"),
        ("học", "VERB"),
        ("tiếng", "NOUN"),
        ("Việt", "PROPN"),
        ("tại", "ADP"),
        ("trường", "NOUN"),
        ("đại", "ADJ"),
        ("học", "NOUN"),
    ]

    report = analyzer.get_detailed_analysis_report(test_pos_tagged)

    print("\n=== GRAMMAR ANALYSIS REPORT ===")
    print(f"Input: {report['input_analysis']['sentence']}")
    print(f"Complexity Score: {report['conversion_summary']['complexity_score']}")
    print("\nStructural Changes:")
    for rule in report["grammar_analysis"]["conversion_applied"]:
        print(f"  - {rule['rule']}: {rule['description']}")
    print("\nEducational Insights:")
    for insight in report["educational_insights"]:
        print(f"  {insight}")
