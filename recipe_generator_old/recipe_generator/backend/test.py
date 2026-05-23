from recommender1 import recommend_recipes

print(
    recommend_recipes(
        user_ingredients=["onion", "tomato", "garlic"],
        veg="veg",
        top_n=3
    )
)
