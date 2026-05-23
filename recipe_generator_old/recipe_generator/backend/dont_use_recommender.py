import os
import pandas as pd

# -----------------------------
# File Path Handling
# -----------------------------
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
FILE = os.path.join(DATA_DIR, "recipes_FEATURE_READY.csv")

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv(FILE)

# -----------------------------
# Validate Required Columns
# -----------------------------
REQUIRED_COLUMNS = [
    "recipe_name",
    "cuisine",
    "ingredients",
    "instructions",
    "prep_time",
    "difficulty",
    "category",
    "veg_nonveg",
    "calories",
    "image_url"
]

missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns in CSV: {missing_cols}")


# Preprocess once
df["ingredients_list"] = df["ingredients"].str.lower().str.split(",")
df["ingredients_list"] = df["ingredients_list"].apply(
    lambda x: [i.strip() for i in x]
)

# Normalize text fields to avoid case mismatch bugs
df["veg_nonveg"] = df["veg_nonveg"].str.lower()
df["difficulty"] = df["difficulty"].str.lower()
df["category"] = df["category"].str.lower()

# -----------------------------
# Ingredient Importance Weights
# -----------------------------
IMPORTANT_INGREDIENTS = {
    "chicken": 3, "paneer": 3, "rice": 3, "egg": 3, "fish": 3,
    "pasta": 3, "noodles": 3,
    "potato": 2, "corn": 2, "bread": 2, "cheese": 2,
    "chickpeas": 2, "semolina": 2,
    "flour": 2, "sugar": 2, "chocolate": 3, "butter": 2,
    "cream": 2, "milk": 2, "dates": 2, "nuts": 2
}

# -----------------------------
# Recommendation Function
# -----------------------------
def recommend_recipes(
    user_ingredients,
    veg=None,
    difficulty=None,
    category=None,
    top_n=5
):
    # Normalize inputs
    user_ingredients = [i.lower().strip() for i in user_ingredients]

    veg = veg.lower() if veg else None
    difficulty = difficulty.lower() if difficulty else None
    category = category.lower() if category else None

    def weighted_score(recipe_ings):
        return sum(
            IMPORTANT_INGREDIENTS.get(i, 1)
            for i in recipe_ings if i in user_ingredients
        )

    data = df.copy()

    # Match score
    data["match_score"] = data["ingredients_list"].apply(
        lambda x: len(set(x) & set(user_ingredients))
    )

    # Weighted score
    data["weighted_score"] = data["ingredients_list"].apply(weighted_score)

    # Remove zero-match recipes
    data = data[data["match_score"] > 0]

    # Apply filters
    if veg:
        data = data[data["veg_nonveg"] == veg]

    if difficulty:
        data = data[data["difficulty"] == difficulty]

    if category:
        data = data[data["category"] == category]

    # No matches case
    if data.empty:
        return []

    # Ranking
    data = data.sort_values(
        by=["weighted_score", "match_score", "prep_time"],
        ascending=[False, False, True]
    )

    # Final output
    return data[[
        "recipe_name",
        "cuisine",
        "ingredients",
        "instructions",
        "prep_time",
        "difficulty",
        "category",
        "calories",
        "image_url"
    ]].head(top_n).to_dict(orient="records")
