import streamlit as st
from model import load_opportunities, compute_opportunity_embeddings, rank_opportunities

st.set_page_config(page_title="OpporTutor – AI Opportunity Navigator", layout="wide")

# --------------------------
# SESSION STATE INIT
# --------------------------
if "shortlist" not in st.session_state:
    st.session_state["shortlist"] = []


# --------------------------
# HEADER
# --------------------------
st.title("🎯 OpporTutor – AI Opportunity Navigator")
st.caption("AI-powered personalized opportunity discovery for students worldwide.")
st.markdown("---")


# --------------------------
# SIDEBAR: USER PROFILE INPUT
# --------------------------
st.sidebar.header("Your Profile")

name = st.sidebar.text_input("Name")
country = st.sidebar.text_input("Country (e.g., India)")
branch = st.sidebar.text_input("Branch / Major")
year = st.sidebar.selectbox("Year of Study", [1, 2, 3, 4])
cgpa = st.sidebar.selectbox("CGPA Range", ["6–7", "7–8", "8–9", "9+"])

interests = st.sidebar.text_area("Your interests (ML, dev, research, etc.)")
goals = st.sidebar.text_area("Describe your goals / constraints")

location_pref = st.sidebar.selectbox("Preferred Location", ["remote", "onsite", "hybrid", "no preference"])
duration_pref = st.sidebar.selectbox("Preferred Duration", ["short-term", "long-term", "any"])

needs_stipend = st.sidebar.checkbox("I need only stipend-based opportunities")
is_female = st.sidebar.checkbox("Female")
low_income = st.sidebar.checkbox("Low-income / financial need")

opportunity_filter = st.sidebar.multiselect(
    "Filter by Opportunity Type",
    ["internship", "scholarship", "fellowship", "research", "program"],
    default=["internship", "scholarship", "fellowship", "research", "program"]
)

submit = st.sidebar.button("Find Opportunities")


# --------------------------
# ON SUBMIT
# --------------------------
if submit:

    # Empty fields handling
    if not interests or not goals:
        st.warning("⚠️ Please fill in both interests and goals to get accurate recommendations.")
        st.stop()

    # Build profile dictionary
    profile = {
        "name": name,
        "country": country,
        "branch": branch,
        "year": year,
        "cgpa": cgpa,
        "interests": interests,
        "goals": goals,
        "location_pref": location_pref,
        "duration_pref": duration_pref,
        "needs_stipend": needs_stipend,
        "is_female": is_female,
        "low_income": low_income,
        "opportunity_filter": opportunity_filter,
    }

    # Load + rank opportunities
    opps = load_opportunities()
    opps = compute_opportunity_embeddings(opps)
    ranked = rank_opportunities(profile, opps)

    # ----------------------
    # TABS
    # ----------------------
    tab1, tab2 = st.tabs(["📌 Recommendations", "⭐ My Shortlist"])

    # ======================================================================
    # TAB 1 — RECOMMENDATIONS
    # ======================================================================
    with tab1:
        st.subheader("🔥 Recommended Opportunities for You")

        for opp, score in ranked[:15]:

            # FILTERING LOGIC
            if opp["type"] not in profile["opportunity_filter"]:
                continue

            # -------------------
            # OPPORTUNITY CARD UI
            # -------------------
            st.markdown(
                f"""
                <div style="
                    border-radius: 12px;
                    padding: 16px;
                    margin-bottom: 15px;
                    background-color: #f9f9f9;
                    border: 1px solid #e6e6e6;
                ">
                    <h3 style="margin: 0;">{opp['title']}</h3>
                    <p style="margin: 0;"><strong>{opp['organization']}</strong></p>
                    <p>{opp['description']}</p>

                    <div style="margin-bottom: 8px;">
                        <span style="
                            background: #e0ffe0;
                            padding: 4px 10px;
                            border-radius: 6px;
                            margin-right: 6px;
                            font-size: 12px;
                        ">📍 {opp['location'].capitalize()}</span>

                        <span style="
                            background: #e0f0ff;
                            padding: 4px 10px;
                            border-radius: 6px;
                            margin-right: 6px;
                            font-size: 12px;
                        ">🗓 Deadline: {opp['deadline']}</span>

                        <span style="
                            background: #fff0e6;
                            padding: 4px 10px;
                            border-radius: 6px;
                            margin-right: 6px;
                            font-size: 12px;
                        ">⭐ Score: {score:.3f}</span>
                    </div>
                """,
                unsafe_allow_html=True,
            )

            # --------------------------
            # BADGES
            # --------------------------
            badge_html = ""

            if "women" in opp["inclusive_flags"]:
                badge_html += """<span style="background:#ffe6f2;padding:4px 10px;border-radius:6px;
                                    margin-right:6px;font-size:12px;">👩 Women-Only</span>"""

            if "low-income" in opp["inclusive_flags"]:
                badge_html += """<span style="background:#fff4cc;padding:4px 10px;border-radius:6px;
                                    margin-right:6px;font-size:12px;">💰 Low-Income Support</span>"""

            if opp["stipend"]:
                badge_html += """<span style="background:#e6ffe6;padding:4px 10px;border-radius:6px;
                                    margin-right:6px;font-size:12px;">💵 Stipend Available</span>"""

            st.markdown(
                f"<div style='margin-top:-10px;margin-bottom:10px;'>{badge_html}</div>",
                unsafe_allow_html=True,
            )

            # --------------------------
            # APPLY BUTTON
            # --------------------------
            st.markdown(
                f"<a href='{opp['link']}' target='_blank'>"
                "<button style='padding:8px 15px;border:none;border-radius:8px;background:#4CAF50;color:white;'>"
                "Apply Now 🔗</button></a>",
                unsafe_allow_html=True,
            )

            # --------------------------
            # SAVE BUTTON
            # --------------------------
            if st.button(f"⭐ Save {opp['id']}", key=f"save_{opp['id']}"):
                if opp not in st.session_state["shortlist"]:
                    st.session_state["shortlist"].append(opp)
                    st.success("Saved to shortlist!")

            st.markdown("<br>", unsafe_allow_html=True)

    # ======================================================================
    # TAB 2 — SHORTLIST
    # ======================================================================
    with tab2:
        st.header("⭐ Your Saved Opportunities")

        if len(st.session_state["shortlist"]) == 0:
            st.info("No items saved yet. Save opportunities from the Recommendations tab.")
        else:
            for opp in st.session_state["shortlist"]:
                st.subheader(opp["title"])
                st.write(opp["description"])
                st.write(f"🔗 [Apply Here]({opp['link']})")
                st.markdown("---")
