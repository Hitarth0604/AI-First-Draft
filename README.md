# ✍️ AI First Draft

**AI First Draft** is a GPT-powered tool that generates complete SEO-friendly blog posts — title, intro, structured sections, meta description, and tags — from just a topic input.

### 🌟 Features
- Input: Topic, tone, and audience
- Output:
  - Blog Title
  - Structured Blog Content (with headings)
  - Meta Description
  - SEO Tags
- Clean UI with Streamlit
- Download as `.docx`
- Sidebar presets & tone previews
- Fallback blog in case of API failure

### 🚀 Tech Stack
- `FastAPI` (API backend)
- `Streamlit` (UI frontend)
- `Groq API` (free GPT model)
- `python-docx` (blog export)
- `dotenv`, `requests`, `pydantic`, `uvicorn`

---

### ▶️ How to Run

#### 1. Clone the project:
```bash
git clone https://github.com/yourusername/ai-first-draft.git
cd ai-first-draft
