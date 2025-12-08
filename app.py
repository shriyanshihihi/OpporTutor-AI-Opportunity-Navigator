# app.py
import streamlit as st
import json
from model import OpportunityMatcher

st.set_page_config(page_title="AI Opportunity Matcher", layout="wide")

matcher = OpportunityMatcher()

st.title("✨ AI-Powered Opportunity Matcher")
st.write("Enter your skills/interests and get the best internship or project matches!")

# --- User input ---
user_profile = st.text_area("Describe your profile (skills, interests, goals):", height=150)

# --- Load opportunities ---
opportunities = matcher.load_opportunities()

if st.button("Find Matches"):
    if not user_profile.strip():
        st.warning("Please write about your skills or interests.")
    elif len(opportunities) == 0:
        st.error("No opportunities found. Add data to data/opportunities.json")
    else:
        results = matcher.match(user_profile, opportunities, top_k=5)

        st.subheader("🔍 Top Matches")
        for opp, score in results:
            st.markdown(f"### {opp['title']}")
            st.markdown(f"**Score:** {round(float(score), 3)}")
            st.markdown(opp["description"])
            st.markdown("---")

# --- Add New Opportunity ---
st.sidebar.header("➕ Add New Opportunity")

title = st.sidebar.text_input("Title")
description = st.sidebar.text_area("Description")

if st.sidebar.button("Add"):
    if not title or not description:
        st.sidebar.warning("Fill both title and description.")
    else:
        new_opp = {"title": title, "description": description}

        with open("data/opportunities.json", "r+") as f:
            data = json.load(f)
            data.append(new_opp)
            f.seek(0)
            json.dump(data, f, indent=4)

        st.sidebar.success("Added successfully!")
