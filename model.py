# model.py
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

class OpportunityMatcher:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

    def encode(self, text):
        return self.model.encode([text])[0]

    def load_opportunities(self, path="data/opportunities.json"):
        with open(path, "r") as f:
            return json.load(f)

    def match(self, user_profile, opportunities, top_k=5):
        user_vec = self.encode(user_profile)

        opp_texts = [opp["description"] for opp in opportunities]
        opp_vecs = self.model.encode(opp_texts)

        scores = cosine_similarity([user_vec], opp_vecs)[0]

        ranked = sorted(
            list(zip(opportunities, scores)),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:top_k]
