from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from .recommender1 import recommend_recipes
from fastapi.staticfiles import StaticFiles

class TaskRequest(BaseModel):        #to check whether the backend is receving data succesfully
    task: str

app = FastAPI(title="Recipe Recommendation API")       #starts backend

app.mount("/images", StaticFiles(directory="Images"), name="images")      #we take images from images folder

# -----------------------------
# Request Schema
# -----------------------------
class RecommendationRequest(BaseModel):         #what data to send from frontend to backend
    ingredients: List[str]
    cuisine: Optional[str] = None
    veg: Optional[str] = None          # "veg" or "non-veg"
    difficulty: Optional[str] = None   # "Easy", "Medium", "High"
    category: Optional[str] = None     # "Breakfast", "Lunch", etc.
    top_n: Optional[int] = 5


# -----------------------------
# Health Check
# -----------------------------
@app.post("/analyze")                        #checks whether the backend is receiving data
def analyze(request: TaskRequest):
    print("API ENDPOINT HIT")
    return {"task": request.task}

@app.get("/")
def health_check():
    return {"status": "API is running"}


# -----------------------------
# Recommendation Endpoint
# -----------------------------
@app.post("/recommend")                             # as soon as we click the generate recipe button this function triggers
def recommend(request: RecommendationRequest):
    results = recommend_recipes(                    #This sends user data to recommender1.py
        user_ingredients=request.ingredients,
        veg=request.veg,
        difficulty=request.difficulty,
        category=request.category,
        cuisine=request.cuisine,
        top_n=request.top_n
    )

    return {                         #backends sends back processed data and then that data is visble in the frontend
        "count": len(results),
        "recipes": results
    }
