import streamlit as st
import streamlit.components.v1 as components
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
st.caption("AI-powered personalised opportunity discovery for students worldwide.")
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

    if not interests or not goals:
        st.warning("⚠️ Please fill in both interests and goals to get accurate recommendations.")
        st.stop()

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

    opps = load_opportunities()
    opps = compute_opportunity_embeddings(opps)
    ranked = rank_opportunities(profile, opps)

    tab1, tab2 = st.tabs(["📌 Recommendations", "⭐ My Shortlist"])

    # ======================================================================
    # TAB 1 — RECOMMENDATIONS
    # ======================================================================
    with tab1:
        st.subheader("🔥 Recommended Opportunities for You")

        for opp, score in ranked[:20]:

            if opp["type"] not in profile["opportunity_filter"]:
                continue

            # ------------------------------------------
            # FULL HTML CARD (SAFE IN DARK MODE)
            # ------------------------------------------
            card_html = f"""
<div style="
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 18px;
    background-color: #ffffff;
    border: 1px solid #e6e6e6;
">
    <h3 style="margin: 0; color: #222;">{opp['title']}</h3>
    <p style="margin: 0; font-weight: bold; color: #444;">{opp['organization']}</p>
    <p style="color: #444;">{opp['description']}</p>

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
        ">🗓 {opp['deadline']}</span>

        <span style="
            background: #fff0e6;
            padding: 4px 10px;
            border-radius: 6px;
            margin-right: 6px;
            font-size: 12px;
        ">⭐ {score:.3f}</span>
    </div>
</div>
"""
            components.html(card_html, height=260, scrolling=False)

            # ------------------------------------------
            # BADGES
            # ------------------------------------------
            badge_html = "<div>"

            if "women" in opp["inclusive_flags"]:
                badge_html += """<span style="background:#ffe6f2;padding:4px 10px;border-radius:6px;
                margin-right:6px;font-size:12px;">👩 Women-Only</span>"""

            if "low-income" in opp["inclusive_flags"]:
                badge_html += """<span style="background:#fff4cc;padding:4px 10px;border-radius:6px;
                margin-right:6px;font-size:12px;">💰 Low-Income Support</span>"""

            if opp["stipend"]:
                badge_html += """<span style="background:#e6ffe6;padding:4px 10px;border-radius:6px;
                margin-right:6px;font-size:12px;">💵 Stipend</span>"""

            badge_html += "</div>"

            components.html(badge_html, height=50, scrolling=False)

            # ------------------------------------------
            # APPLY BUTTON
            # ------------------------------------------
            apply_btn = f"""
<div>
<a href="{opp['link']}" target="_blank">
<button style="
    padding: 8px 15px;
    border: none;
    border-radius: 8px;
    background: #4CAF50;
    color: white;
    cursor: pointer;
">Apply Now 🔗</button>
</a>
</div>
"""
            components.html(apply_btn, height=70)

            # ------------------------------------------
            # SAVE BUTTON
            # ------------------------------------------
            if st.button(f"⭐ Save {opp['id']}", key=f"save_{opp['id']}"):
                if opp not in st.session_state["shortlist"]:
                    st.session_state["shortlist"].append(opp)
                    st.success("Saved!")

            st.markdown("")

    # ======================================================================
    # TAB 2 — SHORTLIST
    # ======================================================================
    with tab2:
        st.header("⭐ Your Saved Opportunities")

        if not st.session_state["shortlist"]:
            st.info("No items saved yet.")
        else:
            for opp in st.session_state["shortlist"]:
                st.subheader(opp["title"])
                st.write(opp["description"])
                st.write(f"🔗 [Apply Here]({opp['link']})")
                st.markdown("---")
