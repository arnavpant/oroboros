import math

def cosine_similarity(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x*x for x in a))
    norm_b = math.sqrt(sum(y*y for y in b))
    return dot / (norm_a * norm_b)

def fake_embedding(text: str, dim=64):
    """
    Deterministic fake embedding.
    Later this will be replaced with Vertex embeddings.
    """
    vec = [0.0] * dim
    for i, ch in enumerate(text.encode("utf-8")):
        vec[i % dim] += ch
    return vec

class SemanticLoopDetector:
    def __init__(self, threshold=0.92, window=5):
        self.threshold = threshold
        self.window = window
        self.embeddings = []

    def check(self, text: str) -> bool:
        emb = fake_embedding(text)
        for prev in self.embeddings:
            sim = cosine_similarity(emb, prev)
            if sim >= self.threshold:
                return True
        self.embeddings.append(emb)
        if len(self.embeddings) > self.window:
            self.embeddings.pop(0)
        return False
