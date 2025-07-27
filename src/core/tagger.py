"""
Vietnamese POS Tagger using UndertheSea
======================================

This module provides Vietnamese Part-of-Speech tagging functionality using
the UndertheSea library. It implements a singleton pattern for efficient
resource management and converts UndertheSea tags to Universal Dependencies format.

Features:
- Singleton pattern for memory efficiency
- Automatic tag conversion to UD format
- Error handling and initialization checking
- Vietnamese language optimization
"""

from typing import List, Tuple

from underthesea import pos_tag


class UndertheSeaPOSTagger:
    """
    Vietnamese Part-of-Speech tagger using UndertheSea library.

    This class provides POS tagging for Vietnamese text using the UndertheSea
    NLP library, which is lightweight and fast for Vietnamese language processing.

    Implements Singleton pattern to ensure only one instance exists and
    to avoid repeated model loading.
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        """
        Singleton pattern implementation.

        Returns:
            UndertheSeaPOSTagger: The singleton instance
        """
        if cls._instance is None:
            cls._instance = super(UndertheSeaPOSTagger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize the UndertheSea POS tagger.

        This method only runs once due to the singleton pattern.
        It tests the pos_tag function to ensure proper initialization.
        """
        # Only initialize once
        if UndertheSeaPOSTagger._initialized:
            return

        try:
            # Test the pos_tag function to ensure it works
            test_result = pos_tag("Xin chào")
            if test_result:
                self.is_initialized = True
                UndertheSeaPOSTagger._initialized = True
            else:
                self.is_initialized = False
                print("[-] Failed to initialize UndertheSea POS Tagger.")
        except Exception as e:
            print(f"[-] Error initializing UndertheSea: {e}")
            self.is_initialized = False

    def tag_sentence(self, sentence: str) -> List[Tuple[str, str]]:
        """
        Perform POS tagging on a Vietnamese sentence.

        Args:
            sentence: Vietnamese text string to be tagged

        Returns:
            List of tuples containing (word, POS_tag) pairs
            Example: [('Tôi', 'PRON'), ('đi', 'VERB'), ('học', 'VERB')]
        """
        if not self.is_initialized:
            print("[-] UndertheSea POS tagger is not initialized.")
            return []

        try:
            # Use UndertheSea for POS tagging
            pos_tags_result = pos_tag(sentence)

            # Convert UndertheSea tags to Universal Dependencies format
            formatted_tags = []
            for word, tag in pos_tags_result:
                ud_tag = self._convert_to_ud_tag(tag)
                formatted_tags.append((word, ud_tag))

            return formatted_tags

        except Exception as e:
            print(f"[-] Error during POS tagging: {e}")
            return []

    def _convert_to_ud_tag(self, underthesea_tag: str) -> str:
        """
        Convert UndertheSea POS tags to Universal Dependencies tags.

        This mapping ensures compatibility with international NLP standards
        and provides consistent tag formats across different tools.

        Args:
            underthesea_tag: POS tag from UndertheSea

        Returns:
            Corresponding Universal Dependencies tag
        """
        # Mapping from UndertheSea tags to UD tags
        tag_mapping = {
            # Nouns
            "N": "NOUN",  # Common noun
            "Np": "PROPN",  # Proper noun
            "Ny": "NOUN",  # Noun abbreviation
            # Verbs
            "V": "VERB",  # Main verb
            "Vb": "VERB",  # Be verb
            "Vu": "AUX",  # Auxiliary verb
            # Adjectives
            "A": "ADJ",  # Adjective
            "Ab": "ADJ",  # Adjective base
            # Adverbs
            "R": "ADV",  # Adverb
            "Rb": "ADV",  # Adverb base
            # Pronouns
            "P": "PRON",  # Pronoun
            "Pp": "PRON",  # Personal pronoun
            # Prepositions/Adpositions
            "E": "ADP",  # Preposition
            "Eb": "ADP",  # Preposition base
            # Conjunctions
            "C": "CCONJ",  # Coordinating conjunction
            "Cc": "CCONJ",  # Coordinating conjunction
            "Cs": "SCONJ",  # Subordinating conjunction
            # Determiners
            "L": "DET",  # Determiner
            "Lb": "DET",  # Determiner base
            # Numbers
            "M": "NUM",  # Number
            "Mb": "NUM",  # Number base
            # Punctuation
            "CH": "PUNCT",  # Punctuation
            ".": "PUNCT",  # Period
            ",": "PUNCT",  # Comma
            "?": "PUNCT",  # Question mark
            "!": "PUNCT",  # Exclamation mark
            # Particles
            "T": "PART",  # Particle
            "Tb": "PART",  # Particle base
            # Interjections
            "I": "INTJ",  # Interjection
            # Others
            "X": "X",  # Other/Unknown
            "Fw": "X",  # Foreign word
        }

        return tag_mapping.get(underthesea_tag, "X")

    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance of the UndertheSea POS Tagger.

        Returns:
            UndertheSeaPOSTagger: The singleton instance
        """
        return cls()


# Demo and testing code
if __name__ == "__main__":
    # Example sentence for testing
    test_sentence = "Sinh viên trường Đại học Khoa học Tự Nhiên rất năng động."

    print("=== UndertheSea POS Tagger Demo ===")

    # Initialize tagger using singleton pattern
    demo_tagger = UndertheSeaPOSTagger.get_instance()

    # Perform POS tagging
    if demo_tagger.is_initialized:
        tagged_words = demo_tagger.tag_sentence(test_sentence)

        # Display results
        print(f"\\nInput: {test_sentence}")
        print("Output (UndertheSea -> UD tags):")
        for word, tag in tagged_words:
            print(f"  {word:15} -> {tag}")

        # Test singleton pattern
        print("\\n=== Singleton Pattern Test ===")
        tagger1 = UndertheSeaPOSTagger()
        tagger2 = UndertheSeaPOSTagger.get_instance()
        print(f"tagger1 is tagger2: {tagger1 is tagger2}")
        print(f"Same instance ID: {id(tagger1) == id(tagger2)}")
    else:
        print("[-] Failed to initialize UndertheSea tagger")