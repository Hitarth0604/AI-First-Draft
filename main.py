# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from blog import generate_blog
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or your Streamlit URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BlogRequest(BaseModel):
    topic: str
    tone: str = "Informative"
    audience: str = "General"

@app.post("/generate")
def generate_blog_api(req: BlogRequest):
    try:
        blog = generate_blog(req.topic, req.tone, req.audience)

        # Print full response for debugging
        print("\n--- FULL BLOG RESPONSE ---\n", blog, "\n--------------------------\n")

        # Use safe parsing
        title = ""
        meta = ""
        tags = ""
        body = blog

        if "**Title:**" in blog:
            title = blog.split("**Title:**")[1].split("\n")[0].strip()

        if "**Meta Description:**" in blog:
            meta = blog.split("**Meta Description:**")[1].split("**Tags:**")[0].strip()

        if "**Tags:**" in blog:
            tags = blog.split("**Tags:**")[1].split("---")[0].strip()

        if "---" in blog:
            body = blog.split("---")[1].strip()

        return {
            "title": title,
            "meta_description": meta,
            "tags": tags,
            "body": body
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
