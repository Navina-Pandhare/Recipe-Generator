import os                      #decides the file paths
import pandas as pd            #used to read excel files and work with data inside tables

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(__file__)                 # backend/
PROJECT_ROOT = os.path.dirname(BASE_DIR)             # recipe_generator/


#creates the path to dataset
FEATURE_FILE = os.path.join(BASE_DIR, "data", "recipes_FEATURE_READY.csv")
MASTER_FILE = os.path.join(PROJECT_ROOT, "recipes_MASTER_FINAL.csv")

# -----------------------------
# Load Data
# -----------------------------
features_df = pd.read_csv(FEATURE_FILE)         #Reads the main recipe data into Python
master_df = pd.read_csv(MASTER_FILE)

# -----------------------------
# Merge image_url into feature data  that is combining two datsets into one table
# -----------------------------
df = features_df.merge(
    master_df[["recipe_name", "image_url"]],
    on="recipe_name",
    how="left"
)

# -----------------------------
# Normalization helpers             #cleans text
# -----------------------------
def normalize_text(x):
    if not isinstance(x, str):
        return ""                  #If value is empty or not text return empty string
    return x.lower().strip()       #converts text to lovercase and removes extra spaces

def normalize_ingredient(i):
    return normalize_text(i).replace("-", " ")   #normalizes text eg chicken CHICKEN Chicken is all considered same

# -----------------------------
# Preprocessing
# -----------------------------
'''df["ingredients_list"] = (
    df["ingredients"]
    .str.lower()
    .str.split(",")
    .apply(lambda x: [i.strip() for i in x])
)

df["veg_nonveg"] = df["veg_nonveg"].str.lower()
df["difficulty"] = df["difficulty"].str.lower()
df["category"] = df["category"].str.lower()
df["cuisine"] = df["cuisine"].str.lower().str.strip()
df["image_url"] = df["image_url"].fillna("")'''

df["ingredients_list"] = (              #converts input into list
    df["ingredients"]
    .fillna("")
    .apply(lambda x: [normalize_ingredient(i) for i in x.split(",")])   #Splits ingredients by comma and cleans each one
)
#cleans the values that is normalizing it 
df["veg_nonveg"] = df["veg_nonveg"].apply(normalize_text)
df["difficulty"] = df["difficulty"].apply(normalize_text)
df["category"] = df["category"].apply(normalize_text)
df["cuisine"] = df["cuisine"].apply(normalize_text)
df["image_url"] = df["image_url"].fillna("")

# -----------------------------
# Ingredient Weights
# -----------------------------    # here high number = high value given to ingreditients
IMPORTANT_INGREDIENTS = {
    "chicken": 3, "paneer": 3, "rice": 3, "egg": 3, "fish": 3,
    "pasta": 3, "noodles": 3,
    "potato": 2, "corn": 2, "bread": 2, "cheese": 2,
    "chickpeas": 2, "semolina": 2,
    "flour": 2, "sugar": 2, "chocolate": 3, "butter": 2,
    "cream": 2, "milk": 2, "dates": 2, "nuts": 2
}

BASE_IMAGE_URL = "http://127.0.0.1:8000/images"

'''def normalize_image_url(image):
    if not image or not isinstance(image, str):
        return None'''
    
def normalize_image_url(image):
    if not image:
        return None               #If no image → return nothing

    image = image.replace("\\", "/").strip()

    '''# Case 1: Internet image
    if image.startswith("http://") or image.startswith("https://"):
        return image'''
    if image.startswith("http"):       #If image is already online → use it directly.
        return image

    # Case 2: Local image from CSV
    #image = image.replace("\\", "/")

    if image.startswith("Images/"):
        image = image.replace("Images/", "")

    return f"{BASE_IMAGE_URL}/{image.replace(' ', '%20')}"   #gives final image url for frontend to display

# -----------------------------
# Scoring functions                           #Calculates how well recipe matches user ingredients
# -----------------------------
def ingredient_match_score(recipe_ings, user_ings):
    score = 0
    for r in recipe_ings:
        for u in user_ings:
            if u in r or r in u:
                score += IMPORTANT_INGREDIENTS.get(u, 1)
    return score

def missing_penalty(recipe_ings, user_ings):
    return len(set(recipe_ings) - set(user_ings))

# -----------------------------
# Recommendation Logic
# -----------------------------
def recommend_recipes(
    user_ingredients,
    veg=None,
    difficulty=None,
    category=None,
    cuisine=None, 
    top_n=5
):
    user_ingredients = [normalize_ingredient(i) for i in user_ingredients]
    veg = normalize_text(veg) if veg else None
    difficulty = normalize_text(difficulty) if difficulty else None
    category = normalize_text(category) if category else None
    cuisine = normalize_text(cuisine) if cuisine else None

    data = df.copy()


    '''def weighted_score(recipe_ings):
        return sum(
            IMPORTANT_INGREDIENTS.get(i, 1)
            for i in recipe_ings if i in user_ingredients
        )'''

    

    '''data["match_score"] = data["ingredients_list"].apply(
        lambda x: len(set(x) & set(user_ingredients))
    )

    data["weighted_score"] = data["ingredients_list"].apply(weighted_score)

    data = data[data["match_score"] > 0]'''

#filters out recipes 
# Hard filters (basic sanity)
    if veg:
        data = data[data["veg_nonveg"] == veg]

    if difficulty:
        data = data[data["difficulty"] == difficulty]

    if category:
        data = data[data["category"] == category]

    if cuisine:
        data = data[data["cuisine"].str.contains(cuisine)]

    # print("Cuisine requested:", cuisine)
    # print("Recipes after cuisine filter:", len(data))                                                                                                                           

    if data.empty:
        return []
    

    #---------- SCORING ---------- Best recipes first, faster ones earlier.
    data["match_score"] = data["ingredients_list"].apply(
    lambda x: ingredient_match_score(x, user_ingredients)  
    )

    data["missing_penalty"] = data["ingredients_list"].apply(
    lambda x: missing_penalty(x, user_ingredients)
    )

    #data["weighted_score"] = data["ingredients_list"].apply(weighted_score)

    # Base score
    data["score"] = data["match_score"] - 0.5 * data["missing_penalty"]

    # Soft cuisine preference
    if cuisine:
        data["score"] += data["cuisine"].apply(
            lambda c: 2 if c == cuisine else 0
        )

    # Remove garbage matches
    data = data[data["score"] > 0]

    if data.empty:
        return []

    # -----------------------------
    # Final ranking
    # -----------------------------
    data = data.sort_values(
        by=["score", "prep_time"],
        ascending=[False, True]
    )

    '''data = data.sort_values(
        by=["weighted_score", "match_score", "prep_time"],
        ascending=[False, False, True]
    )'''

    """return data[[
        "recipe_name",
        "cuisine",
        "ingredients",
        "instructions",
        "prep_time",
        "difficulty",
        "category",
        "calories",
        "image_url"
    ]].head(top_n).to_dict(orient="records")"""

    results = []


    #Picks top recipes. and prepares final result to be displayed 
    for _, row in data.head(top_n).iterrows():
        results.append({
            "recipe_name": row["recipe_name"],
            "image_url": normalize_image_url(row.get("image_url")),
            "ingredients": row.get("ingredients"),
            "instructions": row.get("instructions"),
            "difficulty": row.get("difficulty"),
            "prep_time": row.get("prep_time"),
            "category": row.get("category"),
            "veg": row.get("veg_nonveg"),
            "cuisine": row.get("cuisine")
        })

    return results

