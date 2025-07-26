from underthesea import pos_tag


class UndertheSeaPOSTagger:
    """
    Một lớp để thực hiện gán nhãn từ loại cho tiếng Việt sử dụng UndertheSea.
    UndertheSea là một thư viện NLP tiếng Việt nhẹ và nhanh.

    Implements Singleton pattern để đảm bảo chỉ có một instance duy nhất.
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            cls._instance = super(UndertheSeaPOSTagger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Khởi tạo UndertheSea POS tagger.
        """
        # Chỉ khởi tạo một lần duy nhất
        if UndertheSeaPOSTagger._initialized:
            return

        try:
            # Test the pos_tag function to make sure it works
            test_result = pos_tag("Xin chào")
            if test_result:
                self.is_initialized = True
                UndertheSeaPOSTagger._initialized = True
                print("[+] UndertheSea POS Tagger initialized successfully.")
            else:
                self.is_initialized = False
                print("[-] Failed to initialize UndertheSea POS Tagger.")
        except Exception as e:
            print(f"[-] Error initializing UndertheSea: {e}")
            self.is_initialized = False

    def tag_sentence(self, sentence: str) -> list:
        """
        Gán nhãn từ loại cho một câu tiếng Việt.

        Args:
            sentence: Một chuỗi string là câu tiếng Việt cần gán nhãn.

        Returns:
            Một danh sách các tuple, mỗi tuple chứa (từ, nhãn_từ_loại).
            Ví dụ: [('Tôi', 'P'), ('đi', 'V'), ('học', 'V'), ('.', 'CH')]
        """
        if not self.is_initialized:
            print("[-] UndertheSea POS tagger is not initialized.")
            return []

        try:
            # Sử dụng UndertheSea để gán nhãn từ loại
            pos_tags_result = pos_tag(sentence)

            # UndertheSea trả về list of tuples: [('word', 'tag'), ...]
            # Chuyển đổi nhãn UndertheSea sang Universal Dependencies nếu cần
            formatted_tags = []
            for word, tag in pos_tags_result:
                # Chuyển đổi nhãn từ UndertheSea sang UD tags
                ud_tag = self._convert_to_ud_tag(tag)
                formatted_tags.append((word, ud_tag))

            return formatted_tags
        except Exception as e:
            print(f"[-] Error during POS tagging: {e}")
            return []

    def _convert_to_ud_tag(self, underthesea_tag: str) -> str:
        """
        Chuyển đổi nhãn POS của UndertheSea sang Universal Dependencies tags.

        Args:
            underthesea_tag: Nhãn POS từ UndertheSea

        Returns:
            Nhãn Universal Dependencies tương ứng
        """
        # Mapping từ UndertheSea tags sang UD tags
        tag_mapping = {
            # Nouns
            "N": "NOUN",  # Noun
            "Np": "PROPN",  # Proper noun
            "Ny": "NOUN",  # Noun abbreviation
            # Verbs
            "V": "VERB",  # Verb
            "Vb": "VERB",  # Verb be
            "Vu": "VERB",  # Verb auxiliary
            # Adjectives
            "A": "ADJ",  # Adjective
            "Ab": "ADJ",  # Adjective
            # Adverbs
            "R": "ADV",  # Adverb
            "Rb": "ADV",  # Adverb
            # Pronouns
            "P": "PRON",  # Pronoun
            "Pp": "PRON",  # Personal pronoun
            # Prepositions
            "E": "ADP",  # Preposition
            "Eb": "ADP",  # Preposition
            # Conjunctions
            "C": "CCONJ",  # Conjunction
            "Cc": "CCONJ",  # Coordinating conjunction
            "Cs": "SCONJ",  # Subordinating conjunction
            # Determiners
            "L": "DET",  # Determiner
            "Lb": "DET",  # Determiner
            # Numbers
            "M": "NUM",  # Number
            "Mb": "NUM",  # Number
            # Punctuation
            "CH": "PUNCT",  # Punctuation
            ".": "PUNCT",  # Period
            ",": "PUNCT",  # Comma
            "?": "PUNCT",  # Question mark
            "!": "PUNCT",  # Exclamation mark
            # Particles
            "T": "PART",  # Particle
            "Tb": "PART",  # Particle
            # Interjections
            "I": "INTJ",  # Interjection
            # Others
            "X": "X",  # Other
            "Fw": "X",  # Foreign word
        }

        return tag_mapping.get(underthesea_tag, "X")

    @classmethod
    def get_instance(cls):
        """
        Lấy singleton instance của UndertheSea POS Tagger.

        Returns:
            UndertheSeaPOSTagger: Singleton instance
        """
        return cls()


# Only run demo if this file is executed directly
if __name__ == "__main__":
    # Câu ví dụ
    test_sentence = "Sinh viên trường Đại học Khoa học Tự Nhiên rất năng động."

    # Initialize tagger for demo - using singleton
    demo_tagger = UndertheSeaPOSTagger.get_instance()

    # Thực hiện gán nhãn
    if demo_tagger.is_initialized:
        tagged_words = demo_tagger.tag_sentence(test_sentence)

        # In kết quả
        print(f"\nInput: {test_sentence}")
        print("Output (UndertheSea -> UD tags):")
        for word, tag in tagged_words:
            print(f"\t- {word}: {tag}")

        # Test singleton pattern
        print("\n[Singleton Test]")
        tagger1 = UndertheSeaPOSTagger()
        tagger2 = UndertheSeaPOSTagger.get_instance()
        print(f"tagger1 is tagger2: {tagger1 is tagger2}")
        print(f"Same instance ID: {id(tagger1) == id(tagger2)}")
    else:
        print("[-] Failed to initialize UndertheSea tagger")
