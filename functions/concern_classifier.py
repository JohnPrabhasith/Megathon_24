from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def concern_classifier(text, reference_entry, valid_categories):
    """Classify the mental health concern category"""
    prompt = f"""Classify this text into one mental health category: '{text}'
                Categories: Anxiety, Depression, Stress, Insomnia, Eating Disorder, Health Anxiety, Positive Outlook
                Respond with exactly one category."""
    
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a mental health professional who classifies concerns into specific categories. Respond with exactly one category."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.1-70b-versatile",
        temperature=0.3,
    )
    
    category = response.choices[0].message.content.strip()
    return category if category in valid_categories else reference_entry['Category']