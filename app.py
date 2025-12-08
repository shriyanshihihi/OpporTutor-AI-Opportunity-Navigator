import streamlit as st
from model import load_opportunities, compute_opportunity_embeddings, rank_opportunities

st.set_page_config(page_title="OpporTutor", layout="wide")

st.title("🎯 OpporTutor – AI Opportunity Finder for Students")
st.write("Discover scholarships, internships, and programs tailored to your profile.")

# Sidebar – User Profile
st.sidebar.header("Your Profile")

name = st.sidebar.text_input("Name")
branch = st.sidebar.text_input("Branch / Major")
year = st.sidebar.selectbox("Year of Study", [1, 2, 3, 4])
interests = st.sidebar.text_area("Your interests (ML, dev, research, etc.)")
goals = st.sidebar.text_area("Describe your goals in 2–3 lines")

location_pref = st.sidebar.selectbox(
    "Preferred Location", ["remote", "onsite", "hybrid", "no preference"]
)

needs_stipend = st.sidebar.checkbox("I need only stipend-based opportunities")
is_female = st.sidebar.checkbox("Female")
low_income = st.sidebar.checkbox("Low-income / financial need")

if st.sidebar.button("Find Opportunities"):
    profile = {
        "name": name,
        "branch": branch,
        "year": year,
        "interests": interests,
        "goals": goals,
        "location_pref": location_pref,
        "needs_stipend": needs_stipend,
        "is_female": is_female,
        "low_income": low_income,
    }

    opps = load_opportunities()
    opps = compute_opportunity_embeddings(opps)
    ranked = rank_opportunities(profile, opps)

    st.subheader("🔥 Recommended for You")

    for opp, score in ranked[:10]:
        with st.container():
            st.markdown(f"### {opp['title']}  \n**{opp['organization']}**")
            st.write(opp['description'])
            st.write(f"**Score:** {score:.3f}")

            cols = st.columns(3)
            cols[0].markdown(f"🔗 [Apply Here]({opp['link']})")
            cols[1].write(f"📍 {opp['location']}")
            cols[2].write(f"🗓 Deadline: {opp['deadline']}")

            st.divider()
