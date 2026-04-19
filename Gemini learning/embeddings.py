import numpy as np
from numpy.linalg import norm

# Mock 3D embeddings
vector_king = np.array([0.9, 0.1, 0.8])
vector_queen = np.array([0.8, 0.2, 0.9])
vector_apple = np.array([-0.5, 0.8, -0.2])

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors."""
    return np.dot(vec1, vec2) / (norm(vec1) * norm(vec2))

# Calculate similarities
similarity_king_queen = cosine_similarity(vector_king, vector_queen)
similarity_king_apple = cosine_similarity(vector_king, vector_apple)

print(f"Cosine similarity between King and Queen: {similarity_king_queen:.4f}")
print(f"Cosine similarity between King and Apple: {similarity_king_apple:.4f}")