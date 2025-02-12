from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
import spacy
import numpy as np
from rapidfuzz import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

# Initialize FastAPI
app = FastAPI()

# Load spaCy NLP model (small English model for efficiency)
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

# Administrator-defined skills list (simulating a database)
admin_skills = ["Python", "Relational Database", "Software Engineering", 
                "Data Science", "NLP", "Natural Language Processing"]

# Precompute TF-IDF vectors for admin skills
vectorizer = TfidfVectorizer().fit(admin_skills)
admin_skill_vectors = vectorizer.transform(admin_skills)

# Data storage for queries and match results (simulating database tables)
query_log: List[Dict] = []
match_results_log: List[Dict] = []

class SkillRequest(BaseModel):
    user_skill: str

def spacy_similarity(user_skill: str, skill_name: str) -> float:
    """Calculate semantic similarity using spaCy NLP model."""
    user_doc, skill_doc = nlp(user_skill.lower()), nlp(skill_name.lower())
    return round(user_doc.similarity(skill_doc), 3)

def fuzzy_similarity(user_skill: str, skill_name: str) -> float:
    """Calculate fuzzy matching similarity (Levenshtein distance)."""
    return round(fuzz.partial_ratio(user_skill.lower(), skill_name.lower()) / 100, 3)

def tfidf_cosine_similarity(user_skill: str) -> Dict[str, float]:
    """Calculate cosine similarity between user skill and admin skills using TF-IDF."""
    user_vector = vectorizer.transform([user_skill])
    cos_sim = cosine_similarity(user_vector, admin_skill_vectors).flatten()
    return {admin_skills[i]: round(score, 3) for i, score in enumerate(cos_sim) if score > 0.5}

@app.post("/match-skill/")
def match_skill(skill_request: SkillRequest):
    """Matches a user-submitted skill against the administrator skill list using multiple techniques."""
    user_skill = skill_request.user_skill
    timestamp = datetime.now().isoformat()

    # Log user query
    query_entry = {
        "query_id": len(query_log) + 1,
        "user_skill": user_skill,
        "submitted_at": timestamp
    }
    query_log.append(query_entry)

    # Compute matches using multiple methods
    match_results = []
    for skill in admin_skills:
        spacy_score, fuzzy_score = spacy_similarity(user_skill, skill), fuzzy_similarity(user_skill, skill)
        combined_score = (spacy_score * 0.6 + fuzzy_score * 0.4)  # Weighted scoring system

        if combined_score > 0.5:  # Keep only relevant matches
            match_entry = {
                "match_id": len(match_results_log) + 1,
                "query_id": query_entry["query_id"],
                "skill": skill,
                "matching_method": "NLP + Fuzzy",
                "match_score": round(combined_score, 3),
                "created_at": timestamp
            }
            match_results.append(match_entry)
            match_results_log.append(match_entry)

    # Include TF-IDF Cosine Similarity results
    for skill, score in tfidf_cosine_similarity(user_skill).items():
        match_entry = {
            "match_id": len(match_results_log) + 1,
            "query_id": query_entry["query_id"],
            "skill": skill,
            "matching_method": "TF-IDF",
            "match_score": score,
            "created_at": timestamp
        }
        match_results.append(match_entry)
        match_results_log.append(match_entry)

    # Sort results by highest match score
    sorted_matches = sorted(match_results, key=lambda x: x["match_score"], reverse=True)

    return {
        "submitted_skill": user_skill,
        "matches": sorted_matches,
        "query_log": query_log,
        "match_results_log": match_results_log
    }

@app.get("/")
def home():
    """Root endpoint to verify API is running."""
    return {"message": "Welcome to Teamo AI - Optimized Skill Matching API"}
