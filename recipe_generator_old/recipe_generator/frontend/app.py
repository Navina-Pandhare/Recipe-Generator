import streamlit as st
import pandas as pd
import requests
import os

# -----------------------------
# CONFIG
# -----------------------------
API_URL = "http://127.0.0.1:8000/recommend"

st.set_page_config(
    page_title="The Recipe Book - AI Powered",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for likes
if 'liked_recipes' not in st.session_state:
    st.session_state.liked_recipes = set()

# -----------------------------
# COOKBOOK-INSPIRED CSS
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Crimson+Text:wght@400;600;700&family=Montserrat:wght@300;400;600;700&display=swap');

/* App background - vintage paper texture */
.stApp {
    background: linear-gradient(to bottom, #f9f6f0 0%, #efe8dd 100%);
    font-family: 'Crimson Text', serif;
}

/* Sidebar - Cookbook spine */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #8B4513 0%, #654321 50%, #3e2723 100%);
    border-right: 3px solid #d4af37;
    box-shadow: inset -5px 0 15px rgba(0,0,0,0.3);
}

section[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(255,255,255,0.03) 2px,
        rgba(255,255,255,0.03) 4px
    );
    pointer-events: none;
}

/* Sidebar text - gold embossed look */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] p {
    color: #f4e4c1 !important;
    font-family: 'Montserrat', sans-serif;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}

section[data-testid="stSidebar"] h2 {
    color: #d4af37 !important;
    font-family: 'Crimson Text', serif;
    font-weight: 700;
    font-size: 28px !important;
    text-align: center;
    border-bottom: 2px solid #d4af37;
    padding-bottom: 10px;
    margin-bottom: 20px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
}

/* Sidebar inputs */
section[data-testid="stSidebar"] .stSelectbox > div > div,
section[data-testid="stSidebar"] .stSlider > div {
    background-color: rgba(244, 228, 193, 0.15) !important;
    border: 1px solid #d4af37 !important;
    border-radius: 8px !important;
}

/* Dropdown menu items */
div[data-baseweb="select"] ul {
    background-color: #2d2d2d !important;
}

div[data-baseweb="select"] li {
    background-color: #2d2d2d !important;
    color: #f4e4c1 !important;
}

div[data-baseweb="select"] li:hover {
    background-color: #3d3d3d !important;
    color: #d4af37 !important;
}

/* Main content area */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Cookbook header */
.cookbook-header {
    background: linear-gradient(135deg, #8B4513 0%, #a0522d 100%);
    padding: 50px 40px;
    border-radius: 20px;
    text-align: center;
    color: #f4e4c1;
    margin-bottom: 40px;
    box-shadow: 
        0 10px 40px rgba(0,0,0,0.3),
        inset 0 1px 0 rgba(255,255,255,0.2);
    border: 3px solid #d4af37;
    position: relative;
    overflow: hidden;
}

.cookbook-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
        repeating-linear-gradient(
            45deg,
            transparent,
            transparent 10px,
            rgba(212, 175, 55, 0.05) 10px,
            rgba(212, 175, 55, 0.05) 20px
        );
    pointer-events: none;
}

.cookbook-header h1 {
    font-family: 'Crimson Text', serif;
    font-size: 56px;
    font-weight: 700;
    margin: 0;
    text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
    letter-spacing: 2px;
}

.cookbook-header p {
    font-family: 'Montserrat', sans-serif;
    font-size: 18px;
    margin-top: 15px;
    color: #f4e4c1;
    font-weight: 300;
    letter-spacing: 1px;
}

