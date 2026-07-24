import os
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocess import preprocess_text

# ==========================================
# LOAD KNOWLEDGE BASE
# ==========================================

knowledge_path = "knowledge_base"
knowledge = []

for filename in os.listdir(knowledge_path):

    if filename.endswith(".json"):

        print("Loading:", filename)

        try:

            with open(
                os.path.join(knowledge_path, filename),
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, list):
                    knowledge.extend(data)
                else:
                    knowledge.append(data)

        except Exception as e:

            print("❌ ERROR IN:", filename)
            print(e)

            # ==========================================
# FAST EXACT LOOKUP
# ==========================================

question_lookup = {
    item["question"].strip().lower(): item
    for item in knowledge
}
# ==========================================
# PREPARE DOCUMENTS
# ==========================================

documents = []

for item in knowledge:

    question = item.get("question", "")
    category = item.get("category", "")
    keywords = " ".join(item.get("keywords", []))

    text = f"{question} {keywords} {category}"

    documents.append(preprocess_text(text))

# ==========================================
# TF-IDF
# ==========================================
vectorizer = TfidfVectorizer(
    stop_words="english",
    lowercase=True,
    ngram_range=(1,2),
    max_features=4000
)
faq_vectors = vectorizer.fit_transform(documents)

# ==========================================
# CHATBOT
# ==========================================

def get_answer(user_question):

    lower = user_question.lower().strip()

    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    thanks = [
        "thanks",
        "thank you",
        "thx"
    ]

    bye_words = [
        "bye",
        "goodbye",
        "exit",
        "quit"
    ]

    if lower in greetings:
        return (
            "👋 Hello! Welcome to the AI Knowledge Assistant.\n\nAsk me anything about AI, Machine Learning, Python, NLP, Data Science and more.",
            0.99,
            "Greeting"
        )

    if lower in thanks:
        return (
            "😊 You're welcome! Happy to help.",
            0.99,
            "Greeting"
        )

    if lower in bye_words:
        return (
            "👋 Goodbye! Happy Learning!",
            0.99,
            "Greeting"
        )

       # ---------------------------------------
    # Check for Exact Question Match
    # ---------------------------------------
    for item in knowledge:
        if item["question"].strip().lower() == lower:
            response = f""" 
# 🤖 {item['question']}

<small style="color:#6B7280;font-size:15px;">
Artificial Intelligence Knowledge Base
</small>

---

"""

            response += f"""
###📖 Definition

{item['definition']}

"""

            if "history" in item:
                response += f"### 📜 History\n{item['history']}\n\n"

            if "types" in item:
                response += "###📚 Types\n"
                for t in item["types"]:
                    response += f"- {t}\n"

            if "applications" in item:
                response += "\n###🌍 Applications\n"
                for app in item["applications"]:
                 response += f"- {app}\n"

            if "advantages" in item:
                response += "\n## ✅ Advantages\n"
                for adv in item["advantages"]:
                    response += f"- {adv}\n"

            if "disadvantages" in item:
                response += "\n###❌ Disadvantages\n"
                for dis in item["disadvantages"]:
                    response += f"- {dis}\n"

            if "examples" in item:
                response += "\n###💼 Examples\n"
                for ex in item["examples"]:
                    response += f"- {ex}\n"

            if "future" in item:
                response += f"\n###📈 Future Scope\n{item['future']}\n"

            if "related_topics" in item:
                response += "\n###🔗 Related Topics\n"
                for topic in item["related_topics"]:
                    response += f"- {topic}\n"

            return response, 1.0, item["category"]

    # ---------------------------------------
    # TF-IDF Search
    # ---------------------------------------

    user_vector = vectorizer.transform(
    [preprocess_text(user_question)]
)

    similarity = cosine_similarity(user_vector, faq_vectors)

    best = similarity.argmax()

    confidence = float(similarity[0, best])

    if confidence < 0.30:
        return (
            "😔 Sorry, I couldn't find a suitable answer.\n\nTry asking the question in another way.",
            confidence,
            "Unknown"
        )

    item = knowledge[best]

    response = f"# 🤖 {item['question']}\n\n"

    # ===============================
    # Definition
    # ===============================
    if item.get("definition"):
        response += f"""
### 📖 Definition

{item['definition']}

---
"""

    # ===============================
    # History
    # ===============================
    if item.get("history"):
        response += f"""

### 📜 History

{item['history']}

---
"""

    # ===============================
    # Types
    # ===============================
    if item.get("types"):
        response += "\n## 📚 Types\n\n"
        for t in item["types"]:
            response += f"✅ {t}\n\n"
        response += "\n---\n"

    # ===============================
    # Applications
    # ===============================
    if item.get("applications"):
        response += "\n## 🌍 Applications\n\n"
        for app in item["applications"]:
            response += f"🌟 {app}\n\n"
        response += "\n---\n"

    # ===============================
    # Advantages
    # ===============================
    if item.get("advantages"):
        response += "\n##✅ Advantages\n\n"
        for adv in item["advantages"]:
            response += f"✔ {adv}\n\n"
        response += "\n---\n"

    # ===============================
    # Disadvantages
    # ===============================
    if item.get("disadvantages"):
        response += "\n##❌ Disadvantages\n\n"
        for dis in item["disadvantages"]:
            response += f"❌ {dis}\n\n"
        response += "\n---\n"

    # ===============================
    # Examples
    # ===============================
    if item.get("examples"):
        response += "\n##💻 Examples\n\n"
        for ex in item["examples"]:
            response += f"💡 {ex}\n\n"
        response += "\n---\n"

    # ===============================
    # Future Scope
    # ===============================
    if item.get("future"):
        response += f"""
### 🚀 Future Scope

{item['future']}

---
"""

    # ===============================
    # Related Topics
    # ===============================
    if item.get("related_topics"):
        response += "\n##🔗 Related Topics\n\n"
        for topic in item["related_topics"]:
            response += f"🔗 {topic}\n\n"

    return response, confidence, item.get("category", "General")
