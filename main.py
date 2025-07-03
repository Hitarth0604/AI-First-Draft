print("🔥 main.py is loading...")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

print("✅ Step 1: FastAPI + os imported")

try:
    from blog import generate_blog
    print("✅ Step 2: Imported generate_blog successfully")
except Exception as import_error:
    print("❌ Import failed:", str(import_error))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    print("📥 Received request:", data)
    print("🔑 GROQ_API_KEY present:", os.getenv("GROQ_API_KEY") is not None)
    try:
        result = generate_blog(data.topic, data.tone, data.audience)
        print("✅ Blog generated")
        return result
    except Exception as e:
        print("❌ ERROR in generate_blog:", str(e))
        return {"error": "Internal server error"}
