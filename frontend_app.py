# frontend_app.py
import streamlit as st
import requests
from io import BytesIO
from output_utils import blog_to_docx

# --- Config ---
API_URL = "http://127.0.0.1:8000/generate"
st.set_page_config(page_title="AI First Draft", layout="wide")

# --- Custom CSS: Cursor-inspired ---
st.markdown("""
    <style>
    html, body {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f6f7f9;
        color: #1a1a1a;
    }

    .block-container {
        padding: 2rem 3rem;
        max-width: 1000px;
        margin: auto;
    }

    h1, h2, h3 {
        color: #333;
        font-weight: 600;
    }

    .stTextInput > div > div > input {
        font-size: 16px;
        padding: 10px;
        border-radius: 6px;
    }

    .stButton button {
        background-color: #3b82f6;
        color: white;
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        font-weight: bold;
        border: none;
        margin-top: 1rem;
    }

    .stDownloadButton > button {
        background-color: #10b981 !important;
        color: white;
        border-radius: 6px;
        font-weight: bold;
        padding: 0.5rem 1rem;
        margin-top: 1rem;
    }

    .stMarkdown p {
        font-size: 16px;
        line-height: 1.6;
    }

    #MainMenu, footer {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.title("✍️ AI First Draft")
st.caption("A clean, modern blog generator powered by GPT")

# --- Sidebar ---
with st.sidebar:
    st.header("🛠️ Settings")

    preset_topic = st.selectbox("Preset Topics", [
        "", "Top AI Tools in 2025", "Morning Routine for Designers",
        "Marketing Hacks for Startups", "Mental Health for Remote Workers"
    ])

    tone = st.selectbox("Tone", [
        "Informative", "Friendly", "Motivational", "Professional", "Casual"
    ])

    audience = st.text_input("Target Audience", "General")

    tone_examples = {
        "Informative": "Factual, structured, clear.",
        "Friendly": "Warm, conversational, approachable.",
        "Motivational": "Energetic, inspiring, action-driven.",
        "Professional": "Corporate, serious, to-the-point.",
        "Casual": "Chill, relaxed, everyday tone."
    }

    st.caption(f"💬 Tone preview: *{tone_examples[tone]}*")

# --- Input Area ---
st.subheader("🔤 Blog Topic")
topic = st.text_input("What should the blog be about?", value=preset_topic)

submitted = st.button("🚀 Generate Blog")

# --- Blog Output ---
if submitted:
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        with st.spinner("🧠 Crafting your blog..."):
            try:
                res = requests.post(API_URL, json={
                    "topic": topic,
                    "tone": tone,
                    "audience": audience
                })

                if res.status_code == 200:
                    blog = res.json()
                    st.success("✅ Blog generated!")

                    st.markdown(f"### 📝 `{blog['title']}`")
                    st.markdown(f"**Meta Description:** {blog['meta_description']}")
                    st.markdown("**Tags:** " + ", ".join(blog['tags'].split(",")))
                    st.markdown("---")

                    st.code(blog["body"], language="markdown")

                    st.markdown("---")
                    st.markdown(f"📏 Word Count: {len(blog['body'].split())} words")
                    st.markdown(f"🏷️ Tags: {len(blog['tags'].split(','))} tags")

                    doc = blog_to_docx(blog['title'], blog['meta_description'], blog['tags'], blog['body'])
                    buffer = BytesIO()
                    doc.save(buffer)
                    st.download_button(
                        "📄 Download as .docx",
                        buffer.getvalue(),
                        file_name="blog.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                else:
                    st.error(f"Error: {res.status_code}")
                    st.code(res.text)

            except Exception as e:
                st.error("Something went wrong! Showing fallback content...")

                blog = {
                    "title": "5 Tips to Boost Productivity Remotely",
                    "meta_description": "Remote workers, here’s how to stay sharp and focused from home.",
                    "tags": "remote work, focus, productivity, home office, habits",
                    "body": (
                        "Working from home can be empowering — but it comes with distractions...\n\n"
                        "**Start with structure**\nMake a plan every morning...\n\n"
                        "**Stay active, take breaks**\nYour brain needs rest too..."
                    )
                }

                st.markdown(f"### 📝 `{blog['title']}`")
                st.markdown(f"**Meta Description:** {blog['meta_description']}")
                st.markdown("**Tags:** " + ", ".join(blog['tags'].split(",")))
                st.markdown("---")
                st.code(blog["body"], language="markdown")

