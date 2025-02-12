Teamo AI - Skill Matching System
📌 Overview

Teamo AI is a skill-matching service that intelligently compares user-submitted skills against an administrator-curated skill database. By leveraging Natural Language Processing (NLP), fuzzy matching, and TF-IDF similarity, Teamo AI provides accurate, typo-tolerant, and semantically relevant skill recommendations.

🛠 Problem Statement
Many users search for skills using different naming conventions, abbreviations, or misspellings. For example:

✅ ML instead of Machine Learning
✅ Phyton instead of Python (typo)
✅ Someone searching for Data Science may also be interested in AI or Big Data

The challenge is to accurately map user input to the closest administrator-defined skills while handling spelling mistakes, variations, and synonyms.


🚀 Solution Approach
Teamo AI enhances skill-matching accuracy by combining three powerful matching techniques:

1️⃣ Multiple Matching Algorithms for Higher Accuracy
🔹 NLP Semantic Similarity (spaCy) → Understands meaning-based relationships between words.
🔹 Fuzzy Matching (Levenshtein Distance) → Handles typos, abbreviations, and partial matches.
🔹 TF-IDF Cosine Similarity → Matches based on word frequency and importance.

Each method contributes to a weighted scoring system to ensure precise and robust skill-matching.

2️⃣ Optimized Query Processing
    ✅ Precomputed NLP embeddings → Faster similarity calculations.
    ✅ NumPy-optimized cosine similarity → Avoids slow Python loops.
    ✅ Weighted aggregation of multiple methods → Balances accuracy and efficiency.

3️⃣ FastAPI-Based REST API
The system is designed as a FastAPI web service, making it scalable, lightweight, and easy to integrate into applications.


📝 How It Works
🔹 Skill Matching Workflow
The user submits a skill name via the API.
The system processes the input using multiple similarity algorithms.
Each method computes a match score based on relevance.
The system aggregates results and returns the best-matching skills.

Example Request & Response

📥 API Input (JSON)
{
    "user_skill": "machine learning"
}

📤 API Output (JSON)
{
    "submitted_skill": "machine learning",
    "matches": [
        {"skill": "data science", "match_score": 0.85},
        {"skill": "NLP", "match_score": 0.78},
        {"skill": "Software engineering", "match_score": 0.65}
    ]
}

📌 Installation & Setup

1️⃣ Install Dependencies
pip install fastapi uvicorn spacy numpy rapidfuzz scikit-learn
python -m spacy download en_core_web_sm

2️⃣ Run the API
uvicorn main:app --reload

3️⃣ Test the API (Using Postman or cURL)
curl -X 'POST' \
  'http://127.0.0.1:8000/match-skill/' \
  -H 'Content-Type: application/json' \
  -d '{"user_skill": "machine learning"}'

🎯 Key Features & Benefits

✅ Supports NLP-based intelligent matching (Handles synonyms & semantics).
✅ Fuzzy matching for typos & abbreviations (e.g., "Phyton" → "Python").
✅ TF-IDF for keyword relevance (Finds similar skills based on word importance).
✅ FastAPI-based RESTful API (Easy integration with any application).
✅ Efficient computation using NumPy & precomputed vectors.

📌 Contributors

[Jovan Bogoeski] - Developer & API Architect


