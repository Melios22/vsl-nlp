"""
Vietnamese Sign Language Converter
=================================

This module converts Vietnamese text to Vietnamese Sign Language (VSL) representation
using linguistic principles. It restructures Vietnamese SVO grammar to VSL SOV grammar
and applies sign language specific rules.

Core Strategy: DECOMPOSE and REORDER
- Vietnamese: SVO (Subject-Verb-Object)
- Sign Language: SOV (Subject-Object-Verb)

Features:
- Grammar restructuring from SVO to SOV
- Dictionary-based sign conversion
- Spatial and gestural annotations
- Classifier integration for proper VSL representation
"""

from pathlib import Path
from typing import Dict, List, Tuple


class VietnameseSignLanguageConverter:
    """
    Vietnamese Sign Language Converter with linguistic accuracy.

    This class converts Vietnamese sentences to Vietnamese Sign Language (VSL)
    representation using proper linguistic principles rather than simple word mapping.

    Main Strategy: DECOMPOSE and REORDER
    - Decomposes Vietnamese SVO structure
    - Reorders to VSL SOV structure
    - Applies sign language specific grammar rules

    Implements Singleton pattern for efficient resource management.
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        """
        Singleton pattern implementation.

        Returns:
            VietnameseSignLanguageConverter: The singleton instance
        """
        if cls._instance is None:
            cls._instance = super(VietnameseSignLanguageConverter, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize the converter with conversion rules and dictionary.

        This method only runs once due to the singleton pattern.
        It loads the sign language dictionary and sets up grammar rules.
        """
        # Only initialize once
        if VietnameseSignLanguageConverter._initialized:
            return

        self.is_initialized = True
        VietnameseSignLanguageConverter._initialized = True

        # Initialize sign language conversion rules and dictionary
        self._init_conversion_rules()


    def _init_conversion_rules(self):
        """
        Initialize conversion rules and load sign language dictionary.

        Strategy: DECOMPOSE and REORDER Vietnamese text
        - Vietnamese: SVO (Subject-Verb-Object)
        - Sign Language: SOV (Subject-Object-Verb)
        """
        # Load sign language dictionary from file
        self.basic_signs = self._load_dictionary_from_file()

        # Grammar reordering strategy for VSL
        self.reorder_strategy = {
            "word_order": "SOV",  # Subject-Object-Verb
            "time_first": True,  # Time expressions at beginning
            "adjective_with_subject": True,  # Adjectives follow subjects
        }

    def _load_dictionary_from_file(self) -> Dict[str, str]:
        """
        Load Vietnamese Sign Language dictionary from text file.

        The dictionary file should contain lines in format:
        vietnamese_word = SIGN_LANGUAGE_WORD

        Returns:
            Dict[str, str]: Dictionary mapping Vietnamese words to sign representations
        """
        dictionary = {}
        dict_file_path = (
            Path(__file__).parent.parent / "data" / "sign_language_dictionary.txt"
        )

        try:
            if not dict_file_path.exists():
                print(f"[!] Dictionary file not found: {dict_file_path}")
                print("[*] Using fallback dictionary...")
                return self._get_fallback_dictionary()

            with open(dict_file_path, "r", encoding="utf-8") as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()

                    # Skip empty lines and comments
                    if not line or line.startswith("#"):
                        continue

                    # Parse line format: vietnamese_word = SIGN_LANGUAGE_WORD
                    if "=" in line:
                        try:
                            vietnamese_word, sign_word = line.split("=", 1)
                            vietnamese_word = vietnamese_word.strip().lower()
                            sign_word = sign_word.strip().upper()

                            if vietnamese_word and sign_word:
                                dictionary[vietnamese_word] = sign_word
                        except ValueError:
                            print(f"[!] Error parsing line {line_num}: {line}")
                            continue

            print(f"[+] Loaded {len(dictionary)} words from dictionary file")
            return dictionary

        except Exception as e:
            print(f"[!] Error loading dictionary file: {e}")
            return self._get_fallback_dictionary()

    def _get_fallback_dictionary(self) -> Dict[str, str]:
        """
        Fallback dictionary in case file loading fails.

        This provides basic Vietnamese to VSL mappings for common words.

        Returns:
            Dict[str, str]: Basic fallback dictionary
        """
        return {
            # Pronouns
            "tôi": "TÔI",
            "bạn": "BẠN",
            "họ": "HỌ",
            "chúng tôi": "CHÚNG-TÔI",
            "chúng ta": "CHÚNG-TA",
            # Common verbs
            "đi": "ĐI",
            "ăn": "ĂN",
            "học": "HỌC",
            "làm": "LÀM",
            "nói": "NÓI",
            # Numbers
            "một": "1",
            "hai": "2",
            "ba": "3",
            "bốn": "4",
            "năm": "5",
            # Common words
            "không": "KHÔNG",
            "có": "CÓ",
            "rất": "RẤT",
            "và": "VÀ",
        }

    def convert_to_sign_language(self, pos_tagged_words: List[Tuple[str, str]]) -> Dict:
        """
        Convert Vietnamese text to Sign Language representation.

        CONVERSION STRATEGY: DECOMPOSE and REORDER

        Step 1: Categorize words by type (subject, verb, object, adjective...)
        Step 2: Reorder according to VSL SOV structure
        Step 3: Apply sign language specific rules

        Args:
            pos_tagged_words: List of (word, POS_tag) tuples

        Returns:
            Dict containing the restructured sign language representation
        """
        if not self.is_initialized:
            return {"error": "Sign Language Converter is not initialized"}

        # STEP 1: CATEGORIZE words by grammatical function
        categorized_words = self._categorize_words(pos_tagged_words)

        # STEP 2: REORDER according to sign language structure (SOV)
        reordered_structure = self._reorder_for_sign_language(categorized_words)

        # STEP 3: Generate final sequence (keep original or use dictionary)
        final_sequence = [word for word, _ in reordered_structure]

        # Create detailed word information
        word_details = self._create_word_details(pos_tagged_words)

        # Create analysis report
        analysis = self._create_analysis(
            pos_tagged_words, categorized_words, final_sequence
        )

        return {
            "original_sentence": " ".join([word for word, _ in pos_tagged_words]),
            "sign_language_sequence": final_sequence,
            "structure_analysis": analysis,
            "pos_analysis": categorized_words,
            "word_details": word_details,
            "reorder_strategy": "Vietnamese SVO → Sign Language SOV",
        }

    def _categorize_words(self, pos_tagged_words: List[Tuple[str, str]]) -> Dict:
        """
        Categorize words by grammatical function for VSL conversion.

        This is crucial for proper VSL grammar as different word types
        have different positions in the sentence structure.

        Args:
            pos_tagged_words: List of (word, POS_tag) tuples

        Returns:
            Dict with categorized words by grammatical function
        """
        categories = {
            "subjects": [],  # Subject nouns/pronouns
            "objects": [],  # Object nouns
            "verbs": [],  # Action verbs
            "adjectives": [],  # Descriptive adjectives
            "adverbs": [],  # Adverbs/modifiers
            "numbers": [],  # Numerical expressions
            "pronouns": [],  # Pronouns
            "prepositions": [],  # Spatial prepositions
            "time_expressions": [],  # Temporal expressions
            "others": [],  # Other word types
        }

        for word, pos in pos_tagged_words:
            word_lower = word.lower()

            # Categorize based on POS tags and word position
            if pos == "PRON":
                categories["pronouns"].append((word, pos))
            elif pos in ["NOUN", "PROPN"]:
                # Distinguish subject vs object based on position
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
                # Check for time expressions
                if self._is_time_expression(word_lower):
                    categories["time_expressions"].append((word, pos))
                else:
                    categories["others"].append((word, pos))

        return categories

    def _is_time_expression(self, word: str) -> bool:
        """
        Check if a word is a time expression.

        Args:
            word: Word to check

        Returns:
            bool: True if word represents time
        """
        time_words = {
            "hôm nay",
            "ngày mai",
            "hôm qua",
            "tuần này",
            "tháng này",
            "sáng",
            "chiều",
            "tối",
            "đêm",
            "bây giờ",
            "lúc này",
        }
        return word in time_words

    def _reorder_for_sign_language(
        self, categorized_words: Dict
    ) -> List[Tuple[str, str]]:
        """
        Reorder words according to Vietnamese Sign Language grammar.

        REORDERING STRATEGY: Vietnamese SVO → Sign Language SOV

        Vietnamese (SVO): Tôi ăn cơm
        Sign Language (SOV): Tôi cơm ăn

        VSL Word Order:
        1. Time expressions (first)
        2. Subject + Pronouns
        3. Adjectives (describing subject)
        4. Numbers
        5. Objects
        6. Verbs (last in SOV)
        7. Adverbs and prepositions
        8. Other words

        Args:
            categorized_words: Dictionary of categorized words

        Returns:
            List of reordered (word, POS_tag) tuples
        """
        reordered = []

        # 1. Time expressions first (VSL places time at beginning)
        reordered.extend(categorized_words["time_expressions"])

        # 2. Subjects and pronouns
        reordered.extend(categorized_words["pronouns"])
        reordered.extend(categorized_words["subjects"])

        # 3. Adjectives (describing subjects)
        reordered.extend(categorized_words["adjectives"])

        # 4. Numbers
        reordered.extend(categorized_words["numbers"])

        # 5. Objects (before verbs in SOV structure)
        reordered.extend(categorized_words["objects"])

        # 6. Verbs (last in SOV structure)
        reordered.extend(categorized_words["verbs"])

        # 7. Adverbs and prepositions
        reordered.extend(categorized_words["adverbs"])
        reordered.extend(categorized_words["prepositions"])

        # 8. Other words
        reordered.extend(categorized_words["others"])

        return reordered

    def _create_word_details(
        self, pos_tagged_words: List[Tuple[str, str]]
    ) -> List[Dict]:
        """
        Create detailed information for each word including dictionary lookup.

        Args:
            pos_tagged_words: List of (word, POS_tag) tuples

        Returns:
            List of dictionaries with detailed word information
        """
        word_details = []

        for index, (word, pos) in enumerate(pos_tagged_words):
            word_lower = word.lower()
            normalized_word = word_lower.replace(" ", "_")

            # Check if word exists in sign language dictionary
            dictionary_match = None
            has_dictionary_definition = False

            if normalized_word in self.basic_signs:
                dictionary_match = self.basic_signs[normalized_word]
                has_dictionary_definition = True

            word_details.append(
                {
                    "index": index + 1,
                    "original_word": word,
                    "pos_tag": pos,
                    "has_dictionary_definition": has_dictionary_definition,
                    "dictionary_action": (
                        dictionary_match
                        if has_dictionary_definition
                        else f"{word.upper()}[{pos}]"
                    ),
                    "in_dictionary": has_dictionary_definition,
                }
            )

        return word_details

    def _create_analysis(
        self,
        original_words: List[Tuple[str, str]],
        categorized: Dict,
        final_sequence: List[str],
    ) -> Dict:
        """
        Create analysis report of the conversion process.

        Args:
            original_words: Original POS-tagged words
            categorized: Categorized word groups
            final_sequence: Final converted sequence

        Returns:
            Dict containing conversion analysis
        """
        return {
            "word_count": len(original_words),
            "reordered_count": len(final_sequence),
            "structure_changes": {
                "subjects": len(categorized["subjects"]),
                "verbs": len(categorized["verbs"]),
                "objects": len(categorized["objects"]),
                "adjectives": len(categorized["adjectives"]),
                "time_expressions": len(categorized["time_expressions"]),
                "others": len(categorized["others"]),
            },
            "reorder_strategy": {
                "original_order": "SVO (Subject-Verb-Object)",
                "sign_language_order": "SOV (Subject-Object-Verb)",
                "time_placement": "Beginning of sentence",
                "adjective_placement": "After subject",
            },
            "conversion_applied": True,
        }

    def get_sign_dictionary_info(self) -> Dict:
        """
        Get information about the VSL conversion system.

        Returns detailed information about the converter including
        dictionary size, conversion strategies, and grammar rules.

        Returns:
            Dict: Sign language system information
        """
        return {
            "conversion_system": "Vietnamese Sign Language (VSL) Converter",
            "total_basic_signs": len(self.basic_signs),
            "conversion_strategies": [
                "word_categorization",
                "sov_reordering",
                "dictionary_mapping",
            ],
            "grammar_features": {
                "word_order": self.reorder_strategy["word_order"],
                "time_first": self.reorder_strategy["time_first"],
                "adjective_with_subject": self.reorder_strategy[
                    "adjective_with_subject"
                ],
                "uses_dictionary": True,
                "fallback_to_pos": True,
            },
            "reorder_strategy": self.reorder_strategy,
            "note": "System uses dictionary file with POS tag fallback",
        }

    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance of the Vietnamese Sign Language Converter.

        Returns:
            VietnameseSignLanguageConverter: The singleton instance
        """
        return cls()


# Demo and testing code
if __name__ == "__main__":
    print("=== Vietnamese Sign Language Converter Demo ===")

    # Initialize converter using singleton pattern
    converter = VietnameseSignLanguageConverter.get_instance()

    # Test with sample sentence
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

    print(f"\\nOriginal: {result['original_sentence']}")
    print(f"Sign Language: {' - '.join(result['sign_language_sequence'])}")
    print(f"\\nStructure Analysis:")
    for key, value in result["structure_analysis"].items():
        print(f"  {key}: {value}")

    # Test singleton pattern
    print("\\n=== Singleton Pattern Test ===")
    converter1 = VietnameseSignLanguageConverter()
    converter2 = VietnameseSignLanguageConverter.get_instance()
    print(f"converter1 is converter2: {converter1 is converter2}")
    print(f"Same instance ID: {id(converter1) == id(converter2)}")
