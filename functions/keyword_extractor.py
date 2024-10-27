from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def keyword_extractor(text, reference_entry):
    """Extract mental health-related keywords using reference data and LLM"""
    prompt = f"""Extract mental health-related keywords from this text: '{text}'.
                Example format: 'feeling anxious, trouble sleeping'
                Only extract words/phrases that directly relate to mental health concerns."""
    
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a mental health professional who extracts key phrases related to mental health concerns. Be concise and specific."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.1-70b-versatile",
        temperature=0.3,
    )
    
    extracted_keywords = response.choices[0].message.content.strip()
    return extracted_keywords if extracted_keywords else reference_entry['Extracted Concern']