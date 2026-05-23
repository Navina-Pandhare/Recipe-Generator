import streamlit as st
import pandas as pd
import requests

# -----------------------------
# CONFIG
# -----------------------------
API_URL = "http://127.0.0.1:8000/recommend"

st.set_page_config(
    page_title="AI Recipe Recommender",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# GLOBAL CSS (THIS IS THE MAGIC)
# -----------------------------
st.markdown("""
<style>

/* App background */
.stApp {
    background-color: #eadaf7;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #d888f7, #5A54E8);
    color: white;
}

/* Sidebar text */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div {
    color: white !important;
}

/* Main header */
.hero {
    background: linear-gradient(90deg, #6C63FF, #8E85FF);
    padding: 40px;
    border-radius: 18px;
    text-align: center;
    color: white;
    margin-bottom: 40px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.15);
}

/* Section titles */
.section-title {
    font-size: 26px;
    font-weight: 700;
    color: #2B2B2B;
    margin-bottom: 10px;
}

/* Card */
.card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

/* Button */
.stButton > button {
    background: linear-gradient(90deg, #FFB703, #FFA000);
    color: black;
    border-radius: 12px;
    height: 55px;
    font-size: 18px;
    font-weight: 700;
    border: none;
    box-shadow: 0px 6px 18px rgba(255,183,3,0.4);
}

.stButton > button:hover {
    transform: scale(1.03);
}

/* Inputs */
input, textarea, select {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    """
    <div style="text-align:center; padding: 20px 0;">
        <h1>🍽️ AI Recipe Recommendation System</h1>
        <p style="font-size:16px; color:gray;">
            Select ingredients and filters to get smart recipe recommendations
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# LOAD METADATA
# -----------------------------
@st.cache_data
def load_metadata():
    df = pd.read_csv("../backend/data/recipes_MASTER_FINAL.csv")

    ingredients = sorted(
        set(
            ing.strip().lower()
            for row in df["ingredients"].dropna()
            for ing in row.split(",")
        )
    )

    return {
        "ingredients": ingredients,
        "categories": sorted(df["category"].dropna().str.lower().unique()),
        "cuisines": sorted(df["cuisine"].dropna().str.lower().unique()),
        "difficulty": sorted(df["difficulty"].dropna().str.lower().unique()),
        "veg": sorted(df["veg_nonveg"].dropna().str.lower().unique())
    }

meta = load_metadata()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.markdown("## 🔍 Filters")

veg = st.sidebar.selectbox("Veg / Non-Veg", [""] + meta["veg"])
difficulty = st.sidebar.selectbox("Difficulty", [""] + meta["difficulty"])
category = st.sidebar.selectbox("Category", [""] + meta["categories"])
cuisine = st.sidebar.selectbox("Cuisine", [""] + meta["cuisines"])
top_n = st.sidebar.slider("Number of Recipes", 1, 10, 5)

# -----------------------------
# INGREDIENT INPUT
# -----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🥕 Choose Ingredients</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    selected_ingredients = st.multiselect(
        "Select ingredients",
        meta["ingredients"]
    )

with col2:
    manual_input = st.text_input(
        "Add custom ingredients (comma separated)"
    )

st.markdown('</div>', unsafe_allow_html=True)

manual_ingredients = [
    i.strip().lower()
    for i in manual_input.split(",")
    if i.strip()
]

final_ingredients = list(set(selected_ingredients + manual_ingredients))

st.markdown("---")

# -----------------------------
# API CALL
# -----------------------------
st.markdown("<br>", unsafe_allow_html=True)
center = st.columns([3, 1, 3])[1]

with center:
    recommend_btn = st.button("Recommend Recipes", use_container_width=True, key="recommend_btn")

if recommend_btn:
    if not final_ingredients:
        st.warning("Please select at least one ingredient.")
    else:
        payload = {
            "ingredients": final_ingredients,
            "veg": veg or None,
            "difficulty": difficulty or None,
            "category": category or None,
            "cuisine": cuisine or None,
            "top_n": top_n
        }

        with st.spinner("Finding the best recipes for you..."):
            res = requests.post(API_URL, json=payload)

        if res.status_code != 200:
            st.error("Backend API error. Check server logs.")
        else:
            recipes = res.json()["recipes"]

            st.markdown("## 🍲 Recommended Recipes")

            if not recipes:
                st.info("No recipes match your selected filters.")
            else:
                for r in recipes:
                    st.markdown(
                        '<div class="card">',
                        unsafe_allow_html=True
                    )

                    cols = st.columns([1, 2])

                    with cols[0]:
                        if r.get("image_url"):
                            st.image(
                                r["image_url"],
                                use_container_width=True
                            )

                    with cols[1]:
                        st.markdown(f"### {r['recipe_name']}")
                        st.write(f"**Cuisine:** {r['cuisine'].title()}")
                        st.write(f"**Difficulty:** {r['difficulty'].title()}")
                        st.write(f"**Prep Time:** {r['prep_time']} mins")

                        with st.expander("Ingredients"):
                            st.write(r["ingredients"])

                        with st.expander("Instructions"):
                            st.write(r["instructions"])

                    st.markdown("</div>", unsafe_allow_html=True)
