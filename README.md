# OpporTutor – AI Opportunity Navigator for Students 🎯

**OpporTutor** is a web-app that helps students discover scholarships, internships, fellowships and programs tailored to their profile (branch, year, interests, financial need, inclusive-status, location preference).  
It uses AI-based embedding + similarity matching 👇 to rank opportunities — making it easier for students (especially from underrepresented / non-traditional backgrounds) to find relevant opportunities without endless manual search.

---

## 🧠 Motivation & Problem

- Many students — especially from small towns or tier-2/3 colleges — miss great opportunities simply because they don’t know where to look or the information is scattered.  
- OpporTutor aims to **democratize access to opportunities** by providing a simple, inclusive, and personalized navigator.  
- By combining natural-language profile description with AI-matching, OpporTutor turns a long manual search into a 1-click “recommendations feed”.

---

## 🚀 Features

- Submit your profile: branch, year, interests/goals, stipend-need, gender / low-income / inclusive flags, location preference (remote/onsite/hybrid)  
- AI-based matching: finds and ranks relevant opportunities using sentence-embeddings + custom scoring  
- Results show: opportunity title, org, short description, location, deadline, link to apply  
- Supports: internships, fellowships, scholarships, research programs, training schools  
- Inclusive-badges: shows when an opportunity targets women, low-income students, or underrepresented groups (social-good focus)  
- Easy to run locally (Streamlit) — no heavy infra needed  

---

## 📦 Tech Stack

- **Backend / ML**: Python, `sentence-transformers` (all-MiniLM-L6-v2), `scikit-learn` / NumPy for similarity & scoring  
- **Frontend / UI**: Streamlit (single-page, forms + results feed)  
- **Data**: JSON file (`data/opportunities.json`) containing opportunity metadata + description + eligibility + tags  
- **Repository**: Clean, modular — `app.py`, `model.py`, `data/`, `requirements.txt`  

---

## 🛠️ Installation & Running Locally (Quick Start)

```bash
# clone the repo
git clone https://github.com/your-username/OpporTutor-AI-Opportunity-Navigator.git
cd OpporTutor-AI-Opportunity-Navigator

# install dependencies
pip install -r requirements.txt

# run the app
streamlit run app.py
