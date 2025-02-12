from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import spacy
import numpy as np
from rapidfuzz import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize FastAPI
app = FastAPI()

# Load optimized spaCy model (disabling unnecessary components for efficiency)
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

# Administrator-defined skill list (simulating a database)
admin_skills = [
    "Python", "Relational Database", "Software Engineering",
    "Data Science", "NLP", "Natural Language Processing"
]

# Precompute spaCy embeddings for admin skills (Optimized for faster NLP similarity)
admin_skill_vectors: Dict[str, np.ndarray] = {
    skill: nlp(skill.lower()).vector for skill in admin_skills
}

# Precompute TF-IDF vectors for admin skills (Optimized for keyword similarity)
vectorizer = TfidfVectorizer().fit(admin_skills)
admin_skill_tfidf_vectors = vectorizer.transform(admin_skills)

# Define API request model
class SkillRequest(BaseModel):
    user_skill: str

# Function to compute spaCy similarity using NumPy for performance
def spacy_similarity(user_skill: str) -> Dict[str, float]:
    """Compute similarity scores using precomputed NLP embeddings."""
    user_vector = nlp(user_skill.lower()).vector
    return {
        skill: float(round(np.dot(user_vector, skill_vector) /
                     (np.linalg.norm(user_vector) * np.linalg.norm(skill_vector)), 3))
        for skill, skill_vector in admin_skill_vectors.items()
    }

# Function to compute fuzzy string similarity
def fuzzy_similarity(user_skill: str) -> Dict[str, float]:
    """Compute similarity using fuzzy string matching (Levenshtein distance)."""
    return {skill: float(round(fuzz.partial_ratio(user_skill.lower(), skill.lower()) / 100, 3))
            for skill in admin_skills}

# Function to compute TF-IDF cosine similarity
def tfidf_cosine_similarity(user_skill: str) -> Dict[str, float]:
    """Compute TF-IDF cosine similarity between user skill and admin skills."""
    user_vector = vectorizer.transform([user_skill])  # Convert user input to TF-IDF vector
    cos_sim = cosine_similarity(user_vector, admin_skill_tfidf_vectors).flatten()
    return {admin_skills[i]: float(round(score, 3)) for i, score in enumerate(cos_sim) if score > 0.5}

@app.post("/match-skill/")
def match_skill(skill_request: SkillRequest):
    """Matches a user-submitted skill against the administrator-defined skill list using multiple algorithms."""
    user_skill = skill_request.user_skill

    # Compute similarity scores using different methods
    spacy_scores = spacy_similarity(user_skill)
    fuzzy_scores = fuzzy_similarity(user_skill)
    tfidf_scores = tfidf_cosine_similarity(user_skill)

    # Aggregate results using a weighted scoring system
    match_results = {}
    for skill in admin_skills:
        combined_score = (
            float(spacy_scores.get(skill, 0)) * 0.4 +  # 40% weight for NLP-based similarity
            float(fuzzy_scores.get(skill, 0)) * 0.3 +  # 30% weight for fuzzy string matching
            float(tfidf_scores.get(skill, 0)) * 0.3    # 30% weight for TF-IDF cosine similarity
        )
        if combined_score > 0.5:  # Keep only relevant matches
            match_results[skill] = round(float(combined_score), 3)  # Convert to standard Python float

    # Sort matches by highest score
    sorted_matches = sorted(match_results.items(), key=lambda x: x[1], reverse=True)

    return {"submitted_skill": user_skill, "matches": sorted_matches}

@app.get("/")
def home():
    """Root endpoint to verify API is running."""
    return {"message": "Welcome to Teamo AI - Optimized Skill Matching API"}
