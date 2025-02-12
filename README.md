Teamo AI - Skill Matching System'

📌 Overview

Teamo AI is a FastAPI-based service designed to help users find relevant skills by comparing user-submitted skill names against an administrator-curated skill list. The system applies multiple matching algorithms (NLP, Fuzzy Matching, TF-IDF) to determine similarity scores and returns the best-matching skills to the user.

Why use Teamo AI?

Intelligent Matching: Uses Natural Language Processing (NLP) to understand skill similarities.

Typo-Tolerance: Handles misspellings, abbreviations, and synonyms.

Structured Logging: Stores queries, match results, and matching methods (simulating a database structure).


🛠 Problem Statement
Many users search for skills using different naming conventions, abbreviations, or misspellings. For example:

✅ ML instead of Machine Learning
✅ Phyton instead of Python (typo)
✅ Someone searching for Data Science may also be interested in AI or Big Data

The challenge is to accurately map user input to the closest administrator-defined skills while handling spelling mistakes, variations, and synonyms.


🚀 Solution Approach

Teamo AI uses three different matching algorithms to ensure accurate and typo-resistant skill matching:

🔹 1. NLP Semantic Similarity (spaCy)

Understands meaning-based relationships between words.

Example: AI and Machine Learning might be considered similar.

🔹 2. Fuzzy Matching (Levenshtein Distance)

Handles typos, partial matches, and misspellings.

Example: Phyton can match Python.

🔹 3. TF-IDF Cosine Similarity

Matches based on word frequency and importance.

Example: Data Scientist could match Data Science.

✅ Each method has a weight and threshold to balance accuracy.


📌 Features

✅ Logs user queries (mimicking a Query table in a database)

✅ Stores match results (like a MatchResult table)

✅ Implements multiple matching methods (configurable like a MatchingMethodConfig table)

✅ FastAPI-based RESTful API (easy to integrate into applications)

✅ Efficient computation using NumPy & precomputed vectors



📝 How It Works

🔹 Workflow Example

1️⃣ A user submits a skill name via the API.
2️⃣ The system processes the input using NLP, Fuzzy Matching, and TF-IDF.
3️⃣ Each method calculates similarity scores, and the system aggregates results.
4️⃣ The best-matching skills are returned to the user.5️⃣ The system logs the query & match results for tracking.


🔍 API Endpoints

✅ Get Available Matching Methods

GET /matching-methods/
Returns all matching methods and their thresholds.

✅ Submit a Skill for Matching
POST /match-skill/

Example Input:
{
    "user_skill": "machine learning"
}

{
    "submitted_skill": "machine learning",
    "matches": [
        {
            "match_id": 1,
            "query_id": 1,
            "skill": "data science",
            "matching_method": "NLP Semantic Similarity",
            "match_score": 0.75,
            "created_at": "2025-02-12T14:00:00"
        },
        {
            "match_id": 2,
            "query_id": 1,
            "skill": "Software Engineering",
            "matching_method": "Fuzzy Matching",
            "match_score": 0.68,
            "created_at": "2025-02-12T14:00:00"
        }
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

📌 Contributors

[Jovan Bogoeski] - Developer & API Architect


