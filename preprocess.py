import nltk
import string
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download required resources
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)   # <-- ADD THIS
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))
synonyms = {
    "ai": "artificial intelligence",
    "ml": "machine learning",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "gpt": "chatgpt"
}


def preprocess_text(text):

    if text is None:
        return ""

    text = str(text).lower()

    text = re.sub(r"\s+", " ", text)

    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    for key, value in synonyms.items():
        text = text.replace(key, value)

    words = word_tokenize(text)

    cleaned = []

    for word in words:

        if word not in stop_words:

            cleaned.append(
                lemmatizer.lemmatize(word)
            )

    return " ".join(cleaned)