import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

class LoopDetector:
    def __init__(self, threshold=0.95):
        self.history = []
        self.threshold = threshold
        self.vectorizer = TfidfVectorizer()

    def analyze(self, text: str) -> bool:
        """
        Returns True if the new text is semantically identical 
        to recent history.
        """
        if not text or len(text.strip()) < 5:
            return False
            
        self.history.append(text)
        if len(self.history) > 10:
            self.history.pop(0)

        if len(self.history) < 2:
            return False

        try:
            # Convert text to "meaning vectors"
            vectors = self.vectorizer.fit_transform(self.history)
            similarity_matrix = (vectors * vectors.T).toarray()
            
            # Compare latest (-1) vs previous (-2)
            similarity = similarity_matrix[-1, -2]
            print(f"   📊 [LoopDetector] Similarity: {similarity:.4f}")
            
            return similarity >= self.threshold
        except Exception:
            return False