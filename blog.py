# blog_writer.py (Groq version)
from config import OPENAI_API_KEY
from groq import Groq

client = Groq(api_key=OPENAI_API_KEY)

def generate_blog(topic, tone="Informative", audience="General"):
    prompt = f"""
You are a professional blog writer.

Write a complete SEO-friendly blog post on the topic: "{topic}"

- Write an attention-grabbing title
- Use a {tone.lower()} tone
- Target audience: {audience}
- Start with a brief introduction
- Add 4-6 sections with proper H2 subheadings
- Conclude with a short summary
- At the end, provide:
  - A 160-character meta description
  - 5 SEO-friendly tags
"""
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are a professional blog writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1500
    )

    return response.choices[0].message.content.strip()
