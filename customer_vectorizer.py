import numpy as np


def word_to_vector(word: str, dim: int = 16) -> np.ndarray:
    """
    Converts a word into a deterministic vector using character-level encoding.
    Similar words will have similar vectors.

    Parameters:
    ----------
    word : str
        The word to convert to a vector.
    dim : int
        The dimensionality of the output vector.

    Returns:
    -------
    np.ndarray
        A deterministic vector representation of the word.
    """
    # Initialize the vector
    vector = np.zeros(dim)

    # Scale factor for normalization
    scale = 1 / max(1, len(word))  # Prevent division by zero

    # Distribute character contributions across the vector
    for i, char in enumerate(word):
        char_value = ord(char) * scale  # Normalize by word length
        vector[i % dim] += char_value  # Cycle through vector dimensions

    # Normalize the vector magnitude for consistency
    vector /= np.linalg.norm(vector) if np.linalg.norm(vector) > 0 else 1.0
    return vector


def generate_customer_vector(name: str, age: int, interests: list[str]) -> np.ndarray:
    """
    Generates a 32-dimensional vector for a customer.

    Parameters:
    ----------
    name : str
        The name of the customer.
    age : int
        The age of the customer.
    interests : list[str]
        A list of interests associated with the customer.

    Returns:
    -------
    np.ndarray
        A fixed 32-dimensional customer vector.
    """
    # Encode name: sum ASCII values of characters normalized by length, expanded to 8 dimensions
    name_vector = np.full(8, sum(ord(char) for char in name) / len(name))

    # Encode age: normalize age between 0 and 1, expanded to 8 dimensions
    age_vector = np.full(8, age / 100)

    # Encode interests: average the predefined embeddings
    interest_vectors = np.array([word_to_vector(interest, dim=16) for interest in interests])
    if len(interest_vectors) > 0:
        interest_vector = np.mean(interest_vectors, axis=0)
    else:
        interest_vector = np.zeros(16)

    # Combine all components into a single 32-dimensional vector
    customer_vector = np.concatenate([name_vector, age_vector, interest_vector])
    return customer_vector