/* Section cards - recipe card style */
.recipe-card {
    background: linear-gradient(to bottom, #ffffff 0%, #faf8f3 100%);
    padding: 30px;
    border-radius: 15px;
    box-shadow: 
        0 8px 30px rgba(0,0,0,0.15),
        inset 0 1px 0 rgba(255,255,255,0.8);
    margin-bottom: 30px;
    border: 2px solid #e8d5b7;
    position: relative;
}

.recipe-card::before {
    content: '';
    position: absolute;
    top: 10px;
    left: 10px;
    right: 10px;
    bottom: 10px;
    border: 1px dashed #d4af37;
    border-radius: 10px;
    pointer-events: none;
    opacity: 0.3;
}

/* Section titles - handwritten style */
.section-title {
    font-size: 36px;
    font-weight: 700;
    color: #5d4037;
    margin-bottom: 20px;
    font-family: 'Crimson Text', serif;
    padding-bottom: 10px;
    display: inline-block;
}

/* Recommend button - vintage cookbook style */
.stButton > button {
    background: linear-gradient(to bottom, #d4af37 0%, #b8941e 100%);
    color: #3e2723;
    border-radius: 15px;
    height: 60px;
    font-size: 22px;
    font-weight: 700;
    border: 3px solid #8B4513;
    box-shadow: 
        0px 6px 20px rgba(139, 69, 19, 0.4),
        inset 0 1px 0 rgba(255,255,255,0.4);
    font-family: 'Crimson Text', serif;
    letter-spacing: 1px;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 
        0px 8px 25px rgba(139, 69, 19, 0.5),
        inset 0 1px 0 rgba(255,255,255,0.4);
    background: linear-gradient(to bottom, #e6c04e 0%, #c9a426 100%);
}

/* Recipe result cards */
.recipe-result {
    background: linear-gradient(to bottom, #ffffff 0%, #faf8f3 100%);
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    margin-bottom: 25px;
    border: 2px solid #d4af37;
    transition: transform 0.2s ease;
}

.recipe-result:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.15);
}

.recipe-result h3 {
    font-family: 'Crimson Text', serif;
    color: #5d4037 !important;
    font-size: 28px;
    margin-bottom: 15px;
    padding-bottom: 8px;
}

.recipe-result img {
    border-radius: 10px;
    border: 4px solid #8B4513;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

/* Expanders - aged paper look */
.streamlit-expanderHeader {
    background: linear-gradient(to right, #f4e4c1 0%, #efe8dd 100%) !important;
    border: 1px solid #d4af37 !important;
    border-radius: 8px !important;
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 600 !important;
    color: #5d4037 !important;
}

.streamlit-expanderContent {
    background: #faf8f3 !important;
    border: 1px solid #e8d5b7 !important;
    border-top: none !important;
    font-family: 'Crimson Text', serif !important;
    color: #3e2723 !important;
    line-height: 1.8;
}

/* Text inside expanders */
.streamlit-expanderContent p,
.streamlit-expanderContent div {
    color: #3e2723 !important;
}

/* Input fields - vintage style */
.stMultiSelect > div > div,
.stTextInput > div > div > input {
    background-color: #faf8f3 !important;
    border: 2px solid #d4af37 !important;
    border-radius: 10px !important;
    color: #3e2723 !important;
    font-family: 'Montserrat', sans-serif !important;
}

/* Multi-select dropdown */
.stMultiSelect div[data-baseweb="select"] ul {
    background-color: #2d2d2d !important;
}

.stMultiSelect div[data-baseweb="select"] li {
    background-color: #2d2d2d !important;
    color: #f4e4c1 !important;
}

.stMultiSelect div[data-baseweb="select"] li:hover {
    background-color: #3d3d3d !important;
    color: #d4af37 !important;
}

/* Divider */
hr {
    border: none;
    height: 2px;
    background: linear-gradient(to right, transparent, #d4af37, transparent);
    margin: 30px 0;
}

/* Info/warning boxes */
.stAlert {
    background: #fff8e1 !important;
    border-left: 5px solid #d4af37 !important;
    border-radius: 8px !important;
    font-family: 'Montserrat', sans-serif;
    color: #3e2723 !important;
}

/* Decorative elements */
.decorative-line {
    text-align: center;
    margin: 20px 0;
    font-size: 24px;
    color: #d4af37;
}

/* Labels */
label {
    font-family: 'Montserrat', sans-serif !important;
    color: #5d4037 !important;
    font-weight: 600 !important;
}

/* Recipe metadata */
.recipe-meta {
    display: inline-block;
    padding: 5px 12px;
    background: #f4e4c1;
    border-radius: 20px;
    margin-right: 10px;
    margin-bottom: 8px;
    font-family: 'Montserrat', sans-serif;
    font-size: 14px;
    color: #5d4037;
    border: 1px solid #d4af37;
}

/* Like button styling */
div[data-testid="column"] > div > div > div > button[kind="secondary"] {
    background: linear-gradient(to bottom, #ff6b6b 0%, #ee5a52 100%) !important;
    color: white !important;
    border: 2px solid #d4af37 !important;
    border-radius: 10px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    padding: 8px 16px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 10px rgba(255, 107, 107, 0.3) !important;
}

div[data-testid="column"] > div > div > div > button[kind="secondary"]:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 6px 15px rgba(255, 107, 107, 0.4) !important;
}

/* Section headings */
h2 {
    color: #5d4037 !important;
    font-family: 'Crimson Text', serif !important;
}

/* Paragraph text */
p {
    color: #3e2723 !important;
}

/* All text elements */
div, span, a, li {
    color: #3e2723 !important;
}

/* Override Streamlit's default white text */
.main * {
    color: #3e2723 !important;
}

/* Except for specific colored elements */
.recipe-meta,
.cookbook-header,
.cookbook-header *,
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] * {
    color: inherit !important;
}

/* Remove white space/border around images */
div[data-testid="stImage"] {
    padding: 0 !important;
    margin: 0 !important;
}

div[data-testid="stImage"] > img {
    padding: 0 !important;
    margin: 0 !important;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    """
    <div class="cookbook-header">
        <h1>📖 The Recipe Book</h1>
        <p>AI-Powered Culinary Companion | Discover Your Next Favorite Dish</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# LOAD METADATA
# -----------------------------
@st.cache_data
def load_metadata():
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level and then into backend/data
    csv_path = os.path.join(current_dir, "..", "backend", "data", "recipes_MASTER_FINAL.csv")
    
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        st.error(f"❌ Could not find CSV file at: {csv_path}")
        st.error("Please make sure recipes_MASTER_FINAL.csv exists in backend/data/")
        st.stop()

    ingredients = sorted(
        set(
            ing.strip().lower()
            for row in df["ingredients"].dropna()
            for ing in row.split(",")
        )
    )

    return {
        "ingredients": ingredients,
        "categories": list(sorted(df["category"].dropna().str.lower().unique())),
        "cuisines": list(sorted(df["cuisine"].dropna().str.lower().unique())),
        "difficulty": list(sorted(df["difficulty"].dropna().str.lower().unique())),
        "veg": list(sorted(df["veg_nonveg"].dropna().str.lower().unique()))
    }

meta = load_metadata()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.markdown("## 🔖 Filter Recipes")

veg = st.sidebar.selectbox("Dietary Preference", [""] + meta["veg"])
difficulty = st.sidebar.selectbox("Skill Level", [""] + meta["difficulty"])
category = st.sidebar.selectbox("Recipe Category", [""] + meta["categories"])
cuisine = st.sidebar.selectbox("Cuisine Type", [""] + meta["cuisines"])
top_n = st.sidebar.slider("Number of Recipes", 1, 10, 5)

st.sidebar.markdown("---")

# -----------------------------
# INGREDIENT INPUT
# -----------------------------
st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🥕 Select Your Ingredients</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    selected_ingredients = st.multiselect(
        "Choose from available ingredients",
        meta["ingredients"],
        help="Select the ingredients you have on hand"
    )

with col2:
    manual_input = st.text_input(
        "Add custom ingredients",
        placeholder="e.g., tomato, garlic, basil",
        help="Enter ingredients separated by commas"
    )

st.markdown('</div>', unsafe_allow_html=True)

manual_ingredients = [
    i.strip().lower()
    for i in manual_input.split(",")
    if i.strip()
]

final_ingredients = list(set(selected_ingredients + manual_ingredients))

# Display selected ingredients
if final_ingredients:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**📝 Your Selected Ingredients:**")
    ingredients_html = " ".join([f'<span class="recipe-meta">{ing.title()}</span>' for ing in final_ingredients])
    st.markdown(ingredients_html, unsafe_allow_html=True)

st.markdown('<div class="decorative-line">✦ ✦ ✦</div>', unsafe_allow_html=True)

# -----------------------------
# API CALL
# -----------------------------
center = st.columns([2, 1, 2])[1]

with center:
    recommend_btn = st.button("🍳 Find Recipes", use_container_width=True, key="recommend_btn")

if recommend_btn:
    if not final_ingredients:
        st.warning("⚠️ Please select at least one ingredient to get started.")
    else:
        payload = {
            "ingredients": final_ingredients,
            "veg": veg if veg else None,
            "difficulty": difficulty if difficulty else None,
            "category": category if category else None,
            "cuisine": cuisine if cuisine else None,
            "top_n": top_n
        }

        with st.spinner("🔍 Searching through our cookbook..."):
            try:
                res = requests.post(API_URL, json=payload, timeout=10)

                if res.status_code != 200:
                    st.error(f"❌ Backend error (Status {res.status_code})")
                    st.error(f"Response: {res.text}")
                else:
                    try:
                        response_data = res.json()
                        
                        # Handle both response formats
                        if isinstance(response_data, dict):
                            recipes = response_data.get("recipes", [])
                        elif isinstance(response_data, list):
                            recipes = response_data
                        else:
                            st.error("❌ Backend returned invalid data format")
                            st.error(f"Expected dict or list, got: {type(response_data)}")
                            st.stop()
                        
                        if not isinstance(recipes, list):
                            st.error("❌ Recipes data is not a list")
                            st.error(f"Got: {type(recipes)}")
                            st.stop()
                    except Exception as json_error:
                        st.error(f"❌ Error parsing backend response: {str(json_error)}")
                        st.error(f"Raw response: {res.text[:500]}")
                        st.stop()

                    st.markdown('<div class="decorative-line">✦ ✦ ✦</div>', unsafe_allow_html=True)
                    st.markdown("## 🍽️ Your Recommended Recipes")
                    st.markdown("<br>", unsafe_allow_html=True)

                    if not recipes:
                        st.info("📭 No recipes found matching your criteria. Try adjusting your filters or ingredients.")
                    else:
                        for idx, r in enumerate(recipes, 1):
                            st.markdown(
                                '<div class="recipe-result">',
                                unsafe_allow_html=True
                            )

                            # Create unique recipe ID for like button
                            recipe_name = r.get('recipe_name') or r.get('name', 'Unknown Recipe')
                            recipe_id = f"recipe_{idx}_{recipe_name.replace(' ', '_')}"

                            cols = st.columns([1, 2])

                            with cols[0]:
                                # Handle both image field names
                                image_url = r.get("image_url") or r.get("image")
                                if image_url:
                                    st.image(
                                        image_url,
                                        use_container_width=True,
                                        caption=f"Recipe #{idx}"
                                    )
                                else:
                                    st.markdown(
                                        f"""
                                        <div style='background: linear-gradient(135deg, #f4e4c1, #e8d5b7); 
                                        height: 200px; border-radius: 10px; display: flex; 
                                        align-items: center; justify-content: center; 
                                        border: 4px solid #8B4513;'>
                                            <span style='font-size: 48px;'>🍽️</span>
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )

                            with cols[1]:
                                st.markdown(f"### {recipe_name}")
                                
                                recipe_cuisine = r.get('cuisine', 'Unknown')
                                recipe_difficulty = r.get('difficulty', 'Unknown')
                                recipe_prep_time = r.get('prep_time', 'N/A')
                                
                                st.markdown(
                                    f"""
                                    <span class="recipe-meta">🌍 {recipe_cuisine.title()}</span>
                                    <span class="recipe-meta">👨‍🍳 {recipe_difficulty.title()}</span>
                                    <span class="recipe-meta">⏱️ {recipe_prep_time} mins</span>
                                    """,
                                    unsafe_allow_html=True
                                )
                                
                                st.markdown("<br>", unsafe_allow_html=True)

                                # Handle ingredients (can be string or list)
                                ingredients = r.get("ingredients", "Not available")
                                if isinstance(ingredients, list):
                                    ingredients = ", ".join(ingredients)
                                
                                with st.expander("📋 Ingredients List"):
                                    st.write(ingredients)

                                with st.expander("👩‍🍳 Cooking Instructions"):
                                    st.write(r.get("instructions", "Not available"))

                            st.markdown("</div>", unsafe_allow_html=True)
                            
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to the recipe server. Please ensure the backend API is running at http://127.0.0.1:8000")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div class="decorative-line">✦ ✦ ✦</div>', unsafe_allow_html=True)