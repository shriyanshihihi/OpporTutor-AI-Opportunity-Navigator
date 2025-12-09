import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from utils.scoring import total_score

model = SentenceTransformer("all-MiniLM-L6-v2")


def load_opportunities():
    with open("data/opportunities.json", "r") as f:
        return json.load(f)


def embed_text(text):
    return model.encode([text])[0]


def compute_opportunity_embeddings(opportunities):
    for opp in opportunities:
        opp["embedding"] = embed_text(
            opp["title"] + " " + opp["description"] + " " + " ".join(opp["tags"])
        )
    return opportunities


def rank_opportunities(profile, opportunities):
    profile_text = f"{profile['interests']}{profile['branch']}"
    profile_vec = embed_text(profile_text)

    ranked = []

    for opp in opportunities:
        base_sim = cosine_similarity([profile_vec], [opp["embedding"]])[0][0]

        score_val = total_score(base_sim, opp, profile)

        ranked.append((opp, float(score_val)))

    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked
