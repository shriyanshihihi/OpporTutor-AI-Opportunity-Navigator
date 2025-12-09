# 🎯 OpporTutor – AI-Powered Opportunity Navigator  
### Personalized internship, scholarship, fellowship & research recommendations for students worldwide.

OpporTutor is an AI-driven platform that helps students discover **relevant, high-quality opportunities** based on their academic background, interests, goals, location preferences, and diversity attributes.  

Built for **BatchHacks**, this project focuses on **accessibility, fairness, and real-world impact** by reducing information inequality among students.

---

## 🚀 Problem Statement  
Students—especially from non–Tier 1 colleges—miss out on life-changing opportunities because:

- Information is scattered across hundreds of websites  
- Most platforms show generic results, not personalized ones  
- Diversity-based opportunities (women, low-income, PWD) often go unnoticed  
- Beginners don’t know which opportunities match their profile

🎓 **OpporTutor solves this using AI-powered recommendation matching.**

---

## 💡 Project Features  
### 🔍 1. **AI Matching Engine**
Uses **sentence-transformer embeddings** + custom scoring rules to match student profiles with opportunity descriptions:

- Cosine similarity on embeddings  
- Bonus scoring for:  
  ✔ Academic year match  
  ✔ Location preference  
  ✔ Stipend requirement  
  ✔ Women-in-tech / low-income / PWD inclusivity  
  ✔ Opportunity type filters  

### 🧭 2. **Rich Dataset (40 curated entries)**
Includes diverse opportunities:
- Internships  
- Fellowships  
- Scholarships  
- Research programs  
- Women-only, low-income, PWD inclusive options  
- India + Global mix  

### 🖥️ 3. **Interactive Streamlit App**
- Profile form (branch, year, interests, goals, filters, stipend, gender, income status)  
- Top-N personalized recommendations  
- Clean, card-style UI with badges (Women-only, Stipend, Low-income, etc.)  
- Shortlist & save opportunities (⭐ Save Feature)  
- Apply buttons for each opportunity  

### ⭐ 4. **Social Good Focus**
OpporTutor highlights opportunities for:
- Women in STEM  
- Low-income students  
- First-generation learners  
- Students with disabilities  

Helping reduce inequality in access to global programs.

---

## 🧠 Tech Stack  
- **Python 3.10+**  
- **Streamlit** – UI  
- **Sentence Transformers (MiniLM-L6-v2)** – Embedding model  
- **Scikit-learn** – Similarity computation  
- **Custom Scoring Logic** – Fairness-aware ranking  
- **JSON Dataset** – 40 real & simulated opportunities  

---

## 📁 Project Structure
opportutor/
│── app.py # Streamlit frontend
│── model.py # Embedding + ranking logic
│── utils/
│ └── scoring.py # Custom scoring rules
│── data/
│ └── opportunities.json # 40 curated opportunities
│── requirements.txt
│── README.md


---

## 🧩 How It Works (Under the Hood)

### 1️⃣ Embedding Generation  
We embed:
- Opportunity descriptions  
- Tags  
- Student’s interests + goals  

using `sentence-transformers/all-MiniLM-L6-v2`.

### 2️⃣ Similarity & Scoring  
Final score =  
**Semantic Similarity**  
+ **Year Fit**  
+ **Stipend Fit**  
+ **Location Fit**  
+ **Diversity Bonus**  

This produces **highly relevant, student-specific recommendations.**

### 3️⃣ Ranking  
Top opportunities are sorted and displayed with:
- Score  
- Category  
- Deadline  
- Apply CTA  
- Badges (Women-only, Stipend, Low-income, etc.)

---

## 🛠️ Installation & Running Locally  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/YOUR-USERNAME/OpporTutor-AI-Opportunity-Navigator.git
cd OpporTutor-AI-Opportunity-Navigator

pip install -r requirements.txt

streamlit run app.py
