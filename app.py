import streamlit as st
import pandas as pd
from model import load_opportunities, compute_opportunity_embeddings, rank_opportunities

# ---------------------------------------------
# PAGE CONFIG
# ---------------------------------------------
st.set_page_config(
    page_title="OpporTutor – AI Opportunity Navigator",
    layout="wide"
)

# ---------------------------------------------
# SESSION STATE
# ---------------------------------------------
if "shortlist" not in st.session_state:
    st.session_state["shortlist"] = []

if "ranked" not in st.session_state:
    st.session_state["ranked"] = None

if "profile" not in st.session_state:
    st.session_state["profile"] = None

# ---------------------------------------------
# HEADER
# ---------------------------------------------
st.title("🎯 OpporTutor – AI Opportunity Navigator")
st.caption("AI-powered personalized opportunity discovery for students worldwide.")
st.write("")

# ---------------------------------------------
# SIDEBAR INPUT
# ---------------------------------------------
st.sidebar.header("Your Profile")

name = st.sidebar.text_input("Name")
country = st.sidebar.text_input("Country (e.g., India)")
branch = st.sidebar.text_input("Branch / Major")
year = st.sidebar.selectbox("Year of Study", [1, 2, 3, 4])
cgpa = st.sidebar.selectbox("CGPA Range", ["6–7", "7–8", "8–9", "9+"])

interests = st.sidebar.text_area("Your interests (ML, dev, research, etc.)")
goals = st.sidebar.text_area("Describe your goals / constraints")

location_pref = st.sidebar.selectbox(
    "Preferred Location", ["remote", "onsite", "hybrid", "no preference"]
)
duration_pref = st.sidebar.selectbox(
    "Preferred Duration", ["short-term", "long-term", "any"]
)

needs_stipend = st.sidebar.checkbox("I need only stipend-based opportunities")
is_female = st.sidebar.checkbox("Female")
low_income = st.sidebar.checkbox("Low-income / financial need")

opportunity_filter = st.sidebar.multiselect(
    "Filter by Opportunity Type",
    ["internship", "scholarship", "fellowship", "research", "program"],
    default=["internship", "scholarship", "fellowship", "research", "program"]
)

submit = st.sidebar.button("Find Opportunities")

# ---------------------------------------------
# PROCESS USER INPUT
# ---------------------------------------------
if submit:
    if not interests or not goals:
        st.warning("⚠️ Please enter both interests and goals.")
    else:
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

        with st.spinner("🔎 Matching opportunities..."):
            opps = load_opportunities()
            opps = compute_opportunity_embeddings(opps)
            ranked = rank_opportunities(profile, opps)

        st.session_state["ranked"] = ranked
        st.session_state["profile"] = profile

# ---------------------------------------------
# NO RESULTS YET
# ---------------------------------------------
if st.session_state["ranked"] is None:
    st.info("Fill your profile and click **Find Opportunities** to begin.")
    st.stop()

ranked = st.session_state["ranked"]
profile = st.session_state["profile"]

# ---------------------------------------------
# TABS
# ---------------------------------------------
tab1, tab2 = st.tabs(["📌 Recommendations", "⭐ My Shortlist"])

# ---------------------------------------------
# TAB 1 — RECOMMENDATIONS
# ---------------------------------------------
with tab1:
    st.subheader("🔥 Recommended Opportunities for You")

    # Search inside results
    search_term = st.text_input(
        "🔍 Search within results (AI, Google, women, research...)",
        key="search_input"
    )

    filtered = list(ranked)

    if search_term:
        q = search_term.lower()
        filtered = [
            (opp, score)
            for opp, score in filtered
            if q in opp["title"].lower()
            or q in opp["description"].lower()
            or q in " ".join(opp.get("tags", [])).lower()
        ]

    # Category filter
    selected_cat = st.multiselect(
        "🎛️ Filter by Category",
        ["internship", "scholarship", "fellowship", "research", "program"],
        default=profile["opportunity_filter"],
        key="category_filter"
    )
    filtered = [(opp, s) for opp, s in filtered if opp["type"] in selected_cat]

    if not filtered:
        st.info("No opportunities match your filters.")
    else:
        for opp, score in filtered[:20]:
            with st.container():

                # TITLE + ORG
                st.markdown(f"### {opp['title']}")
                st.caption(opp["organization"])

                # DESCRIPTION
                desc = opp["description"][:220]
                if len(opp["description"]) > 220:
                    desc += "..."
                st.write(desc)

                # MAIN DETAILS
                st.write(
                    f"📍 **Location:** {opp['location'].capitalize()}  \n"
                    f"🗓 **Deadline:** {opp['deadline']}  \n"
                    f"🎓 **Type:** {opp['type'].capitalize()}  \n"
                    f"⭐ **Match Score:** {score:.3f}"
                )

                # BADGES
                badges = []
                if "women" in opp.get("inclusive_flags", []):
                    badges.append("👩 Women-Only")
                if "low-income" in opp.get("inclusive_flags", []):
                    badges.append("💰 Low-Income Support")
                if opp.get("stipend"):
                    badges.append("💵 Stipend Available")

                if badges:
                    st.write("**Badges:** " + " | ".join(badges))

                # SCORE BAR
                # st.progress(int(max(0, min(1, score)) * 100))

                # ACTION BUTTONS
                col1, col2 = st.columns(2)

                with col1:
                    st.link_button("Apply Now 🔗", opp["link"])

                with col2:
                    save_key = f"save_{opp['id']}"
                    if st.button("⭐ Save", key=save_key):
                        ids = [o["id"] for o in st.session_state["shortlist"]]
                        if opp["id"] not in ids:
                            st.session_state["shortlist"].append(opp)
                            st.success("Saved!")
                        else:
                            st.info("Already saved.")

                st.write("---")

# ---------------------------------------------
# TAB 2 — SHORTLIST
# ---------------------------------------------
with tab2:
    st.header("⭐ Your Saved Opportunities")

    if not st.session_state["shortlist"]:
        st.info("No items saved yet.")
    else:
        # CSV Download
        if st.button("⬇️ Download Shortlist as CSV"):
            df = pd.DataFrame(st.session_state["shortlist"])
            df.to_csv("shortlist.csv", index=False)
            st.success("Downloaded shortlist.csv!")

        for opp in st.session_state["shortlist"]:
            st.markdown(f"### {opp['title']}")
            st.caption(opp["organization"])
            st.write(opp["description"])
            st.markdown(f"🔗 [Apply Here]({opp['link']})")
            st.write("---")
