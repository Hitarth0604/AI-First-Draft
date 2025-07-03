from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from blog import generate_blog
import os

app = FastAPI()

# CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your Streamlit app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BlogRequest(BaseModel):
    topic: str
    tone: str
    audience: str

@app.post("/generate")
def generate_blog_api(data: BlogRequest):
    print("Received data:", data)
    print("API key present:", os.getenv("GROQ_API_KEY") is not None)
    try:
        result = generate_blog(data.topic, data.tone, data.audience)
        print("Blog generated successfully.")
        return result
    except Exception as e:
        print("ERROR while generating blog:", str(e))
        return {"error": "Internal server error"}
