# Recipe Recommendation System

A smart recipe recommendation web application that suggests recipes based on user-selected ingredients, cuisine preferences, dietary filters, and cooking difficulty.

The project uses a custom rule-based recommendation engine with weighted ingredient scoring to generate relevant recipe suggestions.

---

## Features

- Ingredient-based recipe recommendations
- Cuisine filtering
- Veg / Non-Veg filtering
- Difficulty level filtering
- Recipe category filtering
- Interactive Streamlit frontend
- FastAPI backend integration
- Recipe image support
- Responsive cookbook-inspired UI

---

## Tech Stack

### Frontend
- Streamlit

### Backend
- FastAPI
- Uvicorn
- Pydantic

### Data Processing
- Pandas
- Custom recommendation engine

---

##  Recommendation Logic

The recommendation engine works using:

- Ingredient similarity matching
- Weighted ingredient importance scoring
- Recipe ranking based on score and preparation time

Important ingredients are assigned higher weights to improve recommendation quality.

---

##  Project Structure

```bash
recipe_generator/
│
├── backend/
│   ├── api.py
│   ├── recommender1.py
│   ├── data/
│
├── frontend/
│   ├── app.py
│
├── Images/
│
├── requirements.txt
├── README.md
├── .gitignore
```

---

##  Installation

### 1. Clone Repository

```bash
git clone https://github.com/Navina-Pandhare/Recipe-Generator.git
cd Recipe-Generator
cd recipe_generator_old
cd recipe_generator
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run Backend Server

```bash
uvicorn backend.api:app --reload
```

Backend will run at:

```bash
http://127.0.0.1:8000
```

---

### 4. Run Frontend

```bash
streamlit run frontend/app.py
```

---


