import json
import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from utils.scoring import total_score


# Cache model for speed
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()


def load_opportunities():
    with open("data/opportunities.json", "r") as f:
        return json.load(f)


def embed_text(text):
    return model.encode([text])[0]


@st.cache_data
def compute_opportunity_embeddings(opportunities):

    for opp in opportunities:

        tags = opp.get("tags", [])
        inclusive = opp.get("inclusive_flags", [])

        text = (
            f"{opp['title']} {opp['description']} "
            f"{' '.join(tags)} {opp['type']} {opp['location']} "
            f"{'stipend' if opp['stipend'] else 'no stipend'} "
            f"{' '.join(inclusive)}"
        )

        opp["embedding"] = embed_text(text)

    return opportunities


def rank_opportunities(profile, opportunities):

    profile_text = (
        f"{profile['interests']} {profile['branch']} {profile['goals']} "
        f"{profile['location_pref']} "
        f"{'female' if profile['is_female'] else ''} "
        f"{'low-income' if profile['low_income'] else ''}"
    )

    profile_vec = embed_text(profile_text)

    ranked = []

    for opp in opportunities:

        base_sim = cosine_similarity([profile_vec], [opp["embedding"]])[0][0]

        final_score, explanation = total_score(
            base_sim, opp, profile, return_details=True
        )

        opp["explain"] = explanation

        ranked.append((opp, float(final_score)))

    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked
